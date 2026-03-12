from src.models.posts.Post import Post

class TwitterPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'twitter/x'
        self.source = 'https://x.com/{0}/status/{1}'.format(
            metadata['user']['name'], metadata['tweet_id'])
        

        self.description = metadata['content']
        self.rating = 'g'

        if metadata['sensitive']:
            self.rating = 'u'

        self.tags = metadata['hashtags']
        self.tags.append(metadata['user']['name'])
        self.tags.append(metadata['author']['name'])
        
        self.prepend_prefix('twx')
        self.tags.append(self.category)
        self.tags.append("rating_request")
        self.clean_tags()