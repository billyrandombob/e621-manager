from src.models.posts.Post import Post


class GelbooruPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'gelbooru'
        self.source = '{0}%0Ahttps://gelbooru.com/index.php?page=post&s=view&id={1}'.format(self.source, metadata['id'])
        
        if metadata['source']:
            self.source = '{0}%0A{1}'.format(self.source, metadata['source'])

        self.rating = metadata['rating']
        
        if metadata['rating'] == 'safe' or metadata['rating'] == 'general':
            self.rating = 's'
        elif metadata['rating'] == 'questionable' or metadata['rating'] == 'sensitive':
            self.rating = 'q'
        elif metadata['rating'] == 'explicit':
            self.rating = 'e'
        
        
        self.tags = metadata['tags'].split()
        self.prepend_prefix('gel')
        self.tags.append('gelbooru')
        self.tags.append(metadata['extension'])
        self.clean_tags()