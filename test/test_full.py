import unittest

from renops.scheduler import Scheduler


class SchedulerTestLocationOutsideEU(unittest.TestCase):
    """ Test rp on set location outside EU """
    def setUp(self):
        # Create a Scheduler instance with sample parameters
        self.scheduler = Scheduler(
            deadline=1,
            runtime=1,
            location="NY",
            action=lambda: print("Executing action"),
            verbose=True,
            optimise_type="renewable_potential",
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


class SchedulerTestAutoLocation(unittest.TestCase):
    """ Test rp on with auto location """
    def setUp(self):
        # Create a Scheduler instance with sample parameters
        self.scheduler = Scheduler(
            deadline=1,
            runtime=1,
            location="auto",
            action=lambda: print("Executing action"),
            verbose=True,
            optimise_type="renewable_potential",
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


class SchedulerTestPriceOptimisation(unittest.TestCase):
    """Test price optimisation """
    def setUp(self):
        # Create a Scheduler instance with sample parameters
        self.scheduler = Scheduler(
            deadline=1,
            runtime=1,
            location="Berlin",
            action=lambda: print("Executing action"),
            verbose=True,
            optimise_type="price",
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


class SchedulerTestCarbonEmissions(unittest.TestCase):
    """Test carbon emissions optimisation """
    def setUp(self):
        # Create a Scheduler instance with sample parameters
        self.scheduler = Scheduler(
            deadline=1,
            runtime=1,
            location="Ljubljana",
            action=lambda: print("Executing action"),
            verbose=True,
            optimise_type="carbon_emissions",
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
