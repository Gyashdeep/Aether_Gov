import os
import asyncio
import streamlit as st
import plotly.graph_objects as go
from typing import Literal
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. AUTHENTICATION & SECURE ACCESS
# ============================================================
# ENTER YOUR ACTUAL KEY HERE
os.environ["GROQ_API_KEY"] = "gsk_your_actual_key_here"

# ============================================================
# 2. SOVEREIGN SCHEMAS 
# ============================================================

class ArbitrageDecision(BaseModel):
    action: Literal['MAX_COMPUTE', 'SELL_GRID', 'THERMAL_PROTECT'] = Field(description="Operational directive.")
    power_limit_kw: int = Field(ge=50, le=500, description="GPU power cap.")
    expected_profit_delta: float = Field(description="Projected hourly P&L change.")
    audit_trace: str = Field(description="Reasoning for Data Factory.")

@dataclass
class FacilityContext:
    facility_id: str
    temp_c: float
    grid_price_mwh: float
    compute_yield_mwh: float = 215.0

# ============================================================
# 3. THE GOVERNOR (Bulletproof Agent Syntax)
# ============================================================

# Define model explicitly
model = GroqModel('deepseek-v4-pro')

# Minimal Agent initialization to avoid "Unknown keyword argument" errors
governor = Agent(model)

SYSTEM_INSTRUCTION = (
    "You are the Sovereign Governor. Mission: Maximize Profit-per-Watt. "
    "Logic: If Grid Price > Compute Yield, SELL electricity to the grid. "
    "Logic: If Compute Yield > Grid Price, MAXIMIZE Compute throughput. "
    "Safety: If Temp > 85°C, FORCE THERMAL_PROTECT regardless of profit. "
    "Return the result as an ArbitrageDecision object."
)

# ============================================================
# 4. MISSION CONTROL (Streamlit Industrial HUD)
# ============================================================

def main():
    st.set_page_config(page_title="AETHER-GOV // SOVEREIGN OS", layout="wide")
    
    st.markdown("""
        <style>
        .main { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        div[data-testid="stMetric"] { border: 1px solid #333; padding: 15px; background: #111; }
        .stButton>button { background-color: #00FF41; color: black; font-weight: bold; width: 100%; border-radius: 0px; }
        </style>
    """, unsafe_allow_code=True)

    st.title("⚡ AETHER-GOV // Sovereign Master OS")
    st.caption("Raipur Hub // Nexus-Flow Energy Arbitrage Protocol")
    
    with st.sidebar:
        st.header("📡 Live Telemetry")
        f_id = st.text_input("Facility ID", value="NEXUS-RAIPUR-01")
        live_temp = st.slider("Core Temp (°C)", 40.0, 95.0, 74.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=290)
        st.divider()
        st.info("Enterprise Data Factory: ACTIVE")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Thermal Headroom", f"{90 - live_temp:.1f}°C")
    with m2:
        spread = grid_spot - 215.0
        st.metric("Market Arbitrage", f"${spread:.2f}/MWh", delta="SELL" if spread > 0 else "COMPUTE")
    with m3:
        st.metric("Groq LPU Latency", "34ms")

    if st.button("TRIGGER SOVEREIGN REASONING"):
        with st.status("DeepSeek-V4-Pro Reasoning...", expanded=True) as status:
            async def run_agent():
                # We specify the result_type here in the .run() call instead of the Agent constructor
                return await governor.run(
                    f"CONTEXT: {f_id}, TEMP: {live_temp}C, GRID PRICE: ${grid_spot}/MWh. " + SYSTEM_INSTRUCTION,
                    result_type=ArbitrageDecision
                )
            
            try:
                result = asyncio.run(run_agent())
                res = result.data
                
                st.subheader(f"DIRECTIVE: {res.action}")
                st.write(f"**Hardware Target:** {res.power_limit_kw} KW")
                st.write(f"**Profit Impact:** +${res.expected_profit_delta}/hr")
                
                with st.expander("View Logic Audit Trace"):
                    st.code(res.audit_trace)
                
                status.update(label="Decision Finalized", state="complete")

                # Gauge Visualization
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = res.power_limit_kw,
                    title = {'text': "Assigned Power (KW)"},
                    gauge = {'axis': {'range': [None, 500]}, 'bar': {'color': "#00FF41"}}
                ))
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Reasoning Error: {str(e)}")
                status.update(label="Execution Failed", state="error")

if __name__ == "__main__":
    if os.environ.get("GROQ_API_KEY") == "gsk_your_actual_key_here":
        st.error("Please update the script with your actual Groq API Key.")
    else:
        main()
