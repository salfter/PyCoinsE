#!/usr/bin/env python
# coding=iso-8859-1

# usage example for PyCoinsE
#
# Copyright © 2014 Scott Alfter
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# PyCoinsE is mainly an object-oriented adaptation of the example code at
# https://www.coins-e.com/assets/api/coins-e_api_example.py.

import sys
from PyCoinsE import *
import pprint

api=PyCoinsE("INSERT_COINSE_PUBKEY_HERE", "INSERT_COINSE_PRIVKEY_HERE")

#unauthenticated requests
#List of all markets and the status
pprint.pprint(api.unauthenticated_request("markets/list/"))

#List of all coins and the status
pprint.pprint(api.unauthenticated_request('coins/list/'))

#get consolidated market data
pprint.pprint(api.unauthenticated_request('markets/data/'))

#authenticated requests
pprint.pprint(api.authenticated_request('wallet/all/',"getwallets")["wallets"])
    
# quit this test without executing the following examples    
sys.exit()

# more examples follow
    
working_pair = "WDC_BTC"

#placing a new order    
new_order_request = api.authenticated_request('market/%s/' % (working_pair),"neworder",{'order_type':'buy',
                                                                                         'rate':'0.002123',
                                                                                         'quantity':'1',})
print new_order_request

#get information about an order
get_order_request = api.authenticated_request('market/%s/' % (working_pair),"getorder",{'order_id':new_order_request['order']['id']})
print get_order_request
                                          
#get list of orders
get_list_of_order_request = api.authenticated_request('market/%s/' % (working_pair),"listorders",{'limit':2})

print get_list_of_order_request

for each_order in get_list_of_order_request['orders']:
    print each_order['status']

#cancel an order
order_cancel_request = api.authenticated_request('market/%s/' % (working_pair),"cancelorder",{'order_id':get_order_request['order']['id']})
print order_cancel_request
