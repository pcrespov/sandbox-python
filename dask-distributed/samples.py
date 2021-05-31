
# %%
# https://distributed.readthedocs.io/en/latest/

from dask.base import visualize

def inc(i):
    return i + 1

def add(a, b):
    return a + b

x = 1
y = inc(x)
z = add(y, 10)

dsk = {'x': 1,
     'y': (inc, 'x'),
     'z': (add, 'y', 10)}

visualize(dsk , filename="dsk", format="svg", verbose=True)


# %%
# # https://docs.dask.org/en/latest/custom-graphs.html#custom-graphs

def load(filename):
    ...

def clean(data):
    ...

def analyze(sequence_of_data):
    ...

def store(result):
    with open(..., 'w') as f:
        f.write(result)

dsk = {'load-1': (load, 'myfile.a.data'),
       'load-2': (load, 'myfile.b.data'),
       'load-3': (load, 'myfile.c.data'),
       'clean-1': (clean, 'load-1'),
       'clean-2': (clean, 'load-2'),
       'clean-3': (clean, 'load-3'),
       'analyze': (analyze, ['clean-%d' % i for i in [1, 2, 3]]),
       'store': (store, 'analyze')}
visualize(dsk , filename="dsk", format="svg", verbose=True)

#from dask.multiprocessing import get
#get(dsk, 'store')  # executes in parallel


# %%
