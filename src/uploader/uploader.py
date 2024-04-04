from os import path, walk
from pathlib import Path
import src.services.post_service as ps

from src.factories.PostFactory import PostFactory

YES_NO = ['y', 'Y', 'n', 'N']
RATINGS = ['s', 'e', 'u', 'q', 'safe', 'explicit', 'questionable', 'suggestive']
VALID_EXTENSIONS = ['.mp4', '.webm', '.jpg', '.jpeg', '.gif']

def get_rating():
    selection = ''
    while selection not in RATINGS:
        print('Set rating (leave blank for default/metadata value)')
        print('Options: safe(s) / questionable(q) / suggestive(u) / explicit(e)')
        selection = input('Rating: ').lower().strip()
        
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

                print('Extension: {0}'.format(extension))
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
        
        count = 1
        for file in files:
            
            success = False
            while success == False:
                print('({0}/{1}) - {2}'.format(count, total_files, file) )
                
                post_factory = PostFactory()
                post = post_factory.create(file, metadata, rating, extra_tags, source)
                
                response = ps.create_post(config, post, source)
                print(response.text)
                success = True
                count = count + 1

    
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