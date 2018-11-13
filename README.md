# netcdf-to-zarr-experiment
Large-scale netCDF→ zarr conversion

## Case 1: case-b.e11.B20TRC5CNBDRD 
- [Script](scripts/case-b.e11.B20TRC5CNBDRD.py)
-  Throughput data

| Data size in (GB) | Chunk size          | Transfer time (s)  | Throughput (Mb/s) |
|-------------------|---------------------|--------------------|-------------------|
| 5.1               | (1, 1032, 289, 288) | 285.2              | 146               |
| 5.1               | (1, 516, 289, 288)  | 309.3              | 135               |
| 5.1               | (1, 258, 289, 288)  | 350.7              | 119               |
| 5.1               | (1, 129, 289, 288)  | 439.0              | 95                |
