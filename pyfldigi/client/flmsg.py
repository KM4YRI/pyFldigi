'''
'''


class Flmsg(object):

    '''All of the commands related to flmsg in the XML-RPC spec for fldigi.

    .. note:: These commands are under the 'main' section in the XML-RPC spec but they're put here for organizational purposes.

    .. note:: An instance of this class automatically gets created under :py:class:`pyfldigi.client.client.Client` when it is constructed.
    '''

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client

    @property
    def online(self):
        '''flmsg online indication

        :returns: Returns True if flmsg is online.  False otherwise.
        :rtype: bool
        '''
        return bool(self.client.main.flmsg_online())

    @property
    def available(self):
        '''flmsg data available

        :returns: Returns True if flmsg data is available.  False otherwise.
        :rtype: bool
        '''
        return bool(self.client.main.flmsg_available())

    def transfer(self):
        '''??

        :returns: ?? No idea what this function is for.
        :rtype: ''
        '''
        return self.client.main.flmsg_transfer()

    @property
    def squelch(self):
        '''??

        :returns: ?? No idea what this function is for.
        :rtype: bool
        '''
        return bool(self.client.main.flmsg_squelch())
