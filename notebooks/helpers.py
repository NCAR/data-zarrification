import os
import random
import shutil
from functools import reduce
from operator import mul

import xarray as xr
from distributed.utils import format_bytes


def print_ds_info(ds, var):
    """Function for printing chunking information"""
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


def zarr_store(
    exp,
    cmp,
    frequency,
    var,
    write=False,
    dirout='/glade/scratch/abanihi/lens-aws',
):
    """ Create zarr store name/path
    """
    path = f'{dirout}/{cmp}/{frequency}/cesmLE-{exp}-{var}.zarr'
    if write and os.path.exists(path):
        shutil.rmtree(path)
    print(path)
    return path


def save_data(ds, store):
    try:
        ds.to_zarr(store, consolidated=True)
        del ds
    except Exception as e:
        print(f'Failed to write {store}: {e}')


def process_variables(
    col, variables, component, stream, experiment, verbose=False
):
    query = dict(
        component=component,
        stream=stream,
        variable=variables,
        experiment=experiment,
    )
    subset = col.search(**query)
    if verbose:
        print(
            subset.unique(
                columns=['variable', 'component', 'stream', 'experiment']
            )
        )
    return subset, query


def enforce_chunking(datasets, chunks, field_separator):
    """Enforce uniform chunking"""
    dsets = datasets.copy()
    choice = random.choice(range(0, len(dsets)))
    for i, (key, ds) in enumerate(dsets.items()):
        c = chunks.copy()
        for dim in list(c):
            if dim not in ds.dims:
                del c[dim]
        ds = ds.chunk(c)
        keys_to_delete = ['intake_esm_dataset_key', 'intake_esm_varname']
        for k in keys_to_delete:
            del ds.attrs[k]
        dsets[key] = ds
        variable = key.split(field_separator)[-1]
        print_ds_info(ds, variable)
        if i == choice:
            print(ds)
        print('\n')
    return dsets


def get_grid_vars(ds, variables):
    vars_to_drop = [vname for vname in ds.data_vars if vname not in variables]
    coord_vars = [
        vname
        for vname in ds.data_vars
        if 'time' not in ds[vname].dims or 'bound' in vname
    ]
    ds_fixed = ds.set_coords(coord_vars)
    data_vars_dims = []
    for data_var in ds_fixed.data_vars:
        data_vars_dims.extend(list(ds_fixed[data_var].dims))
    coords_to_drop = [
        coord for coord in ds_fixed.coords if coord not in data_vars_dims
    ]
    grid_vars = list(
        set(vars_to_drop + coords_to_drop) - set(['time', 'time_bound'])
    )

    return grid_vars


def create_grid_dataset(sample_file, variables):
    ds = xr.open_dataset(sample_file, chunks={}, decode_times=False)
    grid_vars = get_grid_vars(ds, variables)
    grid = ds.set_coords(grid_vars)[grid_vars].drop_dims('time')
    grid.attrs = {}
    return grid
