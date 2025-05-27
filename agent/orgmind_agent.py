import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseOutputParser
from langchain.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from typing import Optional

class OrgMindDataAnalyzer:
    def __init__(self):
        self.datasets = self.load_mock_data()
        
    def load_mock_data(self):
        """Load all mock datasets"""
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
                
        return datasets
    
    def analyze_hiring_trends(self, department=None, months=6):
        """Analyze hiring vs attrition trends"""
        df = self.datasets['hiring'].copy()
        
        # Filter by department if specified
        if department:
            df = df[df['department'].str.lower() == department.lower()]
            
        # Get recent months
        df['month'] = pd.to_datetime(df['month'])
        recent_date = df['month'].max() - pd.DateOffset(months=months)
        df = df[df['month'] >= recent_date]
        
        # Aggregate by month
        monthly_stats = df.groupby('month').agg({
            'hired': 'sum',
            'attrition': 'sum',
            'net_growth': 'sum'
        }).reset_index()
        
        return monthly_stats
    
    def analyze_employee_growth(self, months=6):
        """Analyze employee growth over time"""
        hiring_data = self.analyze_hiring_trends(months=months)
        
        # Calculate cumulative growth
        hiring_data['cumulative_hired'] = hiring_data['hired'].cumsum()
        hiring_data['cumulative_attrition'] = hiring_data['attrition'].cumsum()
        hiring_data['total_growth'] = hiring_data['cumulative_hired'] - hiring_data['cumulative_attrition']
        
        return hiring_data
    
    def forecast_profit(self, months_ahead=3):
        """Forecast profit based on current burn rate"""
        df = self.datasets['financial'].copy()
        df['month'] = pd.to_datetime(df['month'])
        
        # Get recent trend
        recent_data = df.tail(6)
        avg_revenue_growth = recent_data['revenue'].pct_change().mean()
        avg_burn_rate = recent_data['burn_rate'].mean()
        
        # Simple linear forecast
        last_revenue = recent_data['revenue'].iloc[-1]
        last_month = recent_data['month'].iloc[-1]
        
        forecasts = []
        for i in range(1, months_ahead + 1):
            future_month = last_month + pd.DateOffset(months=i)
            projected_revenue = last_revenue * (1 + avg_revenue_growth) ** i
            projected_expenses = avg_burn_rate * 30  # Monthly expenses
            projected_profit = projected_revenue - projected_expenses
            
            forecasts.append({
                'month': future_month,
                'projected_revenue': projected_revenue,
                'projected_expenses': projected_expenses,
                'projected_profit': projected_profit
            })
            
        return pd.DataFrame(forecasts)
    
    def analyze_engineering_velocity(self):
        """Analyze engineering team velocity"""
        df = self.datasets['sprints'].copy()
        df['completion_rate'] = (df['story_points_completed'] / df['story_points_planned'] * 100).round(1)
        
        # Recent performance
        recent_sprints = df.head(10)
        avg_velocity = recent_sprints['team_velocity'].mean()
        avg_completion = recent_sprints['completion_rate'].mean()
        
        return {
            'avg_velocity': avg_velocity,
            'avg_completion_rate': avg_completion,
            'recent_data': recent_sprints
        }
    
    def get_okr_summary(self):
        """Get OKR performance summary"""
        df = self.datasets['okrs'].copy()
        
        # Current quarter performance
        current_quarter = df['quarter'].iloc[-5:]  # Last 5 objectives
        summary = df.groupby('quarter').agg({
            'current_score': 'mean',
            'target_score': 'mean'
        }).round(1)
        
        summary['achievement_rate'] = (summary['current_score'] / summary['target_score'] * 100).round(1)
        
        return summary

class HiringAnalysisTool(BaseTool):
    name: str = "hiring_analysis"
    description: str = "Analyze hiring and attrition trends for specific departments or overall organization"
    analyzer: OrgMindDataAnalyzer
    
    def __init__(self, analyzer: OrgMindDataAnalyzer):
        super().__init__(analyzer=analyzer)
    
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        # Parse query for department and timeframe
        department = None
        months = 6
        
        if "engineering" in query.lower():
            department = "Engineering"
        elif "sales" in query.lower():
            department = "Sales"
        elif "marketing" in query.lower():
            department = "Marketing"
            
        if "12 months" in query.lower() or "year" in query.lower():
            months = 12
        elif "3 months" in query.lower():
            months = 3
            
        data = self.analyzer.analyze_hiring_trends(department, months)
        
        # Create visualization
        fig = px.line(data, x='month', y=['hired', 'attrition'], 
                     title=f'Hiring vs Attrition Trends - {department or "All Departments"}')
        fig.write_html('hiring_trends.html')
        
        # Generate summary
        total_hired = data['hired'].sum()
        total_attrition = data['attrition'].sum()
        net_growth = total_hired - total_attrition
        
        summary = f"""
        Hiring Analysis Results ({months} months):
        - Total Hired: {total_hired}
        - Total Attrition: {total_attrition}
        - Net Growth: {net_growth}
        - Average Monthly Hiring: {data['hired'].mean():.1f}
        - Average Monthly Attrition: {data['attrition'].mean():.1f}
        
        Chart saved as 'hiring_trends.html'
        """
        
        return summary

