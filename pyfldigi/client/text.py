# import logging


class Text(object):

    '''Read the demodulated and decoded text received by FLDIGI.  Send text to FLDIGI to be encoded, modulated, and transmitted

    .. note::
        This class spawns a TX Monitor thread that ensures the transmitter gets keyed on and off at the appropriate
        times.  It monitors Transmit duty cycle (%), max transmit time (seconds) aka Dead Man's Switch?, and max text
        length.  You can set these with the getters and setters below, but you should probably just leave them alone.

        You get all of this functionality for free.  I don't see any use-case where it wouldn't be useful, so it can't be disabled.
        It uses a daemon thread which starts when Client() is instantiated (which calls Text()), and ends when the program shuts down.

    .. note:: An instance of this class automatically gets created under :py:class:`pyfldigi.client.client.Client` when it is constructed.
    '''

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client
        # self.logger = logging.getLogger('pyfldigi.client.text')
        self.txmonitor = clientObj.txmonitor
        self.mutex = clientObj.mutex

    def add_tx(self, value):
        if isinstance(value, bytes):
            self.client.text.add_tx_bytes(value)
        elif isinstance(value, str):
            self.client.text.add_tx(value)
        else:
            raise TypeError('text must be in bytes or str format')

    def clear_tx(self):
        '''Clears the TX text widget
        '''
        self.client.text.clear_tx()  # Clear the TX buffer in FLDIGI

    def get_tx_data(self, suppress_errors=False):
        self.mutex.acquire()
        try:
            return self.client.tx.get_data()
        except Exception as e:
            print(e)
            if suppress_errors is True:
                return None
            else:
                raise e
        finally:
            self.mutex.release()

    def transmit(self, text, block=False):
        '''Changes to Transmit Mode.  Transmits the specified text block.  Then sets the mode back to Receive.'''
        return self.txmonitor.transmit(text, block=block)

    def get_rx_data(self):
        '''Returns all RX data received since last query.
        '''
        return self.client.rx.get_data()

    def clear_rx(self):
        '''Clears the RX text widget
        '''
        self.client.text.clear_rx()

    def receive(self, timeout):
        '''Returns text received'''
        pass
