'''
'''


class Rig(object):

    def __init__(self, client):
        self.client = client

    @property
    def name(self):
        '''Returns the rig name previously set via rig.set_name
        '''
        return self.client.rig.get_name()

    @name.setter
    def name(self, name):
        '''Sets the rig name for xmlrpc rig
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        return self.client.rig.set_name(str(name))

    def set_frequency(self, freq):
        '''Sets the RF carrier frequency. Returns the old value
        '''
        return self.client.rig.set_frequency(float(freq))

    @property
    def modes(self):
        '''Returns the list of available rig modes
        '''
        return self.client.rig.get_modes()

    @modes.setter
    def modes(self, value):
        '''Sets the list of available rig modes
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.rig.set_modes(value)

    @property
    def mode(self):
        '''Returns the name of the current transceiver mode
        '''
        return self.client.rig.get_mode()

    @mode.setter
    def mode(self, value):
        '''Selects a mode previously added by rig.set_modes
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.rig.set_mode(str(value))

    @property
    def bandwidths(self):
        '''Returns the list of available rig bandwidths
        '''
        return self.client.rig.get_bandwidths()

    @bandwidths.setter
    def bandwidths(self, bandwidths):
        '''Sets the list of available rig bandwidths
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.rig.set_bandwidths(bandwidths)

    @property
    def bandwidth(self):
        '''Returns the name of the current transceiver bandwidth
        '''
        return self.client.rig.get_bandwidth()

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        '''Selects a bandwidth previously added by rig.set_bandwidths
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.rig.set_bandwidth(bandwidth)

    def take_control(self):
        '''Switches rig control to XML-RPC
        '''
        return self.client.rig.take_control()

    def release_control(self):
        '''Switches rig control to previous setting
        '''
        return self.client.rig.release_control()
