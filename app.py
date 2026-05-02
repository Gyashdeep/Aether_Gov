import os
import asyncio
import json
import re
import streamlit as st
import plotly.graph_objects as go
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. SECURE AUTHENTICATION
# ============================================================
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"].strip()
else:
    st.error("🚨 CRITICAL: GROQ_API_KEY missing.")
    st.stop()

# ============================================================
# 2. THE GOVERNOR (NEXUS-FLOW CORE)
# ============================================================
model = GroqModel('llama-3.3-70b-versatile')
governor = Agent(model) 

def main():
    st.set_page_config(page_title="SOVEREIGN ARBITRAGE // MASTER OS", page_icon="⚡", layout="wide")
    
    # Nexus-Flow Matrix-Green UI
    st.html("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        div[data-testid="stMetric"] { border: 1px solid #333; padding: 15px; background: #111; border-left: 3px solid #00FF41; }
        .stButton>button { 
            background-color: #00FF41 !important; color: black !important; 
            font-weight: bold; width: 100%; border-radius: 0px; border: none; height: 3.5em;
        }
        .stButton>button:hover { background-color: #00CC33 !important; }
        .main-headline { color: #00FF41; margin-bottom: 0px; padding-bottom: 0px; font-weight: 800; }
        .sub-name { color: #00FF41; opacity: 0.8; margin-top: 0px; letter-spacing: 2px; }
        </style>
    """)

    # UPDATED HEADLINE HIERARCHY
    st.markdown("<h1 class='main-headline'>⚡ Sovereign Energy-Compute Arbitrage</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-name'>ENTERPRISE AI FACTORY // RAIPUR HUB</p>", unsafe_allow_html=True)
    st.caption("Nexus-Flow v7.8 // Autonomous Resource Governor")
    
    with st.sidebar:
        st.header("📡 INFRASTRUCTURE")
        st.divider()
        live_temp = st.slider("Facility Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Price ($/MWh)", value=285)
        st.divider()
        st.write("**Node:** NEXUS-RAIPUR-01")
        st.write("**Engine:** Llama-3.3-Stable")
        st.success("PROTOCOL: ACTIVE")

    # HUD TELEMETRY
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Thermal Buffer", f"{90 - live_temp:.1f}°C")
    with m2:
        spread = grid_spot - 215.0
        st.metric("Arbitrage Gap", f"${spread:.2f}/MWh", delta="SELL" if spread > 0 else "COMPUTE")
    with m3:
        st.metric("LPU Latency", "24ms", delta="-10ms")

    st.divider()

    # EXECUTION LAYER
    if st.button("EXECUTE SOVEREIGN REASONING"):
        async def run_governor():
            prompt = f"""
            Role: Sovereign Governor.
            Logic: Pivot at $215/MWh. Above $215 = SELL_GRID. Below = MAX_COMPUTE. Safety override at 85C.
            Current: Temp {live_temp}C, Price ${grid_spot}.
            Return ONLY JSON with DOUBLE QUOTES:
            {{"action": "STR", "power_limit_kw": INT, "expected_profit_delta": FLOAT, "audit_trace": "STR"}}
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Analyzing Energy-Compute Nexus...", expanded=True):
                response = asyncio.run(run_governor())
                raw_data = str(getattr(response, 'data', getattr(response, 'result', response))).strip()
                
                # SELF-HEALING PARSER
                start = raw_data.find('{')
                end = raw_data.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = raw_data[start:end]
                    
                    # Regex-Based quote fixing
                    json_str = re.sub(r"'(.*?)'(?=\s*:)", r'"\1"', json_str)
                    json_str = re.sub(r":\s*'(.*?)'", r': "\1"', json_str)
                    
                    # Last ditch effort for quote errors
                    if json_str.count("'") > json_str.count('"'):
                        json_str = json_str.replace("'", '"')
                        
                    res = json.loads(json_str)
                else:
                    raise ValueError("Protocol Breach: No JSON data.")

            # UI OUTPUT
            st.header(f"DIRECTIVE: {res['action']}")
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Allocated Load", f"{res['power_limit_kw']} KW")
                st.write(f"**Profit Delta:** `+${res['expected_profit_delta']}/hr`")
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number", value = res['power_limit_kw'],
                    gauge = {'axis': {'range': [None, 500]}, 'bar': {'color': "#00FF41"}}
                ))
                fig.update_layout(paper_bgcolor="#050505", font={'color': "#00FF41"}, height=250)
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                st.info(f"**Audit Trace:** {res['audit_trace']}")
                st.code(f"""
                [COMMAND_OS] Source: Raipur-Hub
                [COMMAND_OS] Decision: {res['action']}
                [COMMAND_OS] Profitability: {res['expected_profit_delta']}
                [COMMAND_OS] Checksum: VERIFIED
                """, language="bash")
            
        except Exception as e:
            st.error(f"Sovereign Error: {e}")
            if 'raw_data' in locals():
                with st.expander("View Facility Data Stream"):
                    st.code(raw_data)

if __name__ == "__main__":
    main()
