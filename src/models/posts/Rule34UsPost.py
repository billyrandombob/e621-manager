from src.models.posts.Post import Post


class Rule34UsPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'rule34us'
        self.source = '{0}%0Ahttps://rule34.us/index.php?r=posts/view&id={1}'.format(self.source, metadata['id'])
        self.rating="e"
        
        if metadata.get('tags_general'):
            self.tags += metadata['tags_general'].split()
        if metadata.get('tags_artist'):
            self.tags += metadata['tags_artist'].split()
        if metadata.get('tags_character'):
            self.tags += metadata['tags_character'].split()
        if metadata.get('tags_copyright'):
            self.tags += metadata['tags_copyright'].split()
        if metadata.get('tags_metadata'):
            self.tags += metadata['tags_metadata'].split()
        self.prepend_prefix('r34u')
        self.tags.append('rule34us')
        self.clean_tags()