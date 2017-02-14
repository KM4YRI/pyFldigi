'''ARQ/KISS I/O port
'''


class Io(object):

    '''
    .. note:: An instance of this class automatically gets created under :py:class:`pyfldigi.client.client.Client` when it is constructed.
    '''

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client

    def in_use(self):
        '''Returns the IO port in use (ARQ/KISS).
        '''
        return self.client.io.in_use()

    def enable_kiss(self):
        '''Switch to KISS I/O
        '''
        self.client.io.enable_kiss()

    def enable_arq(self):
        '''Switch to ARQ I/O
        '''
        self.client.io.enable_arq()
