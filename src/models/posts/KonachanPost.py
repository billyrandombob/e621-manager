from src.models.posts.Post import Post


class KonachanPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'konachan'
        self.source = '{0}%0Ahttps://konachan.com/post/show/{1}'.format(self.source, metadata['id'])

        self.rating = metadata['rating']
        self.tags = metadata['tags'].split()
        self.prepend_prefix('kona')
        self.tags.append('konachan')
        self.clean_tags()