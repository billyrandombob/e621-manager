from os import path

class Post:
    def __init__(self, file_path):
        self.tags = []
        self.file = file_path
        self.source = "local:{0}".format(path.basename(file_path))
        self.rating = 'safe'
        self.category = ''
    
    def clean_tags(self):
        new_tags = []
        for tag in self.tags:
            new_tag = tag.replace(' ', '_').strip().lower()
            if len(new_tag) > 0:
                new_tags.append(new_tag)
        self.tags = new_tags

    def prepend_prefix(self, prefix: str):
        new_tags = []
        for tag in self.tags:
            prefixed_tag = "<{0}>{1}".format(prefix, tag)
            new_tags.append(prefixed_tag)
        self.tags = new_tags
        
    def __str__(self):
        return 'File: {0}\nTags: {1}\nSource: {2}\nRating: {3}\nCategory: {4}'.format(self.file, self.tags, self.source, self.rating, self.category)