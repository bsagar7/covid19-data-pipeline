import requests
import boto3
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import StringIO, BytesIO


countries = [
    "CHN", "TWN", "USA", "JPN", "THA", "KOR", "SGP", "PHL", "MYS", "VNM", "AUS", "MEX", "BRA", "COL", "FRA", "NPL",
    "CAN", "KHM", "LKA", "CIV", "DEU", "FIN", "ARE", "IND", "ITA", "GBR", "RUS", "SWE", "ESP", "BEL", "EGY",
    "IRN", "ISR", "LBN", "IRQ", "OMN", "AFG", "BHR", "KWT", "AUT", "DZA", "HRV", "CHE", "PAK", "GEO", "GRC", "MKD",
    "NOR", "ROU", "DNK", "EST", "NLD", "SMR", "AZE", "BLR", "ISL", "LTU", "NZL", "NGA", "IRL", "LUX", "MCO", "QAT",
    "ECU", "CZE", "ARM", "DOM", "IDN", "PRT", "AND", "LVA", "MAR", "SAU", "SEN", "ARG", "CHL", "JOR", "UKR", "BLM",
    "HUN", "FRO", "GIB", "LIE", "POL", "TUN", "PSE", "BIH", "SVN", "ZAF", "BTN", "CMR", "CRI", "PER", "SRB", "SVK",
    "TGO", "VAT", "GUF", "MLT", "MTQ", "BGR", "MDV", "BGD", "MDA", "PRY", "ALB", "CYP", "BRN", "MAC", "MAF", "BFA",
    "GGY-JEY", "MNG", "PAN", "TWN", "BOL", "HND", "COD", "JAM", "REU", "TUR", "CUB", "GUY", "KAZ", "CYM",
    "GLP", "ETH", "SDN", "GIN", "ATG", "ABW", "KEN", "URY", "GHA", "JEY", "NAM", "SYC", "TTO", "VEN", "CUW", "SWZ",
    "GAB", "GTM", "GGY", "MRT", "RWA", "LCA", "VCT", "SUR", "RKS", "CAF", "COG", "GNQ", "UZB", "GUM", "PRI", "BEN",
    "GRL", "LBR", "MYT", "SOM", "TZA", "BHS", "BRB", "MNE", "GMB", "KGZ", "MUS", "ZMB", "DJI", "TCD", "SLV", "FJI",
    "NIC", "MDG", "HTI", "AGO", "CPV", "NER", "PNG", "ZWE", "TLS", "ERI", "UGA", "DMA", "GRD", "MOZ", "SYR"
]


year = 2022
base_url = "https://covid-api.com/api/reports/total"

# Generate all (country, date) combinations 
dates = [f"{year}-{month:02d}-01" for month in range(1, 13)]
tasks = [(country, date) for country in countries for date in dates]

# Function to fetch one API call
def fetch_covid_data(country, date_str):
    try:
        response = requests.get(base_url, params={"iso": country, "date": date_str}, timeout=10)
        if response.status_code == 200:
            data = response.json().get("data", {})
            if data:
                data["country"] = country
                return data
    except Exception as e:
        print(f"❌ {country} on {date_str} failed: {e}")
    return None

# Parallel fetching 
all_data = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_covid_data, c, d): (c, d) for c, d in tasks}
    print(f"📅 Fetching data for: {dates}")
    for future in as_completed(futures):
        result = future.result()
        if result:
            all_data.append(result)


# Fetch country ISO list
def fetch_country_iso_list():
    regfion_url = "https://covid-api.com/api/regions"
    page = 1
    all_regions = []

    while True:
        response = requests.get(regfion_url, params={"per_page": 190, "page": page})
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch page {page}: {response.status_code}")
            break

        json_data = response.json()
        data = json_data.get("data", [])
        if not data:
            break

        all_regions.extend(data)

        next_page_url = json_data.get("next_page_url")
        if not next_page_url:
            break
        page += 1

    return all_regions


# Convert reports to CSV 
df = pd.DataFrame(all_data)

timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
csv_buffer = BytesIO()
df.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)

# Upload to reports to S3 
bucket_name = "covid-19-api-data"  # Replace this
s3_key = f"covid-data/monthly_summary_{timestamp}.csv"

s3 = boto3.client("s3")
s3.upload_fileobj(csv_buffer, bucket_name, s3_key)

print(f"✅ Uploaded to s3://{bucket_name}/{s3_key}")

# Convert regions to CSV 

regions = fetch_country_iso_list()
df = pd.DataFrame(regions)

timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
csv_buffer = BytesIO()
df.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)

# Upload regions to S3 
bucket_name = "covid-19-api-data"  # Replace this
s3_key = f"regions/iso_country_code_{timestamp}.csv"

s3 = boto3.client("s3")
s3.upload_fileobj(csv_buffer, bucket_name, s3_key)

print(f"✅ Uploaded to s3://{bucket_name}/{s3_key}")

