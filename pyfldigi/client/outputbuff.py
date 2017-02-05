'''
'''


class Outputbuff(object):

    def __init__(self, client):
        self.client = client
        self.buff = ''

    def __str__(self):
        return self.buff

    def __iadd__(self, other):
        '''Adds a string to the TX text widget
        '''
        if isinstance(other, bytes):
            return self.client.text.add_tx_bytes(other)
        elif isinstance(other, str):
            return self.client.text.add_tx(other)
        else:
            raise TypeError('text must be in bytes or str format')

    def clear(self):
        '''Clears the TX text widget
        '''
        return self.client.text.clear_tx()

    def get_tx_data(self):
        '''Returns all TX data transmitted since last query.
        '''
        return self.client.tx.get_data()
