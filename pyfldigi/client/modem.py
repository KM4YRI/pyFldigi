'''
'''


class Modem(object):

    '''A collection of methods and properties that interface to fldigi's modem functionality.
    For full documentation on the various modems available, see:
    http://www.w1hkj.com/FldigiHelp-3.21/html/modems_page.html

    .. note:: An instance of this class automatically gets created under :py:class:`pyfldigi.client.client.Client` when it is constructed.
    '''

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client
        self.olivia = Olivia(clientObj)
        self.wefax = Wefax(clientObj)
        self.navtex = Navtex(clientObj)

    @property
    def name(self):
        '''The modem name.  This determines which modulation/demodulation protocol is used when
        transmitting and/or receiving.

        .. note:: A full list of names can be queried with: :py:attr:`Client.Modem.names`

        :getter: Returns the name of the current modem
        :setter: Sets the current modem.
        :type: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.name  # read to demonstrate its initial value
        'CW'
        >>> fldigi.modem.name = 'BPSK31'  # set to BPSK31
        >>> fldigi.modem.name  # read back to demonstrate that it changed
        'BPSK31'
        '''
        return self.client.modem.get_name()

    @name.setter
    def name(self, value):
        '''Sets the current modem.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.modem.set_by_name(str(value))

    @property
    def names(self):
        '''Returns all modem names

        :rtype: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.names
        ['NULL', 'CW', 'CTSTIA', 'DOMEX4', 'DOMEX5', 'DOMEX8', 'DOMX11', 'DOMX16', 'DOMX22', 'DOMX44',
        'DOMX88', 'FELDHELL', 'SLOWHELL', 'HELLX5', 'HELLX9', 'FSKHELL', 'FSKH105', 'HELL80', 'MFSK8',
        'MFSK16', 'MFSK32', 'MFSK4', 'MFSK11', 'MFSK22', 'MFSK31', 'MFSK64', 'MFSK128', 'MFSK64L', 'MFSK128L',
        'WEFAX576', 'WEFAX288', 'NAVTEX', 'SITORB', 'MT63-500S', 'MT63-500L', 'MT63-1KS', 'MT63-1KL',
        'MT63-2KS', 'MT63-2KL', 'BPSK31', 'BPSK63', 'BPSK63F', 'BPSK125', 'BPSK250', 'BPSK500', 'BPSK1000',
        'PSK125C12', 'PSK250C6', 'PSK500C2', 'PSK500C4', 'PSK800C2', 'PSK1000C2', 'QPSK31', 'QPSK63',
        'QPSK125', 'QPSK250', 'QPSK500', '8PSK125', '8PSK125FL', '8PSK125F', '8PSK250', '8PSK250FL',
        '8PSK250F', '8PSK500', '8PSK500F', '8PSK1000', '8PSK1000F', '8PSK1200F', 'OLIVIA', 'Olivia-4-250',
        'Olivia-8-250', 'Olivia-4-500', 'Olivia-8-500', 'Olivia-16-500', 'Olivia-8-1K', 'Olivia-16-1K',
        'Olivia-32-1K', 'Olivia-64-2K', 'RTTY', 'THOR4', 'THOR5', 'THOR8', 'THOR11', 'THOR16', 'THOR22',
        'THOR25x4', 'THOR50x1', 'THOR50x2', 'THOR100', 'THROB1', 'THROB2', 'THROB4', 'THRBX1', 'THRBX2',
        'THRBX4', 'PSK125R', 'PSK250R', 'PSK500R', 'PSK1000R', 'PSK63RC4', 'PSK63RC5', 'PSK63RC10',
        'PSK63RC20', 'PSK63RC32', 'PSK125RC4', 'PSK125RC5', 'PSK125RC10', 'PSK125RC12', 'PSK125RC16',
        'PSK250RC2', 'PSK250RC3', 'PSK250RC5', 'PSK250RC6', 'PSK250RC7', 'PSK500RC2', 'PSK500RC3', 'PSK500RC4',
        'PSK800RC2', 'PSK1000RC2', 'FSQ', 'IFKP', 'SSB', 'WWV', 'ANALYSIS', 'FREQSCAN']

        '''
        return self.client.modem.get_names()

    @property
    def id(self):
        '''The numeric id of the modem.  This is effectively the enumeration value used internally by fldigi.

        :getter: Returns the ID of the current modem
        :setter: Sets the current modem by the numeric id.
        :type: int

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.name  # read to demonstrate its initial value
        'CW'
        >>> fldigi.modem.id
        1
        >>> fldigi.modem.name = 'BPSK31'
        >>> fldigi.modem.id
        39
        >>> fldigi.modem.id = 1
        >>> fldigi.modem.id
        1
        >>> fldigi.modem.name
        'CW'
        '''
        return self.client.modem.get_id()

    @id.setter
    def id(self, value):
        '''Sets the current modem.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.modem.set_by_id(int(value))

    @property
    def max_id(self):
        '''Returns the maximum modem ID number

        :type: int

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.max_id
        124
        '''
        return self.client.modem.get_max_id()

    @property
    def carrier(self):
        '''The modem carrier frequency, in Hz.

        .. note::
            This is NOT the same as the rig carrier frequency which is usually in the kHz or MHz range.
            The modem carrier frequency is usually ~1000 Hz or so, well within the audio range.

        :getter: Returns the modem carrier frequency
        :setter: Sets modem carrier.
        :type: int

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.carrier
        1000
        >>> fldigi.modem.carrier = 1020
        >>> fldigi.modem.carrier
        1020
        '''
        return self.client.modem.get_carrier()

    @carrier.setter
    def carrier(self, freq):
        '''Sets modem carrier.

        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property
        '''
        self.client.modem.set_carrier(int(freq))

    @property
    def afc_search_range(self):
        '''The modem AFC [auto frequency control] search range

        :getter: Returns the modem AFC [auto frequency control] search range
        :setter: Sets the modem AFC [auto frequency control] search range.
        :type: int
        '''
        return self.client.modem.get_afc_search_range()

    @afc_search_range.setter
    def afc_search_range(self, range):
        '''Sets the modem AFC [auto frequency control] search range.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.modem.set_afc_search_range(int(range))

    @property
    def bandwidth(self):
        '''The modem bandwidth.

        :getter: Returns the modem bandwidth
        :setter: Sets the modem bandwidth.
        :type: int

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.bandwidth
        0
        >>> fldigi.modem.bandwidth = 500
        0
        '''
        return self.client.modem.get_bandwidth()

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        '''Sets the modem bandwidth.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.modem.set_bandwidth(int(bandwidth))

    @property
    def quality(self):
        '''Returns the modem signal quality in the range [0:100]

        :getter: Returns the modem bandwidth
        :type: int

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.quality
        0
        '''
        return self.client.modem.get_quality()

    def search_up(self):
        '''Searches upward in frequency

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.search_up()
        '''
        self.client.modem.search_up()

    def search_down(self):
        '''Searches downward in frequency

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.search_up()
        '''
        self.client.modem.search_down()


