import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

# List of 50 countries (G20 + others for diversity)
countries = [
    'United_States', 'China', 'India', 'Germany', 'Brazil', 'Japan', 'United_Kingdom',
    'France', 'Canada', 'Australia', 'Russia', 'South_Korea', 'Mexico', 'Indonesia',
    'Nigeria', 'South_Africa', 'Argentina', 'Saudi_Arabia', 'Italy', 'Spain',
    'Turkey', 'Netherlands', 'Switzerland', 'Sweden', 'Belgium', 'Poland', 'Thailand',
    'Malaysia', 'Philippines', 'Vietnam', 'Singapore', 'Egypt', 'Algeria', 'Morocco',
    'Kenya', 'Ethiopia', 'Ghana', 'Pakistan', 'Bangladesh', 'Iran', 'United_Arab_Emirates',
    'Qatar', 'Chile', 'Colombia', 'Peru', 'New_Zealand', 'Norway', 'Denmark', 'Finland',
    'Ireland'
]

def clean_numeric_value(text):
    """Extract numeric value from text (e.g., '$2.5 trillion' -> 2.5)."""
    if not text:
        return None
    text = re.sub(r'[^\d.]', '', text)
    try:
        return float(text)
    except ValueError:
        return None

def clean_percentage(text):
    """Extract percentage value (e.g., '5.2%' -> 5.2)."""
    if not text:
        return None
    match = re.search(r'[\d.]+', text)
    if match:
        return float(match.group())
    return None

def clean_population(text):
    """Extract population in millions (e.g., '331 million' -> 331)."""
    if not text:
        return None
    match = re.search(r'[\d.]+', text)
    if match:
        return float(match.group())
    return None

def clean_currency(text):
    """Extract currency name (e.g., 'US Dollar (USD)' -> 'USD')."""
    if not text:
        return None
    match = re.search(r'\((.*?)\)', text) or re.search(r'\w+', text)
    if match:
        return match.group(1) if '(' in text else match.group(0)
    return None

def clean_text(text):
    """Clean text fields (e.g., economic sectors)."""
    if not text:
        return None
    return text.strip()

def scrape_wikipedia_economic_data(country):
    """Scrape economic data from a country's Wikipedia economy page."""
    url = f"https://en.wikipedia.org/wiki/Economy_of_{country}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the infobox table
        infobox = soup.find('table', {'class': 'infobox'})
        if not infobox:
            print(f"No infobox found for {country}")
            return None
        
        data = {'Country': country.replace('_', ' '), 'Year': 2023}  # Assume latest year
        
        # Extract indicators from infobox
        rows = infobox.find_all('tr')
        for row in rows:
            header = row.find('th')
            value = row.find('td')
            if header and value:
                header_text = header.text.strip().lower()
                value_text = value.text.strip()
                
                # Map headers to indicators
                if 'gdp' in header_text and 'nominal' in header_text:
                    data['GDP_Nominal'] = clean_numeric_value(value_text)
                elif 'gdp (ppp)' in header_text:
                    data['GDP_PPP'] = clean_numeric_value(value_text)
                elif 'gdp growth' in header_text:
                    data['GDP_Growth'] = clean_percentage(value_text)
                elif 'gdp per capita' in header_text:
                    data['GDP_Per_Capita'] = clean_numeric_value(value_text)
                elif 'inflation' in header_text:
                    data['Inflation_Rate'] = clean_percentage(value_text)
                elif 'unemployment' in header_text:
                    data['Unemployment_Rate'] = clean_percentage(value_text)
                elif 'population' in header_text:
                    data['Population'] = clean_population(value_text)
                elif 'gini' in header_text:
                    data['Gini_Coefficient'] = clean_percentage(value_text)
                elif 'hdi' in header_text:
                    data['HDI'] = clean_numeric_value(value_text)
                elif 'debt' in header_text and 'gdp' in header_text:
                    data['Debt_to_GDP'] = clean_percentage(value_text)
                elif 'trade balance' in header_text:
                    data['Trade_Balance'] = clean_numeric_value(value_text)
                elif 'currency' in header_text:
                    data['Currency'] = clean_currency(value_text)
                elif 'reserves' in header_text:
                    data['Foreign_Reserves'] = clean_numeric_value(value_text)
                elif 'labor force' in header_text:
                    data['Labor_Force'] = clean_numeric_value(value_text)
                elif 'exports' in header_text and 'goods' in header_text:
                    data['Exports'] = clean_numeric_value(value_text)
                elif 'imports' in header_text and 'goods' in header_text:
                    data['Imports'] = clean_numeric_value(value_text)
                elif 'poverty' in header_text:
                    data['Poverty_Rate'] = clean_percentage(value_text)
                elif 'main industries' in header_text or 'sectors' in header_text:
                    data['Main_Sectors'] = clean_text(value_text)
        
        return data
    except Exception as e:
        print(f"Error scraping {country}: {e}")
        return None

def main():
    all_data = []
    for country in countries:
        print(f"Scraping data for {country}...")
        data = scrape_wikipedia_economic_data(country)
        if data:
            all_data.append(data)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/raw_economic_data.csv', index=False)
    print("Data scraped and saved to data/raw_economic_data.csv")
    print(f"Dataset size: {df.shape[0]} countries, {df.shape[1]} columns")
    return df

if __name__ == "__main__":
    main()