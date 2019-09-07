import unittest 
import os 

from api import app 
from bson.objectid import ObjectId
from json import dumps 

from pymongo import MongoClient 
from flask import (Flask, jsonify, request)

db_client = MongoClient('mongodb://localhost:27017/')
db = db_client['test_db']


class TestUser(unittest.TestCase): 
    """Test API calls for user."""

    def setUp(self): 
        """Set up elements before every test."""

        self.app = app.test_client()
        self.app.testing = True 
    
    def test_create_user_200(self): 
        """POST new user."""

        email = 'test@apitests.com'
        phone_numbers = '1234567890'
        legal_names = "Test User"
        
        results = self.app.post('/v1/users', 
                                data={'email': email, 
                                      'phone_numbers': phone_numbers,
                                      'legal_names': legal_names})
        
        self.assertEqual(results.status_code, 200)
    
    def test_get_all_users_200(self): 
        """GET all users."""

        results = self.app.get('/v1/users')
        self.assertEqual(results.status_code, 200)


    def test_get_one_user_200(self): 
        """GET one user.""" 

        email = 'test@apitests.com'
        phone_numbers = '1234567890'
        legal_names = "Test User"
        
        results = self.app.post('/v1/users', 
                                data={'email': email, 
                                      'phone_numbers': phone_numbers,
                                      'legal_names': legal_names})
        
        self.assertEqual(results.status_code, 200)

        user_id = results.user_id 
        results = self.app.get(f'/v1/users{user_id}')
        self.assertEqual(results.status_code, 200)


class TestLinkAccounts(uniitest.TestCase): 
    """Test API calls for link accounts.""" 

    def setUp(self): 
        """Set up elements before every test."""
        self.app = app.test_client()
        self.app.testing = True 
    
    def test_link_bank_accounts_200(self):
        """POST new linked bank account."""

        user_id = user_id 

        type_ = 'ACH-US'
        bank_id = '123456666'
        bank_pw= '1234453333'
        bank_name = 'Bank of America' # change these values 

        results = self.app.post(f'/v1/users/{user_id}/links', 
                                data={'type': tupe_, 
                                      'bank_id': nickname,
                                      'bank_pw': account_num,
                                      'bank_name': routing_num,
                                      })
        
        self.assertEqual(results.status_code, 200)

    def test_view_bank_account_200(self): 
        """GET linked bank account."""
        user_id = '122345'
        node_id = '12344' # change these 

        results = self.app.get(f'/v1/users/{user_id}/links/{node_id}')
        self.assertEqual(results.status_code, 200)
    
    def test_new_transaction_200(self):
        """POST transaction to linked bank account."""

        to_type = request.json["to_type"]
        to_id = request.json["to_id"]
        amount = request.json["amount"]
        amount_currency = request.json["currency"]
        ip = request.json["ip"]     # change these value 

        results = self.app.post(f'/v1/users/{user_id}/links/{node_id}/trans',
                                data={to_type...... })
        self.assertEqual(results.status_code, 200)


class TestSpendingAccount(uniitest.TestCase):
    """Test API calls for spending accounts.""" 

    def setUp(self): 
        """Set up elements before every test."""

        self.app = app.test_client()
        self.app.testing = True 

    def test_open_spending_account_200(self): 
        """POST new spending account.""" 

        type_ = "DEPOSIT-US"
        nickname = "my spending account"

        results = self.app.post(f'/v1/users/{user_id}/spending',
                                data={"type": type_, 
                                      "nickname": nickname})
        self.assertEqual(results.status_code, 200)

    def test_view_spending_account_200(self): 
        """GET spending account.""" 
        
        user_id = '12334556'
        node_id = '12344556'
        results = self.app.get(f'/v1/users/{user_id}/spending/{node_id}')
        self.assertEqual(results.status_code, 200)


    def test_spending_account_transaction_200(self):
        """POST changes to spending account, fund or withdraw."""  

        user_id = '123445'
        node_id = '123445566'

        to_type = request.json['type']
        to_id = request.json["id"]
        amount = reuqest.json["amount"]
        amount_currency = request.json["currency"]
        ip = request.json["ip"]
        note = request.json["note"]

        results = self.app.post(f'/v1/users/{user_id}/spending/{node_id}/trans',
                                data={})
        self.assertEqual(results.status_code, 200)


