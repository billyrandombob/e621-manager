from src.models.posts.Post import Post


class SubscribestarPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'subscribestar'
        self.source = '{0}%0Ahttps://subscribestar.adult/posts/{1}'.format(self.source, metadata['post_id'])

        self.rating = 'e'
        self.tags.append(metadata['author_name'])
        self.prepend_prefix('subs')
        self.tags.append(metadata['date'][:4])
        self.tags.append('{0}0s'.format(metadata['date'][:3]))
        self.tags.append('subscribestar')
        self.clean_tags()