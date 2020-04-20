import subprocess
from pathlib import Path

import click
import xarray as xr
from tqdm.auto import tqdm


@click.command()
@click.option(
    '-rp',
    '--root-path',
    default='/glade/campaign/cisl/iowa/lens-aws/',
    type=str,
    show_default=True,
)
@click.option(
    '-b', '--bucket', default='ncar-cesm-lens', type=str, show_default=True,
)
@click.option(
    '-p', '--profile', default='stratus-cesm', type=str, show_default=True,
)
def _main(root_path, bucket, profile):
    #     import os
    #     import fsspec
    S3_URL = 'https://stratus.ucar.edu'
    #     fs = fsspec.filesystem(
    #         's3',
    #         secret=os.environ['STRATUS_SECRET_KEY'],
    #         key=os.environ['STRATUS_ACCESS_KEY'],
    #         anon=False,
    #         client_kwargs={'endpoint_url': S3_URL},
    #     )
    #     fs = fsspec.filesystem(
    #         's3', profile='stratus-cesm', anon=False,
    #         client_kwargs={'endpoint_url': S3_URL}
    #     )
    root = Path(root_path)
    stores_list = root.glob('*/*/*.zarr')
    x = {
        store: xr.open_zarr(store.as_posix(), consolidated=True).nbytes
        for store in stores_list
    }
    y = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    stores = list(y.keys())[257:]
    store_mapping = {}
    root_remote_path = bucket
    for store in stores:
        parts = store.parts
        x = parts[-3:-1]
        remote_path = f's3://{root_remote_path}/{x[0]}/{x[1]}/{parts[-1]}'
        local_path = store.as_posix()
        store_mapping[local_path] = remote_path
    for local_path, remote_path in tqdm(store_mapping.items()):
        #         cmd = [
        #             'aws',
        #             '--endpoint-url',
        #             'https://stratus.ucar.edu',
        #             '--profile',
        #             'stratus-cesm',
        #             's3',
        #             'cp',
        #             '--recursive',
        #             local_path,
        #             remote_path,
        #             '--quiet',
        #         ]
        cmd = [
            'aws',
            '--endpoint-url',
            f'{S3_URL}',
            '--profile',
            f'{profile}',
            's3',
            'sync',
            local_path,
            remote_path,
            '--quiet',
        ]
        print(f'Uploading {local_path} --> {remote_path}')
        subprocess.check_call(cmd)


if __name__ == '__main__':

    _main()
