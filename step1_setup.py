# Real Estate Analysis - Beginner Setup
# Save this file as: step1_setup.py

# Step 1: Install required packages
# Open your terminal/command prompt and run:
# pip install pandas matplotlib plotly

print("🏠 Welcome to Real Estate Analysis!")
print("Let's start with the basics...")

# Import the libraries we need
import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Create some simple data to practice with
print("\n📊 Creating sample real estate data...")

# This is like creating a simple Excel sheet in Python
data = {
    'City': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune'],
    'Average_Price_Lakhs': [120, 85, 65, 55, 50],
    'Price_Per_SqFt': [12000, 8500, 6500, 5500, 5000]
}

# Convert to DataFrame (think of it as a smart Excel table)
df = pd.DataFrame(data)

# Step 3: Look at your data
print("\n🔍 Here's your data:")
print(df)

# Step 4: Do some basic analysis
print("\n📈 Basic Analysis:")
print(f"Most expensive city: {df.loc[df['Average_Price_Lakhs'].idxmax(), 'City']}")
print(f"Least expensive city: {df.loc[df['Average_Price_Lakhs'].idxmin(), 'City']}")
print(f"Average price across all cities: ₹{df['Average_Price_Lakhs'].mean():.1f} Lakhs")

# Step 5: Create your first chart
print("\n📊 Creating your first chart...")

plt.figure(figsize=(10, 6))
plt.bar(df['City'], df['Average_Price_Lakhs'], color='lightblue')
plt.title('Average Property Prices by City', fontsize=16)
plt.xlabel('City', fontsize=12)
plt.ylabel('Price (Lakhs)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the chart
plt.savefig('dashboards/my_first_chart.png')
plt.show()

print("\n✅ Success! You've created your first real estate analysis!")
print("📁 Check the 'dashboards' folder for your chart.")

# Step 6: Save your data to Excel
df.to_excel('data/basic_real_estate_data.xlsx', index=False)
print("💾 Data saved to Excel file: data/basic_real_estate_data.xlsx")

print("\n🎉 Congratulations! You've completed Step 1!")
print("Next: We'll make this data more realistic and add more analysis.")