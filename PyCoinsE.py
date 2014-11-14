#!/usr/bin/env python
# coding=iso-8859-1

# PyCoinsE: a Python binding to the Coins-E API
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

# This is mainly an object-oriented adaptation of the example code at
# https://www.coins-e.com/assets/api/coins-e_api_example.py.

import urllib,urllib2
import time
import hmac
import hashlib
import json

class PyCoinsE:

  # constructor 
  # pubkey: API public key, privkey: API private key
  # get keys from https://www.coins-e.com/exchange/api/access/

  def __init__(self, pubkey, privkey):
    self.PUBLIC_KEY=pubkey
    self.PRIVATE_KEY=privkey;
    self.BASE_API_URL="https://www.coins-e.com/api/v2"

  # issue unauthenticated requests

  def unauthenticated_request(self, url_suffix):
    url_request_object = urllib2.Request("%s/%s" % (self.BASE_API_URL,url_suffix))
    response = urllib2.urlopen(url_request_object)    
    response_json = {}
    try:
        response_content = response.read()
        response_json = json.loads(response_content)        
        return response_json
    finally:
        response.close()
    return "failed"
    
  # issue authenticated requests  
    
  def authenticated_request(self, url_suffix, method, post_args={}):
    nonce=int(time.time())
    post_args['method'] = method        
    post_args['nonce'] = nonce        
    post_data = urllib.urlencode(post_args)
    required_sign = hmac.new(self.PRIVATE_KEY, post_data, hashlib.sha512).hexdigest()
    headers = {}
    headers['key'] = self.PUBLIC_KEY
    headers['sign'] = required_sign
    url_request_object = urllib2.Request("%s/%s" % (self.BASE_API_URL,url_suffix),
                                         post_data,
                                         headers)    
    response = urllib2.urlopen(url_request_object)    

    try:
      response_content = response.read()
      response_json = json.loads(response_content)        
      if not response_json['status']:
        raise Exception("unable to retrieve or decode response")   
      return response_json
    finally:
      response.close()        
    return "failed"

    # see https://www.coins-e.com/exchange/api/documentation/ for more info
    