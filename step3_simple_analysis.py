# Step 3: Simple Real Estate Market Analysis
# Save this as: step3_simple_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("🔍 Step 3: Simple Real Estate Market Analysis")
print("=" * 55)

# Load the data we created in Step 2
print("📂 Loading data...")
try:
    df = pd.read_excel('data/realistic_real_estate_data.xlsx')
    print(f"✅ Loaded {len(df)} property records")
except FileNotFoundError:
    print("❌ Data file not found! Please run step2_realistic_data.py first")
    exit()

# Let's answer some basic business questions!
print("\n🤔 Let's answer some important business questions...")

# Question 1: Which city has the highest property prices?
print("\n1️⃣  QUESTION: Which city is most expensive?")
print("-" * 40)

city_avg_prices = df.groupby('city')['price_lakhs'].mean().sort_values(ascending=False)
most_expensive_city = city_avg_prices.index[0]
highest_price = city_avg_prices.iloc[0]

print(f"🏆 Most expensive city: {most_expensive_city}")
print(f"💰 Average price: ₹{highest_price:.2f} Lakhs")

print("\n📊 All cities ranking:")
for i, (city, price) in enumerate(city_avg_prices.items(), 1):
    print(f"   {i}. {city}: ₹{price:.2f} Lakhs")

# Question 2: What's the best value for money?
print("\n2️⃣  QUESTION: Which property type gives best value?")
print("-" * 45)

# Calculate price per sq ft by property type
value_analysis = df.groupby('property_type').agg({
    'price_per_sqft': 'mean',
    'area_sqft': 'mean',
    'price_lakhs': 'mean'
}).round(2)

print("🏠 Value analysis by property type:")
for prop_type in value_analysis.index:
    row = value_analysis.loc[prop_type]
    print(f"   {prop_type}: ₹{row['price_per_sqft']}/sq ft, "
          f"Avg area: {row['area_sqft']} sq ft, "
          f"Avg price: ₹{row['price_lakhs']} Lakhs")

best_value = value_analysis['price_per_sqft'].idxmin()
print(f"\n🎯 Best value: {best_value} (lowest price per sq ft)")

# Question 3: How does property age affect price?
print("\n3️⃣  QUESTION: Do older properties cost less?")
print("-" * 42)

# Create age groups
df['age_group'] = pd.cut(df['property_age_years'], 
                        bins=[0, 5, 10, 15, 25], 
                        labels=['0-5 years', '6-10 years', '11-15 years', '16+ years'])

age_analysis = df.groupby('age_group')['price_lakhs'].mean()
print("🕐 Price by property age:")
for age_group, avg_price in age_analysis.items():
    print(f"   {age_group}: ₹{avg_price:.2f} Lakhs")

newest_properties = age_analysis.iloc[0]
oldest_properties = age_analysis.iloc[-1]
price_difference = newest_properties - oldest_properties
print(f"\n📉 Price difference: ₹{price_difference:.2f} Lakhs "
      f"({price_difference/oldest_properties*100:.1f}% more for new properties)")

# Question 4: Which locations are premium?
print("\n4️⃣  QUESTION: How much does location matter?")
print("-" * 42)

location_analysis = df.groupby('location_score').agg({
    'price_lakhs': 'mean',
    'price_per_sqft': 'mean'
}).round(2)

print("📍 Price by location score (1=worst, 10=best):")
for score in [1, 5, 10]:
    if score in location_analysis.index:
        row = location_analysis.loc[score]
        print(f"   Score {score}: ₹{row['price_lakhs']:.2f} Lakhs, "
              f"₹{row['price_per_sqft']}/sq ft")

# Calculate the "location premium"
if 10 in location_analysis.index and 1 in location_analysis.index:
    premium = location_analysis.loc[10, 'price_lakhs'] - location_analysis.loc[1, 'price_lakhs']
    print(f"\n🌟 Location premium: ₹{premium:.2f} Lakhs difference between best and worst locations")

# Create visualizations for our analysis
print("\n📊 Creating analysis charts...")

# Chart 1: Price vs Age Analysis
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# Age vs Price
age_prices = df.groupby('property_age_years')['price_lakhs'].mean()
ax1.scatter(age_prices.index, age_prices.values, alpha=0.7, color='red')
ax1.plot(age_prices.index, age_prices.values, color='darkred', alpha=0.5)
ax1.set_xlabel('Property Age (years)')
ax1.set_ylabel('Average Price (Lakhs)')
ax1.set_title('Property Price vs Age')
ax1.grid(True, alpha=0.3)

# Location Score vs Price
location_prices = df.groupby('location_score')['price_lakhs'].mean()
ax2.bar(location_prices.index, location_prices.values, color='green', alpha=0.7)
ax2.set_xlabel('Location Score (1-10)')
ax2.set_ylabel('Average Price (Lakhs)')
ax2.set_title('Price by Location Quality')
ax2.grid(True, alpha=0.3)

