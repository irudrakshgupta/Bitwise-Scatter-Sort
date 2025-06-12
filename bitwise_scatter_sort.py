from typing import List, Optional
import numpy as np

def bitwise_scatter_sort(arr: List[int], threshold: int = 32) -> List[int]:
    """
    Sort a list of non-negative integers using bitwise scatter sort algorithm.
    
    Args:
        arr: List of non-negative integers to sort
        threshold: Minimum partition size before falling back to built-in sort
        
    Returns:
        Sorted list of integers
    
    Raises:
        ValueError: If any number in the array is negative
    """
    if not arr:
        return arr
    
    # Validate input
    if any(x < 0 for x in arr):
        raise ValueError("Bitwise scatter sort only works with non-negative integers")
    
    # Convert to numpy array for faster bit operations
    nums = np.array(arr, dtype=np.uint32)
    
    def _scatter_sort_recursive(numbers: np.ndarray, bit_pos: int = 31) -> np.ndarray:
        """Recursive implementation of bitwise scatter sort."""
        # Base cases
        if len(numbers) <= threshold or bit_pos < 0:
            return np.sort(numbers)
        
        if len(numbers) == 1:
            return numbers
            
        # Extract the bit at current position for all numbers
        bits = (numbers >> bit_pos) & 1
        
        # Split into two buckets based on the bit value
        bucket0 = numbers[bits == 0]
        bucket1 = numbers[bits == 1]
        
        # Recursively sort each bucket
        if len(bucket0) > 0:
            bucket0 = _scatter_sort_recursive(bucket0, bit_pos - 1)
        if len(bucket1) > 0:
            bucket1 = _scatter_sort_recursive(bucket1, bit_pos - 1)
            
        # Combine results maintaining stability
        return np.concatenate([bucket0, bucket1]) if len(bucket0) > 0 else bucket1
    
    # Start the recursive sorting process
    result = _scatter_sort_recursive(nums)
    return result.tolist()


def parallel_bitwise_scatter_sort(arr: List[int], 
                                threshold: int = 32,
                                min_parallel_size: int = 1000) -> List[int]:
    """
    Parallel implementation of bitwise scatter sort using multiprocessing.
    
    Args:
        arr: List of non-negative integers to sort
        threshold: Minimum partition size before falling back to built-in sort
        min_parallel_size: Minimum size of subarray to spawn a parallel process
        
    Returns:
        Sorted list of integers
    """
    from multiprocessing import Pool
    import math
    
    if len(arr) < min_parallel_size:
        return bitwise_scatter_sort(arr, threshold)
    
    # Validate input
    if any(x < 0 for x in arr):
        raise ValueError("Bitwise scatter sort only works with non-negative integers")
    
    # Convert to numpy array
    nums = np.array(arr, dtype=np.uint32)
    
    # Extract MSB for initial parallel partitioning
    msb = (nums >> 31) & 1
    bucket0 = nums[msb == 0]
    bucket1 = nums[msb == 1]
    
    # Create process pool
    num_processes = min(2, math.ceil(len(arr) / min_parallel_size))
    with Pool(processes=num_processes) as pool:
        # Sort buckets in parallel
        results = []
        if len(bucket0) > 0:
            results.append(pool.apply_async(bitwise_scatter_sort, (bucket0.tolist(), threshold)))
        if len(bucket1) > 0:
            results.append(pool.apply_async(bitwise_scatter_sort, (bucket1.tolist(), threshold)))
        
        # Gather results
        sorted_buckets = [result.get() for result in results]
        
    # Combine results
    return sorted_buckets[0] + sorted_buckets[1] if len(sorted_buckets) > 1 else sorted_buckets[0]


# Vectorized version using NumPy for small arrays
def vectorized_bitwise_scatter_sort(arr: List[int], max_bits: int = 32) -> List[int]:
    """
    Vectorized implementation of bitwise scatter sort for small arrays.
    This version is optimized for modern CPU architectures with SIMD support.
    
    Args:
        arr: List of non-negative integers to sort
        max_bits: Maximum number of bits to consider
        
    Returns:
        Sorted list of integers
    """
    if not arr:
        return arr
        
    # Convert to numpy array
    nums = np.array(arr, dtype=np.uint32)
    n = len(nums)
    
    # Create bit matrix
    bit_matrix = np.zeros((n, max_bits), dtype=np.uint8)
    for i in range(max_bits):
        bit_matrix[:, i] = (nums >> (max_bits - 1 - i)) & 1
    
    # Convert bit patterns to indices
    indices = np.packbits(bit_matrix).view(np.uint32)
    
    # Sort based on bit patterns
    sorted_indices = np.argsort(indices)
    return nums[sorted_indices].tolist() 