import logging


class Text(object):

    '''Read the demodulated and decoded text received by FLDIGI.  Send text to FLDIGI to be encoded, modulated, and transmitted

    .. note:: An instance of this class automatically gets created under :py:class:`pyfldigi.client.client.Client` when it is constructed.
    '''

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client
        self.logger = logging.getLogger('pyfldigi.client.text')

    def add_tx(self, value):
        '''
        :param value: The data to be sent to FLDIGI's TX text widget
        :type value: bytes or str
        '''
        if isinstance(value, bytes):
            self.logger.debug('add_tx({})'.format(value))
            self.client.text.add_tx_bytes(value)
        elif isinstance(value, str):
            self.logger.debug('add_tx(\'{}\')'.format(value))
            self.client.text.add_tx(value)
        else:
            raise TypeError('text must be in bytes or str format')

    def clear_tx(self):
        '''Clears the TX text widget
        '''
        self.logger.debug('clear_tx()')
        self.client.text.clear_tx()  # Clear the TX buffer in FLDIGI

    def get_tx_data(self, suppress_errors=False):
        '''Returns all TX data transmitted since last query.

        :param suppress_error: if True, no exceptions will be emitted, in the case of an error.
        :type suppress_error: bool

        :returns: TX data transmitted since last query.
        :rtype: str (or None if no data since last query)
        '''
        try:
            data = self.client.tx.get_data()
        except Exception as e:
            print(e)
            if suppress_errors is True:
                return None
            else:
                raise e
        else:
            self.logger.debug('get_tx_data() returned: {}'.format(data))
            return data

    def get_rx_data(self):
        '''Returns all RX data received since last query.

        :returns: RX data received since last query
        :rtype: str
        '''
        data = self.client.rx.get_data()
        self.logger.debug('get_rx_data() returned: {}'.format(data))
        return data

    def clear_rx(self):
        '''Clears the RX text widget
        '''
        self.logger.debug('clear_rx()')
        self.client.text.clear_rx()
