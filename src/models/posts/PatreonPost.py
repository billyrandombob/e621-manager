from src.lib.dtext_utils import convert_to_dtext
from src.models.posts.Post import Post

class PatreonPost(Post):

    def format_description(self, metadata):
        description = ''

        if metadata['title']:
            print('Title: {0}'.format(metadata['title']))
            description = 'h4. {0}'.format(metadata['title'])
        if metadata['content']:
            print('Content: {0}'.format(metadata['content']))
            if description == '':
                description = '{0}'.format(metadata['content'])
            else:
                description = '{0}\n{1}'.format(description, metadata['content'])
        if description == '':
            print('No description')
            return ''
        description = convert_to_dtext(description)
        print("Description:\n{0}".format(description))
        return description

    def __init__(self, file_path, metadata):
        super().__init__(file_path)

        self.category = 'patreon'
        self.source = '{0}%0A{1}'.format(self.source, metadata['url'])
        self.rating = 'u'

        self.description = self.format_description(metadata)

        self.tags = [tag.lower() for tag in metadata['tags']]
        self.tags.append(metadata['creator']['full_name'])
        self.tags.append(metadata['date'][:4])
        self.tags.append('{0}0s'.format(metadata['date'][:3]))
        self.prepend_prefix('pat')
        self.tags.append("rating_request")
        self.tags.append('patreon')
        self.clean_tags()