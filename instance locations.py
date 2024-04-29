# Final
import csv
import requests
import time

# the filenames
input_filename = 'resolved_ips_timeline.csv'
output_filename = 'resolved_loc_timeline.csv'
# Calculate how often requests should be sent
rate_limit = 60 / 43

def fetch_geo_info(ip):
    """Fetch geographical information based on IP address."""
    url = f'http://ip-api.com/json/{ip}'
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            if result['status'] == 'success':
                return {
                    'country': result['country'],
                    'city': result['city'],
                    'regionName': result['regionName'],
                    'isp': result['isp']
                }
        else:
            print(f"Data retrieval failed for {ip}: HTTP {resp.status_code}")
    except Exception as e:
        print(f"Error processing {ip}: {e}")

    return {
        'city': 'Unavailable',
        'regionName': 'Unavailable',
        'country': 'Unavailable',
        'isp': 'Unavailable'
    }

# Open the input and output files, then process each row
with open(input_filename, 'r', encoding='utf-8') as infile, \
     open(output_filename, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=['Domain', 'IP', 'Country', 'City', 'Region Name', 'ISP'])
    writer.writeheader()

    for entry in reader:
        ip = entry['IP Address']
        geo_data = fetch_geo_info(ip)
        writer.writerow({
            'Domain': entry['Domain'],
            'IP': ip,
            'Country': geo_data['country'],
            'City': geo_data['city'],
            'Region Name': geo_data['regionName'],
            'ISP': geo_data['isp']
        })
        time.sleep(rate_limit)

