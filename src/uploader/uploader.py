from os import path, walk
from pathlib import Path
import time
import src.services.post_service as ps

from src.factories.PostFactory import PostFactory

YES_NO = ['y', 'Y', 'n', 'N']
RATINGS = ['s', 'e', 'u', 'q', 'safe', 'explicit', 'questionable', 'suggestive']
VALID_EXTENSIONS = ['.mp4', '.webm', '.jpg', '.jpeg', '.gif', '.png']

def get_rating():
    selection = None
    while selection not in RATINGS and selection != '':
        print('Set rating (leave blank for default/metadata value)')
        print('Options: safe(s) / questionable(q) / suggestive(u) / explicit(e)')
        selection = input('Rating: ').lower().strip()
        print('Selection is empty string: {0}'.format(selection == ''))
        
    selection = selection
    
    if selection == 's' or selection == 'safe':
        return 's'
    elif selection == 'q' or selection == 'questionable':
        return 'q'
    elif selection == 'u' or selection == 'suggestive':
        return 'u'
    elif selection == 'e' or selection == 'explicit':
        return 'e'
    else:
        return None

def include_metadata():
    selection = ''
    while selection not in YES_NO:
        selection = input('Include metadata? (y/n): ')
    
    if selection == 'y' or selection == 'Y':
        return True
    else:
        return False

def get_files(dir_str: str):
    directory = Path(dir_str)
    
    if directory.exists():
        files = []
        for (dirpath, dirnames, filenames) in walk (directory, topdown=False):
            for filename in filenames:
                file_path = path.join(dirpath, filename)
                file, extension = path.splitext(file_path)

                if extension.lower() in VALID_EXTENSIONS:
                    files.append(file_path)
        files.sort()
        print('Found {0} files'.format(len(files)))
        return files
    else:
        print('No files found')
        return None

def upload_directory(config):
    dir_str = input('Directory: ')
    files = get_files(dir_str)
    
    if files:
        metadata = include_metadata()
        extra_tags = input('Add tags: ')
        rating = get_rating()
        total_files = len(files)
        source = None
        
        wait_time = 1
        count = 1
        for file in files:
            time.sleep(0.2)
            print('({0}/{1}) - {2}'.format(count, total_files, file) )
            post_factory = PostFactory()
            post = post_factory.create(file, metadata, rating, extra_tags, source)
            
            retries = 0
            success = False
            while success == False:
                response = ps.create_post(config, post, source)
                if response.status_code == 200:
                    print('Successfully created')
                    success = True
                    count = count + 1
                elif '"reason":"duplicate"' in response.text:
                    print('Duplicate post. Skipping...')
                    success = True
                    count = count + 1
                else:
                    print('Failed to upload:\n{0}'.format(response.text))
                    success = False
                    retries += 1
                    
                    if retries >= 3:
                        success = True
                        print('Failed to upload afte 3 retries. Skipping...')
                    else:
                        wait_time = wait_time * retries
                        print('Failed to upload:\n{0}\nRetry {1}/3 after {2} seconds'.format(response.text, retries, wait_time))
                        time.sleep(wait_time)

    
def upload_file(config):
    file_str = input('File: ')
    filepath = Path(file_str)
    
    if filepath.exists():
        metadata = include_metadata()
        extra_tags = input('Add tags: ')
        rating = get_rating()
        source = input('Source: ')
        
        
        
        
    else:
        print('File Not Found!')