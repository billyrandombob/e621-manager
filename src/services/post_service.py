import base64
import json

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