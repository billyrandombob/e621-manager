from src.models.posts.Post import Post


class KonachanPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'konachan'
        self.source = '{0}%0Ahttps://konachan.com/post/show/{1}'.format(self.source, metadata['id'])

        if metadata['source']:
            self.source = '{0}%0A{1}'.format(self.source, metadata['source'])

        self.tags = metadata['tags'].split()
        self.prepend_prefix('kona')


        if metadata['rating'] == 's' or metadata['rating'] == 'safe':
            self.rating = 'g'
        else:
            self.rating = 'm'

        self.tags.append("rating_request")
        self.tags.append('{0}_(source)'.format(self.category))
        self.clean_tags()