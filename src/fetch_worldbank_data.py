import requests
import pandas as pd
import os
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

def fetch_worldbank_data(countries, indicators, years=(2015, 2023)):
    # Map Wikipedia country names to World Bank country codes
    country_codes = {
        'United States': 'USA', 'China': 'CHN', 'India': 'IND', 'Germany': 'DEU',
        'Brazil': 'BRA', 'Japan': 'JPN', 'United Kingdom': 'GBR', 'France': 'FRA',
        'Canada': 'CAN', 'Australia': 'AUS', 'Russia': 'RUS', 'South Korea': 'KOR',
        'Mexico': 'MEX', 'Indonesia': 'IDN', 'Nigeria': 'NGA', 'South Africa': 'ZAF',
        'Argentina': 'ARG', 'Saudi Arabia': 'SAU', 'Italy': 'ITA', 'Spain': 'ESP',
        'Turkey': 'TUR', 'Netherlands': 'NLD', 'Switzerland': 'CHE', 'Sweden': 'SWE',
        'Belgium': 'BEL', 'Poland': 'POL', 'Thailand': 'THA', 'Malaysia': 'MYS',
        'Philippines': 'PHL', 'Vietnam': 'VNM', 'Singapore': 'SGP', 'Egypt': 'EGY',
        'Algeria': 'DZA', 'Morocco': 'MAR', 'Kenya': 'KEN', 'Ethiopia': 'ETH',
        'Ghana': 'GHA', 'Pakistan': 'PAK', 'Bangladesh': 'BGD', 'Iran': 'IRN',
        'United Arab Emirates': 'ARE', 'Qatar': 'QAT', 'Chile': 'CHL', 'Colombia': 'COL',
        'Peru': 'PER', 'New Zealand': 'NZL', 'Norway': 'NOR', 'Denmark': 'DNK',
        'Finland': 'FIN', 'Ireland': 'IRL'
    }
    
    # Initialize data list
    all_data = []
    
    # Set up requests session with retries
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    # Test a single API call for debugging
    test_url = "https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?date=2020&format=json"
    try:
        test_response = session.get(test_url, timeout=10)
        test_response.raise_for_status()
        test_data = test_response.json()
        print("Test API response:", json.dumps(test_data, indent=2))
    except Exception as e:
        print(f"Test API call failed: {e}")
    
    # Fetch data for each country, year, and indicator (fallback to single indicator calls)
    for country in tqdm(countries, desc="Fetching countries"):
        country_code = country_codes.get(country.title())
        if not country_code:
            print(f"No country code for {country}")
            continue
        
        for year in range(years[0], years[1] + 1):
            for indicator_code, indicator_name in indicators.items():
                url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?date={year}&format=json&per_page=1000"
                try:
                    response = session.get(url, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Check if data is valid
                    if len(data) > 1 and data[1] and len(data[1]) > 0:
                        for entry in data[1]:
                            value = entry.get('value')
                            if value is not None:
                                all_data.append({
                                    'Country': country.title(),
                                    'date': year,
                                    indicator_name: float(value)
                                })
                                print(f"Fetched {indicator_name} for {country} in {year}: {value}")
                            else:
                                print(f"No data for {indicator_name} in {country} {year}")
                    else:
                        print(f"Empty response for {country} {year} {indicator_name}: {data}")
                except requests.exceptions.HTTPError as e:
                    print(f"HTTP error for {country} {year} {indicator_name}: {e}")
                except requests.exceptions.ConnectionError as e:
                    print(f"Connection error for {country} {year} {indicator_name}: {e}")
                except requests.exceptions.Timeout as e:
                    print(f"Timeout for {country} {year} {indicator_name}: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"Request error for {country} {year} {indicator_name}: {e}")
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    if not df.empty:
        df = df.groupby(['Country', 'date']).first().reset_index()
    else:
        print("No data collected. Falling back to CSV or check API connectivity.")
    return df

def main():
    # Define World Bank indicators
    indicators = {
        'NY.GDP.MKTP.CD': 'GDP_Current_USD',
        'NY.GDP.PCAP.CD': 'GDP_Per_Capita_USD',
        'FP.CPI.TOTL.ZG': 'Inflation_Rate_WB',
        'SL.UEM.TOTL.ZS': 'Unemployment_Rate_WB',
        'NY.GDP.PCAP.KD.ZG': 'GDP_Per_Capita_Growth',
        'NE.EXP.GNFS.CD': 'Exports_WB',
        'NE.IMP.GNFS.CD': 'Imports_WB',
        'SI.POV.GINI': 'Gini_Coefficient_WB',
        'SP.POP.TOTL': 'Population_WB'
    }
    
    # Load Wikipedia countries
    try:
        df_wiki = pd.read_csv('data/raw_economic_data.csv')
        countries = df_wiki['Country'].tolist()
    except FileNotFoundError:
        print("Error: raw_economic_data.csv not found. Run scrape_economic_data.py first.")
        return
    
    # Fetch data
    df_wb = fetch_worldbank_data(countries, indicators)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df_wb.to_csv('data/worldbank_data.csv', index=False)
    print("World Bank data saved to data/worldbank_data.csv")
    print(f"World Bank dataset size: {df_wb.shape[0]} rows, {df_wb.shape[1]} columns")

if __name__ == "__main__":
    main()