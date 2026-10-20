import unittest
from app import read_sources, demo_review

class TestMsMinchin(unittest.TestCase):
    def setUp(self):
        self.instructions, self.personalization, self.registry = read_sources()

    def test_explicit_skill_trigger(self):
        result = demo_review("Apply ACC to this report", "Here is my report.", self.registry)
        self.assertIn("Accuracy Control", result)

    def test_complete_revision(self):
        result = demo_review("Rewrite this memo", "Only the changed section is below.", self.registry)
        self.assertIn("Full revised deliverable", result)

    def test_no_intervention(self):
        result = demo_review("What is 2 + 2?", "4", self.registry)
        self.assertTrue(result.startswith("NO_INTERVENTION"))

if __name__ == "__main__":
    unittest.main()
