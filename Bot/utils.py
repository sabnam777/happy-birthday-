import os

# Constants

BOT_TOKEN = os.environ.get('BOT_TOKEN')

MONGO_URI = os.environ.get('MONGO_URI')

# Utility functions

def connect_to_database():

    """

    Connects to the MongoDB database and returns the database instance.

    """

    from pymongo import MongoClient

    client = MongoClient(MONGO_URI)

    return client.get_database()

def get_random_video():

    """

    Returns a random video from the database of birthday videos.

    """

    import random

    db = connect_to_database()

    videos_collection = db['birthday_videos']

    video_count = videos_collection.count_documents({})

    if video_count > 0:

        random_video = videos_collection.aggregate([{ "$sample": { "size": 1 } }]).next()

        return f"https://www.youtube.com/watch?v={random_video['video_id']}"

    else:

        return None

def get_random_image_url():

    """

    Returns a random image URL from the list of available image URLs.

    """

    import random

    image_urls = ["https://picsum.photos/300/200?random=1",

                  "https://picsum.photos/300/200?random=2",

                  "https://picsum.photos/300/200?random=3"]

    return random.choice(image_urls)

