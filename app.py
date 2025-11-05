"""
Streamlit web interface for the Financial Statement AI Chatbox
"""

import streamlit as st
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.chatbot import FinancialChatbot

# Page configuration
st.set_page_config(
    page_title="Financial Statement AI Chatbox",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = FinancialChatbot()
    st.session_state.messages = []
    st.session_state.analyzed = False

# Title and description
st.title("💰 Financial Statement AI Chatbox")
st.markdown("""
A conversational AI agent for analyzing financial statements. Upload your financial documents, 
and get instant insights, key indicators, risk assessment, and interactive Q&A.
""")

# Sidebar for file upload
with st.sidebar:
    st.header("📤 Upload Financial Statement")
    
    uploaded_file = st.file_uploader(
        "Choose a file (PDF or Image)",
        type=['pdf', 'png', 'jpg', 'jpeg'],
        help="Upload a financial statement in PDF or image format"
    )
    
    if uploaded_file is not None:
        # Save uploaded file
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("🔍 Analyze Document", type="primary"):
            with st.spinner("Analyzing financial statement..."):
                results = st.session_state.chatbot.upload_and_analyze(str(file_path))
                
                if 'error' in results:
                    st.error(f"Error: {results['error']}")
                else:
                    st.session_state.analyzed = True
                    st.success("✅ Analysis complete!")
                    st.rerun()
    
    # Settings
    st.header("⚙️ Settings")
    
    if st.button("🔄 Reset Analysis"):
        st.session_state.chatbot.reset()
        st.session_state.messages = []
        st.session_state.analyzed = False
        st.rerun()
    
    # About
    st.header("ℹ️ About")
    st.markdown("""
    This AI chatbot analyzes financial statements and provides:
    - 📊 Key financial indicators
    - 📈 Trend analysis
    - ⚠️ Risk assessment
    - 💡 AI-powered insights
    - 💬 Interactive Q&A
    """)

# Main content area
if not st.session_state.analyzed:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👈 Upload a financial statement to get started")
        
        st.markdown("""
        ### How it works:
        
        1. **Upload** your financial statement (PDF or image)
        2. **Analyze** to extract key information
        3. **Review** insights and financial indicators
        4. **Ask questions** about the document
        
        ### Supported formats:
        - PDF documents
        - Images (PNG, JPG, JPEG)
        """)
else:
    # Display analysis results
    summary = st.session_state.chatbot.get_summary()
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Summary", "💬 Q&A Chat", "📈 Details"])
    
    with tab1:
        st.markdown("### Analysis Summary")
        st.text(summary)
        
        # Download summary
        st.download_button(
            label="📥 Download Summary",
            data=summary,
            file_name="financial_analysis_summary.txt",
            mime="text/plain"
        )
    
    with tab2:
        st.markdown("### Interactive Q&A")
        st.markdown("Ask any questions about the analyzed financial statement.")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about the financial statement..."):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.ask_question(prompt)
                    st.markdown(response)
            
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with tab3:
        st.markdown("### Detailed Analysis")
        
        results = st.session_state.chatbot.analysis_results
        
        # Financial Data
        if results.get('financial_data'):
            st.subheader("💰 Financial Metrics")
            col1, col2 = st.columns(2)
            
            metrics = results['financial_data']
            metric_items = list(metrics.items())
            mid = len(metric_items) // 2
            
            with col1:
                for key, value in metric_items[:mid]:
                    if value is not None and isinstance(value, (int, float)):
                        st.metric(key.replace('_', ' ').title(), f"${value:,.2f}")
            
            with col2:
                for key, value in metric_items[mid:]:
                    if value is not None and isinstance(value, (int, float)):
                        st.metric(key.replace('_', ' ').title(), f"${value:,.2f}")
        
        # Financial Ratios
        if results.get('ratios'):
            st.subheader("📈 Financial Ratios")
            cols = st.columns(len(results['ratios']))
            
            for idx, (key, value) in enumerate(results['ratios'].items()):
                with cols[idx]:
                    st.metric(key.replace('_', ' ').title(), f"{value:.2f}%")
        
        # Risks
        if results.get('risks'):
            st.subheader("⚠️ Risk Assessment")
            if not results['risks']:
                st.success("No significant risks identified")
            else:
                for risk in results['risks']:
                    if risk['severity'] == 'High':
                        st.error(f"**{risk['type']}**: {risk['description']}")
                    elif risk['severity'] == 'Medium':
                        st.warning(f"**{risk['type']}**: {risk['description']}")
                    else:
                        st.info(f"**{risk['type']}**: {risk['description']}")
        
        # AI Insights
        if results.get('insights'):
            st.subheader("💡 AI-Generated Insights")
            st.markdown(results['insights'])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Powered by AI • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
