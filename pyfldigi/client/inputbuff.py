'''
'''


class Inputbuff(object):

    def __init__(self, client):
        self.client = client
        self.buff = ''

    def __str__(self):
        self._get()  # append any new data onto the buffer
        return self.buff

    def __len__(self):
        self._get()  # append any new data onto the buffer before returning length
        return len(self.buff)

    def _get(self):
        '''Returns all RX data received since last query.
        '''
        resp = self.client.rx.get_data()
        if isinstance(resp, str):
            self.buff += resp

    def clear(self):
        '''Clears the RX text widget
        '''
        self.client.text.clear_rx()
        self.buff = ''
