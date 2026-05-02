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

# 2. THE GOVERNOR
model = GroqModel('llama-3.3-70b-versatile')
governor = Agent(model) 

def main():
    st.set_page_config(page_title="AETHER-GOV // MASTER OS", page_icon="⚡", layout="wide")
    
    st.html("""
        <style>
        .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        div[data-testid="stMetric"] { border: 1px solid #333; padding: 15px; background: #111; }
        .stButton>button { background-color: #00FF41 !important; color: black !important; font-weight: bold; width: 100%; border: none; height: 3.5em; }
        </style>
    """)

    st.title("⚡ AETHER-GOV // MASTER OS")
    st.caption("Raipur Hub // Enterprise Data AI Factory // v7.2 Zero-Fault Core")
    
    with st.sidebar:
        st.header("📡 INFRASTRUCTURE")
        live_temp = st.slider("Core Temp (°C)", 40.0, 95.0, 72.0)
        grid_spot = st.number_input("Grid Spot Price ($/MWh)", value=285)

    if st.button("EXECUTE SOVEREIGN REASONING"):
        async def run_governor():
            # FEW-SHOT PROMPTING: Showing the model exactly how to format
            prompt = f"""
            Role: Sovereign Governor.
            Data: Temp {live_temp}C, Grid ${grid_spot}/MWh.
            
            Return ONLY a valid JSON object. 
            EXAMPLE: {{"action": "SELL_GRID", "power_limit_kw": 100, "expected_profit_delta": 45.5, "audit_trace": "Price exceeds threshold."}}
            
            Strictly use DOUBLE QUOTES (") for all keys and strings.
            """
            return await governor.run(prompt)
        
        try:
            with st.status("Analyzing Energy-Compute Nexus...", expanded=True):
                response = asyncio.run(run_governor())
                raw_data = str(getattr(response, 'data', getattr(response, 'result', response))).strip()
                
                # Locate and Sanitize JSON
                start = raw_data.find('{')
                end = raw_data.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = raw_data[start:end]
                    
                    # Double-check quote formatting before parsing
                    # Replace single quotes surrounding keys and values
                    json_str = re.sub(r"'(.*?)'(?=\s*:)", r'"\1"', json_str)
                    json_str = re.sub(r":\s*'(.*?)'", r': "\1"', json_str)
                    
                    # Final safety sweep
                    if json_str.count("'") > json_str.count('"'):
                        json_str = json_str.replace("'", '"')
                        
                    res = json.loads(json_str)
                else:
                    st.error("No JSON detected in output.")
                    st.stop()
            
            st.divider()
            st.header(f"DIRECTIVE: {res['action']}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Power Allocation", f"{res['power_limit_kw']} KW")
                st.write(f"**Impact:** `+${res['expected_profit_delta']}/hr`")
            with c2:
                st.info(res['audit_trace'])
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = res['power_limit_kw'],
                gauge = {'axis': {'range': [None, 500]}, 'bar': {'color': "#00FF41"}}
            ))
            fig.update_layout(paper_bgcolor="#050505", font={'color': "#00FF41"})
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Sovereign Error: {e}")
            if 'raw_data' in locals():
                with st.expander("View Raw Output Stream"):
                    st.code(raw_data)

if __name__ == "__main__":
    main()
