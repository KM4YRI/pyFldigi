'''For more info on the PSK reporter, please see:
http://www.w1hkj.com/FldigiHelp-3.21/html/psk_reporter_page.html
'''


class Spot(object):

    '''
    '''

    def __init__(self, client):
        self.client = client

    @property
    def auto(self):
        '''spot.get_auto   b:n Returns the autospotter state
        '''
        return self.client.spot.get_auto()

    @auto.setter
    def auto(self, state):
        '''Sets the autospotter state. Returns the old state
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        return self.client.spot.set_auto(bool(state))

    @property
    def pskrep_count(self):
        '''spot.pskrep.get_count   i:n Returns the number of callsigns spotted in the current session
        '''
        return self.client.spot.pskrep.get_count()
