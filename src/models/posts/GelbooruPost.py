from src.models.posts.Post import Post


class GelbooruPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'gelbooru'
        self.source = '{0}%0Ahttps://gelbooru.com/index.php?page=post&s=view&id={1}'.format(self.source, metadata['id'])
        
        if metadata['source']:
            self.source = '{0}%0A{1}'.format(self.source, metadata['source'])

        self.tags = metadata['tags'].split()
        self.prepend_prefix('gel')

        self.rating = metadata['rating']
        
        if metadata['rating'] == 'safe' or metadata['rating'] == 'general':
            self.rating = 'g'
            self.tags.append('safe')
        elif metadata['rating'] == 'sensitive':
            self.rating = 'g'
            self.tags.append('risque')
        elif metadata['rating'] == 'questionable':
            self.rating = 'm'
            self.tags.append('risque')
        elif metadata['rating'] == 'explicit':
            self.rating = 'm'
            self.tags.append('rating_request')
        
        
        
        
        self.tags.append('gelbooru')
        self.tags.append(metadata['extension'])
        self.clean_tags()