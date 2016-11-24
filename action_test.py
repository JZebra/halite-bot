import unittest
from action import Action
from hlt import Location


class ActionTest(unittest.TestCase):

    def setUp(self):
        self.loc1 = Location(0, 0)
        self.loc2 = Location(0, 0)
        self.loc3 = Location(1, 1)
        # arbitrary
        self.direction = 1
        self.action1 = (Action(self.loc1, self.loc3, self.direction))
        self.action2 = (Action(self.loc2, self.loc3, self.direction))
        self.action3 = (Action(self.loc3, self.loc1, self.direction))
        self.action4 = (Action(self.loc3, self.loc2, self.direction))

    def test__eq__(self):
        self.assertEqual(self.action1, self.action2)
        self.assertEqual(self.action3, self.action4)

    def test__ne__(self):
        self.assertNotEqual(self.action1, self.action3)
        self.assertNotEqual(self.action2, self.action4)

    def test_has_end(self):
        self.assertTrue(self.action3.has_end(self.loc1))
        self.assertTrue(self.action3.has_end(self.loc2))
        self.assertFalse(self.action3.has_end(self.loc3))


if __name__ == '__main__':
    unittest.main()
