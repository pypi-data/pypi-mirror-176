# This file is placed in the Public Domain.


import unittest


from operbot.irc import User


class TestUser(unittest.TestCase):

    def test_user(self):
        user = User()
        self.assertEqual(type(user), User)
