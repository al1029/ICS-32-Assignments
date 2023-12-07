import unittest
import jumpgame
class Jump_Game_Test(unittest.TestCase):

    def test_happy_case(self):
        #checks a case that would be True
        happy_case = [2, 0, 1, 3, 0, 1]
        self.assertEquals(jumpgame.jumpgame(happy_case), True)

    def test_failed_test_case(self):
        #checks a case that would be False
        failed_test = [1, 3, 0, 0, 0, 1]
        self.assertEquals(jumpgame.jumpgame(failed_test), False)

if __name__ ==  "__main__":
    unittest.main()