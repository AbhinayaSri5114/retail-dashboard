import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

st.title("🛒 Retail Analytics Dashboard")

# ---------------- CONNECTION ----------------
@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )
# ---------------- TEST CONNECTION ----------------
try:
    conn = get_connection()
    st.success("✅ Connected to Snowflake successfully!")
except Exception as e:
    st.error(f"❌ Connection Failed: {e}")
    st.stop()

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data(query):
    return pd.read_sql(query, conn)

top_customers = load_data("SELECT * FROM TOP_CUSTOMERS")
top_products = load_data("SELECT * FROM TOP_PRODUCTS")
category_sales = load_data("SELECT * FROM CATEGORY_SALES")
city_sales = load_data("SELECT * FROM CITY_SALES")
monthly_sales = load_data("SELECT * FROM MONTHLY_SALES")

# ---------------- KPI ----------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(top_customers))
col2.metric("Total Products", len(top_products))
col3.metric("Total Revenue", int(category_sales["TOTAL_REVENUE"].sum()))

st.markdown("---")

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

fig1 = px.bar(
    top_customers,
    x="CUSTOMER_NAME",
    y="TOTAL_REVENUE",
    title="💰 Top Customers"
)

fig2 = px.bar(
    top_products,
    x="PRODUCT_NAME",
    y="TOTAL_SOLD",
    title="📦 Top Products"
)

col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

fig3 = px.pie(
    category_sales,
    names="CATEGORY",
    values="TOTAL_REVENUE",
    title="📊 Category Sales"
)

fig4 = px.bar(
    city_sales,
    x="CITY",
    y="TOTAL_REVENUE",
    title="🏙️ City Sales"
)

col1.plotly_chart(fig3, use_container_width=True)
col2.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ---------------- MONTHLY TREND ----------------
fig5 = px.line(
    monthly_sales,
    x="MONTH",
    y="TOTAL_REVENUE",
    markers=True,
    title="📈 Monthly Sales Trend"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ---------------- TABLE ----------------
st.subheader("📋 Data Preview")
st.dataframe(top_customers, use_container_width=True)
