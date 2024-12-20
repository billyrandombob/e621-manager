from src.models.posts.Post import Post

class DanbooruPost(Post):    
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'danbooru'
        self.source = '{0}%0Ahttps://danbooru.donmai.us/posts/{1}'.format(self.source, metadata['id'])
        
        if metadata['rating'] == 'g':
            self.rating = 's'
        elif metadata['rating'] == 's':
            self.rating = 'q'
        elif metadata['rating'] == 'q':
            self.rating = 'u'
        elif metadata['rating'] == 'e':
            self.rating = 'e'
            
        if metadata['artist_commentary']:
            self.description = self.get_description(metadata)
        
        self.tags = metadata['tag_string'].split()
        self.tags.append(self.category)
        self.prepend_prefix('dan')
        self.clean_tags()

    def get_description(self, metadata):
        description = 'h4. Artist Commentary\noriginal\n'
        
        if metadata['artist_commentary']['original_title']:
            description += '[b]{0}[/b]'.format(metadata['artist_commentary']['original_title'])
            
        if metadata['artist_commentary']['original_description']:
            description += '\n{0}'.format(metadata['artist_commentary']['original_description'])
        
        if metadata['artist_commentary']['translated_title'] or metadata['artist_commentary']['translated_description']:
            description += '\n\nTranslated\n'
        
            if metadata['artist_commentary']['translated_title']:
                description = '{0}[b]{1}[/b]'.format(description, metadata['artist_commentary']['translated_title'])
            
            if metadata['artist_commentary']['translated_description']:
                description = '{0}\n{1}'.format(description, metadata['artist_commentary']['translated_description'])
        return description
    