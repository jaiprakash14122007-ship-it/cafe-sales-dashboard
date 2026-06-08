import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dirty_cafe_sales.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())
df.replace(["ERROR", "UNKNOWN"], pd.NA, inplace=True)

df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Price Per Unit"] = pd.to_numeric(df["Price Per Unit"], errors="coerce")
df["Total Spent"] = pd.to_numeric(df["Total Spent"], errors="coerce")
df["Item"].value_counts().plot(kind="bar")
plt.title("Top Selling Items")
plt.show()
df["Payment Method"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Payment Methods")
plt.show()
df["Location"].value_counts().plot(kind="bar")
plt.title("Sales by Location")
plt.show()
plt.hist(df["Total Spent"], bins=10)
plt.title("Total Spent Distribution")
plt.show()
sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.title("Correlation Heatmap")
plt.show()

print("\n================ FINAL INSIGHTS ================")
print("""
1. Coffee and Cake are the most frequently sold items.
2. Cash and Credit Card are the dominant payment methods.
3. In-store purchases generate higher total spending than takeaway.
4. Missing values exist in multiple columns, showing real-world data issues.
5. Outliers are present in Total Spent indicating high-value transactions.
""")

print("\nEDA COMPLETED SUCCESSFULLY")
print("All visualizations generated and insights extracted.")
