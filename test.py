from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_board(self):
        """Test page set-up"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Boggle</h1>", html)
            self.assertIn('<label for="guess">Enter a word:</label>', html)
            self.assertIn('board', session)
            self.assertIn('statistics', session)
            self.assertEqual(session['statistics']['high_score'], 0)
            self.assertEqual(session['statistics']['times_played'], 0)

    def test_guess(self):
        """Test if a word is on the board"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["H", "E", "L", "L", "O"], ["H", "E", "L", "L", "O"],["H", "E", "L", "L", "O"],["H", "E", "L", "L", "O"],["H", "E", "L", "L", "O"]]
            resp = client.get('/guess?guess=hello')
            response_text = resp.json['result']

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(response_text, "ok")   
    
    def test_bad_guess(self):
        """Test if a word is valid english"""
        with app.test_client() as client:
            client.get('/')
            resp = client.get('/guess?guess=krat')
            response_text = resp.json['result']

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(response_text, "not-word")
    
    def test_guess_against_board(self):
        """Test if a word exists, but it is not on the board"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["H", "E", "L", "L", "O"], ["H", "E", "L", "L", "O"],["H", "E", "L", "L", "O"],["H", "E", "L", "L", "O"],["H", "E", "L", "L", "O"]]
            resp = client.get('/guess?guess=good')
            response_text = resp.json['result']

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(response_text, "not-on-board")
        
        # with app.test_client() as client:

