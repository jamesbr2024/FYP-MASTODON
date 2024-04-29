# Final
import csv
import re

# the names for our files
source_file = 'mastodon_instances.csv'
result_file = 'unique_instance_urls.csv'


url_extractor = re.compile(r'https?://([\w.-]+)/')

# the unique URLs in a set to avoid duplicates
collected_urls = set()
with open(source_file, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for line in reader:
        web_address = line['URL']
        found = url_extractor.match(web_address)
        if found:
            neat_url = found.group(0)
            collected_urls.add(neat_url)

# write all the unique URLs we found into a new CSV
with open(result_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Instance URL'])
    for url in sorted(collected_urls):
        writer.writerow([url])

