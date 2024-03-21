import unittest
from renops.scheduler import Scheduler


class SchedulerTests(unittest.TestCase):
    def setUp(self):
        # Create a Scheduler instance with sample parameters
        self.scheduler = Scheduler(
            deadline=24,
            runtime=8,
            location="Kranj",
            action=lambda: print("Executing action"),
            verbose=True,
            optimise_price=False,
            argument=(1, 2, 3),
            kwargs={"key": "value"}
        )
        self.data = self.scheduler.get_data()

    def test_get_data(self):
        # Test the get_data method
        self.assertFalse(self.data.isna().any().any())

    def test_preprocess_data(self):
        # Test the _preprocess_data method
        preprocessed_data = self.scheduler._preprocess_data(self.data)
        self.assertIsNotNone(preprocessed_data)
        # Add more assertions based on the expected behavior of the method


if __name__ == '__main__':
    unittest.main()
