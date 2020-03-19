import os
import shutil
from functools import reduce
from operator import mul

from distributed.utils import format_bytes


def print_ds_info(ds, var):
    dt = ds[var].dtype
    itemsize = dt.itemsize
    chunk_size = ds[var].data.chunksize
    size = format_bytes(ds.nbytes)
    _bytes = reduce(mul, chunk_size) * itemsize
    chunk_size_bytes = format_bytes(_bytes)

    print(f'Variable name: {var}')
    print(f'Dataset dimensions: {ds[var].dims}')
    print(f'Chunk shape: {chunk_size}')
    print(f'Dataset shape: {ds[var].shape}')
    print(f'Chunk size: {chunk_size_bytes}')
    print(f'Dataset size: {size}')
    # print(f"Chunks: {ds[var].chunks}")


def preprocess(ds):
    varname = [ds.attrs['intake_esm_varname']]
    coord_vars = set(ds.data_vars) - set(varname)
    return ds.set_coords(coord_vars)


def _restore_non_dim_coords(ds):
    """restore non_dim_coords to variables"""
    non_dim_coords_reset = set(ds.coords) - set(ds.dims)
    ds = ds.reset_coords(non_dim_coords_reset)
    return ds


# This function removes the time dimension that xarray
# adds to variables during concat().
def remove_time(col_subset, chunks):
    dsets = col_subset.to_dataset_dict(cdf_kwargs={'chunks': chunks})

    datasets = {}
    for key, dset in dsets.items():
        # dset = dset.copy()
        for v in dset.variables:
            if v not in dset.coords and v != dset.attrs['intake_esm_variable']:
                dset[v] = dset[v].isel(time=0).drop('time')
        datasets[key] = dset

    return datasets


dirout = '/glade/scratch/bonnland/lens-aws'


def zarr_store(exp, cmp, frequency, var, write=False, dirout=dirout):
    """ Create zarr store name/path
    """
    path = f'{dirout}/{cmp}/{frequency}/cesmLE-{exp}-{var}.zarr'
    if write and os.path.exists(path):
        shutil.rmtree(path)
    print(path)
    return path


def save_data(ds, var, chunkspec, store):
    try:
        ds = ds.chunk(chunkspec)
        print_ds_info(ds, var)
        ds.to_zarr(store, consolidated=True)
        del ds
    except Exception as e:
        print(e)


def show_ds_info(datasets):
    # Get a list of variable names
    varnames = []
    for dataset in datasets:
        varname = dataset.split('.')[-1]
        varnames.append(varname)
        for variable, ds in zip(varnames, datasets.values()):
            print_ds_info(ds, variable)
            print('\n')
