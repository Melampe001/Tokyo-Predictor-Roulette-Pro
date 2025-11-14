#!/usr/bin/env python3
"""
Tokyo Predictor Roulette Pro
A roulette prediction system based on pattern analysis
"""

import random
import statistics
from typing import List, Dict, Tuple
from collections import Counter


class TokyoRoulettePredictor:
    """Main predictor class for roulette number prediction"""
    
    def __init__(self):
        self.history: List[int] = []
        self.max_history = 100
        
    def add_result(self, number: int) -> None:
        """
        Add a roulette result to history
        
        Args:
            number: Roulette number (0-36)
            
        Raises:
            ValueError: If number is not in valid range
        """
        if not isinstance(number, int) or number < 0 or number > 36:
            raise ValueError("Roulette number must be an integer between 0 and 36")
        
        self.history.append(number)
        
        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def predict_next(self, count: int = 5) -> List[int]:
        """
        Predict next most likely numbers based on pattern analysis
        
        Args:
            count: Number of predictions to return
            
        Returns:
            List of predicted numbers sorted by likelihood
        """
        if len(self.history) < 10:
            # Not enough data, return random predictions
            return random.sample(range(0, 37), min(count, 37))
        
        # Analyze patterns
        predictions = self._analyze_patterns()
        
        # Return top predictions
        return predictions[:count]
    
    def _analyze_patterns(self) -> List[int]:
        """
        Analyze historical patterns to predict next numbers
        
        Returns:
            List of numbers sorted by prediction score
        """
        scores: Dict[int, float] = {i: 0.0 for i in range(37)}
        
        # Frequency analysis
        if len(self.history) >= 10:
            frequency = Counter(self.history[-30:])
            for num, freq in frequency.items():
                scores[num] += freq * 2
        
        # Hot numbers (appeared recently)
        if len(self.history) >= 5:
            recent = self.history[-10:]
            for num in set(recent):
                scores[num] += 3
        
        # Cold numbers (haven't appeared in a while)
        if len(self.history) >= 20:
            recent_20 = set(self.history[-20:])
            all_numbers = set(range(37))
            cold_numbers = all_numbers - recent_20
            for num in cold_numbers:
                scores[num] += 1.5
        
        # Pattern analysis: numbers that follow the last number
        if len(self.history) >= 15:
            last_num = self.history[-1]
            followers = []
            for i in range(len(self.history) - 1):
                if self.history[i] == last_num:
                    followers.append(self.history[i + 1])
            
            if followers:
                follower_counts = Counter(followers)
                for num, count in follower_counts.items():
                    scores[num] += count * 2.5
        
        # Sort by score
        sorted_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [num for num, score in sorted_numbers]
    
    def get_statistics(self) -> Dict:
        """
        Get statistical analysis of current history
        
        Returns:
            Dictionary containing various statistics
        """
        if not self.history:
            return {
                "total_spins": 0,
                "most_common": [],
                "least_common": [],
                "average": 0,
                "red_count": 0,
                "black_count": 0,
                "green_count": 0
            }
        
        counter = Counter(self.history)
        most_common = counter.most_common(5)
        least_common = counter.most_common()[-5:] if len(counter) >= 5 else counter.most_common()
        
        # Roulette color mapping (European roulette)
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
        
        red_count = sum(1 for num in self.history if num in red_numbers)
        black_count = sum(1 for num in self.history if num in black_numbers)
        green_count = sum(1 for num in self.history if num == 0)
        
        return {
            "total_spins": len(self.history),
            "most_common": most_common,
            "least_common": least_common,
            "average": round(statistics.mean(self.history), 2),
            "red_count": red_count,
            "black_count": black_count,
            "green_count": green_count
        }
    
    def check_system(self) -> bool:
        """
        Check if the predictor system is working correctly
        
        Returns:
            True if system is operational, False otherwise
        """
        try:
            # Test adding results
            test_predictor = TokyoRoulettePredictor()
            test_numbers = [12, 24, 36, 5, 17, 0, 23, 14, 31, 9]
            
            for num in test_numbers:
                test_predictor.add_result(num)
            
            # Test predictions
            predictions = test_predictor.predict_next(5)
            if not predictions or len(predictions) != 5:
                return False
            
            # Test statistics
            stats = test_predictor.get_statistics()
            if stats["total_spins"] != len(test_numbers):
                return False
            
            # Test validation
            try:
                test_predictor.add_result(50)  # Invalid number
                return False  # Should have raised ValueError
            except ValueError:
                pass  # Expected
            
            return True
            
        except Exception as e:
            print(f"System check failed: {e}")
            return False


def main():
    """Main function to demonstrate the predictor"""
    print("=" * 60)
    print("TOKYO PREDICTOR ROULETTE PRO")
    print("=" * 60)
    print()
    
    predictor = TokyoRoulettePredictor()
    
    # System check
    print("🔧 Running system check...")
    if predictor.check_system():
        print("✅ System check PASSED - All functions working correctly!")
    else:
        print("❌ System check FAILED - Please check the system")
        return
    
    print()
    print("-" * 60)
    print("Demo Mode: Adding sample roulette results...")
    print("-" * 60)
    
    # Simulate some roulette spins
    sample_results = [
        17, 23, 5, 0, 14, 36, 12, 29, 8, 25,
        11, 30, 3, 19, 22, 7, 33, 15, 28, 1,
        34, 6, 27, 13, 31, 9, 20, 2, 24, 18
    ]
    
    print(f"Adding {len(sample_results)} historical results...")
    for num in sample_results:
        predictor.add_result(num)
    print(f"✅ Added {len(sample_results)} results to history")
    
    print()
    print("-" * 60)
    print("📊 Statistical Analysis")
    print("-" * 60)
    
    stats = predictor.get_statistics()
    print(f"Total spins analyzed: {stats['total_spins']}")
    print(f"Average number: {stats['average']}")
    print(f"Red count: {stats['red_count']}")
    print(f"Black count: {stats['black_count']}")
    print(f"Green (0) count: {stats['green_count']}")
    print()
    print("Most common numbers:")
    for num, count in stats['most_common']:
        print(f"  Number {num}: appeared {count} times")
    
    print()
    print("-" * 60)
    print("🎯 PREDICTIONS")
    print("-" * 60)
    
    predictions = predictor.predict_next(5)
    print("Top 5 predicted numbers for next spin:")
    for i, num in enumerate(predictions, 1):
        print(f"  {i}. Number {num}")
    
    print()
    print("=" * 60)
    print("✅ Tokyo Predictor Roulette Pro is working correctly!")
    print("=" * 60)


if __name__ == "__main__":
    main()
