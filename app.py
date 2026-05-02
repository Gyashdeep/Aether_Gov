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
# 3. THE GOVERNOR (Strictly Formatted)
# ============================================================
model = GroqModel('deepseek-v4-pro')

# Corrected for Pydantic AI strict argument validation
governor = Agent(
    model,
    result_type=ArbitrageDecision,
    system_prompt="Maximize Profit-per-Watt based on energy/compute spread."
)

# ============================================================
# 4. MISSION CONTROL (Streamlit)
# ============================================================
def main():
    st.set_page_config(page_title="AETHER-GOV", layout="wide")
    
    # Python 3.14 compatible CSS injection
    st.html("<style>.stApp{background-color:#050505;color:#00FF41;font-family:monospace;}</style>")
    st.html("<style>div[data-testid='stMetric']{border:1px solid #333;background:#111;}</style>")

    st.title("⚡ AETHER-GOV // Sovereign OS")
    
    with st.sidebar:
        st.header("📡 Telemetry")
        live_temp = st.slider("Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Price ($/MWh)", value=285)

    if st.button("TRIGGER SOVEREIGN REASONING"):
        async def run_agent():
            # Pass everything the agent needs in the prompt string for maximum stability
            prompt = f"STATUS: Temp {live_temp}C, Grid ${grid_spot}/MWh. Decide action."
            return await governor.run(prompt)
        
        try:
            result = asyncio.run(run_agent())
            res = result.data
            
            st.subheader(f"DIRECTIVE: {res.action}")
            st.metric("Power Target", f"{res.power_limit_kw} KW")
            st.info(f"Audit: {res.audit_trace}")
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = res.power_limit_kw,
                gauge = {'axis': {'range': [None, 500]}, 'bar': {'color': "#00FF41"}}
            ))
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Execution Error: {e}")

if __name__ == "__main__":
    main()
