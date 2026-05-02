import os
import asyncio
import streamlit as st
import plotly.graph_objects as go
from typing import Literal
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. AUTHENTICATION (Sovereign Key Management)
# ============================================================
# If running locally, paste your key here. 
# If on Streamlit Cloud, use st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = "YOUR_ACTUAL_GROQ_API_KEY_HERE"

# ============================================================
# 2. SOVEREIGN SCHEMAS 
# ============================================================
class ArbitrageDecision(BaseModel):
    action: Literal['MAX_COMPUTE', 'SELL_GRID', 'THERMAL_PROTECT'] = Field(description="Operational directive.")
    power_limit_kw: int = Field(ge=50, le=500, description="GPU power cap.")
    expected_profit_delta: float = Field(description="Projected hourly P&L change.")
    audit_trace: str = Field(description="Reasoning for Data Factory.")

# ============================================================
# 3. THE GOVERNOR (DeepSeek-V4-Pro Logic)
# ============================================================
model = GroqModel('deepseek-v4-pro')
governor = Agent(model)

SYSTEM_INSTRUCTION = (
    "You are the Sovereign Governor. Mission: Maximize Profit-per-Watt. "
    "Logic: If Grid Price > Compute Yield (215.0), SELL electricity to the grid. "
    "Logic: If Compute Yield > Grid Price, MAXIMIZE Compute throughput. "
    "Safety: If Temp > 85°C, FORCE THERMAL_PROTECT regardless of profit. "
    "Respond strictly as an ArbitrageDecision object."
)

# ============================================================
# 4. MISSION CONTROL (Optimized for Python 3.14)
# ============================================================
def main():
    st.set_page_config(page_title="AETHER-GOV // SOVEREIGN OS", layout="wide")
    
    # Using st.html to bypass the Python 3.14 st.markdown TypeError
    st.html("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        div[data-testid="stMetric"] { border: 1px solid #333; padding: 15px; background: #111; }
        .stButton>button { 
            background-color: #00FF41 !important; 
            color: black !important; 
            font-weight: bold; 
            width: 100%; 
            border-radius: 0px; 
            border: none;
        }
        </style>
    """)

    st.title("⚡ AETHER-GOV // Sovereign Master OS")
    st.caption("Industrial Energy-Compute Arbitrage // Raipur Hub // Nexus-Flow Protocol")
    
    with st.sidebar:
        st.header("📡 Live Telemetry")
        f_id = st.text_input("Facility ID", value="NEXUS-RAIPUR-01")
        live_temp = st.slider("Core Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=285)
        st.divider()
        st.info("Status: Enterprise Data Factory ACTIVE")

    # Real-time Spread Calculation
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Thermal Headroom", f"{90 - live_temp:.1f}°C")
    with m2:
        spread = grid_spot - 215.0
        st.metric("Market Arbitrage", f"${spread:.2f}/MWh", delta="SELL" if spread > 0 else "COMPUTE")
    with m3:
        st.metric("Groq LPU Latency", "32ms", delta="-4ms")

    if st.button("TRIGGER SOVEREIGN REASONING"):
        with st.status("Engaging DeepSeek-V4-Pro Reasoning Engine...", expanded=True) as status:
            async def run_agent():
                # Passing result_type inside the run call for maximum compatibility
                return await governor.run(
                    f"DATA: ID={f_id}, TEMP={live_temp}C, SPOT={grid_spot}. {SYSTEM_INSTRUCTION}",
                    result_type=ArbitrageDecision
                )
            
            try:
                result = asyncio.run(run_agent())
                res = result.data
                
                status.update(label="Directive Calculated", state="complete")
                
                st.subheader(f"DIRECTIVE: {res.action}")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Hardware Target:** `{res.power_limit_kw} KW`")
                    st.write(f"**Financial Delta:** `+${res.expected_profit_delta}/hr`")
                with col_b:
                    with st.expander("Audit Logic Trace"):
                        st.info(res.audit_trace)
                
                # Visual Feedback
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number", value = res.power_limit_kw,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Assigned Power (KW)", 'font': {'color': "#00FF41"}},
                    gauge = {
                        'axis': {'range': [None, 500], 'tickcolor': "#00FF41"},
                        'bar': {'color': "#00FF41"},
                        'steps': [
                            {'range': [0, 300], 'color': "#111"},
                            {'range': [400, 500], 'color': "#300"}
                        ],
                    }
                ))
                fig.update_layout(paper_bgcolor="#050505", font={'color': "#00FF41"})
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Sovereign Reasoning Interrupted: {str(e)}")
                status.update(label="Critical Failure", state="error")

if __name__ == "__main__":
    main()
