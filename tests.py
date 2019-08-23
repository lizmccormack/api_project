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