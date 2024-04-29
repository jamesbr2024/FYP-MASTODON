# Final
import csv
import requests
import time

# Setting up
input_file_name = 'mastodon_instances_inventory_ip1.csv'
output_file_name = 'mastodon_instances_inventory_location1.csv'
request_interval = 60 / 43


def get_location_info(ip_addres):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_addres}', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'country': data['country'],
                    'city': data['city'],
                    'regionName': data['regionName'],
                    'isp': data['isp']
                }
    except requests.exceptions.ConnectTimeout:
        print(f"Connection timed out for {ip_addres}")
    except requests.exceptions.RequestException as e:
        print(f"Request exception for {ip_addres}: {e}")

    return {
        'city': 'N/A',
        'regionName': 'N/A',
        'country': 'N/A',
        'isp': 'N/A'
    }

with open(input_file_name, mode='r', encoding='utf-8') as input_csv_file, \
        open(output_file_name, mode='w', encoding='utf-8', newline='') as output_csv_file:
    csv_reader = csv.DictReader(input_csv_file)
    fieldnames = ['Domain', 'IP', 'Country', 'City', 'Region Name', 'ISP']
    csv_writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for row in csv_reader:
        ip_addres = row['IP Address']
        location_info = get_location_info(ip_addres)
        csv_writer.writerow({
            'Domain': row['Domain'],
            'IP': ip_addres,
            'Country': location_info['country'],
            'City': location_info['city'],
            'Region Name': location_info['regionName'],
            'ISP': location_info['isp']
        })
        time.sleep(request_interval)
