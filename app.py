import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# =========================
# CUSTOM CSS (Aesthetic Look)
# =========================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #f8f9fa;
}
.kpi-box {
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: black;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("supermarket.csv")
    
    # Fix datatypes
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

    # Handle missing values
    df["Postal Code"] = df["Postal Code"].fillna(0).astype(int)

    return df

df = load_data()

# =========================
# HEADER
# =========================
st.title("🛒 Supermarket Sales Dashboard")
st.subheader("📊 Sales Performance, Trends & Customer Insights")

st.markdown("---")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔎 Filter Your Data")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1]))
]

# =========================
# KPI SECTION
# =========================
total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()
avg_sales = filtered_df["Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='kpi-box'>💰 Total Sales<br>${total_sales:,.2f}</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='kpi-box'>📦 Orders<br>{total_orders}</div>", unsafe_allow_html=True)
col3.markdown(f"<div class='kpi-box'>👥 Customers<br>{total_customers}</div>", unsafe_allow_html=True)
col4.markdown(f"<div class='kpi-box'>📈 Avg Sale<br>${avg_sales:,.2f}</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# CHARTS
# =========================
col1, col2 = st.columns(2)

# Sales Over Time
sales_time = filtered_df.groupby("Order Date")["Sales"].sum().reset_index()
fig_line = px.line(
    sales_time,
    x="Order Date",
    y="Sales",
    title="📈 Sales Trend Over Time"
)
col1.plotly_chart(fig_line, use_container_width=True)

# Sales by Category
fig_bar = px.bar(
    filtered_df,
    x="Category",
    y="Sales",
    color="Category",
    title="🧾 Sales by Category"
)
col2.plotly_chart(fig_bar, use_container_width=True)

# =========================
# MORE VISUALS
# =========================
col3, col4 = st.columns(2)

# Histogram
fig_hist = px.histogram(
    filtered_df,
    x="Sales",
    nbins=50,
    title="📊 Sales Distribution"
)
col3.plotly_chart(fig_hist, use_container_width=True)

# Scatter Plot
fig_scatter = px.scatter(
    filtered_df,
    x="Sales",
    y="Ship Mode",
    color="Region",
    title="🚚 Sales vs Ship Mode"
)
col4.plotly_chart(fig_scatter, use_container_width=True)
