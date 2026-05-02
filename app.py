import os
import asyncio
import json
import streamlit as st
import plotly.graph_objects as go
from typing import Literal
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. SECURE AUTHENTICATION (NEXUS-FLOW PROTOCOL)
# ============================================================
if "GROQ_API_KEY" in st.secrets:
    # strip() ensures no accidental whitespace causes 401 errors
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"].strip()
else:
    st.error("🚨 CRITICAL: GROQ_API_KEY not found in Streamlit Secrets.")
    st.stop()

# ============================================================
# 2. THE GOVERNOR (Sovereign Positional Initialization)
# ============================================================
# Positional model injection satisfies strict Python 3.14 constructors
model = GroqModel('deepseek-v4-pro')
governor = Agent(model) 

# ============================================================
# 3. MISSION CONTROL: ENTERPRISE AI FACTORY
# ============================================================
def main():
    st.set_page_config(
        page_title="AETHER-GOV // MASTER OS", 
        page_icon="⚡", 
        layout="wide"
    )
    
    # Nexus-Flow Dark-Mode Aesthetic
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
            height: 3em;
        }
        .stButton>button:hover { background-color: #00CC33 !important; }
        </style>
    """)

    st.title("⚡ AETHER-GOV // NEXUS-FLOW MASTER OS")
    st.caption("Raipur Hub // Enterprise Data AI Factory // v4.0 Sovereign-Core")
    
    with st.sidebar:
        st.header("📡 INFRASTRUCTURE")
        st.write("**Node:** NEXUS-RAIPUR-SEC-01")
        st.write("**Compute:** Groq LPU Array")
        st.divider()
        st.header("📊 LIVE TELEMETRY")
        live_temp = st.slider("Core Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=285)
        st.divider()
        st.success("AUTHENTICATION: VERIFIED")

    # Nexus-Flow Telemetry HUD
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Thermal Headroom", f"{90 - live_temp:.1f}°C")
    with m2:
        # Business Logic: Profitability benchmark at $215/MWh
        spread = grid_spot - 215.0
        st.metric("Arbitrage Spread", f"${spread:.2f}/MWh", delta="SELL" if spread > 0 else "COMPUTE")
    with m3:
        st.metric("LPU Inference", "32ms", delta="-4ms")

    # Execution Trigger
    if st.button("EXECUTE SOVEREIGN REASONING"):
        async def run_governor():
            # Instructions and JSON Schema are defined here to bypass Agent keyword issues
            prompt = f"""
            SYSTEM ROLE: Sovereign Governor.
            GOAL: Maximize Profit-per-Watt for the Enterprise AI Factory.
            
            OPERATIONAL LOGIC:
            - If Grid Price > 215.0, Action = SELL_GRID.
            - If Grid Price <= 215.0, Action = MAX_COMPUTE.
            - If Temperature > 85.0C, Action = THERMAL_PROTECT (Override).
            
            CURRENT TELEMETRY:
            - Facility Temp: {live_temp}C
            - Grid Price: ${grid_spot}/MWh
            
            JSON OUTPUT FORMAT:
            {{
                "action": "STRING",
                "power_limit_kw": "INT (50-500)",
                "expected_profit_delta": "FLOAT",
                "audit_trace": "ONE_SENTENCE_REASONING"
            }}
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Nexus-Flow calculating Energy-Compute Nexus...", expanded=True) as status:
                result = asyncio.run(run_governor())
                
                # Robust extraction to handle potential LLM markdown tags
                raw_data = result.data.replace('```json', '').replace('```', '').strip()
                res = json.loads(raw_data)
                
                status.update(label="Sovereign Decision Finalized", state="complete")
            
            st.divider()
            st.header(f"DIRECTIVE: {res['action']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Target Power Cap", f"{res['power_limit_kw']} KW")
                st.write(f"**Financial Delta:** `+${res['expected_profit_delta']}/hr`")
            with col_b:
                st.subheader("Audit Logic Trace")
                st.info(res['audit_trace'])
            
            # Interactive Data Dashboard Visualization
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = res['power_limit_kw'],
                title = {'text': "Power Allocation (KW)", 'font': {'color': "#00FF41"}},
                gauge = {
                    'axis': {'range': [None, 500], 'tickcolor': "#00FF41"},
                    'bar': {'color': "#00FF41"},
                    'steps': [
                        {'range': [0, 400], 'color': "#111"},
                        {'range': [400, 500], 'color': "#300"}
                    ],
                }
            ))
            fig.update_layout(paper_bgcolor="#050505", font={'color': "#00FF41"})
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Nexus-Flow Interruption: {str(e)}")
            if 'result' in locals():
                st.code(result.data)

if __name__ == "__main__":
    main()
