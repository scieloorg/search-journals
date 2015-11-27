# coding: utf-8
import os
import thriftpy
import json

access_stats_thrift = thriftpy.load(
    os.path.dirname(__file__)+'/access_stats.thrift',
    module_name='access_stats_thrift'
)

from thriftpy.rpc import make_client


if __name__ == '__main__':

    client = make_client(
        access_stats_thrift.AccessStats,
        '127.0.0.1',
        11640
    )

    print json.loads(client.document('S1807-86212013000200003', 'scl'))