from src.models.posts.Post import Post

class YanderePost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'yandere'
        self.source = '{0}%0Ahttps://yande.re/post/show/{1}'.format(self.source, metadata['id'])

        self.rating = metadata['rating']
        self.tags = metadata['tags'].split()
        self.prepend_prefix('yand')
        self.tags.append('yandere')
        self.clean_tags()