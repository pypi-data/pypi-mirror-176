# MIT License
#
# Modifications Copyright (c) Zhassulan Shaikhygali, shaikh.zhas@gmail.com
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# import click
import re
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../avalancheetl')))

print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from avalancheetl.web3_utils import build_web3
from avalancheetl.jobs.export_all_common import export_all_common
from avalancheetl.providers.auto import get_provider_from_uri
from avalancheetl.service.ava_service import AvaService
from avalancheetl.utils import check_classic_provider_uri
from blockchainetl.logging_utils import logging_basic_config


logging_basic_config()


def is_date_range(start, end):
    """Checks for YYYY-MM-DD date format."""
    return bool(re.match('^2[0-9]{3}-[0-9]{2}-[0-9]{2}$', start) and
                re.match('^2[0-9]{3}-[0-9]{2}-[0-9]{2}$', end))


def is_unix_time_range(start, end):
    """Checks for Unix timestamp format."""
    return bool(re.match("^[0-9]{10}$|^[0-9]{13}$", start) and
                re.match("^[0-9]{10}$|^[0-9]{13}$", end))


def is_block_range(start, end):
    """Checks for a valid block number."""
    return (start.isdigit() and 0 <= int(start) <= 99999999 and
            end.isdigit() and 0 <= int(end) <= 99999999)


def get_partitions(start, end, partition_batch_size, provider_uri):
    """Yield partitions based on input data type."""
    if is_date_range(start, end) or is_unix_time_range(start, end):
        if is_date_range(start, end):
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            end_date = datetime.strptime(end, '%Y-%m-%d').date()

        elif is_unix_time_range(start, end):
            if len(start) == 10 and len(end) == 10:
                start_date = datetime.utcfromtimestamp(int(start)).date()
                end_date = datetime.utcfromtimestamp(int(end)).date()

            elif len(start) == 13 and len(end) == 13:
                start_date = datetime.utcfromtimestamp(int(start) / 1e3).date()
                end_date = datetime.utcfromtimestamp(int(end) / 1e3).date()

        day = timedelta(days=1)

        provider = get_provider_from_uri(provider_uri)
        web3 = build_web3(provider)
        ava_service = AvaService(web3)

        while start_date <= end_date:
            batch_start_block, batch_end_block = ava_service.get_block_range_for_date(start_date)
            partition_dir = '/date={start_date!s}/'.format(start_date=start_date)
            yield batch_start_block, batch_end_block, partition_dir
            start_date += day

    elif is_block_range(start, end):
        start_block = int(start)
        end_block = int(end)

        for batch_start_block in range(start_block, end_block + 1, partition_batch_size):
            batch_end_block = batch_start_block + partition_batch_size - 1
            if batch_end_block > end_block:
                batch_end_block = end_block

            padded_batch_start_block = str(batch_start_block).zfill(8)
            padded_batch_end_block = str(batch_end_block).zfill(8)
            partition_dir = '/start_block={padded_batch_start_block}/end_block={padded_batch_end_block}'.format(
                padded_batch_start_block=padded_batch_start_block,
                padded_batch_end_block=padded_batch_end_block,
            )
            yield batch_start_block, batch_end_block, partition_dir

    else:
        raise ValueError('start and end must be either block numbers or ISO dates or Unix times')


# start = '2022-11-01'
# end = '2022-11-01'
start = '21794128'
end = '21794150'
partition_batch_size = 10000
# provider_uri = 'https://quick-morning-film.avalanche-mainnet.discover.quiknode.pro/151ede6bb4a566d7250a293e51cec7ebffacdd71/ext/bc/C/rpc'
provider_uri = 'https://avax.getblock.io/2553b132-5f35-11ed-96f0-fe4f04a5caff/mainnet/ext/bc/C/rpc'
output_dir = 'output'
max_workers = 5
export_batch_size = 1
def export_all(
    start,
    end,
    partition_batch_size,
    provider_uri,
    output_dir,
    max_workers,
    export_batch_size,
    chain='avalanche'
):
    """Exports all data for a range of blocks."""
    provider_uri = check_classic_provider_uri(chain, provider_uri)
    export_all_common(get_partitions(start, end, partition_batch_size, provider_uri),
                      output_dir, provider_uri, max_workers, export_batch_size)

export_all(start=start, end=end, partition_batch_size=partition_batch_size, provider_uri=provider_uri, output_dir=output_dir, max_workers=max_workers, export_batch_size=export_batch_size)