from src.models.posts.Post import Post


class SexComPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'sexcom'
        self.source = '{0}%0Ahttps://www.sex.com/pin/{1}'.format(self.source, metadata['pin_id'])
        self.rating = 'e'
        self.tags = metadata['tags']
        self.tags.append('sex.com')
        self.prepend_prefix('sxcm')
        self.clean_tags()
        