# TopN
Given an arbitrary large file (e.g. 200GB) where each row contains a number; identify the top N largest numbers.

One of the conceptually simplest approaches to the problem is to sort the data and retrieve the top N values.
```
$ sort -n big-file-100M.txt | head -n 10
```
This works for smaller data sets but has a complexity and O(n log n) so starts to hurt as we increase the size of the dataset.

Alternatively we can recognise that since we're only interested in the top N values we don't need to sort the entire dataset. Instead we can scan the data once keeping track of the top N values. Even better - if we leverage an ordered heap (aka priority queue) to track the top N values we only really have to check, for each scanned row, whether it's larger than the smallest value in the heap - an O(1) operation. Keeping the heap ordered incurs some additional complexity at O(k log k) but assuming N is much smaller tha the data to ne scanned that's much more attractive than before. So overall - checking the smallest value is O(1), scanning the file is O(n) and maintaing the heap is O(k log k) so the end result is approximatly O(n + k log k).

In reality, while the complexity of our approach is important so is the size of the data and processing required for a fast, predictable and reliable solution.

The associated code demonstrates a simple heap based approach (to reduce complexity) combined with a simple map reduce pattern to allow for scale up to multiple CPU or nodes. It's not the fastest approach (at 100M records it matches the sort based approach above) but it allows for horizontal scalability by running and larger machine with more CPUS and mappers or across an existing hadoop, EMR or Dataproc cluster.

The initial code drop has been tested on OS X 10.10.5. It has been manualluy tested in inline (no parallel processing) and local (process per mapper) modes. It has not been tested against external runtimes. As such it should currently considered a prototype.

### Getting the Code
Download from https://github.com/peerside/TopN

### Dependecies
* [python 3](https://www.python.org/downloads/mac-osx/)
* [MrJob](https://github.com/Yelp/mrjob)


### How to Install on Mac OSX
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

Run some manual tests (should print out produce top 10 values)
```
$ cd TopN
$ python TopN.py data/data-1M.txt --jobconf mapreduce.job.reduces=1 --jobconf mapreduce.job.maps=5
$ python TopN.py data/data-1M.txt -r local --jobconf mapreduce.job.reduces=1 --jobconf mapreduce.job.maps=5
$
```

To test with larger datasets generate test data with seq and shuggle with gshuf and increase the number of map jobs accordingly 
```
$ seq -f%.0f 0 100000000 | gshuf > data/data-100M.txt
$ python TopN.py data/data-10M.txt -r local --jobconf mapreduce.job.reduces=1 --jobconf mapreduce.job.maps=10
```

If you don't have gshuf you can get it from coreutils
```
$ brew install coreutils
```

