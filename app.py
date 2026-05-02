import os
import asyncio
import json
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
    st.error("🚨 CRITICAL: GROQ_API_KEY missing from Secrets.")
    st.stop()

# ============================================================
# 2. THE GOVERNOR (Stable Configuration)
# ============================================================
model = GroqModel('llama-3.3-70b-versatile')
governor = Agent(model) 

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
    st.caption("Raipur Hub // Enterprise Data AI Factory // v5.2 Stable-Core")
    
    with st.sidebar:
        st.header("📡 INFRASTRUCTURE")
        st.write("**Node:** NEXUS-RAIPUR-01")
        st.write("**Engine:** Llama-3.3-Stable")
        st.divider()
        live_temp = st.slider("Core Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=285)

    if st.button("EXECUTE SOVEREIGN REASONING"):
        async def run_governor():
            prompt = f"""
            Role: Sovereign Governor.
            Logic: If Grid Price > 215, SELL_GRID. Else, MAX_COMPUTE. If Temp > 85, THERMAL_PROTECT.
            Status: Temp {live_temp}C, Grid ${grid_spot}/MWh.
            Return ONLY a raw JSON object:
            {{"action": "STR", "power_limit_kw": INT, "expected_profit_delta": FLOAT, "audit_trace": "STR"}}
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Accessing Nexus-Flow Core...", expanded=True):
                response = asyncio.run(run_governor())
                
                # FIXED RESULT EXTRACTION
                raw_data = str(getattr(response, 'data', response)).strip()
                
                if "```json" in raw_data:
                    raw_data = raw_data.split("```json")[1].split("```")[0].strip()
                elif "
```" in raw_data:
                    raw_data = raw_data.split("```")[1].strip()
                
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
            # Debugging info
            if 'response' in locals():
                with st.expander("View Raw Nexus-Flow Output"):
                    st.text(response)

if __name__ == "__main__":
    main()
