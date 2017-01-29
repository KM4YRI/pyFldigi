'''
'''


class Io(object):

    def __init__(self, client):
        self.client = client

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
