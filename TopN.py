from mrjob.job import MRJob
from mrjob.step import MRStep
import heapq


# Number of top items to capture
TopN = 10


#
# By default mrjob executes mapper_init, mapper, mapper_final, reducer_init, 
# reducer and reducer_final
#
# Run with:
#  python ./TopN.py  --jobconf mapreduce.job.reduces=1 --jobconf mapreduce.job.maps=10 data_small.txt
#
# For larger datasets run with more mappers. e.g. For 100M rows use 100 mappers etc.
#
 
class MRTopN(MRJob):

	# Initialise each mapper with a top_n_heap
	def mapper_init(self):
		self.top_n_heap = [0]


	# Use the mapper to scan all values and add each to a bounded heap if larger 
	# than the smallest heap value
	def mapper(self, _, line):
		
		value = int(line)
				
		# If value is larger than smallest heap element then add to heap	
		if value > self.top_n_heap[0] or len(self.top_n_heap) < TopN:
			# If the heap is full, remove the smallest element on the heap.
			if len(self.top_n_heap) == TopN: 
				heapq.heappop(self.top_n_heap)
		
			# add the current element
			heapq.heappush(self.top_n_heap,value)

	
	# Yield the top_n_heap contents when a partition has been processed	
	def mapper_final(self):
		#print("Mapper yeld: ", self.top_n_heap) 
		for key in self.top_n_heap:
			yield key, 1

	# Initialize each reducer with a top_n_heap
	def reducer_init(self):
		self.top_n_heap = [0]
		
	# Use the reducer to scan the mapper results and like before - add to a 
	# bounded heap if larger than the heaps smalled value
	def reducer(self, word, counts):
		value = int(word)	
		if value > self.top_n_heap[0] or len(self.top_n_heap) < TopN:
			# If the heap is full, remove the smallest element on the heap.
			if len(self.top_n_heap) == TopN:
				heapq.heappop(self.top_n_heap)
			# add the current element as the new smallest.
			heapq.heappush(self.top_n_heap,value)

		
	# When the reducer has completed yield the top_n_heap contents
	def reducer_final(self):
		#print("Reducer yeld: ", self.top_n_heap) 
		for v in self.top_n_heap:
			yield v, 1
	
	
		
if __name__ == '__main__':
    MRTopN.run()