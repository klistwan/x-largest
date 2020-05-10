# Finding the x largest values
## Problem Statement
Write a program that reads file contents from `stdin` or optionally, the absolute path of a file.

The data stream is in the format `<unique record identifier><white_space><numeric value>` (e.g. `1426828028 350`).

The output should be a list of unique IDs associated with the X-largest values. X is specified by an input parameter.

The output can be in any order and the solution should accomodate very large files.

## Summary
This is my Python solution in reading `n` lines of data and producing the `x` IDs that have the largest values.

Based on the problem description that extremely large files should be taken into account, it doesn't seem feasible to read all input data into memory. As a result, my approach was to use the file object as an iterator and maintain a min-heap that is `x` elements in size. Depending on our actual time and space requirements, there are different ways of solving this problem that I explain in the Other Ideas section below.

For the first `x` elements, we simply add them directly to a list without doing any checks on values they have. Once our list is `x` elements in length, we create the min-heap by using Python's `heapify` function. For all subsequent elements, we check to see if they are larger than the minimum value in the min-heap. If they are, we pop the heap and push this new element into it.

By running `heapify` once we've built our list of X elements, this only costs us O(x) whereas if we built an empty heap and added all elements via `heappush`, this would have cost us O(x * log(x)).

## Algorithmic Complexity
With respect to space complexity, we are only storing up to X elements in our heap so it is O(x). I verified this by profiling my code using [Memory Profiler](https://pypi.org/project/memory-profiler/). I did a few separate tests with different amounts of input (e.g. 10^3, 10^4, 10^5, etc) while keeping X constant.

```bash
$ python main.py 8 30000.bin 
Filename: main.py

Line #    Mem usage    Increment   Line Contents
================================================
    20     10.8 MiB     10.8 MiB   @profile
    21                             def x_largest(lines, x):
    22     10.8 MiB      0.0 MiB   	heap = []
    23     10.8 MiB      0.0 MiB   	for line in lines:
    24     10.8 MiB      0.0 MiB   		current_record = Record(line)
    25                             		# If we haven't seen x elements yet, just add them to our list.
    26     10.8 MiB      0.0 MiB   		if len(heap) < x:
    27     10.8 MiB      0.0 MiB   			heap.append(current_record)
    28                             			# When we reach our xth element, turn it into a heap.
    29     10.8 MiB      0.0 MiB   			if len(heap) == x:
    30     10.8 MiB      0.0 MiB   				heapify(heap)
    31                             		else:
    32                             			# If our heap is already full, check if this value is larger than the heap's smallest.
    33     10.8 MiB      0.0 MiB   			if heap[0].value < current_record.value:
    34                             				# If it is, pop the smallest and push the current value.
    35     10.8 MiB      0.0 MiB   				heapreplace(heap, current_record)
    36     10.8 MiB      0.0 MiB   	return heap
```

 In all my tests, memory usage stayed constant. It was only when I changed my value for X did my memory usage change.

With respect to time complexity, I've looked at each line of my code and documented its associated time complexity. 

Though I did use Python's `.strip()` and `.split()` when converting each line to a Record, I'm assuming the goal of this challenge is moreso to focus on the data structure and algorithm used in calculating the X largest values, rather than how we parse data. I also wasn't sure if there is a guarantee on the format data comes in (e.g. are UIDs only integers, is the whitespace separate a single space). But if every millisecond of performance was important, there is room for optimization there.

```python
def x_largest(lines, x):
	heap = []
	for line in lines: # O(n) for each line.
		current_record = Record(line)
		if len(heap) < x:  # O(1) to check list length.
			heap.append(current_record)  # O(1) to append to a list.
			if len(heap) == x:  # O(1) as per above.
				heapify(heap)  # O(x) per Python docs.
		else:
			if heap[0] < current_record:  # O(1) for a comparison.
				# Worst-case, we enter here (n - x) times.
				heapreplace(heap, current_record)  # O(log(x)).
	return heap
```

The above listed runtimes are per [the official Python documentation](https://docs.python.org/3.0/library/heapq.html). So what is the total? Let's break this down into two separate parts: input lines 1 through x, and input lines x+1 through n.

The first part is simply O(x) since we iterate through x lines and run a single O(x) method `heapify`. The second part has a worst-case of O(log(x) * (n - x)). As a result, our total is O(x + (n-x) * log(x)).

## Other notes
### Paralell processing
If we have access to a multi-core CPU system, another approach can be to process the input data in parallel, so if we have `P` processes, each process will only have to iterate through `N/P` lines of data. Depending on the value of `x` relative to `N`, it may be worthwhile for each process to have its own separate heap with a final aggregation step that combines each heap to produce a single one. Alternatively, having a shared heap in some shared memory may also work. Given Python's GIL, performance testing would have to be done to determine if a more performant solution can be achived using either the `threading` or `multiprocessing` module.

Of course, the downsides include the added implementation complexity, the additional memory required if each process would maintain its own heap of length `x`, and any additional overhead.

### Order statistics
Another potentially viable approach if we have enough memory is to use an [order statistic algorithm](http://staff.ustc.edu.cn/~csli/graduate/algorithms/book6/chap10.htm) or a selection algorithm like [median of medians](https://en.wikipedia.org/wiki/Median_of_medians) to find the xth largest element in O(n) time. After, you can traverse all the elements once again to find all larger or equal to it.

## Building & Running

## Tests
