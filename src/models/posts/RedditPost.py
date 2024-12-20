from src.models.posts.Post import Post

class RedditPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'reddit'
        self.source = 'https://reddit.com{0}'.format(metadata['permalink'])
        self.tags.append(metadata['subreddit_name_prefixed'])
        if metadata['link_flair_text']:
            self.tags.append(metadata['link_flair_text'].lower())
            
        self.description = 'h4.{0}'.format(metadata['title'])
        
        if metadata['selftext']:
            self.description = '{0}\n\n{1}\n\nPosted by u/{2}'.format(
                self.description, metadata['selftext'], metadata['author'])
        
        self.prepend_prefix('red')
        self.tags.append('reddit')
        self.clean_tags()
        
        