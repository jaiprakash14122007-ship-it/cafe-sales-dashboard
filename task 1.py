import pandas as pd
import numpy as np

df = pd.read_csv("dirty_cafe_sales.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())

df.replace("ERROR", np.nan, inplace=True)
df.replace("UNKNOWN", np.nan, inplace=True)

# Convert columns to correct data types
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Price Per Unit"] = pd.to_numeric(df["Price Per Unit"], errors="coerce")
df["Total Spent"] = pd.to_numeric(df["Total Spent"], errors="coerce")

df["Transaction Date"] = pd.to_datetime(
    df["Transaction Date"],
    errors="coerce"
)

print("\nData Types After Conversion:")
print(df.dtypes)

# Fill missing values in numerical columns
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())
df["Price Per Unit"] = df["Price Per Unit"].fillna(df["Price Per Unit"].median())
df["Total Spent"] = df["Total Spent"].fillna(df["Total Spent"].median())

# Fill missing values in categorical columns
df["Item"] = df["Item"].fillna(df["Item"].mode()[0])
df["Payment Method"] = df["Payment Method"].fillna("Unknown")
df["Location"] = df["Location"].fillna("Unknown")

# Fill missing dates
df["Transaction Date"] = df["Transaction Date"].fillna(
    df["Transaction Date"].mode()[0]
)

print("\nMissing Values After Filling:")
print(df.isnull().sum())
print("\nDuplicate Rows:", df.duplicated().sum())

df.to_csv("cleaned_cafe_sales.csv", index=False)

print("Cleaned dataset saved successfully!")

import matplotlib.pyplot as plt
import seaborn as sns   
plt.figure(figsize=(8,5))

df["Item"].value_counts().plot(kind="bar")

plt.title("Top Selling Items")
plt.xlabel("Item")
plt.ylabel("Number of Sales")

plt.show()

plt.figure(figsize=(6,6))

df["Payment Method"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Payment Method Distribution")
plt.ylabel("")
plt.savefig("payment_method_distribution.png")
plt.show()

plt.figure(figsize=(8,5))

df["Location"].value_counts().plot(kind="bar")

plt.title("Sales by Location")
plt.xlabel("Location")
plt.ylabel("Count")
plt.savefig("sales_by_location.png")
plt.show()

plt.figure(figsize=(8,5))

plt.hist(df["Quantity"], bins=10)

plt.title("Quantity Distribution")
plt.xlabel("Quantity")
plt.ylabel("Frequency")
plt.savefig("quantity_distribution.png")
plt.show()

plt.figure(figsize=(8,5))

plt.hist(df["Total Spent"], bins=10)

plt.title("Total Spent Distribution")
plt.xlabel("Total Spent")
plt.ylabel("Frequency")
plt.savefig("total_spent_distribution.png")
plt.show()

plt.figure(figsize=(8,5))

sns.boxplot(y=df["Total Spent"])

plt.title("Outlier Detection - Total Spent")
plt.savefig("outlier_detection_total_spent.png")
plt.show()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Cafe Sales Dashboard",
    page_icon="☕",
    layout="wide"
)

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>
.stApp {
    background-color: white;
}

h1, h2, h3 {
    color: #1f2937;
    font-weight: bold;
}

[data-testid="stMetricValue"] {
    color: #2563eb;
}

section[data-testid="stSidebar"] {
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("cleaned_cafe_sales.csv")

df["Transaction Date"] = pd.to_datetime(
    df["Transaction Date"],
    errors="coerce"
)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("☕ Cafe Analytics Dashboard")

st.sidebar.markdown("---")

st.sidebar.info("""
Analyze:
- Sales Performance
- Customer Spending
- Payment Trends
- Location Insights
""")

# Filters
location_filter = st.sidebar.selectbox(
    "Select Location",
    ["All"] + sorted(df["Location"].dropna().unique().tolist())
)

payment_filter = st.sidebar.selectbox(
    "Select Payment Method",
    ["All"] + sorted(df["Payment Method"].dropna().unique().tolist())
)

# Apply Filters
filtered_df = df.copy()

if location_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Location"] == location_filter
    ]

if payment_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Payment Method"] == payment_filter
    ]

# ---------------------------
# TITLE
# ---------------------------
st.title("☕ Cafe Sales Analytics Dashboard")
st.markdown("### Business Performance Overview")
color ="#000000"
# ---------------------------
# KPI CARDS
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Transactions",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Revenue",
    f"${filtered_df['Total Spent'].sum():,.0f}"
)

col3.metric(
    "Average Spend",
    f"${filtered_df['Total Spent'].mean():.2f}"
)

col4.metric(
    "Products Sold",
    f"{int(filtered_df['Quantity'].sum())}"
)

st.divider()

# ---------------------------
# CHARTS ROW 1
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Top Selling Items")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        y=filtered_df["Item"],
        order=filtered_df["Item"].value_counts().index,
        ax=ax
    )

    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("💳 Payment Method Distribution")

    fig, ax = plt.subplots(figsize=(6,4))

    filtered_df["Payment Method"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")
    st.pyplot(fig)

# ---------------------------
# CHARTS ROW 2
# ---------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("📍 Sales by Location")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        y=filtered_df["Location"],
        order=filtered_df["Location"].value_counts().index,
        ax=ax
    )

    plt.tight_layout()
    st.pyplot(fig)

with col4:
    st.subheader("📦 Quantity Distribution")

    fig, ax = plt.subplots(figsize=(6,4))

    ax.hist(
        filtered_df["Quantity"],
        bins=10
    )

    ax.set_xlabel("Quantity")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

# ---------------------------
# CHARTS ROW 3
# ---------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("💰 Total Spent Distribution")

    fig, ax = plt.subplots(figsize=(6,4))

    ax.hist(
        filtered_df["Total Spent"],
        bins=10
    )

    ax.set_xlabel("Total Spent")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

with col6:
    st.subheader("⚠️ Outlier Detection")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.boxplot(
        y=filtered_df["Total Spent"],
        ax=ax
    )

    st.pyplot(fig)

st.divider()

# ---------------------------
# TOP REVENUE ITEMS
# ---------------------------
st.subheader("🏆 Top Revenue Generating Items")

revenue_by_item = (
    filtered_df.groupby("Item")["Total Spent"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(revenue_by_item)

# ---------------------------
# MONTHLY SALES TREND
# ---------------------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby(
        filtered_df["Transaction Date"].dt.month
    )["Total Spent"]
    .sum()
)

st.line_chart(monthly_sales)

# ---------------------------
# DOWNLOAD BUTTON
# ---------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Cleaned Dataset",
    data=csv,
    file_name="cleaned_cafe_sales.csv",
    mime="text/csv"
)

# ---------------------------
# DATA PREVIEW
# ---------------------------
st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df.head(20))

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: white;
}

/* Main Title */
h1 {
    color: #000000 !important;
    font-weight: bold;
}

/* Subheaders */
h3 {
    color: #000000 !important;
    font-weight: bold;
}

/* KPI Values */
[data-testid="stMetricValue"] {
    color: #000000 !important;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: black !important;
}

/* DataFrame Styling */
[data-testid="stDataFrame"] {
    background-color: white;
}

/* Download Button */
.stDownloadButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
}

/* Buttons Hover */
.stDownloadButton button:hover {
    background-color: #1d4ed8;
    color: white;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: #f8fafc;
    border: 1px solid #e5e7eb;
    padding: 15px;
    border-radius: 12px;
}

/* Horizontal Divider */
hr {
    border: 1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)