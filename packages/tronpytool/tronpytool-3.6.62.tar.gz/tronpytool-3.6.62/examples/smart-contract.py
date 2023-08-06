#!/usr/bin/env python
# coding: utf-8
import os

from examples.codec.core.lib import WrapDeploy
from tronpytool import __version__
from tronpytool.common import trc20

print(__version__)
caddress = "TGzXbPmnnRyknJbvx7BCJqpdg76uiZaE92"

ROOT = os.path.join(os.path.dirname(__file__))
# original owner address
NETWORK = "nile"

test_data = [
    ["TPbUCNXm4qe2a8yN34SJ7L1rTo1v8dFQsw", 1000000],
    ["TN8oagb1NUMWNDHZrsCsdyMmAawDe4CynM", 1000000],
    ["TJ1Ed3UGC6iLrKJrfdmBVdNypeRP7CTA6i", 1000000],
    ["THwiDYo5iuNZGfEe8mResy6rU878ec7nG2", 1000000],
    ["TPvfywKCHP4AZXJhgXbwmgprN48qwXLfmT", 1000000],
]

if __name__ == '__main__':
    ws = WrapDeploy(ROOT, NETWORK)
    ws.connect(ROOT, False)

    contract = trc20.TokenLv(ws.tron, ws.getAddr("TokenTrc20"))
    contract.burn(100000)


