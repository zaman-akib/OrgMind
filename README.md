# 🧠 OrgMind: AI Co-Pilot for Organizational Growth

OrgMind is an AI-powered organizational growth monitoring agent that helps growing companies track performance, visualize growth, and drive strategic decisions—all autonomously using natural language queries.

## 🚀 Features

- **Natural Language Queries**: Ask questions in plain English like "Show me engineering hiring vs attrition for the past 6 months"
- **Intelligent Data Analysis**: Automatically analyzes organizational data across multiple dimensions
- **Interactive Visualizations**: Generates dynamic charts and graphs for insights
- **Predictive Analytics**: Forecasts profit, growth trends, and performance metrics
- **Multi-Domain Coverage**: Handles HR, Finance, Engineering, and Strategic data
- **Conversational Interface**: Chat-based interaction with memory and context

## 📊 Supported Analysis Types

### 1. Hiring & Attrition Analysis
- Track hiring trends by department
- Monitor attrition rates and patterns
- Calculate net growth and hiring efficiency
- Visualize recruitment pipeline health

### 2. Employee Growth Tracking
- Monitor overall workforce expansion
- Track cumulative growth over time
- Analyze growth rates and patterns
- Department-wise growth analysis

### 3. Financial Forecasting
- Predict future profit based on current trends
- Analyze burn rate and runway
- Revenue growth projections
- Budget optimization insights

### 4. Engineering Velocity
- Sprint performance analysis
- Story point completion rates
- Feature delivery tracking
- Team productivity metrics

### 5. Strategic OKR Monitoring
- Objective achievement tracking
- Quarterly performance summaries
- Goal completion rates
- Strategic alignment insights

## 🛠️ Technology Stack

- **LangChain**: AI agent framework and orchestration
- **OpenAI GPT**: Natural language processing and reasoning
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Streamlit**: Web interface
- **Matplotlib/Seaborn**: Statistical plotting
- **Faker**: Mock data generation

## 📁 Project Structure

```
orgmind/
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── data_generator.py        # Mock data generation
├── orgmind_agent.py        # Core LangChain agent
├── streamlit_app.py        # Web interface
├── demo.py                 # Demonstration script
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd orgmind

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Generate Mock Data

```bash
# Run the demo to generate sample data
python demo.py
```

### 4. Launch Web Interface

```bash
# Start Streamlit app
streamlit run streamlit_app.py
```

## 💬 Example Queries

Here are some natural language queries you can ask OrgMind:

### Hiring & HR
- "Show me engineering hiring vs attrition for the past 6 months"
- "What's our employee growth rate over the last year?"
- "Which department has the highest attrition rate?"
- "How many people did we hire in Q2?"

### Financial Analysis
- "Forecast our Q3 profit based on current burn rate"
- "What's our monthly revenue trend?"
- "How much runway do we have at current burn rate?"
- "Show me profit margins over the last 6 months"

### Engineering Performance
- "Analyze engineering team velocity"
- "What's our sprint completion rate?"
- "How many features did we deliver last quarter?"
- "Show me story point trends"

### Strategic Planning
- "Generate OKR performance summary"
- "What's our goal achievement rate this quarter?"
- "Which objectives are at risk?"
- "Design roadmap for the DevOps team based on current market"

## 🔧 Usage Examples

### Using the Agent Directly

```python
from orgmind_agent import OrgMindAgent
import os

# Initialize agent
agent = OrgMindAgent(os.getenv('OPENAI_API_KEY'))

# Ask questions
response = agent.query("Show me hiring trends for engineering")
print(response)
```

### Using the Data Analyzer

```python
from orgmind_agent import OrgMindDataAnalyzer

# Initialize analyzer
analyzer = OrgMindDataAnalyzer()

# Get hiring trends
hiring_data = analyzer.analyze_hiring_trends(department="Engineering", months=6)
print(hiring_data)

# Forecast profit
forecast = analyzer.forecast_profit(months_ahead=3)
print(forecast)
```

### Generating Mock Data

```python
from data_generator import generate_all_mock_data

# Generate complete dataset
datasets = generate_all_mock_data()

# Access specific data
employees = datasets['employees']
financial = datasets['financial']
```

## 📈 Sample Output

When you ask "Show me engineering hiring vs attrition for the past 6 months", OrgMind provides:

```
Hiring Analysis Results (6 months):
- Total Hired: 24
- Total Attrition: 18
- Net Growth: 6
- Average Monthly Hiring: 4.0
- Average Monthly Attrition: 3.0

Chart saved as 'hiring_trends.html'
```

Plus an interactive chart showing the trends over time.

## 🎯 Key Benefits

### For Leadership
- **Strategic Insights**: Get high-level organizational health metrics
- **Predictive Planning**: Forecast future needs and challenges
- **Data-Driven Decisions**: Base decisions on comprehensive analysis

### For HR Teams
- **Hiring Optimization**: Track recruitment effectiveness
- **Retention Analysis**: Identify attrition patterns
- **Workforce Planning**: Plan future hiring needs

### For Finance Teams
- **Budget Forecasting**: Predict future financial performance
- **Burn Rate Monitoring**: Track spending efficiency
- **ROI Analysis**: Measure investment returns

### For Engineering Teams
- **Velocity Tracking**: Monitor development productivity
- **Sprint Analysis**: Optimize development processes
- **Capacity Planning**: Plan future development work

## 🔮 Advanced Features

### Custom Tool Integration
OrgMind can be extended with custom tools for specific organizational needs:

```python
from langchain.tools import BaseTool

class CustomAnalysisTool(BaseTool):
    name = "custom_analysis"
    description = "Perform custom organizational analysis"
    
    def _run(self, query: str) -> str:
        # Your custom analysis logic
        return "Custom analysis results"
```

### Multi-Source Data Integration
Connect to real organizational systems:
- HR Management Systems (Workday, BambooHR)
- Financial Platforms (QuickBooks, Xero)
- Project Management (Jira, Asana)
- Communication Tools (Slack, Microsoft Teams)

## 🛡️ Security & Privacy

- **API Key Security**: Store OpenAI API keys securely
- **Data Privacy**: Mock data used for demonstration
- **Local Processing**: Data analysis happens locally
- **No Data Storage**: No organizational data stored externally

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions, issues, or feature requests:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

## 🔄 Roadmap

### Phase 1 (Current)
- ✅ Core LangChain agent implementation
- ✅ Mock data generation
- ✅ Basic analysis tools
- ✅ Streamlit web interface

### Phase 2 (Planned)
- [ ] Real data source integrations
- [ ] Advanced ML predictions
- [ ] Custom dashboard builder
- [ ] Multi-tenant support

### Phase 3 (Future)
- [ ] Mobile application
- [ ] Real-time alerts
- [ ] Advanced AI recommendations
- [ ] Enterprise features

## 🏆 Why OrgMind?

Traditional organizational analytics require:
- Complex SQL queries
- Manual report creation
- Technical expertise
- Time-consuming analysis

**OrgMind eliminates all of this** by providing:
- Natural language interface
- Automated analysis
- Instant visualizations
- Actionable insights

Transform your organizational data into strategic advantage with OrgMind! 🚀