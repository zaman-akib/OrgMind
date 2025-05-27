import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random

class OrgDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'DevOps', 'Product']
        self.roles = {
            'Engineering': ['Software Engineer', 'Senior Engineer', 'Tech Lead', 'Engineering Manager'],
            'Sales': ['Sales Rep', 'Account Manager', 'Sales Director', 'VP Sales'],
            'Marketing': ['Marketing Specialist', 'Content Manager', 'Marketing Director'],
            'HR': ['HR Specialist', 'Recruiter', 'HR Manager'],
            'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager'],
            'DevOps': ['DevOps Engineer', 'Site Reliability Engineer', 'DevOps Manager'],
            'Product': ['Product Manager', 'Product Owner', 'VP Product']
        }
        
    def generate_employee_data(self, num_employees=200):
        """Generate mock employee data"""
        employees = []
        
        for i in range(num_employees):
            dept = random.choice(self.departments)
            role = random.choice(self.roles[dept])
            hire_date = self.fake.date_between(start_date='-2y', end_date='today')
            
            employee = {
                'employee_id': f'EMP{i+1:04d}',
                'name': self.fake.name(),
                'department': dept,
                'role': role,
                'hire_date': hire_date,
                'salary': random.randint(50000, 200000),
                'performance_score': round(random.uniform(3.0, 5.0), 1),
                'is_active': random.choice([True] * 9 + [False])  # 90% active
            }
            employees.append(employee)
            
        return pd.DataFrame(employees)
    
    def generate_hiring_data(self, months=12):
        """Generate hiring and attrition data"""
        data = []
        start_date = datetime.now() - timedelta(days=30*months)
        
        for i in range(months):
            month_date = start_date + timedelta(days=30*i)
            
            for dept in self.departments:
                hired = random.randint(0, 8)
                attrition = random.randint(0, 5)
                
                data.append({
                    'month': month_date.strftime('%Y-%m'),
                    'department': dept,
                    'hired': hired,
                    'attrition': attrition,
                    'net_growth': hired - attrition
                })
                
        return pd.DataFrame(data)
    
    def generate_financial_data(self, months=12):
        """Generate financial performance data"""
        data = []
        start_date = datetime.now() - timedelta(days=30*months)
        base_revenue = 1000000
        
        for i in range(months):
            month_date = start_date + timedelta(days=30*i)
            growth_factor = 1 + (i * 0.05) + random.uniform(-0.1, 0.15)
            
            revenue = base_revenue * growth_factor
            expenses = revenue * random.uniform(0.6, 0.8)
            profit = revenue - expenses
            
            data.append({
                'month': month_date.strftime('%Y-%m'),
                'revenue': round(revenue, 2),
                'expenses': round(expenses, 2),
                'profit': round(profit, 2),
                'burn_rate': round(expenses / 30, 2)  # Daily burn rate
            })
            
        return pd.DataFrame(data)
    
    def generate_sprint_data(self, sprints=24):
        """Generate engineering velocity data"""
        data = []
        
        for i in range(sprints):
            sprint_date = datetime.now() - timedelta(weeks=2*i)
            
            data.append({
                'sprint': f'Sprint {sprints-i}',
                'date': sprint_date.strftime('%Y-%m-%d'),
                'story_points_planned': random.randint(40, 80),
                'story_points_completed': random.randint(30, 75),
                'bugs_fixed': random.randint(5, 20),
                'features_delivered': random.randint(2, 8),
                'team_velocity': random.randint(35, 70)
            })
            
        return pd.DataFrame(data)
    
    def generate_okr_data(self, quarters=4):
        """Generate OKR tracking data"""
        data = []
        objectives = [
            'Increase customer acquisition',
            'Improve product quality',
            'Enhance team productivity',
            'Expand market presence',
            'Optimize operational efficiency'
        ]
        
        for q in range(quarters):
            quarter = f'Q{q+1} 2024'
            
            for obj in objectives:
                data.append({
                    'quarter': quarter,
                    'objective': obj,
                    'target_score': 100,
                    'current_score': random.randint(60, 95),
                    'confidence_level': random.choice(['High', 'Medium', 'Low']),
                    'owner': random.choice(self.departments)
                })
                
        return pd.DataFrame(data)

def generate_all_mock_data():
    """Generate all mock datasets"""
    generator = OrgDataGenerator()
    
    datasets = {
        'employees': generator.generate_employee_data(),
        'hiring': generator.generate_hiring_data(),
        'financial': generator.generate_financial_data(),
        'sprints': generator.generate_sprint_data(),
        'okrs': generator.generate_okr_data()
    }
    
    # Save to CSV files
    for name, df in datasets.items():
        df.to_csv(f'mock_data_{name}.csv', index=False)
        print(f"Generated {name} data: {len(df)} records")
    
    return datasets

if __name__ == "__main__":
    generate_all_mock_data()