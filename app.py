import os
import asyncio
import json
import re
import streamlit as st
import plotly.graph_objects as go
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. AUTHENTICATION & NODE CONFIG
# ============================================================
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"].strip()
else:
    st.error("🚨 CRITICAL: GROQ_API_KEY missing.")
    st.stop()

model = GroqModel('llama-3.3-70b-versatile')
governor = Agent(model) 

def main():
    st.set_page_config(page_title="ENTERPRISE AI FACTORY", page_icon="🏭", layout="wide")
    
    # INDUSTRIAL INTERFACE INJECTION
    st.html("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        .factory-banner {
            border: 2px solid #00FF41; padding: 20px; text-align: center;
            background: rgba(0, 255, 65, 0.1); margin-bottom: 25px;
        }
        .node-status { color: #00FF41; font-weight: bold; text-transform: uppercase; }
        div[data-testid="stMetric"] { border: 1px solid #333; background: #111; }
        .stButton>button { 
            background-color: #00FF41 !important; color: black !important; 
            font-weight: bold; width: 100%; border: none; height: 4em; font-size: 1.2em;
        }
        </style>
    """)

    # BIG DISPLAY: ENTERPRISE AI FACTORY
    st.html("""
        <div class="factory-banner">
            <h1 style="margin:0; letter-spacing: 5px;">🏭 ENTERPRISE AI FACTORY</h1>
            <p style="margin:5px 0 0 0; color: #888;">RAIPUR HUB // NEXUS-FLOW COMMAND CENTER</p>
        </div>
    """)
    
    with st.sidebar:
        st.header("🏢 FACILITY MGMT")
        st.info("NODE: RAIPUR-SEC-01")
        st.divider()
        st.header("📊 TELEMETRY")
        live_temp = st.slider("Core Temperature (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=285)
        st.divider()
        st.write("Engine: **Llama-3.3-Stable**")

    # HUD COLUMNS
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Thermal Headroom", f"{90 - live_temp:.1f}°C")
    with m2:
        spread = grid_spot - 215.0
        st.metric("Arbitrage Spread", f"${spread:.2f}/MWh")
    with m3:
        st.metric("Factory Status", "OPERATIONAL", delta="ACTIVE")

    if st.button("RUN SOVEREIGN FACTORY REASONING"):
        async def run_governor():
            prompt = f"""
            SYSTEM: Enterprise AI Factory Governor.
            CONTEXT: Raipur Hub Arbitrage.
            DATA: Temp {live_temp}C, Price ${grid_spot}/MWh.
            LOGIC: Price > 215? SELL_GRID : MAX_COMPUTE. Temp > 85? THERMAL_PROTECT.
            
            Return ONLY a raw JSON object with DOUBLE QUOTES.
            {{
                "action": "STR",
                "power_limit_kw": INT,
                "expected_profit_delta": FLOAT,
                "audit_trace": "STR"
            }}
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Engaging Nexus-Flow...", expanded=True):
                response = asyncio.run(run_governor())
                raw_data = str(getattr(response, 'data', getattr(response, 'result', response))).strip()
                
                # PARSER & SANITIZER
                start = raw_data.find('{')
                end = raw_data.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = raw_data[start:end]
                    # Fix quote issues
                    json_str = re.sub(r"'(.*?)'(?=\s*:)", r'"\1"', json_str)
                    json_str = re.sub(r":\s*'(.*?)'", r': "\1"', json_str)
                    if json_str.count("'") > json_str.count('"'):
                        json_str = json_str.replace("'", '"')
                    
                    res = json.loads(json_str)
                else:
                    st.error("Data Stream Interrupted.")
                    st.stop()
            
            st.divider()
            st.subheader(f"FACTORY DIRECTIVE: {res['action']}")
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Power Cap", f"{res['power_limit_kw']} KW")
                st.write(f"**Profit Impact:** `+${res['expected_profit_delta']}/hr`")
            with c2:
                st.success(f"**Audit Trace:** {res['audit_trace']}")
            
            # Gauge Visualization
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = res['power_limit_kw'],
                gauge = {'axis': {'range': [None, 500]}, 'bar': {'color': "#00FF41"}}
            ))
            fig.update_layout(paper_bgcolor="#050505", font={'color': "#00FF41"})
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Sovereign Error: {e}")
            if 'raw_data' in locals():
                with st.expander("Debug Nexus Stream"):
                    st.code(raw_data)

if __name__ == "__main__":
    main()
