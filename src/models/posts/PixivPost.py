from src.models.posts.Post import Post
from bs4 import BeautifulSoup

def replace_html(html):

    soup = BeautifulSoup(html)
    links = soup.find_all('a')
    


    for a in links:

        if a['href'] == a.contents[0]:
            a.replace_with(a['href'])
        else:
            a.replace_with('"{0}":{1}'.format(a.contents[0], a['href']))


    caption = soup.prettify()

    caption = caption.replace('<br />', '\n')
    caption = caption.replace('<br/>', '\n')
    caption = caption.replace('&gt;&gt;', '>>')
    caption = caption.replace('<strong>', '[b]')
    caption = caption.replace('</strong>', '[/b]')
    return caption

class PixivPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'pixiv'
        self.source = '{0}%0Ahttps://www.pixiv.net/en/artworks/{1}'.format(self.source, metadata['id'])
        
        if metadata['rating'] == 'General':
            self.rating = 'q'
        else:
            self.rating = 'e'

        

        if metadata['title'] and metadata['caption']:
            caption = replace_html(metadata['caption'])
            self.description = 'h5. {0}\n{1}'.format(metadata['title'], caption)
        elif metadata['title']:
            self.description = 'h5. {0}'.format(metadata['title'])
        elif metadata['caption']:
            caption = replace_html(metadata['caption'])
            self.description = '{0}'.format(caption)

        
        self.tags = metadata['tags']
        self.tags.append(metadata['type'])
        self.tags.append(metadata['user']['name'])
        self.prepend_prefix('pxv')
        self.tags.append(self.category)
        self.clean_tags()