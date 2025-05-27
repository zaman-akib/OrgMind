import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
import sys
from pathlib import Path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)
from data.data_generator import generate_all_mock_data
from agent.orgmind_agent import OrgMindAgent
import plotly.express as px
import plotly.graph_objects as go

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="OrgMind - AI Co-Pilot for Organizational Growth",
    page_icon="🧠",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'data_generated' not in st.session_state:
        st.session_state.data_generated = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def generate_mock_data():
    """Generate mock organizational data"""
    with st.spinner("Generating mock organizational data..."):
        datasets = generate_all_mock_data()
        st.session_state.data_generated = True
        return datasets

def display_data_overview(datasets):
    """Display overview of generated data"""
    st.subheader("📊 Data Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Employees", len(datasets['employees']))
    with col2:
        st.metric("Departments", datasets['employees']['department'].nunique())
    with col3:
        st.metric("Months of Data", len(datasets['financial']))
    with col4:
        st.metric("Sprints Tracked", len(datasets['sprints']))
    with col5:
        st.metric("OKRs", len(datasets['okrs']))
    
    # Show sample data
    with st.expander("View Sample Data"):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Employees", "Hiring", "Financial", "Sprints", "OKRs"])
        
        with tab1:
            st.dataframe(datasets['employees'].head())
        with tab2:
            st.dataframe(datasets['hiring'].head())
        with tab3:
            st.dataframe(datasets['financial'].head())
        with tab4:
            st.dataframe(datasets['sprints'].head())
        with tab5:
            st.dataframe(datasets['okrs'].head())

def main():
    initialize_session_state()
    
    # Header
    st.title("🧠 OrgMind")
    st.subheader("AI Co-Pilot for Organizational Growth")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key", 
            type="password",
            help="Enter your OpenAI API key to enable the AI agent"
        )
        
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
        
        st.markdown("---")
        
        # Data generation
        st.header("Data Setup")
        if st.button("Generate Mock Data", type="primary"):
            datasets = generate_mock_data()
            st.success("Mock data generated successfully!")
        
        if st.session_state.data_generated:
            st.success("✅ Mock data ready")
        
        st.markdown("---")
        
        # Sample queries
        st.header("Sample Queries")
        sample_queries = [
            "Show me engineering hiring vs attrition for the past 6 months",
            "Show me the employee growth over last 6 months",
            "Forecast our Q3 profit based on current burn rate",
            "Analyze engineering team velocity",
            "Generate OKR performance summary",
            "What's the current state of our organization?",
            "Give me insights about our team performance",
            "How is our company doing overall?"
        ]
        
        for query in sample_queries:
            if st.button(query, key=f"sample_{hash(query)}"):
                st.session_state.current_query = query
    
    # Main content
    if not st.session_state.data_generated:
        st.info("👈 Please generate mock data first using the sidebar")
        return
    
    # Load datasets for overview
    try:
        datasets = {}
        data_files = [
            'mock_data_employees.csv',
            'mock_data_hiring.csv', 
            'mock_data_financial.csv',
            'mock_data_sprints.csv',
            'mock_data_okrs.csv'
        ]
        
        for file in data_files:
            if os.path.exists(file):
                key = file.replace('mock_data_', '').replace('.csv', '')
                datasets[key] = pd.read_csv(file)
        
        display_data_overview(datasets)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    st.markdown("---")
    
    # Chat interface
    st.header("💬 Chat with OrgMind")
    
    # Initialize agent if API key is provided
    if api_key and not st.session_state.agent:
        try:
            with st.spinner("Initializing OrgMind agent..."):
                st.session_state.agent = OrgMindAgent(api_key)
            st.success("OrgMind agent initialized!")
        except Exception as e:
            st.error(f"Error initializing agent: {str(e)}")
            return
    
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to use the AI agent")
        return
    
    # Chat input
    user_query = st.text_input(
        "Ask OrgMind about your organization:",
        placeholder="e.g., Show me hiring trends for engineering team",
        key="user_input"
    )
    
    # Handle sample query selection
    if hasattr(st.session_state, 'current_query'):
        user_query = st.session_state.current_query
        delattr(st.session_state, 'current_query')
    
    if user_query and st.session_state.agent:
        with st.spinner("OrgMind is analyzing..."):
            try:
                # Clean up old chart files before generating new ones
                chart_files = [
                    'hiring_trends.html',
                    'employee_growth.html',
                    'profit_forecast.html',
                    'engineering_velocity.html',
                    'okr_summary.html'
                ]
                
                # Remove existing chart files to avoid showing old charts
                for chart_file in chart_files:
                    if os.path.exists(chart_file):
                        os.remove(chart_file)
                
                response = st.session_state.agent.query(user_query)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "query": user_query,
                    "response": response
                })
                
                # Display response
                st.success("Analysis Complete!")
                st.write("**Response:**")
                st.write(response)
                
                # Check for newly generated charts
                for chart_file in chart_files:
                    if os.path.exists(chart_file):
                        st.write(f"**Visualization:** {chart_file}")
                        with open(chart_file, 'r') as f:
                            st.components.v1.html(f.read(), height=600)
                        break  # Only show the first (and should be only) chart generated
                
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
    
    # Chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.header("📝 Chat History")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
            with st.expander(f"Query {len(st.session_state.chat_history) - i + 1}: {chat['query'][:50]}..."):
                st.write("**Query:**", chat['query'])
                st.write("**Response:**", chat['response'])
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>OrgMind - Transforming organizational data into actionable insights</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()