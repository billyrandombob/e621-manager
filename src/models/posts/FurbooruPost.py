from src.models.posts.Post import Post
import re

def convert_to_dtext(text: str) -> str:
    """
    Converts Markdown-like text to BBCode/Textile format.
    Handles:
    - Block quotes (> ) removal
    - Bold (**text**) to [b]text[/b]
    - Italics (*text*) to [i]text[/i]
    - Underline (__text__) to [u]text[/u]
    - Strikethrough (~~text~~) to [s]text[/s]
    - Links [text](url) to "text":url
    - Image links [![alt](img) text](url) to "text":url (ignoring image)
    """
    lines = text.split('\n')
    new_lines = []
    
    for line in lines:
        # Remove block quote markers and leading whitespace
        if line.strip().startswith('>'):
            line = line.lstrip('>').lstrip()
        
        # Convert formatting
        # Bold
        line = re.sub(r'\*\*(.*?)\*\*', r'[b]\1[/b]', line)
        # Italics
        line = re.sub(r'\*(.*?)\*', r'[i]\1[/i]', line)
        # Underline
        line = re.sub(r'__(.*?)__', r'[u]\1[/u]', line)
        # Strikethrough
        line = re.sub(r'~~(.*?)~~', r'[s]\1[/s]', line)
        
        # Image links: [![alt](img) text](url) -> "text":url
        line = re.sub(r'\[\!\[([^\]]+)\]\([^)]+\)\s*([^\]]+)\]\(([^)]+)\)', r'"\2":\3', line)
        # Regular links: [text](url) -> "text":url
        line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'"\1":\2', line)
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

class FurbooruPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'furbooru'
        self.source = '{0}%0Ahttps://furbooru.org/images/{1}'.format(self.source, metadata['id'])

        for source in metadata['source_urls']:
            self.source = '{0}%0A{1}'.format(self.source, source)

        self.tags = metadata['tags']
        self.prepend_prefix('frb')

        if metadata['description']:
            self.description = convert_to_dtext(metadata['description'])
        
        if 'safe' in metadata['tags']:
            self.rating = 'g'
        elif 'suggestive' in metadata['tags']:
            self.rating = 'm'
        elif 'questionable' in metadata['tags']:
            self.rating = 'm'
        elif 'explicit' in metadata['tags']:
            self.rating = 'm'

        self.tags.append('rating_request')
        self.tags.append('{0}_(source)'.format(self.category))
        self.clean_tags()