import unittest 
import os 

from api import app 
from bson.objectid import ObjectId
from json import dumps 

from pymongo import MongoClient 
from flask import (Flask, jsonify, request)


USER_ID = '5d7469c87da8972d7d7d343d'
NODE_ID_AHS = '5ade26b4567a900029e2afd2'
NODE_ID_SPENDING = '5ade26b4567a900029e2afd2'
NODE_ID_SAVINGS = '5ade26b4567a900029e2afd2'
# CARD_ID = 

class TestUser(unittest.TestCase): 
    """Test API calls for user."""

    def setUp(self): 
        """Set up elements before every test."""

        self.app = app.test_client()
        app.config['TESTING'] = True 
    
    def test_create_user_200(self): 
        """POST new user."""
        
        headers = {'Content-Type': 'application/json'}
        email = "test@apitests.com"
        phone_numbers = "1234567890"
        legal_names = "Test User"
    
        results = self.app.post('/v1/users', 
                                data={"email": email, 
                                      "phone_numbers": phone_numbers,
                                      "legal_names": legal_names}, 
                                headers=headers)
        
        self.assertEqual(results.status_code, 200)
    
    def test_get_all_users_200(self): 
        """GET all users."""

        results = self.app.get('/v1/users')
        self.assertEqual(results.status_code, 200)


    def test_get_one_user_200(self): 
        """GET one user.""" 

        user_id = USER_ID
        results = self.app.get(f'/v1/users/{user_id}')
        self.assertEqual(results.status_code, 200)


class TestLinkAccounts(unittest.TestCase): 
    """Test API calls for link accounts.""" 

    def setUp(self): 
        """Set up elements before every test."""
        
        self.app = app.test_client()
        app.config['TESTING'] = True   

    def test_link_bank_accounts_200(self):
        """POST new linked bank account."""

        user_id = USER_ID
        headers = {'Content-Type': 'application/json'}

        type_ = "ACH-US"
        bank_id = "synapse_good"
        bank_pw= "test1234"
        bank_name = "fake" 

        results = self.app.post(f'/v1/users/{user_id}/links', 
                                data={'type': type_, 
                                      'bank_id': bank_id,
                                      'bank_pw': bank_pw,
                                      'bank_name': bank_name
                                      },
                                headers=headers)
        
        self.assertEqual(results.status_code, 200)

    def test_view_bank_account_200(self): 
        """GET linked bank account."""

        user_id = USER_ID
        node_id = NODE_ID_AHS 

        results = self.app.get(f'/v1/users/{user_id}/links/{node_id}')
        self.assertEqual(results.status_code, 200)
    
    def test_new_transaction_200(self):
        """POST transaction to linked bank account."""

        user_id = USER_ID
        node_id = NODE_ID_AHS
        headers = {'Content-Type': 'application/json'}

        to_type = 'ACH-US'
        to_id = 'asdfasdfsdf'
        amount = 20.5
        amount_currency = 'USD'
        ip = '192.168.0.1'    

        results = self.app.post(f'/v1/users/{user_id}/links/{node_id}/trans',
                                data={'to_type': to_type,
                                     'to_id': to_id,
                                     'amount': amount,
                                     'amount_currency': amount_currency,
                                     'ip': ip},
                                headers=headers)

        self.assertEqual(results.status_code, 200)


class TestSpendingAccount(unittest.TestCase):
    """Test API calls for spending accounts.""" 

    def setUp(self): 
        """Set up elements before every test."""

        self.app = app.test_client()
        app.config['TESTING'] = True 

    def test_open_spending_account_200(self): 
        """POST new spending account.""" 

        user_id = USER_ID
        headers = {'Content-Type': 'application/json'}

        type_ = "DEPOSIT-US"
        nickname = "my spending account"
        results = self.app.post(f'/v1/users/{user_id}/spending',
                                data={"type": type_, 
                                      "nickname": nickname},
                                headers=headers)
        self.assertEqual(results.status_code, 200)

    def test_view_spending_account_200(self): 
        """GET spending account.""" 
        
        user_id = USER_ID
        node_id = NODE_ID_SPENDING

        results = self.app.get(f'/v1/users/{user_id}/spending/{node_id}')
        self.assertEqual(results.status_code, 200)

    def test_spending_account_transaction_200(self):
        """POST changes to spending account, fund or withdraw."""  

        user_id = USER_ID
        node_id = NODE_ID_SPENDING
        headers = {'Content-Type': 'application/json'}

        to_type = 'DEPOSIT-US',
        to_id = '12334567777'
        amount = 375.21
        amount_currency = "USD"
        ip = "127.0.0.1"
        note = "Test transaction"

        results = self.app.post(f'/v1/users/{user_id}/spending/{node_id}/trans',
                                data={'type': to_type, 
                                     'id': to_id,
                                     'amount': amount, 
                                     'currency': amount_currency,
                                     'ip': ip,
                                     'note': note},
                                headers=headers)

        self.assertEqual(results.status_code, 200)


