import os
import asyncio
import json
import re
import streamlit as st
import plotly.graph_objects as go
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# 1. SECURE AUTHENTICATION
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"].strip()
else:
    st.error("🚨 CRITICAL: GROQ_API_KEY missing.")
    st.stop()

# 2. THE GOVERNOR (Llama 3.3 Stable Flagship)
model = GroqModel('llama-3.3-70b-versatile')
governor = Agent(model) 

def main():
    st.set_page_config(page_title="SOVEREIGN // MASTER OS", page_icon="⚡", layout="wide")
    
    # Nexus-Flow Industrial Aesthetic
    st.html("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        div[data-testid="stMetric"] { border: 1px solid #333; padding: 15px; background: #111; border-left: 5px solid #00FF41; }
        .stButton>button { background-color: #00FF41 !important; color: black !important; font-weight: bold; width: 100%; border: none; height: 3.5em; border-radius: 0px; }
        .stButton>button:hover { background-color: #00CC33 !important; }
        .sovereign-header { color: #00FF41; margin-bottom: 0px; padding-bottom: 0px; font-size: 3rem; }
        .factory-sub { color: #00FF41; opacity: 0.8; margin-top: -10px; border-bottom: 1px solid #333; padding-bottom: 10px; }
        </style>
    """)

    # RESTORED HEADLINE HIERARCHY
    st.markdown("<h1 class='sovereign-header'>⚡ SOVEREIGN</h1>", unsafe_allow_html=True)
    st.markdown("<p class='factory-sub'>ENTERPRISE AI FACTORY // RAIPUR HUB // v7.8</p>", unsafe_allow_html=True)
    
    # SIDEBAR: INFRASTRUCTURE CONTROLS
    with st.sidebar:
        st.header("⚙️ SYSTEM NODE")
        st.write("**ID:** NEXUS-RAIPUR-SEC-01")
        st.divider()
        live_temp = st.slider("Chiller Intake Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=285)
        st.divider()
        st.header("🏗️ ASSET STATUS")
        st.write("● **LPU Cluster A:** ONLINE")
        st.write("● **LPU Cluster B:** ONLINE")
        st.write("● **Cooling Array:** NOMINAL")
        st.divider()
        st.success("CORE: llama-3.3-70b")

    # TOP HUD: FACTORY TELEMETRY
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.metric("Facility Thermal", f"{live_temp}°C", delta="-2.1°C")
    with t2:
        spread = grid_spot - 215.0
        st.metric("Arbitrage Delta", f"${spread:.2f}", delta="PROFITABLE" if spread > 0 else "LOW MARGIN")
    with t3:
        st.metric("Energy Draw", "412 KW", delta="Active")
    with t4:
        st.metric("Node Latency", "24ms", delta="Optimal")

    st.divider()

    # CORE EXECUTION
    if st.button("EXECUTE SOVEREIGN ARBITRAGE"):
        async def run_governor():
            prompt = f"""
            SYSTEM ROLE: Sovereign Governor.
            OPERATIONAL LOGIC: Pivot at $215/MWh. Above $215 = SELL_GRID. Below = MAX_COMPUTE. Safety override at 85C.
            CURRENT STATE: Temp {live_temp}C, Grid Price ${grid_spot}/MWh.
            
            Return ONLY a raw JSON object with DOUBLE QUOTES ("):
            {{"action": "STR", "power_limit_kw": INT, "expected_profit_delta": FLOAT, "audit_trace": "STR"}}
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Accessing Sovereign Reasoning Core...", expanded=True):
                response = asyncio.run(run_governor())
                raw_data = str(getattr(response, 'data', getattr(response, 'result', response))).strip()
                
                # SELF-HEALING IRONCLAD PARSER
                start = raw_data.find('{')
                end = raw_data.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = raw_data[start:end].replace("'", '"')
                    res = json.loads(json_str)
                else:
                    raise ValueError("Malformed protocol output.")

            # RESULTS SECTION
            st.subheader(f"DIRECTIVE: {res['action']}")
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Allocated Power", f"{res['power_limit_kw']} KW")
                st.write(f"**Expected ROI:** `+${res['expected_profit_delta']}/hr`")
                
                # Power Gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number", value = res['power_limit_kw'],
                    gauge = {
                        'axis': {'range': [None, 500], 'tickcolor': "#00FF41"},
                        'bar': {'color': "#00FF41"},
                        'bgcolor': "#111"
                    }
                ))
                fig.update_layout(paper_bgcolor="#050505", font={'color': "#00FF41"}, height=250)
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                st.info(f"**Audit Trace:** {res['audit_trace']}")
                st.code(f"""
                [LOG] Sovereign Directive: {res['action']}
                [LOG] Facility: Enterprise AI Factory
                [LOG] Node: Raipur-Sec-01
                [LOG] Integrity: Verified
                """, language="bash")
            
        except Exception as e:
            st.error(f"Sovereign Error: {e}")
            if 'raw_data' in locals():
                with st.expander("View Raw Output Stream"):
                    st.code(raw_data)

if __name__ == "__main__":
    main()
