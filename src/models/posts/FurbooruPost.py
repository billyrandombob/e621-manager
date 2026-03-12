from src.models.posts.Post import Post

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
            self.description = metadata['description']
        
        if 'safe' in metadata['tags']:
            self.rating = 'g'
        elif 'suggestive' in metadata['tags']:
            self.rating = 'm'
        elif 'questionable' in metadata['tags']:
            self.rating = 'm'
        elif 'explicit' in metadata['tags']:
            self.rating = 'm'

        self.tags.append('rating_request')
        self.tags.append(self.category)
        self.clean_tags()