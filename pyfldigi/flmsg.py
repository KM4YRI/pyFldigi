'''
'''


class Flmsg(object):

    def __init__(self, client):
        self.client = client

    @property
    def online(self):
        '''flmsg online indication
        '''
        return bool(self.client.main.flmsg_online())

    @property
    def available(self):
        '''flmsg data available
        '''
        return bool(self.client.main.flmsg_available())

    def transfer(self):
        '''data transfer to flmsg
        '''
        return bool(self.client.main.flmsg_transfer())

    @property
    def squelch(self):
        '''Returns the squelch state.
        '''
        return bool(self.client.main.flmsg_squelch())
