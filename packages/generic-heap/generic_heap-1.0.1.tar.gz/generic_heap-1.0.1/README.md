
Heap

	Heap data structure,Gives a feel like using priority queue in Java and C++.
	crete instance Heap(List,Key) Key can be any lambda or other function
	
	Eg:-
		do not mix datatypes other wise error may happen
		other wise customize the func to handle multipel datatypes

		def func(x):
			customize the function as you wish and return 

		l =[el1,el2,.......,eln]
	
		Initialization
		heap = Heap(l,key = lambda x: func(x)) <- user negative return value to implement max_hap , by default min_heap
	
		Eg:-
			heap = Heap(l,key = lambda x: func(x)) <- min heap
			heap = Heap(l,key = lambda x: -func(x)) <- max heap
	
			heap.show() <- it shows the entire heap

			heap.size() <- returns the size of the heap(no of element it contains)	

			heap.push(x) <- enter an element
	
			heap.pop() <- removes and returns the top most element

			heap.peek() <- returns the top element without removing it

			heap.empty() <- returns whether heap is empty or not
	
Installation

	copy from PyPi and paste to cmd and enter

How to use it?

	Import it in python script and use by creating Heap class Instance
	from generic_heap import Heap 

License

	Copyright 2021 Pritam Sarkar

This repository is licensed under the MIT license. See LICENSE for details.
