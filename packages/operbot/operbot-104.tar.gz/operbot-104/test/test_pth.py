# This file is placed in the Public Domain.


import unittest


from op import fntime


FN = "op.hdl.Event/c13c5369-8ada-44a9-80b3-4641986f09df/2022-04-11/22:40:31.259218"


class TestPath(unittest.TestCase):

    def test_path(self):
        fnt = fntime(FN)
        self.assertEqual(fnt, 1649709631.259218)
