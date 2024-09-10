from typing import List

from src.models.posts.Post import Post

class SzurubooruPost:
    def __init__(self, post_json):
        self.version = post_json['version']
        self.id = post_json['id']
        self.creationTime = post_json['creationTime']
        self.lastEditTime = post_json['lastEditTime']
        self.safety = post_json['safety']
        self.source = post_json['source']
        self.type = post_json['type']
        self.checksum = post_json['checksum']
        self.checksumMD5 = post_json['checksumMD5']
        self.canvasWidth = post_json['canvasWidth']
        self.canvasHeight = post_json['canvasHeight']
        self.contentUrl = post_json['contentUrl']
        self.thumbnailUrl = post_json['thumbnailUrl']
        self.flags = post_json['flags']

        self.tags: List[List[str]] = []
        for tag in post_json['tags']:
            names = []
            for name in tag['names']:
                names.append(name)
            self.tags.append(names)

        self.relations: List[int] = []
        for relation in post_json['relations']:
            self.relations.append(int(relation['id']))

        self.notes = post_json['notes']

        if post_json['user'] == None or post_json['user']['name'] == None:
            print(post_json)

        self.user = post_json['user']['name']
        self.score = post_json['score']
        self.ownScore = post_json['ownScore']
        self.ownFavorite = post_json['ownFavorite']
        self.tagCount = int(post_json['tagCount'])
        self.favoriteCount = int(post_json['favoriteCount'])
        self.commentCount = int(post_json['commentCount'])
        self.noteCount = int(post_json['noteCount'])
        self.featureCount = int(post_json['featureCount'])
        self.relationCount = int(post_json['relationCount'])
        self.lastFeatureTime = post_json['lastFeatureTime']
        self.favoritedBy = post_json['favoritedBy']
        self.hasCustomThumbnail = post_json['hasCustomThumbnail']
        self.mimeType = post_json['mimeType']
        self.comments = post_json['comments']
        self.pools = post_json['pools']

    def __str__(self) -> str:
        message = '{\n'
        message += '\tId: {0}\n'.format(self.id)
        message += '\tVersion: {0}\n'.format(self.version)
        message += '\tSafety: {0}\n'.format(self.safety)
        message += '\tCreated: {0}\n'.format(self.creationTime)
        message += '\tEdited: {0}\n'.format(self.lastEditTime)
        message += '\tSource: {0}\n'.format(self.source)
        message += '\tUser: {0}\n'.format(self.user)
        message += '\tType: {0}\n'.format(self.type)
        message += '\tChecksum: {0}\n'.format(self.checksum)
        message += '\tMD5: {0}\n'.format(self.checksumMD5)
        message += '\tWidth: {0}\n'.format(self.canvasWidth)
        message += '\tHeight: {0}\n'.format(self.canvasHeight)
        message += '\tContent URL: {0}\n'.format(self.contentUrl)
        message += '\tCustom Thumb: {0}\n'.format(self.hasCustomThumbnail)
        message += '\tThumb URL: {0}\n'.format(self.thumbnailUrl)
        message += '\tTags: {0}\n'.format(self.tags)
        message += '\tTag Count: {0}\n'.format(self.tagCount)
        message += '\tFlags: {0}\n'.format(self.flags)
        message += '\tRelations: {0}\n'.format(self.relations)
        message += '\tRelation Count: {0}\n'.format(self.relationCount)
        message += '\tScore: {0}\n'.format(self.score)
        message += '\tOwn Score: {0}\n'.format(self.ownScore)
        message += '\tOwn Favorite: {0}\n'.format(self.ownFavorite)
        message += '\tFavorite Count: {0}\n'.format(self.favoriteCount)
        message += '\tFavorited By: {0}\n'.format(self.favoritedBy)
        message += '\tComment Count: {0}\n'.format(self.commentCount)
        message += '\tFeature Count: {0}\n'.format(self.featureCount)
        message += '\tLast Feature Time: {0}\n'.format(self.lastFeatureTime)
        message += '\tMIME Type: {0}\n'.format(self.mimeType)
        message += '\tComments: {0}\n'.format(self.comments)
        message += '\tPools: {0}\n'.format(self.pools)
        message += '\tNote Count: {0}\n'.format(self.noteCount)
        message += '\tNotes: {0}\n'.format(self.notes)
        message +='}'
        return message

    def add_tag(self, tag_name: str):
        for tag in self.tags:
            if tag_name in tag:
                return
        self.tags.append([tag_name])
        self.tagCount = len(self.tags)
        
    def add_tags(self, tag_names: List[str]):
        for tag in tag_names:
            self.add_tag(tag)

    def get_tag_names(self):
        names = []
        for tag in self.tags:
            names.append(tag[0])
        return names

    def remove_tag(self, tag_name: str):
        for tag in self.tags:
            if tag_name in tag:
                self.tags.remove(tag)
                self.tagCount = len(self.tags)
                return
    
    def remove_tags(self, tag_names: List[str]):
        for tag in tag_names:
            self.remove_tag(tag)
            
    def convert(self, prefix, file_path):
        
        rating = self.safety
        
        if self.safety == 'safe':
            rating = 's'
        elif self.safety == 'sketchy' or self.safety == 'questionable':
            rating = 'q'
        elif self.safety == 'unsafe' or self.safety == 'explicit':
            rating = 'e'
        
        return Post(source_string=self.source, 
                    tag_list=self.get_tag_names(), 
                    rating=rating,
                    prefix=prefix,
                    file_path=file_path)