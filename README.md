# TopN
Given an arbitrary large file (e.g. 200GB) where each row contains a number; identify the top N largest numbers.

### What is this ?
The simplest approach to the problem is to sort the file and retrieve the top N values and O(n log n) complexity - i.e. we get significently slower as we iincrease the size of the dataset (e.g. $ sort -n big-file-100M.txt | head -n 10 )

Alternatively we recognise that we're only interested in the top N values. If we scan the data once keeping track of the top N values we signicently reduce the complexity of the approach. If we leverage an ordered heap (aka priority queue) to track the top N values as we scan we only really care whether each value is larger than the smallest value in the heap. Keeping track of the smallest heap value incurs some additional complexity is O(k log k), retrieving and updating the smallest value is O(1) and scanning the file is O(n) where k is the size of the heap but the end result is O(n + k log k) which is much more attractive.

In reality, while the complexity of our approach is important so is the size of the data and processing required for a fast, predictable and reliable solution.

The associated code demonstrates a simple heap based approach (to reduce complexity) and a basic map reduce pattern to allow for scalability. The mrjob framework is used for map reduce to allow local development before deploying to a local hadoop, AWS EMR or Google Dataproc system. 

The initial code runs fine locally now (Feb 27 2017) but will require additional effort (test and debugging) to deploy remotely. 

### How to Install
TopN is a python 3 project that relies on mrjob. 

On MacOS:

Install python 3
```
$ brew install python 3
```

Install mrjob
```
$ pip install mrjob
```
Download or clone this repository
```
$ git clone https://github.com/peerside/TopN.git
```

Run a simple test
```
$ cd TopN
$ python TopN.py data/data-small.txt --jobconf mapreduce.job.reduces=1 --jobconf mapreduce.job.maps=10
```

To test with larger datasets generate test data with seq and shuggle with gshuf.  
```
$ seq -f%.0f 0 10000000 | gshuf > data-10M.txt
```
If you don't have gshuf you can get it from coreutils
```
$ brew install coreutils
```

