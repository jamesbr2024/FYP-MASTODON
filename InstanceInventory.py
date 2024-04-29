# Final
from mastodon import Mastodon
import time
import csv

#Mastodon client for the known instance
mastodon = Mastodon(
    api_base_url = 'https://mastodon.social'
)

def get_peers(instance_url):
    try:
        mastodon.api_base_url = instance_url
        peers = mastodon.instance_peers()
        return peers
    except:
        return []

def build_instance_database(start_instance, output_file):
    visited_instances = set()
    instances_to_visit = [start_instance]

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Instance URL'])

        while instances_to_visit:
            current_instance = instances_to_visit.pop(0)
            if current_instance not in visited_instances:
                visited_instances.add(current_instance)
                peers = get_peers(current_instance)

                for peer in peers:
                    if peer not in visited_instances:
                        instances_to_visit.append(peer)

                writer.writerow([current_instance])
                print(f"Discovered instance: {current_instance}")

                time.sleep(1)

output_file = 'mastodon_instances.csv'
build_instance_database('https://mastodon.social', output_file)
