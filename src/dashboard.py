
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config for wide layout and title
st.set_page_config(page_title="Global Economic Dashboard", layout="wide", page_icon="🌍")

# Custom CSS with Tailwind CDN
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .stApp { background-color: #f0f2f6; }
        .metric-card { background-color: #ffffff; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header { font-size: 2.5rem; font-weight: bold; color: #1f2937; }
        .subheader { font-size: 1.5rem; color: #4b5563; }
        .tab { background-color: #ffffff; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df_static = pd.read_csv('data/processed_economic_data.csv')
    df_ts = pd.read_csv('data/processed_worldbank_data.csv')
    return df_static, df_ts

df_static, df_ts = load_data()

# Sidebar for filters
st.sidebar.title("Filters")
countries = st.sidebar.multiselect("Select Countries", options=df_static['Country'].unique(),
                                  default=['United States', 'China', 'India'])
year_range = st.sidebar.slider("Year Range (Time-Series)", min_value=2015, max_value=2023,
                               value=(2015, 2023))
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])

# Apply theme
if theme == "Dark":
    st.markdown("""
        <style>
            .stApp { background-color: #1f2937; color: #ffffff; }
            .metric-card { background-color: #374151; }
            .header, .subheader { color: #ffffff; }
            .tab { background-color: #374151; }
        </style>
    """, unsafe_allow_html=True)

# Filter data
filtered_static = df_static[df_static['Country'].isin(countries)]
filtered_ts = df_ts[(df_ts['Country'].isin(countries)) & 
                    (df_ts['Year'].between(year_range[0], year_range[1]))]

# Main title
st.markdown('<div class="header">Global Economic Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Explore economic indicators for 49 countries (2015–2023)</div>', unsafe_allow_html=True)

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["Overview", "Country Analysis", "Trends"])

with tab1:
    st.markdown('<div class="tab">', unsafe_allow_html=True)
    # KPI Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_gdp = filtered_static['GDP_Per_Capita_Calc'].mean()
        st.markdown(f'<div class="metric-card"><b>Avg GDP Per Capita</b><br>{avg_gdp:,.2f} USD</div>', unsafe_allow_html=True)
    with col2:
        avg_gini = filtered_static['Gini_Coefficient'].mean()
        st.markdown(f'<div class="metric-card"><b>Avg Gini Coefficient</b><br>{avg_gini:.2f}</div>', unsafe_allow_html=True)
    with col3:
        avg_unemp = filtered_static['Unemployment_Rate'].mean()
        st.markdown(f'<div class="metric-card"><b>Avg Unemployment Rate</b><br>{avg_unemp:.2f}%</div>', unsafe_allow_html=True)

    # Treemap for GDP contribution
    st.subheader("GDP Contribution by Country (2023)")
    fig_tree = px.treemap(filtered_static, path=['Country'], values='GDP_Current_USD',
                          color='GDP_Per_Capita_Calc', hover_data=['Country'],
                          color_continuous_scale='Blues', title="GDP Contribution")
    st.plotly_chart(fig_tree, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab">', unsafe_allow_html=True)
    # Scatter plot with clustering
    st.subheader("GDP Per Capita vs. Gini Coefficient (2023)")
    fig_scatter = px.scatter(filtered_static, x='GDP_Per_Capita_Calc', y='Gini_Coefficient',
                             color='Cluster', size='Population_WB', hover_data=['Country', 'Unemployment_Rate'],
                             title="Economic Clustering", opacity=0.8)
    fig_scatter.update_layout(showlegend=True, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Data table with download
    st.subheader("Economic Indicators Data")
    st.dataframe(filtered_static[['Country', 'Year', 'GDP_Per_Capita_Calc', 'Gini_Coefficient', 'Unemployment_Rate', 'Cluster']],
                 use_container_width=True)
    csv = filtered_static.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", csv, "economic_data.csv", "text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tab">', unsafe_allow_html=True)
    # Time-series plot
    st.subheader("GDP Per Capita Growth (2015-2023)")
    fig_line = px.line(filtered_ts, x='Year', y='GDP_Per_Capita_Growth', color='Country',
                       title="GDP Per Capita Growth", line_shape='spline')
    fig_line.update_layout(showlegend=True, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_line, use_container_width=True)

    # Choropleth map
    st.subheader("Gini Coefficient by Country (2023)")
    fig_choro = px.choropleth(filtered_static, locations='Country', locationmode='country names',
                              color='Gini_Coefficient', hover_data=['Country', 'GDP_Per_Capita_Calc'],
                              title="Gini Coefficient", color_continuous_scale='Viridis')
    fig_choro.update_layout(geo=dict(showframe=False, projection_type='equirectangular'))
    st.plotly_chart(fig_choro, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class='text-center text-gray-500 mt-8'>
        Built with Streamlit by [Your Name] | Data: Wikipedia & World Bank (2023)
    </div>
""", unsafe_allow_html=True)

