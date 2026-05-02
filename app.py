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
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"].strip()
else:
    st.error("🚨 CRITICAL: GROQ_API_KEY missing from Secrets.")
    st.stop()

# ============================================================
# 2. THE GOVERNOR (Switching to STABLE Flagship ID)
# ============================================================
# 'llama-3.3-70b-versatile' is the most stable ID on Groq for 2026.
# This prevents the frequent 404/400 errors from deprecated distillations.
model = GroqModel('llama-3.3-70b-versatile')
governor = Agent(model) 

# ============================================================
# 3. MISSION CONTROL: ENTERPRISE AI FACTORY
# ============================================================
def main():
    st.set_page_config(page_title="AETHER-GOV // MASTER OS", page_icon="⚡", layout="wide")
    
    st.html("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        div[data-testid="stMetric"] { border: 1px solid #333; padding: 15px; background: #111; }
        .stButton>button { 
            background-color: #00FF41 !important; color: black !important; 
            font-weight: bold; width: 100%; border-radius: 0px; border: none; height: 3em;
        }
        </style>
    """)

    st.title("⚡ AETHER-GOV // NEXUS-FLOW MASTER OS")
    st.caption("Raipur Hub // Enterprise Data AI Factory // v5.0 Stable-Core")
    
    with st.sidebar:
        st.header("📡 INFRASTRUCTURE")
        st.write("**Node:** NEXUS-RAIPUR-01")
        st.write("**Engine:** Llama-3.3-70B-Versatile")
        st.divider()
        st.header("📊 TELEMETRY")
        live_temp = st.slider("Core Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=285)
        st.success("STABLE ENGINE LOADED")

    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Thermal Headroom", f"{90 - live_temp:.1f}°C")
    with m2: st.metric("Arbitrage Spread", f"${grid_spot - 215.0:.2f}/MWh")
    with m3: st.metric("LPU Latency", "24ms")

    if st.button("EXECUTE SOVEREIGN REASONING"):
        async def run_governor():
            prompt = f"""
            SYSTEM ROLE: Sovereign Governor for Enterprise AI Factory.
            LOGIC:
            - If Grid Price > 215.0, Action = SELL_GRID.
            - If Grid Price <= 215.0, Action = MAX_COMPUTE.
            - If Temperature > 85.0C, Action = THERMAL_PROTECT (Override).
            
            STATUS: Temp {live_temp}C, Grid ${grid_spot}/MWh.
            
            Return ONLY a raw JSON object:
            {{
                "action": "STRING",
                "power_limit_kw": "INT (50-500)",
                "expected_profit_delta": "FLOAT",
                "audit_trace": "ONE_SENTENCE_REASONING"
            }}
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Nexus-Flow analyzing energy nexus...", expanded=True):
                result = asyncio.run(run_governor())
                # Llama-3.3 is cleaner than DeepSeek; simpler parsing works here
                raw_data = result.data.strip()
                if "```json" in raw_data:
                    raw_data = raw_data.split("```json")[1].split("```")[0].strip()
                
                res = json.loads(raw_data)
            
            st.divider()
            st.header(f"DIRECTIVE: {res['action']}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Power Cap", f"{res['power_limit_kw']} KW")
                st.write(f"**Profit Delta:** `+${res['expected_profit_delta']}/hr`")
            with c2:
                st.info(res['audit_trace'])
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = res['power_limit_kw'],
                gauge = {'axis': {'range': [None, 500]}, 'bar': {'color': "#00FF41"}}
            ))
            fig.update_layout(paper_bgcolor="#050505", font={'color': "#00FF41"})
            st.plotly_chart(fig)
            
        except Exception as e:
            st.error(f"Sovereign Error: {e}")

if __name__ == "__main__":
    main()
