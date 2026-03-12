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

        self.tags = metadata['tags']
        self.prepend_prefix('derp')

        if metadata['description']:
            self.description = metadata['description']
        
        if 'safe' in metadata['tags']:
            self.rating = 'g'
            self.tags.append('safe')
        elif 'suggestive' in metadata['tags']:
            self.rating = 'm'
            self.tags.append('rating_request')
        elif 'questionable' in metadata['tags']:
            self.rating = 'm'
            self.tags.append('rating_request')
        elif 'explicit' in metadata['tags']:
            self.rating = 'm'
            self.tags.append('rating_request')
        
        self.tags.append(self.category)
        self.clean_tags()