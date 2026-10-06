import streamlit as st
from main import run_pipeline

st.set_page_config(page_title="Media Trend Agent", layout="wide")

st.title("🤖 Media Trend Analysis + Content Creator")
st.markdown("Automate your content strategy using YouTube & Twitter insights powered by local LLM.")

with st.sidebar:
    st.header("Settings")
    niche = st.text_input("Niche / Keyword", placeholder="e.g. Sustainable Fashion")
    platforms = st.multiselect(
        "Select Data Sources", 
        ["youtube", "twitter"], 
        default=["youtube", "twitter"]
    )
    run_btn = st.button("Generate Content")

if run_btn:
    if not niche:
        st.error("Please enter a niche/keyword.")
    else:
        with st.spinner(f"Analyzing {niche} across {', '.join(platforms)}..."):
            try:
                results = run_pipeline(niche, platforms)
                
                st.success(f"Trending Topic Found: {results['trend']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📱 Social Media Package")
                    st.markdown(results['social'])
                    
                with col2:
                    st.subheader("💻 Landing Page Copy")
                    st.markdown(results['landing'])
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.divider()
st.caption("Powered by CrewAI, Proxy Scrapers, and Local Llama 3.1 LLM.")