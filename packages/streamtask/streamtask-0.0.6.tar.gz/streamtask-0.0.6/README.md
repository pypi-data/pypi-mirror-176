# Streamtask
**Streamtask** is a lightweight python parallel framework for parallelizing the computationally intensive pipelines. It is similar to Map/Reduce, while it is more lightweight. It parallelizes each module in the pipeline with a given processing number to make it possible to leverage the different speeds in different modules. It improves the performance especially there are some heavy I/O operations in the pipeline.

### Example
Suppose we want to process the data in a pipline with 3 blocks, f1, f2 and f3. We can use the following code to  parallelize the processing.

``` python
from streamtask import StreamTask
def f1():
    for i in range(1000000):
        yield i * 2

def f2(n, add, third = 0.01):
    return n + add + third

def f3(n):
    return n + 1

if __name__ == "__main__":
    sl = StreamTask()
    sl.add_module(f1, 2) # use 2 process to compute
    sl.add_module(f2, 2, args = [0.5], third = 0.02)
    sl.add_module(f3, 2)
    #sl.run_serial()
    sl.run()
    sl.join()
    print(sl.get_results())
```
