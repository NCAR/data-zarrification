# netcdf-to-zarr-experiment
Large-scale netCDF→ zarr conversion

## Case 1: case-b.e11.B20TRC5CNBDRD 
- [Script](scripts/case-b.e11.B20TRC5CNBDRD.py)
-  Throughput data

**Dask configuration**
- 1 worker
- 72 threads per worker 


| Data size in (GB) | Chunk size          | Transfer time (s)  | Throughput (Mb/s) |
|-------------------|---------------------|--------------------|-------------------|
| 5.1               | (1, 1032, 289, 288) | 285.2              | 146               |
| 5.1               | (1, 516, 289, 288)  | 309.3              | 135               |
| 5.1               | (1, 258, 289, 288)  | 350.7              | 119               |
| 5.1               | (1, 129, 289, 288)  | 439.0              | 95                |

**Dask configuration**
- 2 workers on the same machine
- 72 threads per worker

| Data size in (GB) | Chunk size          | Transfer time (s)  | Throughput (Mb/s) |
|-------------------|---------------------|--------------------|-------------------|
| 5.1               | (1, 1032, 289, 288) | 16                 | 2611              |
| 5.1               | (1, 516, 289, 288)  | 18                 | 2321              |
| 5.1               | (1, 258, 289, 288)  | 28                 | 1492              |
| 5.1               | (1, 129, 289, 288)  | 47                 | 889               |
