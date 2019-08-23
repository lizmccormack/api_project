import unittest 
from api import app 


class TestUser(unittest.TestCase): 
    """Test API calls for User."""
    
    def setUp(self): 
        """Set up elements before every test."""
        pass 
    
    def tearDown(self):
        """Do at the end of every test."""
        pass 
    
    def test_create_user_200(self):
        """POST new user to test_db."""
        pass 
    
    def test_get_all_users_200(self):
        """GET all users."""
        pass 
    
    def test_get_one_user_200(self):
        """GET one user."""
        pass
    
    def test_update_user_200(self):
        """PUT/PATCH user."""
        pass 
    
    def test_delete_user_200(self):
        """DELETE user."""
        pass 
    

class LinkBankAccounts(unittest.TestCase): 
    """Test API call for linking bank accounts."""
    def setUp(self):
        """Set up elements before every test."""
        pass 
    
    def TearDown(self):
        """Do at the end of every test."""
        pass 
    


class SpendingAccount(unittest.TestCase): 
    """Test API call for creating/managing a direct deposit account."""
    def setUp(self): 
        """Set up elements before every test."""
        pass 
        
    def tearDown(self):
        """Do at the end of every test."""
        pass 


class SavingsAccount(unittest.TestCase): 
    """Test API calls for creating/managing a interest bearing account.""" 
    def setUp(self): 
        """Set up elements before every test."""
        pass 
        
    def tearDown(self):
        """Do at the end of every test."""
        pass 
    
class NewCard(unittest.TestCase): 
    """Test API calls for getting an managing an new card."""
    def setUp(self): 
        """Set up elements before every test."""
        pass 
        
    def tearDown(self):
        """Do at the end of every test."""
        pass 
    
class Transactions(unittest.TestCase): 
    """Test API calls for user/account transactions."""
    def setUp(self): 
        """Set up elements before every test."""
        pass 
        
    def tearDown(self):
        """Do at the end of every test."""
        pass 