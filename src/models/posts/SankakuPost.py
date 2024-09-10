from src.models.posts.Post import Post

class SankakuPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'sankaku'
        self.source = '{0}%0Ahttps://chan.sankakucomplex.com/post/show/{1}'.format(self.source, metadata['id'])
        
        if metadata['rating'] == 's':
            self.rating = 's'
        elif metadata['rating'] == 'q':
            self.rating = 'q'
        elif metadata['rating'] == 'e':
            self.rating = 'e'
        
        self.tags = metadata['tags']
        self.tags.append(self.category)
        self.prepend_prefix('san')
        self.clean_tags()