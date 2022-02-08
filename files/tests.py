from time import sleep
from django.test import TestCase
from .models import MyUser, Link
from django.contrib.auth.models import User
from django.core.signing import TimestampSigner
from django.utils.crypto import get_random_string
from django.core.signing import BadSignature, SignatureExpired
from selenium import webdriver
from django.conf import settings


from django.urls import resolve, reverse
# Create your tests here.

class UnitTests(TestCase):
    def setUp(self):
        # user = User(username="usman3", password="usman123")
        # user.save()
        # my_user = MyUser(user=user, agent="Linux")
        pass

    def test_hello_world(self):
        hello = "hello"
        self.assertEqual(hello, "hello")

    def test_link_validity(self):
        user = User(username="usman3", password="usman123")
        user.save()
        my_user = MyUser(user=user, agent="Linux")
        my_user.save()
        password = get_random_string(10)
        my_link = "https://google.com"
        link = Link(user=my_user, password=password, link=my_link, name="test-link")
        link.save()
        url = link.get_absolute_url() 
        split_url = url.split("/")[-2]
        self.assertEqual(link.security.unsign(split_url), str(link.pk))
        sleep(6) 
        with self.assertRaises(SignatureExpired):
            link.security.unsign(split_url, 5)

        

    def tearDown(self) -> None:
        return
        
        
class FunctionalTests(TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.user = User(username="usman2", password="usman123")
        self.user.save()
        self.my_user = MyUser(user=self.user, agent="linux")
        self.my_user.save()

    def test_there_is_homepage(self):
        self.browser.get(settings.BASE_URL)
        self.assertIn('Welcome to Usman Secure!!!', self.browser.page_source)

    def test_login(self):
        self.browser.get(settings.BASE_URL)
        self.browser.find_element_by_id("login-button").click()
        username = self.browser.find_element_by_id('login-username')
        username.send_keys("usman2")
        password = self.browser.find_element_by_id('login-password')
        password.send_keys("usman123")
        self.browser.find_element_by_name("login-submit").click()
        sleep(10)
        print(self.my_user)
        self.assertEqual(self.browser.current_url, settings.BASE_URL )


    def tearDown(self) -> None:
        self.browser.close()