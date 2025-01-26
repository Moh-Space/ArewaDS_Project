import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def fetch_github_data():
    """Fetch top Python repositories from GitHub API"""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars&per_page=50'
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code: {response.status_code}")

def process_data(data):
    """Process the raw API response into a pandas DataFrame"""
    repositories = []
    
    for repo in data['items']:
        repositories.append({
            'name': repo['name'],
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'issues': repo['open_issues_count'],
            'created_at': datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ').year,
            'description': repo['description'],
            'owner': repo['owner']['login']
        })
    
    return pd.DataFrame(repositories)

def analyze_data(df):
    """Generate summary statistics and insights"""
    summary = {
        'total_repositories': len(df),
        'total_stars': df['stars'].sum(),
        'average_stars': df['stars'].mean(),
        'most_starred': df.nlargest(5, 'stars')[['name', 'stars', 'owner']],
        'most_forked': df.nlargest(5, 'forks')[['name', 'forks', 'owner']],
        'average_age': datetime.now().year - df['created_at'].mean()
    }
    return summary

def create_visualizations(df):
    """Create various visualizations of the repository data"""
    # Set the style
    plt.style.use('seaborn')
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(15, 10))
    
    # 1. Top 10 repositories by stars
    plt.subplot(2, 1, 1)
    top_10 = df.nlargest(10, 'stars')
    sns.barplot(data=top_10, x='stars', y='name')
    plt.title('Top 10 Python Repositories by Stars')
    plt.xlabel('Number of Stars')
    
    # 2. Stars vs Forks scatter plot
    plt.subplot(2, 1, 2)
    plt.scatter(df['forks'], df['stars'], alpha=0.5)
    plt.xlabel('Number of Forks')
    plt.ylabel('Number of Stars')
    plt.title('Stars vs Forks Correlation')
    
    plt.tight_layout()
    plt.show()

def main():
    # Fetch and process data
    raw_data = fetch_github_data()
    df = process_data(raw_data)
    
    # Generate analysis
    summary = analyze_data(df)
    
    # Print summary
    print("\n=== GitHub Python Repositories Analysis ===")
    print(f"\nTotal Repositories Analyzed: {summary['total_repositories']}")
    print(f"Total Stars: {summary['total_stars']:,}")
    print(f"Average Stars per Repository: {summary['average_stars']:,.2f}")
    print(f"Average Repository Age: {summary['average_age']:.1f} years")
    
    print("\nTop 5 Most Starred Repositories:")
    print(summary['most_starred'].to_string())
    
    print("\nTop 5 Most Forked Repositories:")
    print(summary['most_forked'].to_string())
    
    # Create visualizations
    create_visualizations(df)

if __name__ == "__main__":
    main()
