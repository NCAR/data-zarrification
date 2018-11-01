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
    CASE = 'b.e11.B20TRC5CNBDRD.f09_g16'
    list_1 = sorted(root_dir.glob("b.e11.B20TRC5CNBDRD.f09_g16.???.cam.h0.*"))
    # indices of special runs to remove for the original list. 
    # These runs' output have additional ouput, and/or have special time ranges
    indices = 0, 33, 34 
    updated_list = [item for index, item in enumerate(list_1) if index not in indices]
    
    dset = xr.open_mfdataset(updated_list, concat_dim='ensemble')
    dset = dset.chunk({'ensemble': 1, 'time': 20})
    dset.attrs['case'] = CASE  

    # Output: S3 Bucket 
    f_zarr = f'zarr-test-bucket/direct/test02/{CASE}'

    # write data using xarray.to_zarr()
    fs = s3fs.S3FileSystem(anon=False)
    d = s3fs.S3Map(f_zarr, s3=fs)
   
    setup = "from __main__ import write_zarr_to_s3"
    print(timeit.timeit("write_zarr_to_s3(dset, d)", setup=setup))

