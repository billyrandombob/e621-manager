from src.models.posts.Post import Post

class SankakuPost(Post):
    def __init__(self, file_path, metadata):
        super().__init__(file_path)
        
        self.category = 'sankaku'


        id = metadata['id']
        md5 = metadata['md5']

        self.source = '{0}%0Ahttps://chan.sankakucomplex.com/post/show/{1}'.format(self.source, id)
        self.source = '{0}%0Ahttps://chan.sankakucomplex.com/post/show/{1}'.format(self.source, md5)
        self.source = '{0}%0Ahttps://www.sankakucomplex.com/posts/{1}'.format(self.source, id)

        self.tags = metadata['tags']
        self.prepend_prefix('san')
        
        if metadata['rating'] == 's':
            self.rating = 'g'
            self.tags.append('safe')
        elif metadata['rating'] == 'q':
            self.rating = 'g'
            self.tags.append('risque')
        elif metadata['rating'] == 'e':
            self.rating = 'm'
            self.tags.append('rating_request')
        else:
            self.rating = 'u'
            self.tags.append('rating_request')
        
        
        self.tags.append('{0}_(source)'.format(self.category))
        self.clean_tags()