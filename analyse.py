import pandas as pd
import re

#load the dataframe
df = pd.read_csv("property_data.csv")
print(f"{len(df)} done")

#Clean PRICE
def clean_price(price_str):
    """Convert '₦45,000,000' → 45000000.0, 'Price on Request' → NaN"""
    if pd.isna(price_str) or str(price_str).strip().lower() == "price on request":
        return None
    digits = re.sub(r'[^\d]', '', str(price_str))   # strip ₦ and commas
    return float(digits) if digits else None

df['price_clean'] = df['price'].apply(clean_price)
df['price_millions'] = df['price_clean'] / 1_000_000 
# anything above ₦10 Billion (10,000M) is likely a data error
df = df[df['price_millions'] < 10_000]

#CLEAN BEDROOMS
df['bedrooms_clean'] = pd.to_numeric(df['bedrooms'], errors='coerce') # N/A => NaN

# CLEAN LOCATION(keep first part before comma)
df['location_clean'] = df['location'].str.split(',').str[0].str.strip()



# ── 5. OVERVIEW ───────────────────────────────────────────────────────────────
print("=" * 55)
print("📊 OVERVIEW")
print("=" * 55)
total          = len(df)
priced         = df['price_clean'].notna().sum()
price_on_req   = total - priced

print(f"  Total listings      : {total}")
print(f"  With price          : {priced}")
print(f"  Price on Request    : {price_on_req} ({price_on_req/total*100:.1f}%)")

# ── 6. PRICE SUMMARY ──────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("💰 PRICE SUMMARY  (₦ Millions)")
print("=" * 55)
p = df['price_millions'].dropna()
print(f"  Lowest              : ₦{p.min():,.1f}M")
print(f"  Highest             : ₦{p.max():,.1f}M")
print(f"  Average             : ₦{p.mean():,.1f}M")
print(f"  Median              : ₦{p.median():,.1f}M")

# ── 7. TOP LOCATIONS ──────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("📍 TOP 10 LOCATIONS  (by listing count)")
print("=" * 55)
top_locations = df['location_clean'].value_counts().head(10)
for loc, count in top_locations.items():
    print(f"  {loc:<30} {count} listings")

# ── 8. AVERAGE PRICE BY LOCATION (top 8) ─────────────────────────────────────
print("\n" + "=" * 55)
print("💵 AVG PRICE BY LOCATION  (₦ Millions, min 3 listings)")
print("=" * 55)
loc_price = (
    df.groupby('location_clean')['price_millions']
    .agg(['mean', 'count'])
    .query('count >= 3')
    .sort_values('mean', ascending=False)
    .head(8)
)
for loc, row in loc_price.iterrows():
    print(f"  {loc:<30} ₦{row['mean']:,.1f}M  ({int(row['count'])} listings)")

# ── 9. PROPERTY TYPE BREAKDOWN ────────────────────────────────────────────────
print("\n" + "=" * 55)
print("🏠 PROPERTY TYPE BREAKDOWN")
print("=" * 55)
type_counts = df['property_type'].value_counts()
for ptype, count in type_counts.items():
    pct = count / total * 100
    print(f"  {ptype:<30} {count:>4} ({pct:.1f}%)")

# ── 10. BEDROOM DISTRIBUTION ──────────────────────────────────────────────────
print("\n" + "=" * 55)
print("🛏️  BEDROOM DISTRIBUTION")
print("=" * 55)
bed_counts = df['bedrooms_clean'].dropna().astype(int).value_counts().sort_index()
for beds, count in bed_counts.items():
    print(f"  {beds} bedroom(s)   : {count} listings")

# ── 11. AVG PRICE BY BEDROOMS ─────────────────────────────────────────────────
print("\n" + "=" * 55)
print("💰 AVG PRICE BY BEDROOM COUNT  (₦ Millions)")
print("=" * 55)
bed_price = (
    df.groupby('bedrooms_clean')['price_millions']
    .mean()
    .dropna()
    .sort_index()
)
for beds, avg in bed_price.items():
    print(f"  {int(beds)} bedroom(s)   : ₦{avg:,.1f}M avg")

# ── 12. SAVE SUMMARY ──────────────────────────────────────────────────────────
df.to_csv("property_data_clean.csv", index=False)
print("\n✅ Cleaned data saved to property_data_clean.csv")
print("\n📋 ANALYSIS COMPLETE — paste results here for LinkedIn post!")

print(df[df['bedrooms_clean'] >= 7][['name', 'price', 'location']])