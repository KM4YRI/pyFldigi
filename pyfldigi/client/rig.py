'''
'''


class Rig(object):

    '''Rig (CAT) control via flrig, hamlib, RigCAT, RTS/DTR, or GPIO

    .. note:: An instance of this class automatically gets created under fldigi.Client() when it is constructed.
    '''

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client

    @property
    def name(self):
        '''The rig name, e.g. 'FT-817' or 'IC-7300'

        :getter: Returns the rig name previously set via rig.set_name
        :setter: Sets the rig name for xmlrpc rig
        :type: str

        .. note::
            This doesn't seem to have an effect when hamlib is enabled.  However it
            seems to work ex expected when using flrig via xml-rpc.

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.rig.name
        'FT-817'
        '''
        return self.client.rig.get_name()

    @name.setter
    def name(self, name):
        '''Sets the rig name for xmlrpc rig
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        return self.client.rig.set_name(str(name))

    @property
    def frequency(self):
        '''Returns the RF carrier frequency

        :getter: Returns the RF carrier frequency, in Hz.
        :setter: Sets the RF carrier frequency, in Hz.
        :type: float

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.rig.frequency  # read to demonstrate its initial value
        7070200.0
        >>> fldigi.rig.frequency = 7000000.0  # Set to 7 MHz
        >>> fldigi.rig.frequency  # read back to demonstrate that it changed
        7000000.0
        '''
        return self.client.rig.get_frequency()

    @frequency.setter
    def frequency(self, freq):
        '''Sets the RF carrier frequency. Returns the old value
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        return self.client.rig.set_frequency(float(freq))

    @property
    def modes(self):
        '''The list of available rig modes

        :getter: Returns the list of available rig modes.
        :setter: Sets the list of available rig modes
        :type: list of str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.rig.modes  # read to demonstrate its initial value
        ['NONE', 'AM', 'CW', 'USB', 'LSB', 'RTTY', 'FM', 'WFM', 'CWR', 'RTTYR', 'AMS', 'PKTLSB', 'PKTUSB', 'PKTFM']
        '''
        return self.client.rig.get_modes()

    @modes.setter
    def modes(self, value):
        '''Sets the list of available rig modes
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.rig.set_modes(value)

    @property
    def mode(self):
        '''The name of the current transceiver mode

        :getter: Returns the name of the current transceiver mode
        :setter: Selects a transceiver mode
        :type: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.rig.mode
        'CW'
        >>> fldigi.rig.mode = 'USB'
        >>> fldigi.rig.mode
        'USB'
        '''
        return self.client.rig.get_mode()

    @mode.setter
    def mode(self, value):
        '''Selects a mode previously added by rig.set_modes
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.rig.set_mode(str(value))

    @property
    def bandwidths(self):
        '''The list of available rig bandwidths

        :getter: Returns the list of available rig bandwidths
        :setter: Sets the list of available rig bandwidths
        :type: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.rig.bandwidths
        ['  ']  # This is what my radio returns :-/
        '''
        return self.client.rig.get_bandwidths()

    @bandwidths.setter
    def bandwidths(self, bandwidths):
        '''Sets the list of available rig bandwidths
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.rig.set_bandwidths(bandwidths)

    @property
    def bandwidth(self):
        '''The name of the current transceiver bandwidth

        :getter: Returns the name of the current transceiver bandwidth
        :setter: Selects a bandwidth previously added by rig.set_bandwidths
        :type: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.rig.bandwidth
        '  '
        '''
        return self.client.rig.get_bandwidth()

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        '''Selects a bandwidth previously added by rig.set_bandwidths
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.rig.set_bandwidth(bandwidth)

    def take_control(self):
        '''Switches rig control to XML-RPC

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.rig.take_control()
        '''
        self.client.rig.take_control()

    def release_control(self):
        '''Switches rig control to previous setting before take_control() was called

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.rig.release_control()
        '''
        self.client.rig.release_control()
