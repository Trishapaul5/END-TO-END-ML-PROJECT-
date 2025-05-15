Global Economic Analysis Dashboard
Overview
This project analyzes economic indicators for 49 countries using data scraped from Wikipedia and fetched from the World Bank. It features data preprocessing, statistical analysis, visualizations, and an interactive Streamlit dashboard. The dashboard provides dynamic insights into GDP, Gini coefficients, unemployment rates, and more, with clustering and time-series trends from 2015 to 2023.
Dataset

Static Data: data/processed_economic_data.csv
49 countries, 20 indicators (e.g., GDP Per Capita, Gini Coefficient, Unemployment Rate, Cluster).
Source: Wikipedia (2023).


Time-Series Data: data/processed_worldbank_data.csv
441 rows, 11 indicators (e.g., GDP Per Capita Growth, 2015–2023).
Source: World Bank API.



Features

Data Collection: Scrapes Wikipedia (src/scrape_economic_data.py) and fetches World Bank data (src/fetch_worldbank_data.py).
Preprocessing: Cleans and merges data into processed CSVs (src/preprocess_data.py).
Analysis: Jupyter notebook (notebooks/economic_analysis.ipynb) performs:
Correlation analysis (heatmap).
K-means clustering (3 clusters based on GDP Per Capita and Gini Coefficient).
Visualizations: Scatter plots, time-series, choropleth maps, bar plots.


Dashboard: Interactive Streamlit app (src/dashboard.py) with:
Multi-select country filters and year range slider.
Tabs for Overview (metrics, treemap), Country Analysis (scatter, table), and Trends (line, choropleth).
Theme toggle (Light/Dark) and downloadable data.
Styled with Tailwind CSS for a modern look.




Directory Structure
economic-analysis-wikipedia/
├── data/
│   ├── economic_data.csv           # Raw Wikipedia data
│   ├── worldbank_data.csv          # Raw World Bank data
│   ├── processed_economic_data.csv # Processed static data (49 rows, 20 cols)
│   ├── processed_worldbank_data.csv # Processed time-series (441 rows, 11 cols)
├── notebooks/
│   ├── economic_analysis.ipynb     # Analysis and visualizations
├── plots/
│   ├── correlation_heatmap.png     # Correlation matrix
│   ├── economic_clustering.html    # Clustered scatter plot
│   ├── gdp_per_capita_growth.html  # Time-series line plot
│   ├── gini_choropleth.html        # Gini coefficient map
│   ├── unemployment_bar.png        # Unemployment rates
│   ├── dashboard_screenshot.png    # Dashboard screenshot
├── src/
│   ├── scrape_economic_data.py     # Wikipedia scraper
│   ├── fetch_worldbank_data.py     # World Bank API fetcher
│   ├── preprocess_data.py          # Data cleaning
│   ├── dashboard.py                # Streamlit dashboard
├── requirements.txt                # Dependencies
├── README.md                       # This file

Setup Instructions

Clone the Repository:
git clone <your-repo-url>
cd economic-analysis-wikipedia


Set Up Virtual Environment:
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac


Install Dependencies:
pip install -r requirements.txt


Generate Data:
python src/scrape_economic_data.py
python src/fetch_worldbank_data.py
python src/preprocess_data.py


Run Analysis:

Open notebooks/economic_analysis.ipynb in VS Code or Jupyter.
Select the .venv kernel (Python 3.12.4).
Run all cells to generate plots in plots/.


Run Dashboard:
streamlit run src/dashboard.py


Opens at http://localhost:8501.
Use filters to explore data interactively.



Results

Visualizations:
Correlation heatmap shows relationships between indicators (e.g., GDP vs. Gini).
Scatter plot clusters countries by economic profiles.
Time-series tracks GDP per capita growth (2015–2023).
Choropleth map visualizes Gini coefficients globally.
Bar plot compares unemployment rates.


Dashboard: Interactive interface with dynamic filters, treemap for GDP contribution, and downloadable data.
Outputs: Saved in plots/ (PNGs and HTML files).

Technologies Used

Python: 3.12.4
Libraries: Pandas (2.2.2), Matplotlib (3.9.2), Seaborn (0.13.2), Plotly (5.24.1), Scikit-learn (1.5.2), Streamlit (1.39.0), BeautifulSoup (4.12.3), Requests (2.32.3)
Tools: Jupyter Notebook, VS Code, Git

Author
Email: trishapaul2502@gmail.com
License
MIT License. See LICENSE for details.
Acknowledgments

Data sourced from Wikipedia and the World Bank API.
Built as a portfolio project to demonstrate data analysis and visualization skills.


