from importlib.metadata import metadata

from src.lib.dtext_utils import convert_to_dtext
from src.models.posts.Post import Post

class PatreonPost(Post):

    def format_description(self, metadata):
        description = ''

        if metadata['title']:
            description = 'h4. {0}'.format(metadata['title'])
        if metadata['content']:
            if description == '':
                description = '{0}'.format(metadata['content'])
            else:
                description = '{0}\n{1}'.format(description, metadata['content'])
        if description == '':
            return ''
        description = convert_to_dtext(description)
        return description

    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'patreon'
        self.source = '{0}%0A{1}'.format(self.source, metadata['url'])
        self.rating = 'u'

        self.description = self.format_description(metadata)

        name = metadata['creator']['full_name']

        # Add patreon tags from post
        # Use creator's name to make patreon tags unique to creator
        # This is because patreon does not have standardized tags, 
        # so we need to make them unique to avoid conflicts with other creators
        self.tags = [tag.lower() for tag in metadata['tags']]
        self.prepend_prefix('pat:{0}'.format(name))

        # Add user / creator as general patreon tag
        self.tags.append('<pat>user:{0}'.format(name))
        
        # Add various informational tags
        self.tags.append('{0}0s'.format(metadata['date'][:3]))
        self.tags.append(metadata['date'][:4])
        self.tags.append("rating_request")
        self.tags.append('{0}_(source)'.format(self.category))
        self.clean_tags()