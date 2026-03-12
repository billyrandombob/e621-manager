from src.models.posts.Post import Post


class AIBooruPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'aibooru'
        self.source = '{0}%0Ahttps://aibooru.online/posts/{1}'.format(self.source, metadata['id'])
        
        if metadata['description']:
            self.description = metadata['description']

        self.tags = metadata['tag_string'].split()
        self.prepend_prefix('aib')
        
        if metadata['rating'] == 'g':
            self.rating = 'g'
            self.tags.append('safe')
        elif metadata['rating'] == 's':
            self.rating = 'g'
            self.tags.append('rating_request')
        elif metadata['rating'] == 'q':
            self.rating = 'm'
            self.tags.append('rating_request')
        elif metadata['rating'] == 'e':
            self.rating = 'm'
            self.tags.append('rating_request')
        
        self.tags.append(self.category)
        self.clean_tags()
        