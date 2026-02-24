import pandas as pd

def fetch_team_stats():
    url = "https://www.sports-reference.com/cbb/seasons/2024-advanced-school-stats.html"
    df = pd.read_html(url)[0]
    df = df.rename(columns={"Team": "School"})
    df = df.dropna(subset=["School"])
    
    return df