class EmployeeGrowthTool(BaseTool):
    name: str = "employee_growth"
    description: str = "Show employee growth over time with cumulative statistics"
    analyzer: OrgMindDataAnalyzer
    
    def __init__(self, analyzer: OrgMindDataAnalyzer):
        super().__init__(analyzer=analyzer)
    
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        months = 6
        if "12 months" in query.lower() or "year" in query.lower():
            months = 12
            
        data = self.analyzer.analyze_employee_growth(months)
        
        # Create visualization
        fig = make_subplots(rows=2, cols=1, 
                           subplot_titles=['Monthly Hiring/Attrition', 'Cumulative Growth'])
        
        # Monthly data
        fig.add_trace(go.Scatter(x=data['month'], y=data['hired'], 
                                name='Hired', line=dict(color='green')), row=1, col=1)
        fig.add_trace(go.Scatter(x=data['month'], y=data['attrition'], 
                                name='Attrition', line=dict(color='red')), row=1, col=1)
        
        # Cumulative growth
        fig.add_trace(go.Scatter(x=data['month'], y=data['total_growth'], 
                                name='Total Growth', line=dict(color='blue')), row=2, col=1)
        
        fig.update_layout(title='Employee Growth Analysis', height=600)
        fig.write_html('employee_growth.html')
        
        current_growth = data['total_growth'].iloc[-1]
        growth_rate = ((data['total_growth'].iloc[-1] / data['total_growth'].iloc[0]) - 1) * 100
        
        summary = f"""
        Employee Growth Analysis ({months} months):
        - Current Net Growth: {current_growth} employees
        - Growth Rate: {growth_rate:.1f}%
        - Total Hired: {data['hired'].sum()}
        - Total Attrition: {data['attrition'].sum()}
        
        Chart saved as 'employee_growth.html'
        """
        
        return summary

class ProfitForecastTool(BaseTool):
    name: str = "profit_forecast"
    description: str = "Forecast profit based on current burn rate and revenue trends"
    analyzer: OrgMindDataAnalyzer
    
    def __init__(self, analyzer: OrgMindDataAnalyzer):
        super().__init__(analyzer=analyzer)
    
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        months_ahead = 3
        if "q3" in query.lower() or "quarter" in query.lower():
            months_ahead = 3
        elif "6 months" in query.lower():
            months_ahead = 6
            
        forecast_data = self.analyzer.forecast_profit(months_ahead)
        historical_data = self.analyzer.datasets['financial'].tail(6)
        
        # Create visualization
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(x=pd.to_datetime(historical_data['month']), 
                                y=historical_data['profit'],
                                name='Historical Profit', line=dict(color='blue')))
        
        # Forecast data
        fig.add_trace(go.Scatter(x=forecast_data['month'], 
                                y=forecast_data['projected_profit'],
                                name='Forecasted Profit', line=dict(color='orange', dash='dash')))
        
        fig.update_layout(title='Profit Forecast', xaxis_title='Month', yaxis_title='Profit ($)')
        fig.write_html('profit_forecast.html')
        
        avg_forecast_profit = forecast_data['projected_profit'].mean()
        total_forecast_profit = forecast_data['projected_profit'].sum()
        
        summary = f"""
        Profit Forecast ({months_ahead} months ahead):
        - Average Monthly Profit: ${avg_forecast_profit:,.2f}
        - Total Forecasted Profit: ${total_forecast_profit:,.2f}
        - Current Burn Rate: ${self.analyzer.datasets['financial']['burn_rate'].iloc[-1]:,.2f}/day
        
        Chart saved as 'profit_forecast.html'
        """
        
        return summary

