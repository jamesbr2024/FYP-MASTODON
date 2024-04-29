# Final

import csv
from mastodon import Mastodon, MastodonServiceUnavailableError, MastodonNetworkError
import time

# Mastodon API Client with own keys
mastodon = Mastodon(
    client_id='',
    client_secret='',
    access_token='',
    api_base_url='https://mastodon.social'
)

def save_posts_to_csv(posts, filename="mastodon_public_timeline.csv", mode='a'):
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if mode == 'w':
            writer.writerow([
                'ID', 'URI', 'URL', 'Username', 'Account ID', 'In Reply To ID', 'In Reply To Account ID',
                'Content', 'Created At', 'Reblogs Count', 'Favourites Count', 'Replies Count', 'Sensitive',
                'Spoiler Text', 'Visibility', 'Language', 'Application', 'Media Attachments Count', 'Tags Count',
                'Emojis Count'
            ])

        for post in posts:
            writer.writerow([
                post['id'], post['uri'], post['url'],
                post['account']['username'], post['account']['id'],
                post.get('in_reply_to_id', 'N/A'), post.get('in_reply_to_account_id', 'N/A'),
                post['content'], post['created_at'],
                post['reblogs_count'], post['favourites_count'], post.get('replies_count', 'N/A'),
                post['sensitive'], post['spoiler_text'], post['visibility'],
                post.get('language', 'N/A'), (post.get('application') or {}).get('name', 'N/A'),
                len(post.get('media_attachments', [])), len(post.get('tags', [])), len(post.get('emojis', []))
            ])

def fetch_and_save_public_timeline_with_retry(filename="mastodon_public_timeline_extended11.csv", max_retries=100):
    max_id = None
    first_batch = True
    retries = 0
    while True:
        try:
            public_posts = mastodon.timeline_public(limit=40, max_id=max_id)
            if not public_posts:  # If no posts are returned, stop fetching
                break

            save_posts_to_csv(public_posts, filename, mode='w' if first_batch else 'a')
            max_id = public_posts[-1]['id']  # Update max_id to the ID of the last post fetched

            if first_batch:
                first_batch = False

            time.sleep(2)
            retries = 0
        except (MastodonNetworkError, MastodonServiceUnavailableError) as e:
            if retries < max_retries:
                wait = 2 ** retries
                print(f"Error: {e}. Retrying in {wait} seconds.")
                time.sleep(wait)
                retries += 1
            else:
                print("Max retries reached. Exiting.")
                break
fetch_and_save_public_timeline_with_retry()