# Property Type Distribution
prop_count = df['property_type'].value_counts()
ax3.pie(prop_count.values, labels=prop_count.index, autopct='%1.1f%%', startangle=90)
ax3.set_title('Property Type Distribution')

# City-wise Price Range
city_prices = []
cities = []
for city in df['city'].unique():
    city_data = df[df['city'] == city]['price_lakhs']
    city_prices.append([city_data.min(), city_data.max()])
    cities.append(city)

city_prices = pd.DataFrame(city_prices, index=cities, columns=['Min', 'Max'])
city_prices.plot(kind='bar', ax=ax4, color=['lightblue', 'darkblue'])
ax4.set_title('Price Range by City')
ax4.set_ylabel('Price (Lakhs)')
ax4.tick_params(axis='x', rotation=45)
ax4.legend()

plt.tight_layout()
plt.savefig('dashboards/market_analysis_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()

# Create an interactive dashboard
print("🌟 Creating interactive dashboard...")

# Create subplot dashboard
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=['City Price Comparison', 'Property Type Analysis', 
                   'Age vs Price Trend', 'Location Impact'],
    specs=[[{'type': 'bar'}, {'type': 'bar'}],
           [{'type': 'scatter'}, {'type': 'bar'}]]
)

# Chart 1: City comparison
city_avg = df.groupby('city')['price_lakhs'].mean().sort_values(ascending=False)
fig.add_trace(
    go.Bar(x=city_avg.index, y=city_avg.values, name='Avg Price',
           marker_color='lightblue'),
    row=1, col=1
)

# Chart 2: Property type
prop_avg = df.groupby('property_type')['price_lakhs'].mean()
fig.add_trace(
    go.Bar(x=prop_avg.index, y=prop_avg.values, name='Avg Price by Type',
           marker_color='lightgreen'),
    row=1, col=2
)

# Chart 3: Age vs Price
age_avg = df.groupby('property_age_years')['price_lakhs'].mean()
fig.add_trace(
    go.Scatter(x=age_avg.index, y=age_avg.values, mode='markers+lines',
               name='Age vs Price', marker_color='red'),
    row=2, col=1
)

# Chart 4: Location impact
location_avg = df.groupby('location_score')['price_lakhs'].mean()
fig.add_trace(
    go.Bar(x=location_avg.index, y=location_avg.values, name='Location Impact',
           marker_color='orange'),
    row=2, col=2
)

fig.update_layout(
    title_text="Real Estate Market Analysis Dashboard",
    height=800,
    showlegend=False
)

fig.write_html('dashboards/interactive_market_dashboard.html')

# Generate a simple market report
print("\n📋 Generating Market Report...")

report = f"""
🏠 REAL ESTATE MARKET ANALYSIS REPORT
{'='*50}

📊 MARKET OVERVIEW:
• Total Properties Analyzed: {len(df):,}
• Average Property Price: ₹{df['price_lakhs'].mean():.2f} Lakhs
• Price Range: ₹{df['price_lakhs'].min():.2f} - ₹{df['price_lakhs'].max():.2f} Lakhs
• Average Area: {df['area_sqft'].mean():.0f} sq ft

🏆 KEY FINDINGS:

1. MOST EXPENSIVE CITY: {most_expensive_city}
   • Average Price: ₹{highest_price:.2f} Lakhs
   • Premium over cheapest city: {(highest_price/city_avg_prices.iloc[-1] - 1)*100:.1f}%

2. BEST VALUE PROPERTY: {best_value}
   • Lowest cost per sq ft: ₹{value_analysis.loc[best_value, 'price_per_sqft']}/sq ft

3. PROPERTY AGE IMPACT:
   • New properties (0-5 years) cost ₹{price_difference:.2f} Lakhs more than old ones
   • Age depreciation: ~{price_difference/oldest_properties*100:.1f}% premium for new properties

4. LOCATION PREMIUM:
   • Best locations cost significantly more than average locations
   • Location quality is a major price driver

💡 INVESTMENT INSIGHTS:
• Consider {city_avg_prices.index[-1]} for affordable entry into real estate
• {best_value} properties offer best value for money
• Newer properties in good locations command premium prices
• Location score strongly correlates with property value

📈 MARKET TRENDS:
• Premium cities: {', '.join(city_avg_prices.index[:2])}
• Value cities: {', '.join(city_avg_prices.index[-2:])}
• Most popular property type: {df['property_type'].mode()[0]}
"""

# Save the report
with open('dashboards/market_report.txt', 'w') as f:
    f.write(report)

print(report)