class EngineeringVelocityTool(BaseTool):
    name: str = "engineering_velocity"
    description: str = "Analyze engineering team velocity and sprint performance"
    analyzer: OrgMindDataAnalyzer
    
    def __init__(self, analyzer: OrgMindDataAnalyzer):
        super().__init__(analyzer=analyzer)
    
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        velocity_data = self.analyzer.analyze_engineering_velocity()
        sprint_data = velocity_data['recent_data']
        
        # Create visualization
        fig = make_subplots(rows=2, cols=2,
                           subplot_titles=['Team Velocity', 'Story Points', 'Completion Rate', 'Features Delivered'])
        
        fig.add_trace(go.Scatter(x=sprint_data['sprint'], y=sprint_data['team_velocity'],
                                name='Velocity'), row=1, col=1)
        
        fig.add_trace(go.Bar(x=sprint_data['sprint'], y=sprint_data['story_points_planned'],
                            name='Planned', opacity=0.7), row=1, col=2)
        fig.add_trace(go.Bar(x=sprint_data['sprint'], y=sprint_data['story_points_completed'],
                            name='Completed', opacity=0.7), row=1, col=2)
        
        fig.add_trace(go.Scatter(x=sprint_data['sprint'], y=sprint_data['completion_rate'],
                                name='Completion %'), row=2, col=1)
        
        fig.add_trace(go.Bar(x=sprint_data['sprint'], y=sprint_data['features_delivered'],
                            name='Features'), row=2, col=2)
        
        fig.update_layout(title='Engineering Velocity Analysis', height=600)
        fig.write_html('engineering_velocity.html')
        
        summary = f"""
        Engineering Velocity Analysis:
        - Average Team Velocity: {velocity_data['avg_velocity']:.1f} points
        - Average Completion Rate: {velocity_data['avg_completion_rate']:.1f}%
        - Recent Sprint Performance: {len(sprint_data)} sprints analyzed
        - Total Features Delivered: {sprint_data['features_delivered'].sum()}
        
        Chart saved as 'engineering_velocity.html'
        """
        
        return summary

class OKRSummaryTool(BaseTool):
    name: str = "okr_summary"
    description: str = "Generate strategic OKR performance summary"
    analyzer: OrgMindDataAnalyzer
    
    def __init__(self, analyzer: OrgMindDataAnalyzer):
        super().__init__(analyzer=analyzer)
    
    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        okr_data = self.analyzer.get_okr_summary()
        
        # Create visualization
        fig = px.bar(okr_data.reset_index(), x='quarter', y='achievement_rate',
                     title='OKR Achievement Rate by Quarter')
        fig.write_html('okr_summary.html')
        
        latest_quarter = okr_data.index[-1]
        latest_achievement = okr_data['achievement_rate'].iloc[-1]
        
        summary = f"""
        OKR Performance Summary:
        - Latest Quarter ({latest_quarter}): {latest_achievement:.1f}% achievement rate
        - Average Achievement Rate: {okr_data['achievement_rate'].mean():.1f}%
        - Quarters Analyzed: {len(okr_data)}
        
        Chart saved as 'okr_summary.html'
        """
        
        return summary

class OrgMindAgent:
    def __init__(self, openai_api_key: str):
        self.analyzer = OrgMindDataAnalyzer()
        self.llm = ChatOpenAI(temperature=0, base_url="https://openrouter.ai/api/v1", api_key=openai_api_key, model="anthropic/claude-sonnet-4")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Initialize tools
        self.tools = [
            HiringAnalysisTool(self.analyzer),
            EmployeeGrowthTool(self.analyzer),
            ProfitForecastTool(self.analyzer),
            EngineeringVelocityTool(self.analyzer),
            OKRSummaryTool(self.analyzer)
        ]
        
        # Create agent
        self.agent = self._create_agent()
    
    def _create_agent(self):
        prompt = PromptTemplate.from_template("""
        You are OrgMind, an AI co-pilot for organizational growth monitoring. 
        You help growing companies track performance, visualize growth, and drive strategic decisions.
        
        You have access to the following tools:
        {tools}
        
        Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        Question: {input}
        Thought: {agent_scratchpad}
        """)
        
        agent = create_react_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, memory=self.memory, verbose=True, handle_parsing_errors=True)
    
    def query(self, question: str):
        """Process a natural language query"""
        try:
            response = self.agent.invoke({"input": question})
            return response['output']
        except Exception as e:
            return f"Error processing query: {str(e)}"

def main():
    # Example usage
    print("OrgMind Agent initialized!")
    print("Note: Set your OPENAI_API_KEY environment variable to use the agent.")
    
    # For demo purposes, we'll show what the agent can do
    sample_queries = [
        "Show me engineering hiring vs attrition for the past 6 months",
        "Show me the employee growth over last 6 months", 
        "Forecast our Q3 profit based on current burn rate",
        "Analyze engineering team velocity",
        "Generate OKR performance summary"
    ]
    
    print("\nSample queries you can ask:")
    for i, query in enumerate(sample_queries, 1):
        print(f"{i}. {query}")

if __name__ == "__main__":
    main()