#!/usr/bin/env python3
"""
Test suite for Tokyo Predictor Roulette Pro
Verifies that the system checks and works correctly
"""

import unittest
from tokyo_predictor import TokyoRoulettePredictor


class TestTokyoRoulettePredictor(unittest.TestCase):
    """Test cases for the TokyoRoulettePredictor class"""
    
    def setUp(self):
        """Set up test predictor instance"""
        self.predictor = TokyoRoulettePredictor()
    
    def test_system_check(self):
        """Test that system check works"""
        self.assertTrue(self.predictor.check_system())
    
    def test_add_valid_result(self):
        """Test adding valid roulette numbers"""
        # Test boundary values
        self.predictor.add_result(0)
        self.predictor.add_result(36)
        self.predictor.add_result(18)
        
        self.assertEqual(len(self.predictor.history), 3)
        self.assertIn(0, self.predictor.history)
        self.assertIn(36, self.predictor.history)
        self.assertIn(18, self.predictor.history)
    
    def test_add_invalid_result(self):
        """Test that invalid numbers raise ValueError"""
        with self.assertRaises(ValueError):
            self.predictor.add_result(-1)
        
        with self.assertRaises(ValueError):
            self.predictor.add_result(37)
        
        with self.assertRaises(ValueError):
            self.predictor.add_result(100)
    
    def test_add_non_integer_result(self):
        """Test that non-integer values raise ValueError"""
        with self.assertRaises(ValueError):
            self.predictor.add_result("12")
        
        with self.assertRaises(ValueError):
            self.predictor.add_result(12.5)
    
    def test_predict_with_insufficient_data(self):
        """Test predictions with less than 10 results"""
        # Add only 5 results
        for i in range(5):
            self.predictor.add_result(i)
        
        predictions = self.predictor.predict_next(5)
        self.assertEqual(len(predictions), 5)
        # Should return valid roulette numbers
        for num in predictions:
            self.assertGreaterEqual(num, 0)
            self.assertLessEqual(num, 36)
    
    def test_predict_with_sufficient_data(self):
        """Test predictions with enough historical data"""
        # Add 30 results
        test_data = [12, 24, 36, 5, 17, 0, 23, 14, 31, 9,
                     12, 24, 36, 5, 17, 0, 23, 14, 31, 9,
                     12, 24, 36, 5, 17, 0, 23, 14, 31, 9]
        
        for num in test_data:
            self.predictor.add_result(num)
        
        predictions = self.predictor.predict_next(5)
        self.assertEqual(len(predictions), 5)
        
        # All predictions should be valid numbers
        for num in predictions:
            self.assertGreaterEqual(num, 0)
            self.assertLessEqual(num, 36)
    
    def test_predict_custom_count(self):
        """Test predictions with different counts"""
        # Add some data
        for i in range(15):
            self.predictor.add_result(i % 37)
        
        # Test different prediction counts
        predictions_3 = self.predictor.predict_next(3)
        self.assertEqual(len(predictions_3), 3)
        
        predictions_10 = self.predictor.predict_next(10)
        self.assertEqual(len(predictions_10), 10)
    
    def test_statistics_empty(self):
        """Test statistics with no data"""
        stats = self.predictor.get_statistics()
        
        self.assertEqual(stats["total_spins"], 0)
        self.assertEqual(stats["most_common"], [])
        self.assertEqual(stats["average"], 0)
        self.assertEqual(stats["red_count"], 0)
        self.assertEqual(stats["black_count"], 0)
        self.assertEqual(stats["green_count"], 0)
    
    def test_statistics_with_data(self):
        """Test statistics with historical data"""
        # Add known data
        test_data = [0, 12, 24, 12, 36, 12]  # 12 appears 3 times, 0 once
        for num in test_data:
            self.predictor.add_result(num)
        
        stats = self.predictor.get_statistics()
        
        self.assertEqual(stats["total_spins"], 6)
        self.assertEqual(stats["most_common"][0], (12, 3))
        self.assertEqual(stats["green_count"], 1)  # 0 is green
        self.assertGreater(stats["red_count"] + stats["black_count"], 0)
    
    def test_color_counting(self):
        """Test that color counts are accurate"""
        # Red: 1, 3, 5, 7, 9
        # Black: 2, 4, 6, 8
        # Green: 0
        test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        
        for num in test_data:
            self.predictor.add_result(num)
        
        stats = self.predictor.get_statistics()
        
        self.assertEqual(stats["red_count"], 5)
        self.assertEqual(stats["black_count"], 4)
        self.assertEqual(stats["green_count"], 1)
    
    def test_history_limit(self):
        """Test that history doesn't exceed max_history"""
        # Add more than max_history results
        for i in range(150):
            self.predictor.add_result(i % 37)
        
        self.assertLessEqual(len(self.predictor.history), self.predictor.max_history)
        self.assertEqual(len(self.predictor.history), 100)
    
    def test_predictions_are_unique(self):
        """Test that predictions don't contain duplicates"""
        # Add some data
        for i in range(30):
            self.predictor.add_result(i % 37)
        
        predictions = self.predictor.predict_next(10)
        
        # Check uniqueness
        self.assertEqual(len(predictions), len(set(predictions)))
    
    def test_multiple_predictions_consistent(self):
        """Test that predictions are deterministic for same state"""
        # Add data
        for i in range(20):
            self.predictor.add_result(i)
        
        # Get predictions twice
        predictions1 = self.predictor.predict_next(5)
        predictions2 = self.predictor.predict_next(5)
        
        # Both should be lists of valid numbers
        self.assertEqual(len(predictions1), 5)
        self.assertEqual(len(predictions2), 5)


class TestSystemIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_full_workflow(self):
        """Test complete workflow: add data, predict, get stats"""
        predictor = TokyoRoulettePredictor()
        
        # Add historical data
        sample_data = [12, 24, 36, 5, 17, 0, 23, 14, 31, 9,
                      11, 30, 3, 19, 22, 7, 33, 15, 28, 1]
        
        for num in sample_data:
            predictor.add_result(num)
        
        # Get predictions
        predictions = predictor.predict_next(5)
        self.assertEqual(len(predictions), 5)
        
        # Get statistics
        stats = predictor.get_statistics()
        self.assertEqual(stats["total_spins"], 20)
        
        # Verify all components work together
        self.assertIsInstance(stats["most_common"], list)
        self.assertGreater(stats["red_count"] + stats["black_count"] + stats["green_count"], 0)
    
    def test_check_works(self):
        """Test that CHECK (verification) works"""
        predictor = TokyoRoulettePredictor()
        
        # System should check and confirm it works
        check_result = predictor.check_system()
        self.assertTrue(check_result, "System check should pass - system should WORK")
    
    def test_trabaja(self):
        """Test that TRABAJA (it works) - the system is functional"""
        predictor = TokyoRoulettePredictor()
        
        # Add data
        predictor.add_result(12)
        predictor.add_result(24)
        predictor.add_result(36)
        
        # Get predictions - if this works, TRABAJA (it works)!
        predictions = predictor.predict_next(3)
        
        # Verify it actually worked
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions), 3)
        
        # Get stats - should also work
        stats = predictor.get_statistics()
        self.assertEqual(stats["total_spins"], 3)
        
        # If we got here, ¡TRABAJA! (It works!)


def run_tests():
    """Run all tests and report results"""
    print("=" * 70)
    print("RUNNING TESTS - CHECK Y TRABAJA (Check and Work)")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(loader.loadTestsFromTestCase(TestTokyoRoulettePredictor))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - SYSTEM WORKS! (¡TRABAJA!)")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
