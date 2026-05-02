import os
import asyncio
import datetime
import json
import random
import streamlit as st
import plotly.graph_objects as go
from pydantic import BaseModel, Field, validator
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. THE SAFETY SCHEMA (The AI's Guardrails)
# ============================================================
class GovernanceDecision(BaseModel):
    action: str = Field(description="The operational command: SCALE_UP, SHED_LOAD, or HOLD.")
    power_limit_kw: int = Field(description="Target power load for Raipur Hub in Kilowatts.")
    profit_delta: float = Field(description="Projected arbitrage profit in USD/hr.")
    trace: str = Field(description="The logical justification for this move.")

    @validator('power_limit_kw')
    def physical_limit_check(cls, v):
        # HARD PHYSICAL CAP: AI cannot request more than 500kW regardless of price
        return max(0, min(v, 500))

# ============================================================
# 2. INFRASTRUCTURE & SECURITY
# ============================================================
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"].strip()
else:
    st.error("🚨 CRITICAL: GROQ_API_KEY missing in st.secrets.")
    st.stop()

# ============================================================
# 3. PHYSICAL BRIDGE & AUDIT (SOVEREIGN LAYER)
# ============================================================
def commit_to_ledger(data: dict):
    """Saves every sovereign decision to a secure local audit file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"timestamp": timestamp, "decision": data}
    with open("sovereign_ledger.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

def dispatch_hardware_command(decision: GovernanceDecision, current_temp: float):
    """
    SAFETY LAYER: Validates AI intent against real-time physics.
    """
    # SAFETY LOCK: If Temp > 85C, override AI and force SHED_LOAD
    if current_temp > 85.0 and decision.action != "SHED_LOAD":
        return "SAFETY_OVERRIDE: CRITICAL TEMP. FORCING LOAD SHED.", 0
    
    status = f"ACTUATED: {decision.action} @ {decision.power_limit_kw}KW"
    return status, decision.power_limit_kw

# ============================================================
# 4. DATA & CORE ENGINE
# ============================================================
def get_live_data():
    return {
        "grid_price": round(random.uniform(180.0, 320.0), 2),
        "core_temp": round(random.uniform(55.0, 95.0), 1)
    }

model = GroqModel('llama-3.3-70b-versatile')
# We use result_type to ensure the AI speaks 'JSON' naturally
governor = Agent(model, result_type=GovernanceDecision)

# ============================================================
# 5. UI INTERFACE
# ============================================================
def main():
    st.set_page_config(page_title="SOVEREIGN STAGE 4 // RAIPUR", page_icon="⚡", layout="wide")
    
    # Terminal Aesthetics
    st.markdown("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        .stMetric { border: 1px solid #00FF41; background: #0a0a0a; padding: 10px; }
        .log-box { background-color: #000; border: 1px solid #00FF41; padding: 15px; font-size: 0.85em; }
        </style>
    """, unsafe_allow_html=True)

    if 'telemetry' not in st.session_state:
        st.session_state.telemetry = get_live_data()

    st.title("🏛️ SOVEREIGN ENERGY OS")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Market Price", f"${st.session_state.telemetry['grid_price']}/MWh")
    col2.metric("Chiller Temp", f"{st.session_state.telemetry['core_temp']}°C")
    col3.metric("System Health", "NOMINAL" if st.session_state.telemetry['core_temp'] < 85 else "CRITICAL")

    if st.button("EXECUTE GOVERNANCE CYCLE"):
        async def run_governance():
            prompt = (
                f"Market: ${st.session_state.telemetry['grid_price']}. "
                f"Temp: {st.session_state.telemetry['core_temp']}C. "
                "Pivot at $215/MWh. Max Safety 85C."
            )
            return await governor.run(prompt)

        with st.status("Analyzing Control Loop Stability...", expanded=True):
            try:
                result = asyncio.run(run_governance())
                decision = result.data # Automatically a GovernanceDecision object
                
                # RUN PHYSICAL SAFETY BRIDGE
                status_msg, final_kw = dispatch_hardware_command(decision, st.session_state.telemetry['core_temp'])
                
                # LOG TO LEDGER
                commit_to_ledger(decision.dict())

                st.success("Decision Logged and Actuated.")
                
                # HUD DISPLAY
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader(f"Directive: {decision.action}")
                    st.write(f"**Safety Logic:** {decision.trace}")
                    st.write(f"**Profit Delta:** +${decision.profit_delta}/hr")
                
                with c2:
                    st.markdown(f"<div class='log-box'><b>[HARDWARE STATUS]:</b> {status_msg}<br>"
                                f"<b>[FINAL LOAD]:</b> {final_kw} KW<br>"
                                f"<b>[AUDIT]:</b> Entry committed to sovereign_ledger.jsonl</div>", 
                                unsafe_allow_html=True)

            except Exception as e:
                st.error(f"SYSTEM HALT: {str(e)}")

if __name__ == "__main__":
    main()
