import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict


from app import TimelinePost

MODELS = [TimelinePost]

# use SQLite db for testing
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test_db using list MODELS
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not completely necessary since SQLite works in memory,
        # but good practice nonetheless

        test_db.drop_tables(MODELS)
        test_db.close() 

    def test_timeline_post(self):
        # Making sample posts
        first_post = TimelinePost.create(name='John Doe',
        email='john@email.com',content='This is John!')
        assert first_post.id == 1
        
        second_post = TimelinePost.create(name='Jane Doe',
        email='jane@email.com',content='This is Jane!')
        assert second_post.id == 2

        # Test that test data was processed correctly
        get_first = model_to_dict(TimelinePost.get_by_id(1))
        assert get_first['name'] == first_post.name

        get_second = model_to_dict(TimelinePost.get_by_id(2))
        assert get_second['email'] == second_post.email