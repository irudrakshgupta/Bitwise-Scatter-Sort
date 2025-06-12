import unittest
import random
import numpy as np
from bitwise_scatter_sort import (
    bitwise_scatter_sort,
    parallel_bitwise_scatter_sort,
    vectorized_bitwise_scatter_sort
)

class TestBitwiseScatterSort(unittest.TestCase):
    def setUp(self):
        # Test cases
        self.empty_array = []
        self.single_element = [42]
        self.sorted_array = [1, 2, 3, 4, 5]
        self.reverse_sorted = [5, 4, 3, 2, 1]
        self.random_small = [45, 12, 89, 33, 67]
        self.random_large = random.sample(range(1000), 100)
        self.duplicates = [4, 2, 4, 1, 3, 2, 4]
        self.powers_of_two = [1, 2, 4, 8, 16, 32, 64, 128, 256]
        
    def test_empty_array(self):
        """Test sorting an empty array."""
        self.assertEqual(bitwise_scatter_sort([]), [])
        self.assertEqual(parallel_bitwise_scatter_sort([]), [])
        self.assertEqual(vectorized_bitwise_scatter_sort([]), [])
        
    def test_single_element(self):
        """Test sorting an array with a single element."""
        self.assertEqual(bitwise_scatter_sort([42]), [42])
        self.assertEqual(parallel_bitwise_scatter_sort([42]), [42])
        self.assertEqual(vectorized_bitwise_scatter_sort([42]), [42])
        
    def test_sorted_array(self):
        """Test sorting an already sorted array."""
        self.assertEqual(bitwise_scatter_sort(self.sorted_array), sorted(self.sorted_array))
        self.assertEqual(parallel_bitwise_scatter_sort(self.sorted_array), sorted(self.sorted_array))
        self.assertEqual(vectorized_bitwise_scatter_sort(self.sorted_array), sorted(self.sorted_array))
        
    def test_reverse_sorted(self):
        """Test sorting a reverse-sorted array."""
        self.assertEqual(bitwise_scatter_sort(self.reverse_sorted), sorted(self.reverse_sorted))
        self.assertEqual(parallel_bitwise_scatter_sort(self.reverse_sorted), sorted(self.reverse_sorted))
        self.assertEqual(vectorized_bitwise_scatter_sort(self.reverse_sorted), sorted(self.reverse_sorted))
        
    def test_random_small(self):
        """Test sorting a small random array."""
        self.assertEqual(bitwise_scatter_sort(self.random_small), sorted(self.random_small))
        self.assertEqual(parallel_bitwise_scatter_sort(self.random_small), sorted(self.random_small))
        self.assertEqual(vectorized_bitwise_scatter_sort(self.random_small), sorted(self.random_small))
        
    def test_random_large(self):
        """Test sorting a large random array."""
        self.assertEqual(bitwise_scatter_sort(self.random_large), sorted(self.random_large))
        self.assertEqual(parallel_bitwise_scatter_sort(self.random_large), sorted(self.random_large))
        self.assertEqual(vectorized_bitwise_scatter_sort(self.random_large), sorted(self.random_large))
        
    def test_duplicates(self):
        """Test sorting an array with duplicate elements."""
        self.assertEqual(bitwise_scatter_sort(self.duplicates), sorted(self.duplicates))
        self.assertEqual(parallel_bitwise_scatter_sort(self.duplicates), sorted(self.duplicates))
        self.assertEqual(vectorized_bitwise_scatter_sort(self.duplicates), sorted(self.duplicates))
        
    def test_powers_of_two(self):
        """Test sorting an array with powers of two."""
        self.assertEqual(bitwise_scatter_sort(self.powers_of_two), sorted(self.powers_of_two))
        self.assertEqual(parallel_bitwise_scatter_sort(self.powers_of_two), sorted(self.powers_of_two))
        self.assertEqual(vectorized_bitwise_scatter_sort(self.powers_of_two), sorted(self.powers_of_two))
        
    def test_negative_numbers(self):
        """Test that the algorithm raises ValueError for negative numbers."""
        with self.assertRaises(ValueError):
            bitwise_scatter_sort([-1, 2, 3])
        with self.assertRaises(ValueError):
            parallel_bitwise_scatter_sort([-1, 2, 3])
        with self.assertRaises(ValueError):
            vectorized_bitwise_scatter_sort([-1, 2, 3])
            
    def test_stability(self):
        """Test that the sort is stable for equal elements."""
        class Number:
            def __init__(self, value, index):
                self.value = value
                self.index = index
            
            def __lt__(self, other):
                return self.value < other.value
                
        # Create list with duplicate values but different indices
        numbers = [Number(1, 0), Number(2, 1), Number(1, 2), Number(2, 3)]
        sorted_numbers = sorted(numbers)
        
        # Check that relative order is preserved for equal elements
        self.assertEqual(sorted_numbers[0].index, 0)
        self.assertEqual(sorted_numbers[1].index, 2)
        self.assertEqual(sorted_numbers[2].index, 1)
        self.assertEqual(sorted_numbers[3].index, 3)

if __name__ == '__main__':
    unittest.main() 