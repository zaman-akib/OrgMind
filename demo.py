#!/usr/bin/env python3
"""
OrgMind Demo Script
Demonstrates the AI-powered organizational growth monitoring agent
"""

import os
import sys
from data_generator import generate_all_mock_data, OrgDataGenerator
from orgmind_agent import OrgMindAgent, OrgMindDataAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def setup_demo():
    """Setup demo environment"""
    print("🧠 OrgMind Demo - AI Co-Pilot for Organizational Growth")
    print("=" * 60)
    
    # Generate mock data
    print("\n📊 Generating mock organizational data...")
    datasets = generate_all_mock_data()
    print("✅ Mock data generated successfully!")
    
    return datasets

def show_statistical_analysis(datasets):
    """Display statistical analysis of the data"""
    print("\n📈 Statistical Analysis Results")
    print("-" * 40)
    
    analyzer = OrgMindDataAnalyzer()
    
    # Employee Statistics
    employees_df = datasets['employees']
    print(f"\n👥 Employee Statistics:")
    print(f"   Total Employees: {len(employees_df)}")
    print(f"   Active Employees: {len(employees_df[employees_df['is_active']])}")
    print(f"   Departments: {employees_df['department'].nunique()}")
    print(f"   Average Salary: ${employees_df['salary'].mean():,.2f}")
    print(f"   Average Performance Score: {employees_df['performance_score'].mean():.2f}/5.0")
    
    # Department breakdown
    dept_stats = employees_df.groupby('department').agg({
        'employee_id': 'count',
        'salary': 'mean',
        'performance_score': 'mean'
    }).round(2)
    print(f"\n   Department Breakdown:")
    for dept, row in dept_stats.iterrows():
        print(f"   - {dept}: {row['employee_id']} employees, avg salary ${row['salary']:,.0f}")
    
    # Hiring Trends
    hiring_data = analyzer.analyze_hiring_trends(months=12)
    print(f"\n📈 Hiring Trends (12 months):")
    print(f"   Total Hired: {hiring_data['hired'].sum()}")
    print(f"   Total Attrition: {hiring_data['attrition'].sum()}")
    print(f"   Net Growth: {hiring_data['net_growth'].sum()}")
    print(f"   Average Monthly Hiring: {hiring_data['hired'].mean():.1f}")
    print(f"   Average Monthly Attrition: {hiring_data['attrition'].mean():.1f}")
    
    # Financial Performance
    financial_df = datasets['financial']
    print(f"\n💰 Financial Performance:")
    print(f"   Latest Monthly Revenue: ${financial_df['revenue'].iloc[-1]:,.2f}")
    print(f"   Latest Monthly Profit: ${financial_df['profit'].iloc[-1]:,.2f}")
    print(f"   Average Monthly Revenue: ${financial_df['revenue'].mean():,.2f}")
    print(f"   Average Monthly Profit: ${financial_df['profit'].mean():,.2f}")
    print(f"   Current Daily Burn Rate: ${financial_df['burn_rate'].iloc[-1]:,.2f}")
    
    # Revenue growth rate
    revenue_growth = ((financial_df['revenue'].iloc[-1] / financial_df['revenue'].iloc[0]) - 1) * 100
    print(f"   Revenue Growth Rate: {revenue_growth:.1f}%")
    
    # Engineering Velocity
    velocity_data = analyzer.analyze_engineering_velocity()
    print(f"\n⚡ Engineering Velocity:")
    print(f"   Average Team Velocity: {velocity_data['avg_velocity']:.1f} story points")
    print(f"   Average Completion Rate: {velocity_data['avg_completion_rate']:.1f}%")
    
    recent_sprints = velocity_data['recent_data']
    print(f"   Total Features Delivered (recent): {recent_sprints['features_delivered'].sum()}")
    print(f"   Total Bugs Fixed (recent): {recent_sprints['bugs_fixed'].sum()}")
    
    # OKR Performance
    okr_summary = analyzer.get_okr_summary()
    print(f"\n🎯 OKR Performance:")
    for quarter, row in okr_summary.iterrows():
        print(f"   {quarter}: {row['achievement_rate']:.1f}% achievement rate")
    
    print(f"   Overall Average Achievement: {okr_summary['achievement_rate'].mean():.1f}%")

