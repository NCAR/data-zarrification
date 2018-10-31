# netcdf-to-zarr-experiment
Large-scale netCDF→ zarr conversion


## Step 1: netCDF to Zarr conversion via `xarray`

[Case 1: Notebook](notebooks/case-b.e11.BRCP85C5CNBDRD.ipynb)
[Case 2: Notebook](notebooks/case-b.e11.B20TRC5CNBDRD.ipynb)

## Step 2: Configure awscli

Follow instructions from [awscli documentation page](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) to configure awscli. 

Once this is done, we are ready to move to the next step (transferring generated zarr dataset to AWS S3 bucket)

## Step 3: Transfer zarr dataset to S3

    $ cd /glade/scratch/abanihi/data/
  

```bash
abanihi@cheyenne2: /glade/scratch/abanihi/data $ time aws s3 cp --recursive AWS/ s3://zarr-test-bucket --quiet

real    22m5.465s
user    14m26.092s
sys     1m46.620s

abanihi@cheyenne2: /glade/scratch/abanihi/data $ du -s AWS/ -h
9.7G    AWS/
```



## Data Transfer Time

| Data size in (GB) | Transfer time (s)  | Transfer Rate (MBps) |
|-------------------|--------------------|----------------------|
| 9.7               | 972.712            | 10.2                 |


