import os
import asyncio
import json
import re
import random
import datetime
import streamlit as st
import plotly.graph_objects as go
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# ============================================================
# 1. INFRASTRUCTURE & SECURITY
# ============================================================
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"].strip()
else:
    st.error("🚨 CRITICAL: GROQ_API_KEY missing.")
    st.stop()

# ============================================================
# 2. SOVEREIGN LEDGER (THE AUDIT TRAIL)
# ============================================================
def commit_to_ledger(data):
    """Saves every sovereign decision to a secure local audit file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"timestamp": timestamp, "telemetry": st.session_state.telemetry, "decision": data}
    with open("sovereign_ledger.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

# ============================================================
# 3. PHYSICAL BRIDGE (ACTUATION SIMULATOR)
# ============================================================
def dispatch_hardware_command(action, kw_limit):
    """
    Simulates sending a signal to the Raipur Hub Power Management System.
    In production: Replace with API/SNMP calls to physical breakers.
    """
    status = f"SIGNAL_SENT: {action} AT {kw_limit}KW"
    return status

# ============================================================
# 4. DATA NERVOUS SYSTEM (LIVE TELEMETRY)
# ============================================================
def get_live_data():
    return {
        "grid_price": round(random.uniform(180.0, 320.0), 2),
        "core_temp": round(random.uniform(55.0, 95.0), 1)
    }

# ============================================================
# 5. THE GOVERNOR (STABLE ENGINE)
# ============================================================
model = GroqModel('llama-3.3-70b-versatile')
governor = Agent(model)

# ============================================================
# 6. MASTER OS INTERFACE
# ============================================================
def main():
    st.set_page_config(page_title="SOVEREIGN STAGE 4 // RAIPUR HUB", page_icon="🏛️", layout="wide")
    
    st.html("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        div[data-testid="stMetric"] { border: 1px solid #333; background: #111; border-left: 5px solid #00FF41; }
        .stButton>button { background-color: #00FF41 !important; color: black !important; font-weight: bold; border-radius: 0px; height: 3.5em; }
        .log-terminal { background-color: #000; border: 1px solid #00FF41; padding: 10px; color: #00FF41; font-size: 0.8em; }
        </style>
    """)

    st.markdown("<h1 style='color: #00FF41; margin-bottom: 0px;'>⚡ Sovereign Energy-Compute Arbitrage</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00FF41; opacity: 0.8; letter-spacing: 2px;'>STAGE 4: PHYSICAL ACTUATION & AUDIT LEDGER</p>", unsafe_allow_html=True)

    if 'telemetry' not in st.session_state:
        st.session_state.telemetry = get_live_data()

    # SIDEBAR: LEDGER VIEWER
    with st.sidebar:
        st.header("📋 AUDIT LEDGER")
        if st.button("PULL REFRESH"):
            st.session_state.telemetry = get_live_data()
        st.divider()
        st.write("**Node:** NEXUS-RAIPUR-01")
        if os.path.exists("sovereign_ledger.jsonl"):
            with open("sovereign_ledger.jsonl", "r") as f:
                logs = f.readlines()
                st.caption(f"Total Audit Entries: {len(logs)}")
        st.success("STAGE 4 CORE: ACTIVE")

    # HUD
    m1, m2, m3 = st.columns(3)
    m1.metric("Market Price", f"${st.session_state.telemetry['grid_price']}/MWh")
    m2.metric("Chiller Temp", f"{st.session_state.telemetry['core_temp']}°C")
    m3.metric("Actuation Status", "CONNECTED", delta="READY")

    st.divider()

    if st.button("DEPLOY SOVEREIGN COMMAND"):
        async def execute_governance():
            prompt = f"""
            Role: Sovereign Governor Stage 4. 
            Telemetry: Price ${st.session_state.telemetry['grid_price']}, Temp {st.session_state.telemetry['core_temp']}C.
            Logic: Pivot $215/MWh. Thermal safety 85C.
            Return ONLY JSON: {{"action": "STR", "power_limit_kw": INT, "profit_delta": FLOAT, "trace": "STR"}}
            """
            return await governor.run(prompt)

        try:
            with st.status("Computing Sovereign Trajectory...", expanded=True):
                response = asyncio.run(execute_governance())
                raw = str(getattr(response, 'data', getattr(response, 'result', response))).strip()
                
                # SELF-HEALING PARSER
                match = re.search(r'\{.*\}', raw, re.DOTALL)
                if match:
                    json_str = match.group().replace("'", '"')
                    res = json.loads(json_str)
                else:
                    raise ValueError("Handshake Failed.")

                # STAGE 4: THE BRIDGE & THE LEDGER
                actuation_log = dispatch_hardware_command(res['action'], res['power_limit_kw'])
                commit_to_ledger(res)

            # UI DISPLAY
            st.header(f"DIRECTIVE: {res['action']}")
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.metric("Final Load Assignment", f"{res['power_limit_kw']} KW")
                fig = go.Figure(go.Indicator(mode="gauge+number", value=res['power_limit_kw'], gauge={'axis':{'range':[None, 500]}, 'bar':{'color':"#00FF41"}}))
                fig.update_layout(paper_bgcolor="#050505", font={'color':"#00FF41"}, height=250)
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                st.markdown("<div class='log-terminal'>", unsafe_allow_html=True)
                st.write(f"**[BRIDGE]** {actuation_log}")
                st.write(f"**[LEDGER]** Entry committed to sovereign_ledger.jsonl")
                st.write(f"**[REASON]** {res['trace']}")
                st.write(f"**[PROFIT]** Projected +${res['profit_delta']}/hr")
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Sovereign Breach: {e}")

if __name__ == "__main__":
    main()
