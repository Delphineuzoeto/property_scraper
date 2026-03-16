import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("property_data_clean.csv")

# recreate the same location avg price logic from analyse.py
loc_price = (
    df.groupby('location_clean')['price_millions']
    .agg(['mean', 'count'])
    .query('count >= 3')
    .sort_values('mean', ascending=False)
    .head(7)
)

locations = loc_price.index.tolist()
avg_prices_millions = loc_price['mean'].round(0).astype(int).tolist()
avg_prices_billions = [round(p / 1000, 2) for p in avg_prices_millions]  # convert to billions

# plot
plt.figure(figsize=(10, 6))
bars = plt.barh(locations, avg_prices_billions, color='#2ecc71')
plt.xlabel('Average Price (₦ Billions)', fontsize=12)  # updated to billions
# plt.title('Most Expensive Areas in Nigeria\n(Average Property Price)', fontsize=14, fontweight='bold')
plt.title('Most Expensive Areas in Nigeria (Average Property Price)', fontsize=14, fontweight='bold')

for bar, price in zip(bars, avg_prices_billions):
    plt.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2,
             f'₦{price}B', va='center', fontsize=10)

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('nigeria_property_prices.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved!")