def demonstrate_agent_queries():
    """Demonstrate agent queries without requiring OpenAI API"""
    print("\n🤖 OrgMind Agent Capabilities")
    print("-" * 40)
    
    sample_queries = [
        "Show me engineering hiring vs attrition for the past 6 months",
        "Show me the employee growth over last 6 months",
        "Forecast our Q3 profit based on current burn rate",
        "Analyze engineering team velocity",
        "Generate OKR performance summary"
    ]
    
    print("\nThe OrgMind agent can handle these natural language queries:")
    for i, query in enumerate(sample_queries, 1):
        print(f"   {i}. {query}")
    
    print("\nEach query generates:")
    print("   • Statistical analysis")
    print("   • Interactive visualizations (HTML charts)")
    print("   • Actionable insights and recommendations")
    
    # Simulate what each tool would return
    analyzer = OrgMindDataAnalyzer()
    
    print(f"\n📊 Sample Analysis Results:")
    
    # Hiring analysis simulation
    hiring_data = analyzer.analyze_hiring_trends(department="Engineering", months=6)
    print(f"\n1. Engineering Hiring Analysis (6 months):")
    print(f"   - Total Hired: {hiring_data['hired'].sum()}")
    print(f"   - Total Attrition: {hiring_data['attrition'].sum()}")
    print(f"   - Net Growth: {hiring_data['net_growth'].sum()}")
    
    # Employee growth simulation
    growth_data = analyzer.analyze_employee_growth(months=6)
    print(f"\n2. Employee Growth Analysis:")
    print(f"   - Current Net Growth: {growth_data['total_growth'].iloc[-1]} employees")
    print(f"   - Total Hired: {growth_data['hired'].sum()}")
    
    # Profit forecast simulation
    forecast_data = analyzer.forecast_profit(months_ahead=3)
    print(f"\n3. Q3 Profit Forecast:")
    print(f"   - Average Monthly Profit: ${forecast_data['projected_profit'].mean():,.2f}")
    print(f"   - Total Forecasted Profit: ${forecast_data['projected_profit'].sum():,.2f}")
    
    # Engineering velocity simulation
    velocity_data = analyzer.analyze_engineering_velocity()
    print(f"\n4. Engineering Velocity:")
    print(f"   - Average Team Velocity: {velocity_data['avg_velocity']:.1f} points")
    print(f"   - Average Completion Rate: {velocity_data['avg_completion_rate']:.1f}%")
    
    # OKR summary simulation
    okr_data = analyzer.get_okr_summary()
    latest_achievement = okr_data['achievement_rate'].iloc[-1]
    print(f"\n5. OKR Performance Summary:")
    print(f"   - Latest Quarter Achievement: {latest_achievement:.1f}%")
    print(f"   - Average Achievement Rate: {okr_data['achievement_rate'].mean():.1f}%")

def create_sample_visualizations():
    """Create sample visualizations to demonstrate capabilities"""
    print("\n📊 Creating Sample Visualizations...")
    
    analyzer = OrgMindDataAnalyzer()
    
    # Set up matplotlib
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('OrgMind - Organizational Analytics Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Hiring Trends
    hiring_data = analyzer.analyze_hiring_trends(months=12)
    hiring_data['month'] = pd.to_datetime(hiring_data['month'])
    
    axes[0, 0].plot(hiring_data['month'], hiring_data['hired'], marker='o', label='Hired', color='green')
    axes[0, 0].plot(hiring_data['month'], hiring_data['attrition'], marker='s', label='Attrition', color='red')
    axes[0, 0].set_title('Hiring vs Attrition Trends')
    axes[0, 0].set_ylabel('Number of Employees')
    axes[0, 0].legend()
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. Department Distribution
    employees_df = pd.read_csv('mock_data_employees.csv')
    dept_counts = employees_df['department'].value_counts()
    
    axes[0, 1].pie(dept_counts.values, labels=dept_counts.index, autopct='%1.1f%%')
    axes[0, 1].set_title('Employee Distribution by Department')
    
    # 3. Financial Performance
    financial_df = pd.read_csv('mock_data_financial.csv')
    financial_df['month'] = pd.to_datetime(financial_df['month'])
    
    axes[1, 0].plot(financial_df['month'], financial_df['revenue'], marker='o', label='Revenue', color='blue')
    axes[1, 0].plot(financial_df['month'], financial_df['profit'], marker='s', label='Profit', color='green')
    axes[1, 0].set_title('Financial Performance')
    axes[1, 0].set_ylabel('Amount ($)')
    axes[1, 0].legend()
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Engineering Velocity
    sprints_df = pd.read_csv('mock_data_sprints.csv')
    recent_sprints = sprints_df.head(10)
    
    axes[1, 1].bar(range(len(recent_sprints)), recent_sprints['story_points_planned'], 
                   alpha=0.7, label='Planned', color='lightblue')
    axes[1, 1].bar(range(len(recent_sprints)), recent_sprints['story_points_completed'], 
                   alpha=0.7, label='Completed', color='darkblue')
    axes[1, 1].set_title('Sprint Performance (Recent 10)')
    axes[1, 1].set_ylabel('Story Points')
    axes[1, 1].set_xlabel('Sprint')
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig('orgmind_dashboard.png', dpi=300, bbox_inches='tight')
    print("✅ Dashboard saved as 'orgmind_dashboard.png'")
    
    # Show the plot
    plt.show()

def main():
    """Main demo function"""
    try:
        # Setup and generate data
        datasets = setup_demo()
        
        # Show statistical analysis
        show_statistical_analysis(datasets)
        
        # Demonstrate agent capabilities
        demonstrate_agent_queries()
        
        # Create visualizations
        create_sample_visualizations()
        
        print("\n" + "=" * 60)
        print("🎉 OrgMind Demo Complete!")
        print("\nNext Steps:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Run 'streamlit run streamlit_app.py' for the web interface")
        print("3. Or use the OrgMindAgent class directly in your code")
        print("\nFiles generated:")
        print("- Mock data CSV files")
        print("- orgmind_dashboard.png (sample visualization)")
        print("- Interactive HTML charts (when using the agent)")
        
    except Exception as e:
        print(f"❌ Error running demo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()