import unittest
from hlt import Location
from action import Action
from middle_out_bot import MiddleOutBot


class MiddleOutBotTest(unittest.TestCase):

    def setUp(self):
        # init bot
        bot_id = 1
        self.bot = MiddleOutBot(bot_id)

        # make helper vars
        self.loc1 = Location(0, 0)
        self.loc2 = Location(0, 0)
        self.loc3 = Location(1, 1)
        # arbitrary
        self.direction = 1
        self.action1 = (Action(self.loc1, self.loc3, self.direction))
        self.action2 = (Action(self.loc2, self.loc3, self.direction))
        self.action3 = (Action(self.loc3, self.loc1, self.direction))
        self.action4 = (Action(self.loc3, self.loc2, self.direction))

    def test_store_new_action(self):
        self.assertEqual(len(self.bot.last_actions), 0)
        self.bot.store_action(self.action1)
        self.assertEqual(len(self.bot.last_actions), 1)

    def test_store_old_action(self):
        self.assertEqual(len(self.bot.last_actions), 0)
        self.bot.store_action(self.action1)
        self.bot.store_action(self.action1)
        self.assertEqual(len(self.bot.last_actions), 1)


if __name__ == '__main__':
    unittest.main()
