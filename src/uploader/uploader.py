from itertools import islice
import json
from os import path, walk
from pathlib import Path
import time
from json.decoder import JSONDecodeError

from termcolor import colored
import src.services.post_service as ps

from src.factories.PostFactory import PostFactory

YES_NO = ['y', 'Y', 'n', 'N']
RATINGS = ['g', 'm', 'u', 'general', 'mature', 'unrated']
VALID_EXTENSIONS = ['.mp4', '.webm', '.jpg', '.jpeg', '.gif', '.png', '.webp']

def get_source():
    source = input('Source: ').lower().strip()

    if source == None or source == '':
        print('No source provided.')
        return None
    
    return source

def get_rating():
    selection = None
    while selection not in RATINGS and selection != '':
        print('Set rating (leave blank for default/metadata value)')
        print('Options: general(g) / mature(m) / unrated(u)')
        selection = input('Rating: ').lower().strip()
        
    selection = selection
    
    if selection == 'g' or selection == 'general':
        return 'g'
    elif selection == 'm' or selection == 'mature':
        return 'm'
    elif selection == 'u' or selection == 'unrated':
        return 'u'
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
    
def get_start():
    start = ''
    try:
        start = input('Start at (blank = 1): ')
        return int(start) - 1
    except:
        if start.strip().lower() == '':
            print(colored('Starting at file 1', 'green'))
        else:
            print(colored('Invalid number. Starting at 1', 'red'))
        return 0
    

def upload_directory(config):
    dir_str = input('Directory: ')
    files = get_files(dir_str)
    
    if files:
        start = get_start()
        metadata = include_metadata()
        extra_tags = input('Add tags: ')
        rating = get_rating()
        total_files = len(files)
        source = get_source()
        max_retries = config['max_retries']
        max_timeout = config['max_timeout']
        
        count = start + 1
        for file in islice(files, start, None):
            time.sleep(0.2)
            print('({0}/{1}) - {2}'.format(count, total_files, file) )
            post_factory = PostFactory()
            post = post_factory.create(file, metadata, rating, extra_tags, source)
            
            wait_time = 1
            retries = 0
            success = False
            while success == False and retries < max_retries:
                try:
                    response = ps.create_post(config, post)
                    resp_json = json.loads(response.text)
                    
                    if response.status_code == 200:
                        print(colored('Success! {0}'.format(resp_json['location']), 'green'))
                        success = True
                        count = count + 1
                    elif '"reason":"duplicate"' in response.text:
                        print(colored('Duplicate post ({0}). Skipping...'.format(resp_json['post_id']), 'yellow'))
                        success = True
                        count += 1
                    elif 'only jpg, png, gif, webm, mp4, and webp files are allowed' in response.text:

                        if 'application/x-matroska' in response.text:
                            print(colored('Invalid format (application/x-matroska).'.format(response.text), 'red'))
                        elif 'image/webp' in response.text:
                            print(colored('Invalid image format (image/webp).'.format(response.text), 'red'))
                        else:
                            print(colored(response.text, 'red'))
                        print(colored('Skipping...', 'yellow'))
                        success = True
                        count += 1
                    elif 'video container/codec' in response.text:
                        print(colored('Invalid video format.', 'red'))
                        print(colored('Skipping...', 'yellow'))
                        success = True
                        count += 1
                    elif 'File is corrupt' in response.text:
                        print(colored('Corrupt file', 'red'))
                        print(colored('Skipping...', 'yellow'))
                        success = True
                        count += 1
                    else:
                        success = False
                        retries += 1
                        
                        if retries > max_retries:
                            success = True
                            print(colored(
                                'Failed to upload after {0} retries.\n\t{1}\n\tSkipping...'
                                .format(max_retries, response.text), 
                                'red'))
                            count += 1
                        else:
                            wait_time = wait_time * retries
                            
                            if wait_time > max_timeout:
                                wait_time = max_timeout
                            
                            print(colored(
                                'Failed to upload:\n{0}\nRetry {1}/{2} after {3} seconds'
                                .format(response.text, retries, max_retries, wait_time),
                                'red'))
                            time.sleep(wait_time)
                except JSONDecodeError as e:
                    print(colored('Error decoding response JSON\n\n{0}'.format(e), 'red'))
                    retries += 1
                    success = False
                    wait_time = wait_time * retries
                    print(colored('Retrying in {0} seconds...'.format(wait_time), 'red'))
                    time.sleep(wait_time)
                except Exception as e:
                    print(colored('Unknown error\n\n{0}'.format(e), 'red'))
                    retries += 1
                    success = False
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
        print(colored('File Not Found!'), 'red')