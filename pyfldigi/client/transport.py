# -*- coding: utf-8 -*-

'''A replacement transport for Python xmlrpc library.

pyfldigi note:  Shamelessly borrowed from:

https://github.com/astraw/stdeb/blob/master/stdeb/transport.py

..with a few modifications, mainly to make it python 3 friendly, and to get rid of vestigial cruft.
Oh, and I made it HTTP only because fldigi doesn't support HTTPS as far as I know.
The file was originally released under the MIT license'''

import xmlrpc
import requests
import requests.utils


class RequestsTransport(xmlrpc.client.Transport):
    """Drop in Transport for xmlrpclib that uses Requests instead of httplib.

    Inherits xml.client.Transport and is meant to be passed directly to xmlrpc.ServerProxy constructor.

    :example:

    >>> import xmlrpc.client
    >>> from transport import RequestsTransport
    >>> s = xmlrpc.client.ServerProxy('http://yoursite.com/xmlrpc', transport=RequestsTransport())
    >>> s.demo.sayHello()
    Hello!

    """
    # change our user agent to reflect Requests
    user_agent = 'Python-xmlrpc with Requests (python-requests.org)'

    def request(self, host, handler, request_body, verbose):
        '''Make an xmlrpc request.'''
        headers = {'User-Agent': self.user_agent, 'Content-Type': 'text/xml'}
        url = self._build_url(host, handler)
        resp = requests.post(url, data=request_body, headers=headers)
        try:
            resp.raise_for_status()
        except requests.RequestException as e:
            raise xmlrpc.client.ProtocolError(url, resp.status_code, str(e), resp.headers)
        else:
            return self.parse_response(resp)

    def parse_response(self, resp):
        '''Parse the xmlrpc response.'''
        p, u = self.getparser()  # returns (parser, target)
        p.feed(resp.text)
        p.close()
        return u.close()

    def _build_url(self, host, handler):
        '''Build a url for our request based on the host, handler and use_http property'''
        return 'http://{}/{}'.format(host, handler)
