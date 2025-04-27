from src.models.posts.Post import Post

class DerpibooruPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'derpibooru'
        self.source = '{0}%0Ahttps://derpibooru.org/images/{1}'.format(self.source, metadata['id'])


        if 'source_urls' in metadata:
            for source in metadata['source_urls']:
                self.source = '{0}%0A{1}'.format(self.source, source)
        elif 'source_url' in metadata:
            self.source = '{0}%0A{1}'.format(self.source, metadata['source_url'])

        if metadata['description']:
            self.description = metadata['description']
        
        if 'safe' in metadata['tags']:
            self.rating = 's'
        elif 'suggestive' in metadata['tags']:
            self.rating = 'q'
        elif 'questionable' in metadata['tags']:
            self.rating = 'u'
        elif 'explicit' in metadata['tags']:
            self.rating = 'e'
        
        self.tags = metadata['tags']
        self.prepend_prefix('derp')
        self.tags.append(self.category)
        self.clean_tags()