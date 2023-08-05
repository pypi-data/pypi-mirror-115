# Simple Caching

Small project to standardize storing (key, value) data for caching purposes.

## Supported caching methods:
1. Disk
   - **NpyFS** - Numpy array export
2. Memory
   - **DictMemory** - keys are stored as dict keys and recalled from memory


## TODO:
- unit tests
- caching algorithms (LRU, trees etc.) -- should be somehow independent of caching _mechanism_ (memory, disk etc.)
- more caching mechanisms: h5py, sqlite, torch arrays (?), pickle (?)