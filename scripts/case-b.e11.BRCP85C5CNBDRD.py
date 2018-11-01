import xarray as xr
from pathlib import Path 
from dask.distributed import Client 
import s3fs
import timeit 

def write_zarr_to_s3(dset, d):
    dset.to_zarr(store=d, mode='w')


if __name__ == '__main__':

    client = Client(processes=False)
    print(client)

    root_dir = Path("/glade/p_old/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TS")
    CASE = 'b.e11.BRCP85C5CNBDRD.f09_g16'
    list_1 = sorted(root_dir.glob("b.e11.BRCP85C5CNBDRD.f09_g16.???.cam.h0.*.200601-208012*"))
    list_2 = sorted(root_dir.glob("b.e11.BRCP85C5CNBDRD.f09_g16.???.cam.h0.*.208101-210012*"))
    
    # Step 1:
    # Map files in list_1 and list_2 for each ensemble in a list of tuples where each tuple 
    # contains files for each ensemble for the two time ranges.
    case_1 = list(zip(list_1, list_2))
    
    # Loop through the resulting list from step 1, and read those files into a list of datasets. 
    # Under the hood, xarray concatenates files for each ensemble in one dataset.
    ds_list = [xr.open_mfdataset(item) for item in case_1]
    
    # Concatenate list of datasets from step 2 into one xarray dataset. 
    # We concatenate these datasets along the ensemble dimension.
    dset = xr.concat(ds_list, dim='ensemble').chunk({'ensemble': 1, 'time': 20})
    dset.attrs['case'] = CASE
  

    # Output: S3 Bucket 
    f_zarr = f'zarr-test-bucket/direct/test02/{CASE}'

    # write data using xarray.to_zarr()
    fs = s3fs.S3FileSystem(anon=False)
    d = s3fs.S3Map(f_zarr, s3=fs)
    print(timeit.timeit("write_zarr_to_s3(dset, d)", globals=globals()))

