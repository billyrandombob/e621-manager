from src.models.posts.Post import Post

class TheHentaiWorldPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = metadata['category']

        if metadata['type'] == 'video':
            self.source = '{0}%0Ahttps://thehentaiworld.com/videos/{1}'.format(self.source, metadata['slug'])
        elif metadata['type'] == '3d cgi':
            self.source = '{0}%0Ahttps://thehentaiworld.com/3d-cgi-hentai-images/{1}'.format(self.source, metadata['slug'])
        elif metadata['type'] == 'animated':
            self.source = '{0}%0Ahttps://thehentaiworld.com/gif-animated-hentai-images/{1}'.format(self.source, metadata['slug'])
        elif metadata['type'] == 'image':
            self.source = '{0}%0Ahttps://thehentaiworld.com/hentai-images/{1}'.format(self.source, metadata['slug'])

        self.tags = metadata['tags']
        self.prepend_prefix('thw')

        self.rating = 'u'

        if metadata['title']:
            self.description = 'h4. {0}'.format(metadata['title'])

        self.tags.append('{0}_(source)'.format(self.category))
        self.tags.append(metadata['extension'])
        self.clean_tags()