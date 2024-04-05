from src.models.posts.Post import Post


class E621Post(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'e621'
        self.source = '{0}%0Ahttps://e621.net/posts/{1}'.format(self.source, metadata['id'])

        meta_tags = metadata['tags']
        self.tags.extend(meta_tags['artist'])
        self.tags.extend(meta_tags['character'])
        self.tags.extend(meta_tags['copyright'])
        self.tags.extend(meta_tags['general'])
        self.tags.extend(meta_tags['lore'])
        self.tags.extend(meta_tags['meta'])
        self.tags.extend(meta_tags['species'])
        self.prepend_prefix('e621')
        self.tags.append('e621')
        self.clean_tags()
        self.rating = metadata['rating']