import base64
import json
from typing import List

import requests
from src.models.posts.Post import Post

def get_auth_token(config):
    token = base64.b64encode('{0}:{1}'.format(config['username'],config['api_key']).encode('utf-8'))
    return token

def get_headers(config):
    auth_token = get_auth_token(config)
    headers = {
        'Authorization': 'Token {0}'.format(auth_token.decode('utf-8')),
        'Accept': 'application/json'
    }
    return headers

def create_post(config, post: Post, source):
    tags = ' '.join(post.tags)
    
    files = {
        'upload[file]': open(post.file, 'rb')
    }
    
    headers = get_headers(config)
    
    return requests.request(
        'POST', '{0}/uploads.json'.format(config['hostname']),
        headers=headers, files=files, data={
            'upload[rating]': post.rating,
            'upload[tag_string]': tags,
            'upload[source]': post.source
        }
    )

def search_posts(config, terms: str) -> List[Post]:
    headers = get_headers(config)
    posts = []
    total_pages = 1
    print('Fetching page {0}'.format(total_pages))
    response = requests.request(
        'GET', '{0}/posts.json?tags={1}'.format(config['hostname'], terms),
        headers=headers)
    responseJSON = response.json()
    posts = posts + responseJSON['posts']
    
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
    headers = get_headers(config)
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