# Final
from mastodon import Mastodon
import time
import csv

input_file = 'mastodon_instances1tags.csv'
output_file = 'mastodon_instance_trending_tags1.csv'
def get_instance_trending_tags(api_base_url):
    try:
        mastodon = Mastodon(api_base_url=api_base_url)
        trending_tags = mastodon.trending_tags()
        return trending_tags
    except Exception as e:
        print(f"Failed to retrieve trending tags from {api_base_url}: {e}")
        return []

def process_instances(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)

        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Instance URL', 'Trending Tags'])

            for row in reader:
                instance_url = row[0]
                trending_tags = get_instance_trending_tags(instance_url)

                if trending_tags:
                    tags_list = [tag['name'] for tag in trending_tags]
                    tags_string = ', '.join(tags_list)
                    writer.writerow([instance_url, tags_string])
                    print(f"Retrieved trending tags from instance: {instance_url}")
                    print(f"Trending tags: {tags_list}")
                else:
                    print(f"No trending tags found for instance: {instance_url}")

                time.sleep(1)
process_instances(input_file, output_file)