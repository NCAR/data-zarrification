# netcdf-to-zarr-experiment
Large-scale netCDF→ zarr conversion

## Case 1: case-b.e11.B20TRC5CNBDRD 
- [Script](scripts/case-b.e11.B20TRC5CNBDRD.py)
-  Throughput data

**Dask configuration**
- 1 worker
- 72 threads per worker 


| Data size in (GB) | Chunk size          | Transfer time (s)  | Throughput (MB/s) |
|-------------------|---------------------|--------------------|-------------------|
| 5.1               | (1, 1032, 289, 288) | 285.2              | 18.25             |
| 5.1               | (1, 516, 289, 288)  | 309.3              | 16.87               |
| 5.1               | (1, 258, 289, 288)  | 350.7              | 14.87               |
| 5.1               | (1, 129, 289, 288)  | 439.0              | 12                |

**Dask configuration**
- 2 workers on the same machine
- 72 threads per worker

| Data size in (GB) | Chunk size          | Transfer time (s)  | Throughput (MB/s) |
|-------------------|---------------------|--------------------|-------------------|
| 5.1               | (1, 1032, 289, 288) | 16                 | 326.4             |
| 5.1               | (1, 516, 289, 288)  | 18                 | 290              |
| 5.1               | (1, 258, 289, 288)  | 28                 | 186.5             |
| 5.1               | (1, 129, 289, 288)  | 47                 | 111               |
