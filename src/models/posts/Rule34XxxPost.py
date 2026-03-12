from src.models.posts.Post import Post


class Rule34XxxPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'rule3xxx'
        self.source = '{0}%0Ahttps://rule34.xxx/index.php?page=post&s=view&id={1}'.format(self.source, metadata['id'])
        self.rating="u"
        
        if metadata.get('tags'):
            self.tags += metadata['tags'].split()
        
        self.prepend_prefix('r34x')
        self.tags.append("rating_request")
        self.tags.append('rule34xxx')
        self.clean_tags()