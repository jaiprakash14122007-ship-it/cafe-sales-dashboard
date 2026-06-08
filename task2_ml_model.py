import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("cleaned_cafe_sales.csv")
X = df[["Quantity", "Price Per Unit"]]
y = df["Total Spent"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

sample_input = pd.DataFrame(
    [[2, 3.0]],
    columns=["Quantity", "Price Per Unit"]
)

prediction = model.predict(sample_input)


print("\n" + "="*60)
print("        CAFÉ SALES PREDICTION SYSTEM")
print("="*60)

print("\n📊 MODEL PERFORMANCE")
print("-"*40)
print(f"Mean Absolute Error (MAE)   : {mae:.2f}")
print(f"Mean Squared Error (MSE)    : {mse:.2f}")
print(f"R² Score (Accuracy)         : {r2:.2f}")

print("\n🔮 SAMPLE PREDICTION")
print("-"*40)
print("Input Features:")
print("   Quantity = 2")
print("   Price Per Unit = 3.0")

print("\nPredicted Total Spent:")
print(f"   ₹ {prediction[0]:.2f}")

print("\n✅ Model Status: TRAINED & READY")
print("="*60)

plt.figure(figsize=(8,5))
plt.scatter(y_test, y_pred, color="blue")
plt.xlabel("Actual Total Spent")
plt.ylabel("Predicted Total Spent")
plt.title("Actual vs Predicted Values")
plt.grid(True)
plt.show()

importance = model.feature_importances_

plt.figure(figsize=(6,4))
plt.bar(X.columns, importance, color="green")
plt.title("Feature Importance (Model Insight)")
plt.ylabel("Importance Score")
plt.show()