# TopN
Given an arbitrary large file (e.g. 200GB) where each row contains a number; identify the top N largest numbers.

### To Sort or Not to Sort ?
One of the conceptually simplest approaches to the problem is to sort the data and retrieve the top N values.
```
$ sort -n big-file-100M.txt | head -n 10 )
```
This works for smaller data sets but has a complexity and O(n log n) so starts to hurt as we increase the size of the dataset.

Alternatively we can recognise that since we're only interested in the top N values we don't need to sort the entire dataset. Instead we can scan the data once keeping track of the top N values. Even better - if we leverage an ordered heap (aka priority queue) to track the top N values we only really have to check, for each scanned row, whether it's larger than the smallest value in the heap - an O(1) operation. Keeping the heap ordered incurs some additional complexity at O(k log k) but assuming N is much smaller tha the data to ne scanned that's much more attractive than before. So overall - checking the smallest value is O(1), scanning the file is O(n) and maintaing the heap is O(k log k) so the end result is approximatly O(n + k log k).

In reality, while the complexity of our approach is important so is the size of the data and processing required for a fast, predictable and reliable solution.

The associated code demonstrates a simple heap based approach (to reduce complexity) and a basic map reduce pattern to allow for scalability. 

The initial code drop has been tested on OS X 10.10.5. It is not particularly the fastest solution and should be considered a first pass ripe for optization ! It is lacking in tests and doesn't yet support the sbmisson of jobs to AWS EMR, Hadoop or Google Dataproc. As such it should be considered a prototype vs production code.


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

