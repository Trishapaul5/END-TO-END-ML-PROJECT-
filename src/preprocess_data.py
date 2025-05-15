import pandas as pd
import os
import numpy as np

def preprocess_data():
    # Define expected columns for Wikipedia data (subset based on available)
    wiki_columns = [
        'Country', 'Year', 'Currency', 'Population', 'GDP_Growth',
        'GDP_Per_Capita', 'Inflation_Rate', 'Gini_Coefficient', 'Labor_Force',
        'Unemployment_Rate', 'Main_Sectors', 'Foreign_Reserves'
    ]
    
    # Define expected World Bank columns
    wb_columns = [
        'Country', 'date', 'GDP_Current_USD', 'GDP_Per_Capita_USD', 
        'Inflation_Rate_WB', 'Unemployment_Rate_WB', 'GDP_Per_Capita_Growth', 
        'Exports_WB', 'Imports_WB', 'Gini_Coefficient_WB', 'Population_WB'
    ]
    
    # Load data
    try:
        df_wiki = pd.read_csv('data/raw_economic_data.csv')
        df_wb = pd.read_csv('data/worldbank_data.csv')
    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure raw_economic_data.csv and worldbank_data.csv exist.")
        return
    
    # Verify columns
    missing_wiki = [col for col in wiki_columns if col not in df_wiki.columns]
    missing_wb = [col for col in wb_columns if col not in df_wb.columns]
    if missing_wiki:
        print(f"Warning: Missing columns in raw_economic_data.csv: {missing_wiki}")
    if missing_wb:
        print(f"Warning: Missing columns in worldbank_data.csv: {missing_wb}")
    
    # Rename columns for consistency
    df_wiki = df_wiki.rename(columns=lambda x: x.strip().replace(' ', '_'))
    df_wb = df_wb.rename(columns={'date': 'Year'})
    
    # Filter Wikipedia data for latest year (e.g., 2023)
    if 'Year' in df_wiki.columns:
        df_wiki = df_wiki[df_wiki['Year'] == df_wiki['Year'].max()]
    else:
        print("Warning: 'Year' column missing in raw_economic_data.csv. Using all data.")
    
    # Standardize country names
    df_wiki['Country'] = df_wiki['Country'].str.replace('_', ' ').str.title()
    df_wb['Country'] = df_wb['Country'].str.replace('_', ' ').str.title()
    
    # Merge datasets for 2023
    df_merged = pd.merge(
        df_wiki,
        df_wb[df_wb['Year'] == 2023],
        on=['Country', 'Year'],
        how='left'
    )
    
    # Compute derived metrics
    if 'GDP_Current_USD' in df_merged.columns and 'Population_WB' in df_merged.columns:
        try:
            df_merged['GDP_Per_Capita_Calc'] = df_merged['GDP_Current_USD'] / df_merged['Population_WB']
        except Exception as e:
            print(f"Error computing GDP_Per_Capita_Calc: {e}")
    else:
        print("Cannot compute GDP_Per_Capita_Calc: Missing GDP_Current_USD or Population_WB")
    
    # Handle missing values
    numeric_columns = df_merged.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        df_merged[col] = df_merged[col].fillna(df_merged[col].mean())
    
    # Drop non-numeric or non-essential columns if necessary
    df_merged = df_merged.drop(columns=['Currency', 'Main_Sectors'], errors='ignore')
    
    # Save processed static data
    os.makedirs('data', exist_ok=True)
    df_merged.to_csv('data/processed_economic_data.csv', index=False)
    print(f"Processed data saved to data/processed_economic_data.csv")
    print(f"Processed dataset size: {df_merged.shape[0]} countries, {df_merged.shape[1]} columns")
    
    # Save processed time-series data
    df_wb.to_csv('data/processed_worldbank_data.csv', index=False)
    print(f"Time-series data saved to data/processed_worldbank_data.csv")
    print(f"Time-series dataset size: {df_wb.shape[0]} rows, {df_wb.shape[1]} columns")

if __name__ == "__main__":
    preprocess_data()