class TestSavingsAccount(uniitest.TestCase):
    """Test API calls for spending accounts.""" 

    def setUp(self): 
        """Set up elements before every test."""
        
        self.app = app.test_client()
        self.app.testing = True 

    def test_open_savings_account_200(self): 
        """POST new spending account."""
        
        type_ = "DEPOSIT-US"
        nickname = "my savings account"

        results = self.app.post(f'/v1/users/{user_id}/savings',
                                data={})
        self.assertEqual(results.status_code, 200)
    
    def test_view_savings_account_200(self): 
        """GET spending account.""" 
        
        user_id = '12334556'
        node_id = '123345566'
        results = self.app.get(f'/v1/users/{user_id}/savings/{node_id}')
        self.assertEqual(results.status_code, 200)
    
    def test_savings_account_transaction_200(self):
        """POST changes to spending account, fund or withdraw."""
        
        user_id = '123445'
        node_id = '123445566'

        to_type = request.json['type']
        to_id = request.json["id"]
        amount = reuqest.json["amount"]
        amount_currency = request.json["currency"]
        ip = request.json["ip"]
        note = request.json["note"]   # change these 

        results = self.app.post(f'/v1/users/{user_id}/savings/{node_id}/trans',
                                data={})
        self.assertEqual(results.status_code, 200) 


class TestNewCard(unittest.TestCase): 
    """Test API calls for opening a new card""" 

    def setUp(self): 
        """Set up elements before every test."""
        self.app = app.test_client()
        self.app.testing = True 
    
    def test_create_card_number(self):
        """POST new card number."""
        
        nickname = request.json["nickname"]
        account_class = request.json["account_class"]
 
    def test_update_card_status(self):
        """PUT card status."""

        user_id = '1234566' 
        node_id =  '1234456'
        card_id = '123345'

        status = request.json["status"]
        allow_foreign_transactions = request.json["allow_foreign_transactions"]
        daily_atm_withdrawal = request.json["daily_atm_withdrawal"]
        daily_transaction_limit = request.json["daily_transaction_limit"]

        results = self.app.put(f'/v1/users/{user_id}/spending/{node_id}/cards/<{card_id}')
        self.assertEqual(results.status_code, 200) 


    def test_update_card_pin(self);
        """Update user card pin.""" 
        
        user_id = 
        node_id = 

        card_pin = request.json["card_pin"] 

        results = self.app.patch(f'/v1/users/{user_id}/spending/{node_id}/cards/<{card_id}')
        self.assertEqual(results.status_code, 200) 

    def test_view_user_card(self):
        """GET user card."""
        
        user_id = '12334556'
        results = self.app.get(f'/v1/users/{user_id}/spending/{node_id}/cards/{card_id}')
        self.assertEqual(results.status_code, 200)

    def test_send_user_card(self):
        """POST a new card status to send card."""
        
        fee_node_id = request.json["fee_node_id"]
        expedite = request.json["expedite"]
        card_style_id = request.json["card_style_id"]
        cardholder_name = request.json["cardholder_name"]

        results = self.app.post(f'/v1/users/{user_id}/spending/{node_id}/cards/{card_id}/send')
        self.assertEqual(results.status_code, 200)

    def test_delete_card(self): 
        """DELETE user card."""
        
        status = request.json["status"]
        results = self.app.post(f'/v1/users/{user_id}/spending/{node_id}/cards/{card_id}/send')
        self.assertEqual(results.status_code, 200)


class TestTransactions(unittest.TestCase): 
    """Test API calls for opening a new card""" 

    def setUp(self): 
        """Set up elements before every test."""

        self.app = app.test_client()
        self.app.testing = True 

    def test_view_user_transactions_200(self): 
        """GET all transactions for a user."""
       
        user_id = '12334556'

        results = self.app.get(f'/v1/users/{user_id}/trans')
        self.assertEqual(results.status_code, 200)
    
    def test_view_account_transactions_200(self):
        """GET all transactions for an account."""
        
        user_id = '12334556'
        node_id = '123445667'

        results = self.app.get(f'/v1/users/{user_id}/nodes/{node_id}/trans')
        self.assertEqual(results.status_code, 200)
    

if __name__ == '__main__':
    unittest.main()

