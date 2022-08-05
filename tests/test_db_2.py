import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict


from app import TimelinePost

MODELS = [TimelinePost]

# use SQLite db for tests
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db 
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite databases only live during connection
        # but good practice

        test_db.drop_tables(MODELS)

        # closes db connection
        test_db.close() 

    def test_timeline_post(self):
        # post 1
        first_post = TimelinePost.create(name='John Doe',
        email='john@email.com', content='Hi I\'m John!')
        assert first_post.id == 1
        
        # post 2
        second_post = TimelinePost.create(name='Jane Doe',
        email='jane@email.com',content='Hi I\'m Jane!')
        assert second_post.id == 2

        # Get timeline posts and assert they are correct
        get_first = model_to_dict(TimelinePost.get_by_id(1))
        assert get_first['name'] == first_post.name
        assert get_first['email'] == first_post.email

        get_second = model_to_dict(TimelinePost.get_by_id(2))
        assert get_second['name'] == second_post.name
        assert get_second['email'] == second_post.email