'''http://www.w1hkj.com/FldigiHelp-3.21/html/xmlrpc_control_page.html

'''

import time
import xmlrpc.client
from .modem import Modem
from .rig import Rig
from .log import Log
from .ioconfig import Io
from .flmsg import Flmsg


class Client(object):

    def __init__(self, ip_address='127.0.0.1', port=7362):
        self.ip_address = ip_address
        self.port = port
        self.client = xmlrpc.client.ServerProxy('http://{}:{}/'.format(ip_address, port))
        self.modem = Modem(self.client)
        self.main = Client.Main(self.client)
        self.rig = Rig(self.client)
        self.log = Log(self.client)
        self.rx = Client.Rx(self.client)
        self.tx = Client.Tx(self.client)
        self.spotter = Client.Spot(self.client)
        self.flmsg = Flmsg(self.client)
        self.io = Io(self.client)

    @property
    def methods(self):
        '''Returns the list of methods

        :return: Returns the list of methods in which fldigi can handle via the xml-rpc interface
        :rtype: list of dict

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.methods
        [{'name': fldigi.list, 'signature': 'A:n', 'help': 'Returns the list of methods.'}, ... ]
        '''
        return self.client.fldigi.list()

    @property
    def name(self):
        '''Returns the program name and version

        :return: Returns the program name and version
        :rtype: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.name
        fldigi
        '''
        return self.client.fldigi.name()

    @property
    def version(self):
        '''Returns the program version as a python dict

        :return: Returns the program version
        :rtype: dict with the keys: 'major', 'minor', 'patch'

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.version
        {'major': 3, 'minor': 23, 'patch': '.17'}
        '''
        return self.client.fldigi.version_struct()

    @property
    def config_dir(self):
        '''Returns the name of the configuration directory
        :return: the configuration directory.  NOTE: On a Windows machine, backslashes will be replaced with forward slashes
        :rtype: str

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.config_dir
        'C:/Users/jeff/fldigi.files/'
        '''
        return self.client.fldigi.config_dir()

    def terminate(self, save_options=True, save_log=True, save_macros=True):
        '''Terminates fldigi. Sent as a bitmask specifying data to save: 0=options; 1=log; 2=macros

        :param save_options: True to save options; False otherwise.
        :type save_options: bool

        :param save_log: True to save log; False otherwise
        :type save_log: bool

        :param save_macros: True to save macros; False otherwise
        :type save_macros: bool

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.terminate()
        '''
        bitmask = int('0b{}{}{}'.format(int(save_macros), int(save_log), int(save_options), 0))
        self.client.fldigi.terminate(bitmask)

    def delay(self, milliseconds):
        '''Simple delay / blocking call

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.delay(100)  # 100 millisecond delay
        '''
        time.sleep(int(milliseconds / 1000.0))

    class Main(object):

        def __init__(self, client):
            self.client = client

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
        def frequency(self):
            '''Returns the RF carrier frequency

            :getter: Returns the RF carrier frequency, in Hz.
            :setter: Sets the RF carrier frequency, in Hz.
            :type: float

            :Example:

            >>> import pyfldigi
            >>> fldigi = pyfldigi.Client()
            >>> fldigi.main.frequency  # read to demonstrate its initial value
            7070200.0
            >>> fldigi.main.frequency = 7000000.0  # Set to 7 MHz
            >>> fldigi.main.frequency  # read back to demonstrate that it changed
            7000000.0
            '''
            return self.client.main.get_frequency()

        @frequency.setter
        def frequency(self, freq):
            '''Sets the RF carrier frequency. Returns the old value
            NOTE: sphinx ignores docstrings from setters, the documentation is above under the @property'''
            self.client.main.set_frequency(float(freq))

        def increment_frequency(self, freq):
            '''Increments the RF carrier frequency. Returns the new value

            :Example:

            >>> import pyfldigi
            >>> fldigi = pyfldigi.Client()
            >>> fldigi.main.frequency  # read to demonstrate its initial value
            7000000.0
            >>> fldigi.main.increment_frequency(200)  # Increment by 200 Hz
            >>> fldigi.main.frequency  # read back to demonstrate that it changed
            7000000.0
            '''
            return self.client.main.inc_frequency(float(freq))

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
            '''Returns the squelch level

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
            self.client.main.set_squelch_level(float(level))

        def increment_squelch_level(self, inc):
            '''Increments the squelch level. Returns the new level
            :type: float

            :Example:

            >>> import pyfldigi
            >>> fldigi = pyfldigi.Client()
            >>> fldigi.main.squelch_level  # read to demonstrate its initial value
            5.0
            >>> fldigi.main.increment_squelch_level(1.5)  # Increment by 1
            >>> fldigi.main.squelch_level  # read back to demonstrate that it changed
            6.5
            >>> fldigi.main.increment_squelch_level(-1.5)  # Decrement by 1
            >>> fldigi.main.squelch_level  # read back to demonstrate that it changed
            5.0
            '''
            self.client.main.inc_squelch_level(float(inc))  # I was getting erratic return values from this function...
            return self.squelch_level  # So request and return the level here.

        @property
        def reverse(self):
            '''The Reverse Sideband state (whether or not the mark and space are reversed)

            :getter: Returns the Reverse Sideband state
            :setter: Sets the Reverse Sideband state.
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

        def get_trx_status(self):
            '''Returns transmit/tune/receive status
            returns: ['tx', 'rx', 'tune'] ??
            '''
            return self.client.main.get_trx_status()

        def get_trx_state(self):
            '''Returns T/R state
            returns ['RX', 'TX']
            '''
            return self.client.main.get_trx_state()

        def rx(self):
            '''Puts fldigi into receive mode.

            :Example:

            >>> import pyfldigi
            >>> fldigi = pyfldigi.Client()
            >>> fldigi.main.tx()  # Put flgidigi into transmit mode
            >>> fldigi.delay(1000)  # wait a bit
            >>> fldigi.main.rx()  # Put flgidigi into receive mode
            '''
            return self.client.main.rx()

        def tx(self):
            '''Puts fldigi into transmit mode.

            :Example:

            >>> import pyfldigi
            >>> fldigi = pyfldigi.Client()
            >>> fldigi.main.tx()  # Put flgidigi into transmit mode
            >>> fldigi.delay(1000)  # wait a bit
            >>> fldigi.main.rx()  # Put flgidigi into receive mode
            '''
            return self.client.main.tx()

        def tune(self):
            '''Puts fldigi into tune mode.

            :Example:

            >>> import pyfldigi
            >>> fldigi = pyfldigi.Client()
            >>> fldigi.main.tune()  # Put flgidigi into tune mode
            '''
            return self.client.main.tune()

        def abort(self):
            '''Aborts a transmit or tune

            :Example:

            >>> import pyfldigi
            >>> fldigi = pyfldigi.Client()
            >>> fldigi.main.tx()  # Put flgidigi into transmit mode
            >>> fldigi.delay(10)  # wait a bit
            >>> fldigi.main.abort()  # abort the transmit
            '''
            return self.client.main.abort()

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

    class Rx(object):

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

    class Tx(object):

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

        def send(self, text):
            '''Blocking call to 'send
            '''
            self.clear()
            self.client.text.add_tx(str(text))
            self.client.main.tx()  # set transmit
            while(1):
                status = self.client.main.get_trx_status()
                print(status)
                if status == 'rx':
                    break
                print(self.get_tx_data())
                time.sleep(.1)
            # wait until all words have transmitted
            self.client.main.rx()  # set receive

        def abort(self):
            '''main.abort  n:n Aborts a transmit or tune
            '''
            return self.client.main.abort()
