from unittest import TestCase
# from flask import loads

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            # test that you're getting a template
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- THIS IS UNIQUE - SPENCER,PHIL -->', html)

    def test_api_score_word(self):
        """Test scoring a word guess."""

        with self.client as client:
            response = client.post('/api/new-game')
            newgame_data = response.get_json()
            resp1 = client.post('/api/score-word',
                                json={'gameId':newgame_data['gameId'],
                                'wordInput':'RAP'})
            json_response1 = resp1.get_json()
            resp2 = client.post('/api/score-word',
                                json={'gameId':newgame_data['gameId'],
                                'wordInput':'XAP'})
            json_response2 = resp2.get_json()
            resp3 = client.post('/api/score-word',
                                json={'gameId':newgame_data['gameId'],
                                'wordInput':'rap'})
            json_response3 = resp3.get_json()
            # Three separate arretEqual tests


    #     def test_color_submit_json(self):
    #     """test an AJAX request sending JSON to a server"""

    #     with app.test_client() as client:
    #   resp = client.post('/fav-color',
    #                     json={'color': 'blue'})
    #   json_response = resp.get_json()

    #   self.assertEqual({'message': 'blue is best!'}, json_response)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            newgame_data = response.get_json()
            self.assertTrue(isinstance(newgame_data["gameId"], str))
            self.assertEqual(self.is_list_of_lists(newgame_data["board"]), True)

    def is_list_of_lists(self, board):
        """Check if new board created is a list of lists"""

        if not (isinstance(board, list)):
            return False
        else:
            for lst in board:
                if not (isinstance(lst, list)):
                    return False

            return True