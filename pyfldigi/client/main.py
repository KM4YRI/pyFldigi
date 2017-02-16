'''
'''

import time
import logging


class Main(object):

    '''All the commands under 'fldigi.main' in the XML-RPC spec for fldigi.

    .. note:: An instance of this class automatically gets created under :py:class:`pyfldigi.client.client.Client` when it is constructed.
    '''

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client
        self.logger = logging.getLogger('pyfldigi.client.main')

    @property
    def status1(self):
        '''Returns the contents of the first status field (typically s/n)

        :returns: First status field
        :rtype: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.status1
        ''
        '''
        return self.client.main.get_status1()

    @property
    def status2(self):
        '''Returns the contents of the second status field

        :returns: Second status field
        :rtype: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.status2
        ''
        '''
        return self.client.main.get_status2()

    @property
    def wf_sideband(self):
        '''The current waterfall sideband (either USB or LSB)

        :getter: Returns the current waterfall sideband (either USB or LSB)
        :setter: Sets the waterfall sideband to USB or LSB.
        :todo: The setter doesn't seem to work, at least in some contexts or modes.
        :type: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.wf_sideband  # read to demonstrate its initial value
        'USB'
        >>> fldigi.main.wf_sideband = 'LSB'  # set to Lower sideband
        >>> fldigi.main.wf_sideband  # read back to demonstrate that it changed
        'LSB'
        '''
        return self.client.main.get_wf_sideband()

    @wf_sideband.setter
    def set_wf_sideband(self, sideband):
        '''Sets the waterfall sideband to USB or LSB
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        if str(sideband) not in ['USB', 'LSB']:
            raise ValueError('sideband must be USB or LSB')
        self.client.main.set_wf_sideband(str(sideband))

    @property
    def afc(self):
        '''The AFC (auto frequency control) state

        :getter: Returns the AFC [auto frequency control] state
        :setter: Sets the AFC [auto frequency control] state.
        :type: bool

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.afc  # read to demonstrate its initial value
        True
        >>> fldigi.main.afc = False  # disable
        >>> fldigi.main.afc  # read back to demonstrate that it changed
        False
        '''
        return bool(self.client.main.get_afc())

    @afc.setter
    def afc(self, afc):
        '''Sets the AFC (auto frequency control) state.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        if not isinstance(afc, bool):
            raise TypeError('afc must be a bool')
        self.client.main.set_afc(bool(afc))

    @property
    def squelch(self):
        '''The squelch state (True or False)

        :getter: Returns the squelch state.
        :setter: Sets the squelch state.
        :type: bool

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.squelch  # read to demonstrate its initial value
        True
        >>> fldigi.main.squelch = False  # disable
        >>> fldigi.main.squelch  # read back to demonstrate that it changed
        False
        '''
        return bool(self.client.main.get_squelch())

    @squelch.setter
    def squelch(self, squelch):
        '''Sets the squelch state.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        if not isinstance(squelch, bool):
            raise TypeError('squelch state must be a bool')
        self.client.main.set_squelch(bool(squelch))

    @property
    def squelch_level(self):
        '''The squelch level.  Range is 0.0 - 100.0

        :getter: Returns the squelch level
        :setter: Sets the squelch state.
        :type: float

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.squelch_level  # read to demonstrate its initial value
        5.0
        >>> fldigi.main.squelch_level = 4  # set to 4.  will be casted to float.
        >>> fldigi.main.squelch_level  # read back to demonstrate that it changed
        4.0
        '''
        return self.client.main.get_squelch_level()

    @squelch_level.setter
    def squelch_level(self, level):
        '''Sets the squelch level.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        if not 0 <= level <= 100:
            raise ValueError('squelch level must be between 0 and 100')
        self.client.main.set_squelch_level(float(level))

    @property
    def reverse(self):
        '''The Reverse Sideband state (whether or not the mark and space are reversed)

        :getter: Returns the Reverse Sideband state
        :setter: Sets the Reverse Sideband state.
        :type: bool

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.reverse  # read to demonstrate its initial value
        True
        >>> fldigi.main.reverse = False  # disable
        >>> fldigi.main.reverse  # read back to demonstrate that it changed
        False
        '''
        return bool(self.client.main.get_reverse())

    @reverse.setter
    def reverse(self, state):
        '''Sets the Reverse Sideband state.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.main.set_reverse(bool(state))

    @property
    def txlock(self):
        '''The Transmit [frequency] Lock state.  When unlocked the transmit and receive frequencies can be uncoupled.

        :getter: Returns the Transmit [frequency] Lock state
        :setter: Sets the Transmit [frequency] Lock state.
        :type: bool

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.txlock  # read to demonstrate its initial value
        True
        >>> fldigi.main.txlock = False  # disable
        >>> fldigi.main.txlock  # read back to demonstrate that it changed
        False
        '''
        return bool(self.client.main.get_lock())

    @txlock.setter
    def txlock(self, value=True):
        '''Sets the Transmit [frequency] Lock state.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.main.set_lock(bool(value))

    @property
    def rsid(self):
        '''The RSID state.

        Reed-Solomon Identification (RSID) is used in several digital mode programs. RSID allows the automatic
        identification of any digital transmission which has been assigned a unique code identifier.
        On reception of a RS ID, two events occur: the mode used is detected and the central frequency of the RSID,
        which is also the central frequency of the identified mode, is determined with a precision of 2.7 Hz.
        This is sufficient to allow all current modes to begin accurate decoding. This is an excellent way to
        insure that signals like MFSK are properly tuned and decoded.  The RSID signal is transmitted in 1.4 sec
        and has a bandwidth of 172 Hz. Detection of the RSID signal is possible down to a Signal to Noise ratio of
        about -16 dB, so with a sensitivity equal or better than the majority of the digital modes (RTTY, PSK31...),
        except several modes as PSK10, PSKAM10, THROB, THROBX or JT65.

        .. Note:: Consequently, it is possible to detect RSID and not be able to decode the ensuing data signal
            due to it being too weak a signal.

        fldigi allows the RSID signal to be sent at the beginning and the end of each transmission. The leading
        RSID is the normal position.  During reception fldigi can decode RSID signals within the entire audio
        spectrum. It can also be configured to limit the reception to a narrow bandwidth centered on the current
        audio subcarrier. Detection occurs as a background process and does not interfer with the normal signal
        decoding. False detection is possible, but statistically rare due to the use of a very strong
        autocorrelation function associated with the RSID codes.

        .. note:: For more info, please see: http://www.w1hkj.com/RSID_description.html

        :getter: Returns the RSID state.
        :setter: Sets the RSID state.
        :type: bool

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.rsid  # read to demonstrate its initial value
        True
        >>> fldigi.main.rsid = False  # disable
        >>> fldigi.main.rsid  # read back to demonstrate that it changed
        False
        '''
        return bool(self.client.main.get_rsid())

    @rsid.setter
    def rsid(self, value):
        '''Sets the RSID state.
        NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
        self.client.main.set_rsid(bool(value))

    def get_trx_state(self, suppress_errors=False):
        '''Returns transmit/tune/receive status

        :param suppress_errors: if True, no exception will be raised if the xml-rpc request fails.
        :type suppress_errors: bool

        :returns:
            * 'TX' if FLDIGI is transmitting
            * 'RX' if FLDIGI is receiving
            * 'TUNE' if FLDIGI is tuning (rig antenna tuning in progress, etc)
            * 'ERROR' if state isn't one of the above, or an exception occured
        :rtype: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.get_trx_state()
        'RX'
        '''
        for tries in range(0, 3):  # retry up to 3 times.
            try:
                state = str(self.client.main.get_trx_status()).upper()
            except Exception as e:
                if suppress_errors is False:
                    raise
                else:
                    print('Exception @ get_trx_state() : {}'.format(e))
                    state = 'ERROR'
            if state in ['TX', 'RX', 'TUNE']:
                break
            time.sleep(0.005)
        return state

    def rx(self):
        '''Puts fldigi into receive mode.

        .. note::
            This is the default mode that FLDIGI starts in.
            This command is only needed when you've put it into some other mode.


        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.tx()  # Put flgidigi into transmit mode
        >>> fldigi.delay(1000)  # wait a bit
        >>> fldigi.main.rx()  # Put flgidigi into receive mode
        '''
        self.logger.debug('Setting FLDIGI to RX mode')
        self.client.main.rx()

    def tx(self):
        '''Puts fldigi into transmit mode.  This will key the PTT or VOX via CAT control.

        .. note:: If you're looking to transmit a block of text, please use :py:method:`pyfldigi.client.main.send`

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.tx()  # Put flgidigi into transmit mode
        >>> fldigi.delay(1000)  # wait a bit
        >>> fldigi.main.rx()  # Put flgidigi into receive mode
        '''
        self.logger.debug('Setting FLDIGI to TX mode')
        self.client.main.tx()

    def tune(self):
        '''Puts fldigi into tune mode.  I'm assuming that this allows antenna tuning via CAT/RIG control.

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.tune()  # Put flgidigi into tune mode
        '''
        self.logger.debug('Setting FLDIGI to TUNE mode')
        self.client.main.tune()

    def abort(self):
        '''Aborts a transmit or tune

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.tx()  # Put flgidigi into transmit mode
        >>> fldigi.delay(10)  # wait a bit
        >>> fldigi.main.abort()  # abort the transmit
        '''
        self.client.main.abort()

    def run_macro(self, macroNum):
        '''Runs a macro

        :param macroNum: The macro # to run.  Must be a valid #.
        :type macroNum: int
        '''
        return self.client.main.run_macro(int(macroNum))

    def get_max_macro_id(self):
        '''Returns the maximum macro ID number

        :returns: The maximum macro ID number
        :rtype: int
        '''
        return self.client.main.get_max_macro_id()

    def send(self, data, block=True, timeout=10):
        '''This is the preferred way of sending a block of text.

        :param data: The text or data to encode and transmit
        :type data: str or bytes
        :param block: if True, the function blocks until all data has been transmitted.  If False, this method returns immediately while the radio transmits.
        :type block: bool
        :param timeout: The # of seconds to wait before returning a TimeoutError
        :type timeout: float or int

        .. warning::
            FLDIGI does NOT turn the transmit off after the text is done transmitting.
            This library does, however contain a background thread that monitors the TX state and sets it to 'RX' whenever
            the TX data is finished being sent.  HOWEVER if Python crashes, exits, etc, FLDIGI may be left in transmit
            mode.  Please use precaution and always run any code that uses this library while supervised.  A stuck transmit
            is a bad condition for many, many reasons.

        :example:

        >>> import pyfldigi
        >>> c = pyfldigi.Client()
        >>> # Make sure to set up the modem and rig settings here!!!
        >>> c.main.send('Lorem ipsum dolor sit amet', timeout=50)
        '''
        state = self.clientObj.main.get_trx_state()
        self.logger.debug('send(): state={}'.format(state))

        if state == 'TX':  # already chooching
            tx_start = time.time()
            self.clientObj.text.add_tx(data)
        elif state == 'RX':
            self.clientObj.text.clear_tx()
            self.clientObj.txmonitor.history.txdata_history = []  # clear
            tx_start = time.time()
            self.clientObj.main.tx()
            self.clientObj.text.add_tx(data)

            # wait until the first character has been transmitted, even if non blocking
            while(1):
                if len(self.clientObj.txmonitor.history.txdata_history) >= 1:
                    break
                if time.time() - tx_start >= timeout:
                    raise TimeoutError('Timeout while transmitting, waiting for first byte to go out')
        else:
            raise Exception('cannot transmit if FLDIGI state is \'{}\''.format(state))

        if block is True:
            while(1):
                if self.clientObj.txmonitor.transmitting is False:
                    self.logger.debug('Returning from blocking call to send()...')
                    break
                if time.time() - tx_start >= timeout:
                    raise TimeoutError('Timeout while transmitting, waiting for text to be transmitted')