class Olivia(object):

    '''Settings specific to the Olivia modem type.

    .. note:: An instance of this class automatically gets created under :py:class:`pyfldigi.client.modem.Modem` when it is constructed.

    '''

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client

    @property
    def bandwidth(self):
        '''Returns the Olivia bandwidth

        :getter: Returns the modem bandwidth
        :setter: Sets the modem bandwidth.
        :type: int

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.modem.name = 'Olivia-4-250'
        >>> fldigi.modem.olivia.bandwidth
        500
        '''
        return self.client.modem.olivia.get_bandwidth()

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        '''Sets the Olivia bandwidth
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.modem.olivia.set_bandwidth(int(bandwidth))

    @property
    def tones(self):
        '''The # of Olivia tones.  Note that Olivia is a configurable mode where

        :getter: Returns the modem bandwidth
        :setter: Sets the modem bandwidth.
        :type: int

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()

        # Changing the modem name has an effect on the # of tones.
        >>> fldigi.modem.name = 'Olivia-4-250'
        >>> fldigi.modem.tones
        4
        >>> fldigi.modem.name = 'Olivia-8-250'
        >>> fldigi.modem.tones
        8
        # Setting the # of tones will have an effect on the name.
        >>> fldigi.modem.olivia.tones = 4
        >>> fldigi.modem.name
        'Olivia-4-250'
        >>> fldigi.modem.olivia.tones = 8
        >>> fldigi.modem.name
        'Olivia-4-250'
        '''
        return self.client.modem.olivia.get_tones()

    @tones.setter
    def tones(self, tones):
        '''Sets the Olivia tones
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.modem.olivia.set_tones(int(tones))


class Wefax(object):

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client

    def get_engine_state(self):
        '''Returns Wefax engine state (tx and rx) for information.
        '''
        return self.client.wefax.state_string()

    def skip_apt(self):
        '''Skip APT during Wefax reception
        '''
        return self.client.wefax.skip_apt()

    def skip_phasing(self):
        '''Skip phasing during Wefax reception
        '''
        return self.client.wefax.skip_phasing()

    def set_tx_abort_flag(self):
        '''Cancels Wefax image transmission
        '''
        return self.client.wefax.set_tx_abort_flag()

    def end_reception(self):
        '''End Wefax image reception
        '''
        return self.client.wefax.end_reception()

    def start_manual_reception(self):
        '''Starts fax image reception in manual mode
        '''
        return self.client.wefax.start_manual_reception()

    def set_adif_log(self, logging):
        '''Set/reset logging to received/transmit images to ADIF log file
        '''
        return self.client.wefax.set_adif_log(bool(logging))

    def set_max_lines(self, lines):
        '''Set maximum lines for fax image reception
        '''
        return self.client.wefax.set_max_lines(int(lines))

    def get_received_file(self, timeout):
        '''Waits for next received fax file, returns its name with a delay. Empty string if timeout.
        '''
        return self.client.wefax.get_received_file(int(timeout))

    def send_file(self, filename, param):
        '''Send file. returns an empty string if OK otherwise an error message.
        '''
        with open(filename, mode='rb') as f:
            img = f.read()
            img = img.decode('iso-8859-1')  # must be sent out as a string
            return self.client.wefax.send_file(img, param)


class Navtex(object):

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client

    def get_msg(self, timeout):
        '''Returns next Navtex/SitorB message with a max delay in seconds.. Empty string if timeout.
        '''
        return self.client.navtex.get_message(int(timeout))

    def send_msg(self, msg):
        '''Send a Navtex/SitorB message. Returns an empty string if OK otherwise an error message.
        '''
        resp = self.client.navtex.send_message(str(msg))
        if resp != '':
            raise Exception('Unable to send NAVTEX message.  Error message returned: {}'.format(resp))
