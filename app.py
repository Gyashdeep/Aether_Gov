import os
import asyncio
import json
import re
import random
import streamlit as st
import plotly.graph_objects as go
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# STAGE 1: SECURE INFRASTRUCTURE AUTHENTICATION
# ============================================================
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"].strip()
else:
    st.error("🚨 CRITICAL: GROQ_API_KEY missing from Secrets.")
    st.stop()

# ============================================================
# STAGE 2: THE NERVOUS SYSTEM (LIVE DATA CONNECTIVITY)
# ============================================================
def get_live_market_data():
    """Simulates real-time telemetry from IEX and Hub Sensors."""
    return {
        "grid_price": round(random.uniform(185.0, 315.0), 2),
        "core_temp": round(random.uniform(60.0, 92.0), 1),
        "load_capacity": random.randint(400, 500)
    }

# ============================================================
# STAGE 3: THE GOVERNOR (STABLE REASONING CORE)
# ============================================================
# Locked to Llama-3.3-70b-Versatile for 2026 stability.
model = GroqModel('llama-3.3-70b-versatile')
governor = Agent(model) 

# ============================================================
# STAGE 4: MASTER OS INTERFACE & INDUSTRIAL UI
# ============================================================
def main():
    st.set_page_config(page_title="SOVEREIGN ARBITRAGE // MASTER OS", page_icon="⚡", layout="wide")
    
    # Custom CSS for the Matrix-Industrial Aesthetic
    st.html("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        div[data-testid="stMetric"] { border: 1px solid #333; padding: 15px; background: #111; border-left: 4px solid #00FF41; }
        .stButton>button { 
            background-color: #00FF41 !important; color: black !important; 
            font-weight: bold; width: 100%; border-radius: 0px; border: none; height: 3.5em;
        }
        .main-headline { color: #00FF41; margin-bottom: 0px; font-weight: 800; text-transform: uppercase; }
        .sub-name { color: #00FF41; opacity: 0.8; margin-top: 0px; letter-spacing: 2px; font-size: 0.9em; }
        </style>
    """)

    st.markdown("<h1 class='main-headline'>⚡ Sovereign Energy-Compute Arbitrage</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-name'>ENTERPRISE AI FACTORY // RAIPUR HUB</p>", unsafe_allow_html=True)
    st.caption("Nexus-Flow v9.0 // Zero-Fault Sovereign Core")
    
    # Initialize or Refresh Telemetry
    if 'telemetry' not in st.session_state or st.sidebar.button("REFRESH SENSORS"):
        st.session_state.telemetry = get_live_market_data()

    data = st.session_state.telemetry

    with st.sidebar:
        st.header("📡 INFRASTRUCTURE")
        st.write(f"**Grid Spot:** ${data['grid_price']}/MWh")
        st.write(f"**Chiller Intake:** {data['core_temp']}°C")
        st.divider()
        st.write("**Node:** NEXUS-RAIPUR-01")
        st.write("**Asset:** LPU Cluster Alpha")
        st.success("ENGINE: LLAMA-3.3-STABLE")

    # HUD TELEMETRY
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Thermal Headroom", f"{90 - data['core_temp']:.1f}°C")
    with m2:
        spread = data['grid_price'] - 215.0
        st.metric("Arbitrage Spread", f"${spread:.2f}", delta="SELL_GRID" if spread > 0 else "MAX_COMPUTE")
    with m3:
        st.metric("Facility Load", f"{data['load_capacity']} KW", delta="ACTIVE")

    st.divider()

    # ============================================================
    # STAGE 5: EXECUTION & SELF-HEALING REASONING
    # ============================================================
    if st.button("EXECUTE SOVEREIGN COMMAND"):
        async def run_governor():
            # Providing a Few-Shot example inside the prompt to ensure JSON compliance
            prompt = f"""
            Role: Sovereign Governor for Enterprise AI Factory.
            
            Logic: 
            - Pivot: $215/MWh. 
            - If Price > 215, Action = SELL_GRID. 
            - If Price <= 215, Action = MAX_COMPUTE. 
            - If Temp > 85, Action = THERMAL_PROTECT (Override).
            
            Current Telemetry:
            - Price: ${data['grid_price']}
            - Temp: {data['core_temp']}C
            
            Return ONLY a JSON object with DOUBLE QUOTES:
            {{"action": "STR", "power_limit_kw": INT, "expected_profit_delta": FLOAT, "audit_trace": "STR"}}
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Analyzing Energy-Compute Nexus...", expanded=True):
                response = asyncio.run(run_governor())
                raw_data = str(getattr(response, 'data', getattr(response, 'result', response))).strip()
                
                # THE IRONCLAD PARSER (Regex based quote fixing)
                start = raw_data.find('{')
                end = raw_data.rfind('}') + 1
                
                if start != -1 and end != 0:
                    json_str = raw_data[start:end]
                    
                    # Fix keys and values using single quotes
                    json_str = re.sub(r"'(.*?)'(?=\s*:)", r'"\1"', json_str)
                    json_str = re.sub(r":\s*'(.*?)'", r': "\1"', json_str)
                    
                    # Safety check for the "Char 1" error
                    if json_str.startswith("'"):
                        json_str = json_str.replace("'", '"')
                        
                    res = json.loads(json_str)
                else:
                    raise ValueError("Malformed Stream: No JSON detected.")

            # UI OUTPUT: DIRECTIVE
            st.header(f"DIRECTIVE: {res['action']}")
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Commanded Load", f"{res['power_limit_kw']} KW")
                
                # Visual Power Gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number", value = res['power_limit_kw'],
                    gauge = {
                        'axis': {'range': [None, 500], 'tickcolor': "#00FF41"},
                        'bar': {'color': "#00FF41"},
                        'bgcolor': "#111",
                        'steps': [{'range': [400, 500], 'color': "#300"}]
                    }
                ))
                fig.update_layout(paper_bgcolor="#050505", font={'color': "#00FF41"}, height=280)
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                st.info(f"**Reasoning:** {res['audit_trace']}")
                st.code(f"""
                [SYSTEM_LOG] Decision: {res['action']}
                [SYSTEM_LOG] Power_Cap: {res['power_limit_kw']} KW
                [SYSTEM_LOG] Profit_Impact: ${res['expected_profit_delta']}/hr
                [SYSTEM_LOG] Status: Command Executed to Raipur Hub
                """, language="bash")
            
        except Exception as e:
            st.error(f"Sovereign Error: {e}")
            if 'raw_data' in locals():
                with st.expander("View Raw Nexus Stream"):
                    st.code(raw_data)

if __name__ == "__main__":
    main()
