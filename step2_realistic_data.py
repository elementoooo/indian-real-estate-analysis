# Step 2: Create More Realistic Real Estate Data
# Save this as: step2_realistic_data.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta
import random

print("🏠 Step 2: Creating Realistic Real Estate Data")
print("=" * 50)

# Set random seed for consistent results
np.random.seed(42)
random.seed(42)

def create_realistic_property_data(num_properties=500):
    """
    Create realistic property data for Indian cities
    """
    
    # Define cities with their characteristics
    cities_info = {
        'Mumbai': {
            'base_price_per_sqft': 15000,
            'price_variation': 0.4,  # 40% variation
            'avg_area_multiplier': 0.8  # Smaller properties
        },
        'Delhi': {
            'base_price_per_sqft': 12000,
            'price_variation': 0.3,
            'avg_area_multiplier': 1.0
        },
        'Bangalore': {
            'base_price_per_sqft': 8000,
            'price_variation': 0.5,
            'avg_area_multiplier': 1.2
        },
        'Chennai': {
            'base_price_per_sqft': 7000,
            'price_variation': 0.3,
            'avg_area_multiplier': 1.1
        },
        'Pune': {
            'base_price_per_sqft': 7500,
            'price_variation': 0.4,
            'avg_area_multiplier': 1.1
        },
        'Hyderabad': {
            'base_price_per_sqft': 6500,
            'price_variation': 0.5,
            'avg_area_multiplier': 1.3
        }
    }
    
    # Property types with typical area ranges
    property_types = {
        '1BHK': {'min_area': 400, 'max_area': 600},
        '2BHK': {'min_area': 600, 'max_area': 900},
        '3BHK': {'min_area': 900, 'max_area': 1400},
        '4BHK': {'min_area': 1400, 'max_area': 2000}
    }
    
    properties = []
    
    for i in range(num_properties):
        # Choose random city and property type
        city = random.choice(list(cities_info.keys()))
        prop_type = random.choice(list(property_types.keys()))
        
        # Get city characteristics
        city_data = cities_info[city]
        prop_data = property_types[prop_type]
        
        # Generate area (with city modifier)
        base_area = random.randint(prop_data['min_area'], prop_data['max_area'])
        area = int(base_area * city_data['avg_area_multiplier'])
        
        # Generate price per sq ft (with variation)
        base_price = city_data['base_price_per_sqft']
        price_variation = random.uniform(1 - city_data['price_variation'], 
                                       1 + city_data['price_variation'])
        price_per_sqft = int(base_price * price_variation)
        
        # Calculate total price
        total_price_lakhs = (price_per_sqft * area) / 100000  # Convert to lakhs
        
        # Add some realistic attributes
        property_age = random.randint(0, 25)  # Age in years
        floor_number = random.randint(1, 20)
        total_floors = random.randint(floor_number, 25)
        
        # Location score (1-10, affects price slightly)
        location_score = random.randint(1, 10)
        
        # Adjust price based on location score and age
        location_bonus = 1 + (location_score - 5) * 0.02  # ±10% based on location
        age_penalty = 1 - (property_age * 0.01)  # -1% per year of age
        
        final_price = total_price_lakhs * location_bonus * age_penalty
        
        # Create realistic listing date (last 2 years)
        days_ago = random.randint(1, 730)
        listing_date = datetime.now() - timedelta(days=days_ago)
        
        properties.append({
            'city': city,
            'property_type': prop_type,
            'area_sqft': area,
            'price_lakhs': round(final_price, 2),
            'price_per_sqft': price_per_sqft,
            'property_age_years': property_age,
            'floor_number': floor_number,
            'total_floors': total_floors,
            'location_score': location_score,
            'listing_date': listing_date,
            'month_listed': listing_date.strftime('%Y-%m')
        })
    
    return pd.DataFrame(properties)

# Create the realistic dataset
print("🔄 Generating realistic property data...")
df = create_realistic_property_data(500)

print(f"✅ Created data for {len(df)} properties")
print(f"📊 Cities included: {', '.join(df['city'].unique())}")
print(f"🏠 Property types: {', '.join(df['property_type'].unique())}")

# Show sample of the data
print("\n📋 Sample of your data:")
print(df.head())

# Basic statistics
print("\n📈 Basic Statistics:")
print(f"Average property price: ₹{df['price_lakhs'].mean():.2f} Lakhs")
print(f"Price range: ₹{df['price_lakhs'].min():.2f} - ₹{df['price_lakhs'].max():.2f} Lakhs")
print(f"Average area: {df['area_sqft'].mean():.0f} sq ft")

# City-wise analysis
print("\n🏙️ City-wise Average Prices:")
city_stats = df.groupby('city').agg({
    'price_lakhs': 'mean',
    'price_per_sqft': 'mean',
    'area_sqft': 'mean'
}).round(2)

for city in city_stats.index:
    print(f"  {city}: ₹{city_stats.loc[city, 'price_lakhs']:.2f} Lakhs avg, "
          f"₹{city_stats.loc[city, 'price_per_sqft']:.0f}/sq ft")

# Create better visualizations
print("\n📊 Creating improved charts...")

# 1. City-wise price comparison
plt.figure(figsize=(12, 6))
city_avg = df.groupby('city')['price_lakhs'].mean().sort_values(ascending=False)
bars = plt.bar(city_avg.index, city_avg.values, color='skyblue')
plt.title('Average Property Prices by City', fontsize=16, fontweight='bold')
plt.xlabel('City', fontsize=12)
plt.ylabel('Average Price (Lakhs)', fontsize=12)
plt.xticks(rotation=45)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'₹{height:.0f}L', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('dashboards/city_price_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Property type analysis
plt.figure(figsize=(10, 6))
prop_avg = df.groupby('property_type')['price_lakhs'].mean().sort_values(ascending=True)
bars = plt.barh(prop_avg.index, prop_avg.values, color='lightgreen')
plt.title('Average Prices by Property Type', fontsize=16, fontweight='bold')
plt.xlabel('Average Price (Lakhs)', fontsize=12)
plt.ylabel('Property Type', fontsize=12)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width + 2, bar.get_y() + bar.get_height()/2.,
             f'₹{width:.0f}L', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('dashboards/property_type_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 3. Interactive chart with Plotly
print("🌟 Creating interactive chart...")
fig = px.scatter(df, x='area_sqft', y='price_lakhs', 
                color='city', size='location_score',
                hover_data=['property_type', 'property_age_years'],
                title='Property Price vs Area by City',
                labels={'area_sqft': 'Area (sq ft)', 
                       'price_lakhs': 'Price (Lakhs)'})

fig.write_html('dashboards/interactive_price_area_chart.html')
print("💾 Interactive chart saved as 'interactive_price_area_chart.html'")

# Save the dataset
df.to_excel('data/realistic_real_estate_data.xlsx', index=False)
df.to_csv('data/realistic_real_estate_data.csv', index=False)

print("\n✅ Step 2 Complete!")
print("📁 Files created:")
print("   - data/realistic_real_estate_data.xlsx")
print("   - data/realistic_real_estate_data.csv")
print("   - dashboards/city_price_comparison.png")
print("   - dashboards/property_type_analysis.png")
print("   - dashboards/interactive_price_area_chart.html")

print("\n🚀 Ready for Step 3: Advanced Analysis!")