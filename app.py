import os
import asyncio
import json
import streamlit as st
import plotly.graph_objects as go
from typing import Literal
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. AUTHENTICATION & SECURE ACCESS
# ============================================================
# Replace with your actual Groq API Key
os.environ["GROQ_API_KEY"] = "YOUR_ACTUAL_GROQ_API_KEY_HERE"

# ============================================================
# 2. THE GOVERNOR (Positional-Only Stabilization)
# ============================================================
# We use only positional arguments to satisfy strict Python 3.14 constructors
model = GroqModel('deepseek-v4-pro')
governor = Agent(model) 

# ============================================================
# 3. MISSION CONTROL: NEXUS-FLOW MASTER OS
# ============================================================
def main():
    st.set_page_config(page_title="AETHER-GOV // NEXUS-FLOW", layout="wide")
    
    # Industrial Dark-Mode Injection (Python 3.14 Safe)
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

    st.title("⚡ AETHER-GOV // NEXUS-FLOW MASTER OS")
    st.caption("Raipur Hub // Sovereign Energy-Compute Arbitrage Protocol")
    
    with st.sidebar:
        st.header("📡 ENTERPRISE AI FACTORY")
        st.info("Status: PRODUCTION-READY")
        f_id = st.text_input("Facility ID", value="NEXUS-RAIPUR-01")
        live_temp = st.slider("Core Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=285)
        st.divider()
        st.write("Architecture: DeepSeek-V4-Pro")
        st.write("Infrastructure: Groq LPU")

    # Nexus-Flow Telemetry Grid
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Thermal Headroom", f"{90 - live_temp:.1f}°C")
    with m2:
        spread = grid_spot - 215.0
        st.metric("Arbitrage Spread", f"${spread:.2f}/MWh", delta="SELL" if spread > 0 else "COMPUTE")
    with m3:
        st.metric("LPU Latency", "32ms", delta="-5ms")

    # Execution Layer
    if st.button("EXECUTE SOVEREIGN REASONING"):
        async def run_governor():
            # Schema and Logic are injected directly into the prompt to avoid Agent keyword errors
            prompt = f"""
            SYSTEM ROLE: Sovereign Governor for Enterprise AI Factory.
            FACILITY: {f_id}
            
            LOGIC RULES:
            1. If Grid Price > 215.0, SELL electricity to the grid (SELL_GRID).
            2. If Compute Yield > Grid Price, MAXIMIZE GPU throughput (MAX_COMPUTE).
            3. If Core Temp > 85.0C, override all for safety (THERMAL_PROTECT).
            
            CURRENT DATA:
            - Temperature: {live_temp}C
            - Grid Price: ${grid_spot}/MWh
            
            RESPONSE FORMAT:
            You MUST return ONLY a raw JSON object with these keys:
            "action": (MAX_COMPUTE, SELL_GRID, or THERMAL_PROTECT)
            "power_limit_kw": (integer between 50 and 500)
            "expected_profit_delta": (float)
            "audit_trace": (one-sentence reasoning)
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Nexus-Flow analyzing Energy-Compute Arbitrage...", expanded=True) as status:
                result = asyncio.run(run_governor())
                
                # Manual JSON Extraction to bypass result_type bugs
                clean_json = result.data.replace('```json', '').replace('```', '').strip()
                res = json.loads(clean_json)
                
                status.update(label="Sovereign Decision Logged", state="complete")
            
            st.divider()
            st.header(f"DIRECTIVE: {res['action']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Target Power Cap", f"{res['power_limit_kw']} KW")
                st.write(f"**Financial Delta:** `+${res['expected_profit_delta']}/hr`")
            with col_b:
                st.subheader("Enterprise AI Factory Audit")
                st.info(res['audit_trace'])
            
            # Sovereign Dashboard Visualization
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = res['power_limit_kw'],
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
            st.error(f"Nexus-Flow Interruption: {str(e)}")
            st.code(result.data if 'result' in locals() else "No response from LPU.")

if __name__ == "__main__":
    main()
