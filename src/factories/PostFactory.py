import json
from src.models.posts.E621Post import E621Post
from src.models.posts.SubscribestarPost import SubscribestarPost
from src.models.posts.SankakuPost import SankakuPost
from src.models.posts.DanbooruPost import DanbooruPost
from src.models.posts.AIBooruPost import AIBooruPost
from src.models.posts.SexComPost import SexComPost
from src.models.posts.Post import Post


class PostFactory(object):
    
    def create_metadata_item(self, file_path):
        try:
            with open('{0}.json'.format(file_path), 'r') as meta_file:
                metadata = json.load(meta_file)
        except:
            print('Error creating metadata file.')
            print('Creating generic item')
            return Post(file_path)

        category = metadata['category']
        
        if category == 'aibooru':
            return AIBooruPost(file_path, metadata)
        if category == 'danbooru':
            return DanbooruPost(file_path, metadata)
        if category == 'e621':
            return E621Post(file_path, metadata)
        if category == 'sankaku':
            return SankakuPost(file_path, metadata)
        if category == 'sexcom':
            return SexComPost(file_path, metadata)
        if category == 'subscribestar':
            return SubscribestarPost(file_path, metadata)
        
        print('No metadata parser found for {0}. Using generic metadata.'.format(category))
        return Post(file_path)
    
    def create(self, file_path, use_metadata, rating, tags, source):
        post = None
        if use_metadata:
            post = self.create_metadata_item(file_path)
        else:
            post = Post(file_path)
            
        if rating:
            post.rating = rating
        
        if tags:
            post.tags.extend(tags.split())
            
        if source:
            post.source = source
        
        return post
        