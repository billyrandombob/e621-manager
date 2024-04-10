from typing import List
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
    return