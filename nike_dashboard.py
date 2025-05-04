import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# -----------------------------
# Generate Synthetic Nike Sales Data
# -----------------------------

@st.cache_data
def load_data():
    np.random.seed(42)
    regions = ['North America', 'Europe', 'Asia' 'South America']
    categories = ['Shoes', 'Apparel', 'Accessories']
    months = pd.date_range(start='2023-01-01', end='2023-12-01', freq='MS')

    data = []

    for month in months:
        for region in regions:
            for category in categories:
                sales = np.random.randint(20000, 100000)
                marketing = np.random.randint(5000, 20000)
                data.append({
                    'Month': month,
                    'Region': region,
                    'Category': category,
                    'Sales': sales,
                    'Marketing Spend': marketing
                })

    return pd.DataFrame(data)

df = load_data()

# -----------------------------
# Streamlit Dashboard UI
# -----------------------------

st.title("📈 Nike Sales Performance Dashboard")
st.markdown("Use the filters to explore sales data across regions and product categories.")

# Sidebar filters
st.sidebar.header("🔎 Filter Options")
selected_regions = st.sidebar.multiselect("Select Region(s)", df['Region'].unique(), default=df['Region'].unique())
selected_categories = st.sidebar.multiselect("Select Category(ies)", df['Category'].unique(), default=df['Category'].unique())

# Filtered Data
filtered_df = df[(df['Region'].isin(selected_regions)) & (df['Category'].isin(selected_categories))]

# KPIs
total_sales = filtered_df['Sales'].sum()
avg_marketing = filtered_df['Marketing Spend'].mean()

st.metric("💰 Total Sales", f"${total_sales:,.0f}")
st.metric("📢 Avg. Marketing Spend", f"${avg_marketing:,.0f}")

# -----------------------------
# Sales by Region (Bar Chart)
# -----------------------------
st.subheader("🌍 Sales by Region")
region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()

bar_chart = alt.Chart(region_sales).mark_bar().encode(
    x=alt.X('Sales:Q', title='Total Sales'),
    y=alt.Y('Region:N', sort='-x', title='Region'),
    tooltip=['Region', 'Sales']
).properties(height=300)

st.altair_chart(bar_chart, use_container_width=True)

# -----------------------------
# Monthly Sales Trend (Line Chart)
# -----------------------------
st.subheader("📅 Monthly Sales Trend")
monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()

line_chart = alt.Chart(monthly_sales).mark_line(point=True).encode(
    x=alt.X('Month:T', title='Month'),
    y=alt.Y('Sales:Q', title='Sales'),
    tooltip=['Month', 'Sales']
).properties(height=300)

st.altair_chart(line_chart, use_container_width=True)

# -----------------------------
# Category-wise Sales Breakdown
# -----------------------------
st.subheader("📦 Sales by Product Category")
category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
st.dataframe(category_sales)

# -----------------------------
# Enhancements
# -----------------------------

# Enhancement 1: Download Filtered Data
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name='nike_sales_filtered.csv',
    mime='text/csv'
)

# Enhancement 2: Show Raw Data Option
with st.expander("🔍 Show Raw Data Table"):
    st.dataframe(filtered_df)
