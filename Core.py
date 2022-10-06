
import pymongo.database

from pymongo import MongoClient


cluster = MongoClient()


# Database, Collections

boroda4_db: pymongo.database.Database = cluster.Boroda4Bot

rating_coll: pymongo.database.Collection = boroda4_db.Rating
channel_coll: pymongo.database.Collection = boroda4_db.Channels


class RatingMember:
    def __init__(self, member_id: int):
        if rating_coll.find_one({"member_id": member_id}) is None:
            RatingMember.create_member(member_id)
        member = rating_coll.find_one({"member_id": member_id})
        self.member_id = member_id
        self._rating = member.get("rating", 0)

    @staticmethod
    def create_member(member_id: int):
        rating_coll.insert_one({
            "member_id": member_id,
            "rating": 0
        })

    @property
    def rating(self):
        return rating_coll.find_one({"member_id": self.member_id}).get("rating", 0)

    @rating.setter
    def rating(self, a):
        if a < 0:
            a = 0
        rating_coll.update_one({"member_id": self.member_id}, {"$set": {"rating": a}})


def set_dire_channel(channel_id: int):
    if channel_coll.find_one({"team": "dire"}) is None:
        channel_coll.insert_one({"team": "dire", "channel_id": 0})
    channel_coll.update_one({"team": "dire"}, {"$set": {"channel_id": channel_id}})


def set_radiant_channel(channel_id: int):
    if channel_coll.find_one({"team": "dire"}) is None:
        channel_coll.insert_one({"team": "radiant", "channel_id": 0})
    channel_coll.update_one({"team": "radiant"}, {"$set": {"channel_id": channel_id}})


def get_dire_channel():
    return channel_coll.find_one({"team": "dire"})['channel_id']


def get_radiant_channel():
    return channel_coll.find_one({"team": "radiant"})['channel_id']
