import base64
import json
from typing import List

import requests
from src.models.posts.SzurubooruPost import SzurubooruPost
from src.models.posts.Post import Post

def get_auth_token(user, key):
    token = base64.b64encode('{0}:{1}'.format(user,key).encode('utf-8'))
    return token

def get_headers(token):
    headers = {
        'Authorization': 'Token {0}'.format(token.decode('utf-8')),
        'Accept': 'application/json'
    }
    return headers

def convert_response_pages_to_post_list(post_pages: List) -> List[Post]:
    posts = []
    for page in post_pages:
        for post in page['results']:
            posts.append(SzurubooruPost(post))
    return posts

def create_post(config, post: Post):
    tags = ' '.join(post.tags)
    
    files = {
        'upload[file]': open(post.file, 'rb')
    }
    
    headers = get_headers(get_auth_token(config['username'], config['api_key']))
    
    return requests.request(
        'POST', '{0}/uploads.json'.format(config['hostname']),
        headers=headers, files=files, data={
            'upload[rating]': post.rating,
            'upload[tag_string]': tags,
            'upload[source]': post.source
        }
    )

def search_posts(config, terms: str) -> List[Post]:
    headers = get_headers(get_auth_token(config['username'], config['api_key']))
    posts = []
    total_pages = 1
    print('Fetching page {0}'.format(total_pages))
    response = requests.request(
        'GET', '{0}/posts.json?tags={1}'.format(config['hostname'], terms),
        headers=headers)
    responseJSON = response.json()
    if 'posts' in responseJSON:
        posts = posts + responseJSON['posts']
    else:
        print(responseJSON)
        print(response.text)
    
    while len(responseJSON['posts']) == config['posts_per_page']:
        print('Fetching page {0}'.format(total_pages+1))
        response = requests.request(
            'GET', '{0}/posts.json?page={1}&tags={2}'.format(config['hostname'], total_pages + 1, terms),
            headers=headers)
        responseJSON = response.json()
        if responseJSON['posts'] != []:
            total_pages += 1
            posts = posts + responseJSON['posts']
    
    print('Total Pages: {0}'.format(total_pages))
    print('Total Posts: {0}'.format(len(posts)))
    return posts
    
def delete_post(config, post):
    print('Deleting post {0}'.format(post))
    headers = get_headers(get_auth_token(config['username'], config['api_key']))
    response = requests.request(
        'POST', '{0}/moderator/post/posts/{1}/expunge.json'.format(config['hostname'], post), headers=headers)

    print('Status: '.format(response.status_code))
    print('Response:\n'.format(response.text))
    
def delete_posts(config, posts):
    count = 0
    for post in posts:
        count += 1
        print('Deleting post {0} of {1}'.format(count, len(posts)))
        delete_post(config, post['id'])
        
def search_szuru_posts(config, terms: str):
    current_page = 0
    headers = get_headers(get_auth_token(config['szurubooru']['username'], config['szurubooru']['token']))
    response = requests.request(
        'GET', '{0}/api/posts/?offset={1}&limit={2}&query={3}'.format(config['szurubooru']['hostname'], 0, 1, terms),
        headers=headers)
    responseJSON = response.json()
    total: int = responseJSON['total']
    page_size: int = config['szurubooru']['page_size']
    total_pages: int = int(total / page_size) + 1
    all_pages: List = []

    while current_page < total_pages:
        current_page += 1
        print('Fetching page {0} of {1}'.format(current_page, total_pages))
        current_pos = (page_size * current_page) - page_size
        response = requests.request(
            'GET', '{0}/api/posts/?offset={1}&limit={2}&query={3}'.format(config['szurubooru']['hostname'], current_pos, page_size, terms),
            headers=headers)
        if response.status_code != 200:
            print('Failed to fetch page')
            print('Response:\n{0}'.format(response.text))
            return None
        all_pages.append(response.json())
    
    print('Found {0} posts'.format(total))
    
    return convert_response_pages_to_post_list(all_pages)