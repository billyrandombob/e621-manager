from src.models.posts.Post import Post


class PatreonPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'patreon'
        self.source = '{0}%0A{1}'.format(self.source, metadata['url'])

        self.tags = [tag.lower() for tag in metadata['tags']]
        self.tags.append(metadata['creator']['full_name'])
        self.tags.append(metadata['date'][:4])
        self.tags.append('{0}0s'.format(metadata['date'][:3]))
        self.prepend_prefix('pat')
        self.tags.append('patreon')
        self.clean_tags()