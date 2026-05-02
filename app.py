import os
import asyncio
import json
import streamlit as st
import plotly.graph_objects as go
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. SECURE AUTHENTICATION (ENTERPRISE AI FACTORY PROTOCOL)
# ============================================================
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"].strip()
else:
    st.error("🚨 CRITICAL: GROQ_API_KEY missing from Secrets.")
    st.stop()

# ============================================================
# 2. THE GOVERNOR (Stable Infrastructure)
# ============================================================
# Llama-3.3-70B provides the most stable ID for industrial logic.
model = GroqModel('llama-3.3-70b-versatile')
governor = Agent(model) 

# ============================================================
# 3. MISSION CONTROL: NEXUS-FLOW MASTER OS
# ============================================================
def main():
    st.set_page_config(page_title="AETHER-GOV // MASTER OS", page_icon="⚡", layout="wide")
    
    # Nexus-Flow Master OS Dark-Mode Aesthetic
    st.html("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        div[data-testid="stMetric"] { border: 1px solid #333; padding: 15px; background: #111; }
        .stButton>button { 
            background-color: #00FF41 !important; color: black !important; 
            font-weight: bold; width: 100%; border-radius: 0px; border: none; height: 3.5em;
        }
        .stButton>button:hover { background-color: #00CC33 !important; }
        </style>
    """)

    st.title("⚡ AETHER-GOV // NEXUS-FLOW MASTER OS")
    st.caption("Raipur Hub // Enterprise Data AI Factory // v6.0 Resilient-Core")
    
    with st.sidebar:
        st.header("📡 INFRASTRUCTURE")
        st.write("**Node:** NEXUS-RAIPUR-01")
        st.write("**Engine:** Llama-3.3-70B")
        st.divider()
        st.header("📊 LIVE TELEMETRY")
        live_temp = st.slider("Core Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=285)
        st.divider()
        st.success("STABLE ENGINE LOADED")

    # Nexus-Flow Telemetry HUD
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Thermal Headroom", f"{90 - live_temp:.1f}°C")
    with m2:
        spread = grid_spot - 215.0
        st.metric("Arbitrage Spread", f"${spread:.2f}/MWh", delta="SELL" if spread > 0 else "COMPUTE")
    with m3:
        st.metric("LPU Latency", "24ms", delta="-8ms")

    # Execution Layer
    if st.button("EXECUTE SOVEREIGN REASONING"):
        async def run_governor():
            prompt = f"""
            SYSTEM ROLE: Sovereign Governor for Enterprise AI Factory.
            
            OPERATIONAL LOGIC:
            - Threshold: $215/MWh (Compute Profitability).
            - If Grid Price > 215.0, Action = SELL_GRID.
            - If Grid Price <= 215.0, Action = MAX_COMPUTE.
            - If Temperature > 85.0C, Action = THERMAL_PROTECT (Safety Override).
            
            CURRENT DATA:
            - Temperature: {live_temp}C
            - Grid Price: ${grid_spot}/MWh
            
            RETURN FORMAT:
            You must return a raw JSON object with these keys:
            {{
                "action": "STRING (MAX_COMPUTE, SELL_GRID, THERMAL_PROTECT)",
                "power_limit_kw": "INT (50-500)",
                "expected_profit_delta": "FLOAT",
                "audit_trace": "ONE_SENTENCE_REASONING"
            }}
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Accessing Nexus-Flow Core...", expanded=True):
                response = asyncio.run(run_governor())
                
                # 1. EXTRACT RAW DATA SAFELY
                raw_data = str(getattr(response, 'data', getattr(response, 'result', response))).strip()
                
                # 2. IRONCLAD PARSER (Locate JSON boundaries regardless of surrounding text)
                start_index = raw_data.find('{')
                end_index = raw_data.rfind('}') + 1
                
                if start_index != -1 and end_index != 0:
                    json_str = raw_data[start_index:end_index]
                    res = json.loads(json_str)
                else:
                    raise ValueError("Incomplete Protocol: No valid JSON detected in LPU stream.")
            
            st.divider()
            st.header(f"DIRECTIVE: {res['action']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Power Allocation", f"{res['power_limit_kw']} KW")
                st.write(f"**Financial Impact:** `+${res['expected_profit_delta']}/hr`")
            with col_b:
                st.subheader("Audit Logic Trace")
                st.info(res['audit_trace'])
            
            # Dashboard Visualization
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = res['power_limit_kw'],
                title = {'text': "Power Assignment (KW)", 'font': {'color': "#00FF41"}},
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
            st.error(f"Sovereign Error: {e}")
            if 'raw_data' in locals():
                with st.expander("View Raw Nexus-Flow Stream"):
                    st.code(raw_data)

if __name__ == "__main__":
    main()
