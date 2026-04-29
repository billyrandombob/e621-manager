from src.models.posts.Post import Post

class PornhubPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'pornhub'
        if metadata['subcategory'] == 'gif':
            self.source = 'https://www.pornhub.com/gif/{0}'.format(metadata['id'])
        
        self.tags = metadata['tags']
        self.tags.append(metadata['extension'])
        self.tags.append(metadata['subcategory'])
            
        self.description = metadata['title']
        
        self.rating = 'u'
        
        self.prepend_prefix('phb')
        self.tags.append('{0}_(source)'.format(self.category))
        self.tags.append("rating_request")
        self.clean_tags()