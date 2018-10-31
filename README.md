# netcdf-to-zarr-experiment
Large-scale netCDF→ zarr conversion


## Step 1: netCDF to Zarr conversion via `xarray`

[Case 1: Notebook](notebooks/case-b.e11.BRCP85C5CNBDRD.ipynb)

## Step 2: Configure awscli

Follow instructions from [awscli documentation page](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) to configure awscli. 

Once this is done, we are ready to move to the next step (transferring generated zarr dataset to AWS S3 bucket)

## Step 3: Transfer zarr dataset to S3

    $ cd /glade/scratch/abanihi/data/AWS/
  
    $ aws s3 cp --recursive lens/ s3:://zarr-test-bucket 




