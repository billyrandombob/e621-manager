from src.models.posts.Post import Post


class AIBooruPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'aibooru'
        self.source = '{0}%0Ahttps://aibooru.online/posts/{1}'.format(self.source, metadata['id'])
        
        if metadata['description']:
            self.description = metadata['description']
        
        if metadata['rating'] == 'g':
            self.rating = 's'
        elif metadata['rating'] == 's':
            self.rating = 'q'
        elif metadata['rating'] == 'q':
            self.rating = 'u'
        elif metadata['rating'] == 'e':
            self.rating = 'e'
        
        self.tags = metadata['tag_string'].split()
        self.tags.append(self.category)
        self.prepend_prefix('aib')
        self.clean_tags()
        