from src.models.posts.Post import Post

class DanbooruPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'danbooru'
        self.source = '{0}%0Ahttps://danbooru.donmai.us/posts/{0}'.format(self.source, metadata['id'])
        
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
        self.prepend_prefix('dan')
        self.clean_tags()