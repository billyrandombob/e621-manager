import json
from os import path
import time
from typing import List
from urllib.parse import urljoin, urlparse

from termcolor import colored
from src.models.posts.SzurubooruPost import SzurubooruPost
from src.models.posts.Post import Post
import src.services.post_service as ps
import src.uploader.uploader as up

def print_menu():
    print('Please make a selection:')
    print('1 - Upload Posts')
    print('2 - Add Tags to Posts')
    print('3 - Remove Tags from Posts')
    print('4 - Delete Posts')
    print('5 - Add Posts to Favs')
    print('6 - Change Posts Ratings')
    print('7 - Add Posts to Pool')
    print('8 - Set Parent Post')
    print('9 - Transfer from Szurubooru')
    print('0 - Return')


def upload_posts(config):
    selection: str = ''
    while selection != 0:
        
        print('Upload Posts')
        print('1 - Upload directory')
        print('2 - Upload file')
        print('0 - Return')
        selection = input('Selection: ')
        
        if selection == '1':
            print('uploading directory')
            up.upload_directory(config)
            print()
        elif selection == '2':
            print('uploading file')
        elif selection == '0':
            return
        
def delete_posts_by_search(config):
    tags: str = input('Enter tags to search (leave blank to return):\n')
    print()
    
    if tags.strip() == '':
        return

    posts = ps.search_posts(config, tags)

    if posts == None or len(posts) == 0:
        return

    ps.delete_posts(config, posts)
        
def delete_posts(config):
    selection: str = ''
    while selection != '0':
        print('Delete posts')
        print('1 - By search ')
        print('2 - By IDs')
        print('3 - By ID range')
        print('0 - Return')
        selection = input('Selection: ')
        print()

        
        if selection == '1':
            delete_posts_by_search(config)
            return
        elif selection == '2':
            #TODO: Delete posts with ids
            print('Not Implemented\n')
            return
        elif selection == '3':
            #TODO: Delete posts posts within range
            print('Not Implemented\n')
            return
        
def transfer_by_search(config):
    tags = input('Enter tags to search (leave blank to return):\n')
    if tags.strip() == '':
        return
    posts: List[SzurubooruPost] = ps.search_szuru_posts(config, tags)
    
    if posts == None or len(posts) == 0:
        return
    
    keep_tags = False
    selection: str = input('Keep tags? (y/N): ')
    if selection.lower() == 'y':
        keep_tags = True
    print()
    
    to_add: str = input('Add tags:\n')
    print()

    to_add_list: List[str] = str.split(to_add.strip(), ' ')
    
    rating: str = input('Rating (Leave blank to keep original):')
    rating = rating.lower()
    
    count = 1
    max_retries = config['max_retries']
    total_posts = len(posts)
    for post in posts:
        print('({0}/{1}) Transferring post {2}...'.format(count, total_posts, post.id))
        if keep_tags == False:
            post.tags = []
        
        if len(rating) > 0:
            post.safety = rating

        sources = post.source.split('\n')
        new_sources = []
        for source in sources:
            parsed = urlparse(post.source)
            if parsed.netloc == '':
                source = 'local:{0}'.format(source)
            new_sources.append(source)
        
        source_string = '%0A'.join(new_sources)
        file_path = path.join(config['szurubooru']['media_directory'], post.contentUrl.split('/')[-1])
        converted = post.convert('szru', file_path)
        converted.source = source_string
        
        new_tags = list()
        for tag in to_add_list:
            if len(tag) > 0:
                new_tags.append(tag.strip())
        
        converted.tags = converted.tags + new_tags
        
        wait_time = 1
        success = False
        retries = 0
        while success == False:
            response = ps.create_post(config, converted)
            resp_json = json.loads(response.text)
            
            if response.status_code == 200:
                url = urljoin(config['hostname'], resp_json['location'])
                print(colored('Success! {0}'.format(url), 'green'))
                success = True
                count = count + 1
            elif '"reason":"duplicate"' in response.text:
                print(colored('Duplicate post ({0}). Skipping...'.format(resp_json['post_id']), 'yellow'))
                success = True
                count += 1
            else:
                success = False
                retries += 1
                
                if retries > max_retries:
                    success = True
                    print(colored(
                        'Failed to transfer after {0} retries.\n\t{1}\n\tSkipping...'
                        .format(max_retries, response.text), 
                        'red'))
                    count += 1
                else:
                    wait_time = wait_time * retries
                    print(colored(
                        'Failed to transfer:\n{0}\nRetry {1}/{2} after {3} seconds'
                        .format(response.text, retries, max_retries, wait_time),
                        'red'))
                    time.sleep(wait_time)
    
        
def transfer_media(config):
    selection: str = ''
    while selection != '0':
        print('Transfer media')
        print('1 - By search ')
        print('2 - By IDs')
        print('3 - By ID range')
        print('0 - Return')
        selection = input('Selection: ')
        print()

        if selection == '1':
            transfer_by_search(config)
            return
        elif selection == '2':
            #TODO: Add tags to posts with ids
            print('Not Implemented\n')
            return
        elif selection == '3':
            #TODO: Add tags to posts within range
            print('Not Implemented\n')
            return
    
def manage_posts(config):
    selection: str = ''
    while selection != '0':
        print_menu()
        selection = input('Selection: ')
        print()
        if selection == '1':
            upload_posts(config)
        elif selection == '2':
            # add_tags(config)
            print('Not Implemented\n')
        elif selection == '3':
            #TODO: Remove Tags from Posts
            print('Not Implemented\n')
            # remove_tags(config)
        elif selection == '4':
            #TODO: Delete Posts
            delete_posts(config)
        elif selection == '5':
            #TODO: Add Posts to Favs
            print('Not Implemented\n')
        elif selection == '6':
            #TODO: Change Posts Safety
            print('Not Implemented\n')
        elif selection == '7':
            #TODO: Add Posts to Pool
            print('Not Implemented\n')
        elif selection == '8':
            #TODO: Set Parent Post
            print('Not Implemented\n')
        elif selection == '9':
            transfer_media(config)
    return