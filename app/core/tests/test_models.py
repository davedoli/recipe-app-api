"""
Test for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
    def test_new_user_without_email_raises_error(self):
        #This test is expecting a exception to be raised. This is why we use assertRaises and have a context manager. In this case, __enter__ returns self as a reference to the instance
        #But that reference doesn't get passed to the with block.
        #The __exit__ function recieves the exception that was raised in the with block just as we expect.
        #in the __exit__ function checks to see if the exception was a ValueError.
        #if it was, it returns True.(the test passes) if it wasn't, it returns False.(the test fails)



        """Test that creating a user without an email raises a ValueError."""
        #with self.assertRaises(ValueError) tests that that specific error is raised

        #assertRasies returns an object that can be used as a context manager

        with self.assertRaises(ValueError):
            #with asserRaise is designed around the expectation that the exception will be raised within the with block. Below we expect get_user_model() to raise a ValueError. because
            #we are not providing an email, we are expecting it to raise a ValueError. the assertRaise function has an empty __enter__ function

            #The once the ValueError is raised, the with block exits and the __exit__ function in the context manager gets called. 
            get_user_model().objects.create_user('', 'test123')


            #the ValueError is passed to the __exit__ function in the context manager. 
            #the __exit__ function in the context manager checks to see if the exception was a ValueError.
            #if it was, it returns True. if it wasn't, it returns False.
            #if the __exit__ function returns True, the test passes. if it returns False, the test fails.