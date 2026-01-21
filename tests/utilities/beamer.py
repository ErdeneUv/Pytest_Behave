import os
import requests
from dotenv import load_dotenv


load_dotenv()
beamer_key = os.getenv('beamer_key')

API_KEY = 'YOUR_API_KEY'  # Replace with your real Beamer API key
API_BASE = 'https://api.getbeamer.com/v0'

res = requests.get(
    "https://api.getbeamer.com/v0/posts",
    headers={"Beamer-Api-Key": API_KEY}
)
print(f"ERS: {res.status_code, res.json()}")

# Specify the date (YYYY-MM-DD) you want to delete posts from
TARGET_DATE = '2025-07-10'
# Specify keyword to match in the title (case-insensitive)
TITLE_KEYWORD = 'YourKeyword'  # e.g., 'Test Notification'

headers = {
    'Beamer-Api-Key': API_KEY,
    'Content-Type': 'application/json'
}

def get_all_posts():
    all_posts = []
    page = 1
    while True:
        response = requests.get(f'{API_BASE}/posts?page={page}', headers=headers)
        if response.status_code != 200:
            print(f"Error fetching posts: {response.status_code} {response.text}")
            break
        try:
            data = response.json()
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            print(f"Response was: {response.text}")
            break
        posts = data.get('posts', [])
        if not posts:
            break
        all_posts.extend(posts)
        page += 1
    return all_posts

def delete_post(post_id):
    response = requests.delete(f'{API_BASE}/posts/{post_id}', headers=headers)
    return response.status_code == 204

def main():
    posts = get_all_posts()
    print(f"Found {len(posts)} total posts.")

    # Filter posts by date and title keyword (case-insensitive)
    posts_to_delete = [
        post for post in posts
        if post['published_at'].startswith(TARGET_DATE)
        and TITLE_KEYWORD.lower() in post['title'].lower()
    ]

    print(f"Found {len(posts_to_delete)} posts from {TARGET_DATE} with title containing '{TITLE_KEYWORD}' to delete.")

    for post in posts_to_delete:
        deleted = delete_post(post['id'])
        print(f"Deleted post {post['id']} - \"{post['title']}\": {'Success' if deleted else 'Failed'}")

if __name__ == '__main__':
    all_post = get_all_posts()
    print(f"Found {len(all_post)} total posts.")