class TestSavingsAccount(unittest.TestCase):
    """Test API calls for spending accounts.""" 

    def setUp(self): 
        """Set up elements before every test."""
        
        self.app = app.test_client()
        app.config['TESTING'] = True 

    def test_open_savings_account_200(self): 
        """POST new spending account."""
        
        user_id = USER_ID
        headers = {'Content-Type': 'application/json'}

        type_ = "IB-DEPOSIT-US"
        nickname = "my savings account"

        results = self.app.post(f'/v1/users/{user_id}/savings',
                                data={'type': type_, 
                                      'nickname': nickname},
                                headers=headers)

        self.assertEqual(results.status_code, 200)
    
    def test_view_savings_account_200(self): 
        """GET spending account.""" 
        
        user_id = USER_ID
        node_id = NODE_ID_SAVINGS
        results = self.app.get(f'/v1/users/{user_id}/savings/{node_id}')
        self.assertEqual(results.status_code, 200)
    
    def test_savings_account_transaction_200(self):
        """POST changes to spending account, fund or withdraw."""
        
        user_id = USER_ID
        node_id = NODE_ID_SAVINGS
        headers = {'Content-Type': 'application/json'}

        to_type = "IB-DEPOSIT-US"
        to_id = '123445566'
        amount = 375.21
        amount_currency = "USD"
        ip = "127.0.0.1"
        note = "Test transaction" 

        results = self.app.post(f'/v1/users/{user_id}/savings/{node_id}/trans',
                                data={'type': to_type,
                                     'id': to_id, 
                                     'amount': amount,
                                     'currency': amount_currency,
                                     'ip': ip, 
                                     'note': note},
                                headers=headers)

        self.assertEqual(results.status_code, 200) 


class TestNewCard(unittest.TestCase): 
    """Test API calls for opening a new card""" 

    def setUp(self): 
        """Set up elements before every test."""
        self.app = app.test_client()
        app.config['TESTING'] = True 
    
    def test_create_card(self):
        """POST new card."""

        user_id = USER_ID
        node_id = NODE_ID_SPENDING
        card_id = CARD_ID
        headers = {'Content-Type': 'application/json'}
        
        nickname = "My debit card"
        account_class = "DEBIT_CARD"

        results = self.app.post(f'/v1/users/{user_id}/spending/{node_id}/cards',
                                data={'nickname' : nickname,
                                      'account_class' : account_class},
                                headers=headers)
 
    def test_update_card_status(self):
        """PUT card status."""

        user_id = USER_ID 
        node_id =  NODE_ID_SPENDING
        card_id = CARD_ID
        headers = {'Content-Type': 'application/json'}

        status = "ACTIVE"

        results = self.app.put(f'/v1/users/{user_id}/spending/{node_id}/cards/<{card_id}',
                               data={'status' : status},
                               headers=headers)

        self.assertEqual(results.status_code, 200) 

    def test_view_user_card(self):
        """GET user card."""
        
        user_id = USER_ID

        results = self.app.get(f'/v1/users/{user_id}/spending/{node_id}/cards/{card_id}')
        self.assertEqual(results.status_code, 200)

    def test_send_user_card(self):
        """POST a new card status to send card."""

        user_id = USER_ID
        node_id = NODE_ID_SPENDING
        card_id = CARD_ID
        headers = {'Content-Type': 'application/json'}
        
        fee_node_id = "5bba781485411800991b606b"
        expedite = False
        card_style_id = "555"
        cardholder_name = "Test User"

        results = self.app.post(f'/v1/users/{user_id}/spending/{node_id}/cards/{card_id}/send',
                                data={'fee_node_id' : fee_node_id,
                                      'expedite' : expedite,
                                      'card_style_id' : card_style_id,
                                      'cardholder_name' : cardholder_name},
                                headers=headers)

        self.assertEqual(results.status_code, 200)

    def test_delete_card(self): 
        """DELETE user card."""

        USER_ID = USER_ID 
        NODE_ID = NODE_ID_SPENDING
        headers = {'Content-Type': 'application/json'}
        
        status = "TERMINATED"
        results = self.app.post(f'/v1/users/{user_id}/spending/{node_id}/cards/{card_id}/send',
                                data={'status' : status})

        self.assertEqual(results.status_code, 200)


class TestTransactions(unittest.TestCase): 
    """Test API calls for opening a new card""" 

    def setUp(self): 
        """Set up elements before every test."""

        self.app = app.test_client()
        app.config['TESTING'] = True 

    def test_view_user_transactions_200(self): 
        """GET all transactions for a user."""
       
        user_id = USER_ID

        results = self.app.get(f'/v1/users/{user_id}/trans')
        self.assertEqual(results.status_code, 200)
    
    def test_view_account_transactions_200(self):
        """GET all transactions for an account."""
        
        user_id = USER_ID
        node_id = NODE_ID_SPENDING

        results = self.app.get(f'/v1/users/{user_id}/nodes/{node_id}/trans')
        self.assertEqual(results.status_code, 200)
    

if __name__ == '__main__':
    unittest.main()

