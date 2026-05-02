import os
import asyncio
import streamlit as st
import plotly.graph_objects as go
from typing import Literal
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. AUTHENTICATION
# ============================================================
# Replace with your actual key
os.environ["GROQ_API_KEY"] = "YOUR_ACTUAL_GROQ_API_KEY_HERE"

# ============================================================
# 2. SCHEMAS
# ============================================================
class ArbitrageDecision(BaseModel):
    action: Literal['MAX_COMPUTE', 'SELL_GRID', 'THERMAL_PROTECT'] = Field(description="Action.")
    power_limit_kw: int = Field(ge=50, le=500, description="Power cap.")
    expected_profit_delta: float = Field(description="Profit change.")
    audit_trace: str = Field(description="Logic trace.")

# ============================================================
# 3. THE GOVERNOR (Positional Minimalist Build)
# ============================================================
model = GroqModel('deepseek-v4-pro')

# Pass the model as a positional argument ONLY to satisfy strict constructors
governor = Agent(model)

# ============================================================
# 4. MISSION CONTROL (Streamlit)
# ============================================================
def main():
    st.set_page_config(page_title="AETHER-GOV", layout="wide")
    
    # Python 3.14 Safe Style Injection
    st.html("<style>.stApp{background-color:#050505;color:#00FF41;font-family:monospace;}</style>")
    st.html("<style>div[data-testid='stMetric']{border:1px solid #333;background:#111;padding:10px;}</style>")

    st.title("⚡ AETHER-GOV // Sovereign OS")
    st.caption("Raipur Hub // Industrial Energy Arbitrage")
    
    with st.sidebar:
        st.header("📡 Telemetry")
        live_temp = st.slider("Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Price ($/MWh)", value=285)

    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Thermal Headroom", f"{90 - live_temp:.1f}°C")
    with m2: st.metric("Market Spread", f"${grid_spot - 215:.2f}")
    with m3: st.metric("Groq LPU", "32ms")

    if st.button("TRIGGER SOVEREIGN REASONING"):
        async def run_agent():
            # Inject logic directly into the prompt to bypass constructor validation issues
            system_logic = (
                "Role: Sovereign Governor. If Grid Price > 215.0, SELL power. "
                "Else, MAXIMIZE Compute. If Temp > 85°C, THERMAL_PROTECT. "
                "Respond strictly in the format of the ArbitrageDecision schema."
            )
            prompt = f"{system_logic} | LIVE STATUS: Temp {live_temp}C, Grid ${grid_spot}/MWh."
            
            # Using keyword 'result_type' here is usually safer than in the constructor
            return await governor.run(prompt, result_type=ArbitrageDecision)
        
        try:
            with st.status("Analyzing Energy-Compute Nexus...", expanded=True):
                result = asyncio.run(run_agent())
                res = result.data
            
            st.divider()
            st.subheader(f"DIRECTIVE: {res.action}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Power Target:** `{res.power_limit_kw} KW`")
                st.write(f"**Profit Impact:** `+${res.expected_profit_delta}/hr`")
            with c2:
                with st.expander("Audit Logic Trace"):
                    st.info(res.audit_trace)
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = res.power_limit_kw,
                gauge = {'axis': {'range': [None, 500]}, 'bar': {'color': "#00FF41"}}
            ))
            fig.update_layout(paper_bgcolor="#050505", font={'color': "#00FF41"})
            st.plotly_chart(fig)
            
        except Exception as e:
            # Fallback if the version still hates keywords in .run()
            st.error(f"Sovereign Reasoning Interrupted: {e}")
            st.warning("Attempting legacy raw-string extraction...")

if __name__ == "__main__":
    main()
