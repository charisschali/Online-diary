import unittest, json
from app import create_app
from app.models import ClearClass


class Test_Entry_resources(unittest.TestCase):
    key = "Welcome to your personal diary, your access token is"
    get_entries = '/mydiary/v1/entries'
    add_entry = '/mydiary/v1/entries'
    get_single = '/mydiary/v1/entries/1'
    delete_entry = '/mydiary/v1/entries/2'
    edit_entry = '/mydiary/v1/entries/1'

    """ This class tests the functionality of entries endpoint"""
    def setUp(self):
        self.app = create_app('testing')
        self.tester = self.app.test_client(self)
        self.singup_url = '/mydiary/v1/auth/register'
        self.singin_url = '/mydiary/v1/auth/login'
        self.new_user = {"username":'test',
                         'email':'test11e1@camp.com',
                         'password':'test1111',
                         'confirm_password':'test1111'
                        }
        self.user = {'email':'test11e1@camp.com', 'password':'test1111',}
        self.new_entry = {'title':'Bootcamp', 'content':'It was a good experience'}
        self.new_entry2 = {'title':'Andela', 'content':'This is Andela'}
        self.new_entry3 = {'title':'Andelan', 'content':'This is Andela'}
        self.no_title = {'content':'It was a good experience'}

    def register_user(self):
        """register user."""
        return self.tester.post(self.singup_url, data=self.new_user)

    def login_user(self):
        """login user."""
        return self.tester.post(self.singin_url, data=self.user)

    def test_adding_entry(self):
        ''' Testing if the Api can add an entry requested by a logged in user '''
        ClearClass().drop_tables()
        ClearClass().create_table()
        self.register_user()
        res = self.login_user()
        with self.app.app_context():
            #decoding token
            token = json.loads(res.data.decode('utf-8'))[self.key]
            headers = {'Authorization': 'Bearer {}'.format(token)}
            data = json.dumps(self.new_entry)
            data2 = json.dumps(self.new_entry2)
            content_type = 'application/json'
            res = self.tester.post(self.add_entry, headers=headers, data=data, content_type=content_type)
            res = self.tester.post(self.add_entry, headers=headers,data=data2, content_type=content_type)
            self.assertEqual(res.status_code, 201)
    def test_adding_entry_with_missing_title(self):
        ''' Testing if the Api can add an entry requested by a logged in user '''
        res = self.login_user()
        with self.app.app_context():
            #decoding token
            token = json.loads(res.data.decode('utf-8'))[self.key]
            headers = {'Authorization': 'Bearer {}'.format(token)}
            data = json.dumps(self.no_title)
            content_type = 'application/json'
            res = self.tester.post(self.add_entry, headers=headers, data=data, content_type=content_type)
            self.assertIn("Title is required!", str(res.data))
    def test_adding_entry_with_duplicate_title(self):
        ''' Testing if the Api can add an entry requested by a logged in user '''
        res = self.login_user()
        with self.app.app_context():
            #decoding token
            token = json.loads(res.data.decode('utf-8'))[self.key]
            headers = {'Authorization': 'Bearer {}'.format(token)}
            data = json.dumps(self.new_entry)
            content_type = 'application/json'
            res = self.tester.post(self.add_entry, headers=headers, data=data, content_type=content_type)
            res = self.tester.post(self.add_entry, headers=headers, data=data, content_type=content_type)
            self.assertIn("Title already exist, use a different one.", str(res.data))

    def test_get_entries(self):
        ''' Testing if the Api can fetch all entries requested by a logged in user '''
        res = self.login_user()
        token = json.loads(res.data.decode('utf-8'))[self.key]
        headers = {'Authorization': 'Bearer {}'.format(token)}
        res = self.tester.get(self.get_entries, headers=headers,
                              content_type='application/json'
                             )
        self.assertEqual(res.status_code, 200)

    def test_get_single_entry(self):
        ''' Testing if the Api can fetch a single requested by a logged in user '''
        res = self.login_user()
        token = json.loads(res.data.decode('utf-8'))[self.key]
        headers = {'Authorization': 'Bearer {}'.format(token)}
        self.tester.post(self.add_entry, headers=headers, data=json.dumps(self.new_entry),
                         content_type='application/json'
                         )
        res = self.tester.get(self.get_single, headers=headers, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_update_entry(self):
        ''' Testing if the Api can update an entry requested by a logged in user '''
        res = self.login_user()
        token = json.loads(res.data.decode('utf-8'))[self.key]
        headers = {'Authorization': 'Bearer {}'.format(token)}
        data = json.dumps(self.new_entry3)
        res = self.tester.put(self.edit_entry, headers=headers, data=data,
                              content_type='application/json'
                             )
        self.assertEqual(res.status_code, 200)
        self.assertIn("Entry Updated successfully", str(res.data))

    def test_delete_entry(self):
        ''' Testing if the Api can delete an entry requested by a logged in user '''
        res = self.login_user()
        token = json.loads(res.data.decode('utf-8'))[self.key]
        headers = {'Authorization': 'Bearer {}'.format(token)}
        data = json.dumps(self.new_entry)
        self.tester.post(self.add_entry, headers=headers, data=data,
                         content_type='application/json'
                        )
        res = self.tester.delete(self.delete_entry, headers=headers,
                                 content_type='application/json'
                                 )
        self.assertIn("Your entry was successfully deleted", str(res.data))

    def test_using_wrong_url(self):
        ''' Using wrong url '''
        res = self.login_user()
        token = json.loads(res.data.decode('utf-8'))[self.key]
        headers = {'Authorization': 'Bearer {}'.format(token)}
        data = json.dumps(self.new_entry)
        res = self.tester.post("\mydiary\v1\andela", headers=headers, data=data,
                               content_type='application/json'
                              )
        self.assertEqual(res.status_code, 404)
        res = self.tester.post('\mydiary\v1\entries\hi', headers=headers, data=data,
                               content_type='application/json'
                              )
        self.assertEqual(res.status_code, 404)
        ClearClass().drop_tables()
        ClearClass().create_table()
