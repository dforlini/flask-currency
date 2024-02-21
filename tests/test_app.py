from flask import Flask, request, render_template
import unittest
from unittest.mock import patch
from app import app

class IndexRouteTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_index_get(self):
        """Test the index page with GET request"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)
        
    @patch('app.requests.get')
    def test_index_post_valid(self, mock_get):
        """Test the index page with a valid POST request"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.jsonreturn_value = {'result': 100}
        
        response = self.app.post('/', data={
            'from_currency': 'USD',
            'to_currency': 'GBP',
            'amount': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('conversion_result', response.data.decode('utf-8'))
        
    @patch('app.request.get')
    def test_index_post_invalid_amount(self, mock_get):
        """Test the index page with an invalid amount in POST request"""
        response = self.app.post('/', data={
            'from_currency': 'USD',
            'to_currency': 'GBP',
            'amount': '-100'
            
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid amount', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()                    