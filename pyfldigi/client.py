'''http://www.w1hkj.com/FldigiHelp-3.21/html/xmlrpc_control_page.html'''

import time
import xmlrpc.client


class Client(object):

    def __init__(self, ip_address='127.0.0.1', port=7362):
        self.ip_address = ip_address
        self.port = port
        self.client = xmlrpc.client.ServerProxy('http://{}:{}/'.format(ip_address, port))
        self.modem = Client.Modem(self.client)
        self.main = Client.Main(self.client)
        self.rig = Client.Rig(self.client)
        # self.log = Client.Log(self.client)
        self.rx = Client.Rx(self.client)
        self.tx = Client.Tx(self.client)
        self.spotter = Client.Spot(self.client)
        self.flmsg = Client.Flmsg(self.client)

    @property
    def methods(self):
        '''Returns the list of methods'''
        return self.client.fldigi.list()

    @property
    def name(self):
        '''Returns the program name and version'''
        return self.client.fldigi.name()

    @property
    def version(self):
        '''Returns the program version as a python dict'''
        return self.client.fldigi.version_struct()

    @property
    def config_dir(self):
        '''Returns the name of the configuration directory'''
        return self.client.fldigi.terminate()

    def terminate(self, save_options=True, save_log=True, save_macros=True):
        '''Terminates fldigi. ``i'' is bitmask specifying data to save: 0=options; 1=log; 2=macros'''
        bitmask = int('0b{}{}{}'.format(int(save_macros), int(save_log), int(save_options), 0))
        return self.client.fldigi.terminate(bitmask)

    def delay(self, milliseconds):
        '''Simple delay / blocking call'''
        time.sleep(int(milliseconds / 1000.0))

    class Modem(object):

        '''http://www.w1hkj.com/FldigiHelp-3.21/html/modems_page.html'''

        def __init__(self, client):
            self.client = client
            self.olivia = Client.Olivia(client)
            self.wefax = Client.Wefax(client)
            self.navtex = Client.Navtex(client)

        @property
        def name(self):
            '''Returns the name of the current modem'''
            return self.client.modem.get_name()

        @name.setter
        def name(self, value):
            '''Sets the current modem.
            Valid names: ['NULL', 'CW', 'CTSTIA', 'DOMEX4', 'DOMEX5', 'DOMEX8', 'DOMX11', 'DOMX16', 'DOMX22', 'DOMX44',
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
                'PSK800RC2', 'PSK1000RC2', 'FSQ', 'IFKP', 'SSB', 'WWV', 'ANALYSIS', 'FREQSCAN']'''
            self.client.modem.set_by_name(str(value))

        @property
        def names(self):
            '''Returns all modem names'''
            return self.client.modem.get_names()

        @property
        def id(self):
            '''Returns the ID of the current modem'''
            return self.client.modem.get_id()

        @id.setter
        def id(self, value):
            '''Sets the current modem.'''
            self.client.modem.set_by_id(int(value))

        @property
        def max_id(self):
            '''Returns the maximum modem ID number'''
            return self.client.modem.get_max_id()

        @property
        def carrier(self):
            '''Returns the modem carrier frequency'''
            return self.client.modem.get_carrier()

        @carrier.setter
        def carrier(self, freq):
            '''Sets modem carrier.'''
            self.client.modem.set_carrier(int(freq))

        def increment_carrier(self, inc):
            '''Increments the modem carrier frequency. Returns the new carrier'''
            return self.client.modem.inc_carrier(int(inc))

        @property
        def afc_search_range(self):
            '''Returns the modem AFC [auto frequency control] search range'''
            return self.client.modem.get_afc_search_range()

        @afc_search_range.setter
        def afc_search_range(self, range):
            '''Sets the modem AFC [auto frequency control] search range.'''
            self.client.modem.set_afc_search_range(int(range))

        def increment_afc_search_range(self, inc):
            '''Increments the modem AFC [auto frequency control] search range. Returns the new value'''
            return self.client.modem.inc_afc_search_range(int(inc))

        @property
        def bandwidth(self):
            '''Returns the modem bandwidth'''
            return self.client.modem.get_bandwidth()

        @bandwidth.setter
        def bandwidth(self, bandwidth):
            '''Sets the modem bandwidth.'''
            self.client.modem.set_bandwidth(int(bandwidth))

        def increment_bandwidth(self, inc):
            '''Increments the modem bandwidth. Returns the new value'''
            return self.client.modem.inc_bandwidth(int(inc))

        @property
        def quality(self):
            '''Returns the modem signal quality in the range [0:100]'''
            return self.client.modem.get_quality()

        def search_up(self):
            '''Searches upward in frequency'''
            return self.client.modem.search_up()

        def search_down(self):
            '''Searches downward in frequency'''
            return self.client.modem.search_down()

    class Olivia(object):

        def __init__(self, client):
            self.client = client

        @property
        def bandwidth(self):
            '''Returns the Olivia bandwidth'''
            return self.client.modem.olivia.get_bandwidth()

        @bandwidth.setter
        def bandwidth(self, bandwidth):
            '''Sets the Olivia bandwidth'''
            self.client.modem.olivia.set_bandwidth(int(bandwidth))

        @property
        def tones(self):
            '''modem.olivia.get_tones  i:n Returns the Olivia tones'''
            return self.client.modem.olivia.get_tones()

        @tones.setter
        def tones(self, tones):
            '''Sets the Olivia tones'''
            self.client.modem.olivia.set_tones(int(tones))

    class Wefax(object):

        def __init__(self, client):
            self.client = client

        def get_engine_state(self):
            '''Returns Wefax engine state (tx and rx) for information.'''
            return self.client.wefax.state_string()

        def skip_apt(self):
            '''Skip APT during Wefax reception'''
            return self.client.wefax.skip_apt()

        def skip_phasing(self):
            '''wefax.skip_phasing              : s:n   : Skip phasing during Wefax reception'''
            return self.client.wefax.skip_phasing()

        def set_tx_abort_flag(self):
            '''wefax.set_tx_abort_flag         : s:n   : Cancels Wefax image transmission'''
            return self.client.wefax.set_tx_abort_flag()

        def end_reception(self):
            '''wefax.end_reception             : s:n   : End Wefax image reception'''
            return self.client.wefax.end_reception()

        def start_manual_reception(self):
            '''wefax.start_manual_reception    : s:n   : Starts fax image reception in manual mode'''
            return self.client.wefax.start_manual_reception()

        def set_adif_log(self, logging):
            '''wefax.set_adif_log              : s:b   : Set/reset logging to received/transmit images to ADIF log file'''
            return self.client.wefax.set_adif_log(bool(logging))

        def set_max_lines(self, lines):
            '''wefax.set_max_lines             : s:i   : Set maximum lines for fax image reception'''
            return self.client.wefax.set_max_lines(int(lines))

        def get_received_file(self, timeout):
            '''Waits for next received fax file, returns its name with a delay. Empty string if timeout.'''
            return self.client.wefax.get_received_file(int(timeout))

        def send_file(self, filename, param):
            '''Send file. returns an empty string if OK otherwise an error message.'''
            with open(filename, mode='rb') as f:
                img = f.read()
                img = img.decode('iso-8859-1')  # must be sent out as a string
                return self.client.wefax.send_file(img, param)

    class Navtex(object):

        def __init__(self, client):
            self.client = client

        def get_msg(self, timeout):
            '''Returns next Navtex/SitorB message with a max delay in seconds.. Empty string if timeout.'''
            return self.client.navtex.get_message(int(timeout))

        def send_msg(self, msg):
            '''Send a Navtex/SitorB message. Returns an empty string if OK otherwise an error message.'''
            resp = self.client.navtex.send_message(str(msg))
            if resp != '':
                raise Exception('Unable to send NAVTEX message.  Error message returned: {}'.format(resp))

    class Main(object):

        def __init__(self, client):
            self.client = client

        @property
        def status1(self):
            '''Returns the contents of the first status field (typically s/n)'''
            return self.client.main.get_status1()

        @property
        def status2(self):
            '''Returns the contents of the second status field'''
            return self.client.main.get_status2()

        @property
        def wf_sideband(self):
            '''Returns the current waterfall sideband (either USB or LSB)'''
            return self.client.main.get_wf_sideband()

        @wf_sideband.setter
        def set_wf_sideband(self, sideband):
            '''Sets the waterfall sideband to USB or LSB'''
            if str(sideband) not in ['USB', 'LSB']:
                raise ValueError('sideband must be USB or LSB')
            self.client.main.set_wf_sideband(str(sideband))

        @property
        def frequency(self):
            '''Returns the RF carrier frequency'''
            return self.client.main.get_frequency()

        @frequency.setter
        def frequency(self, freq):
            '''Sets the RF carrier frequency. Returns the old value'''
            return self.client.main.set_frequency(float(freq))

        def increment_frequency(self, freq):
            '''Increments the RF carrier frequency. Returns the new value'''
            return self.client.main.inc_frequency(float(freq))

        @property
        def afc(self):
            '''Returns the AFC [auto frequency control] state'''
            return bool(self.client.main.get_afc())

        @afc.setter
        def afc(self, afc):
            '''Sets the AFC [auto frequency control] state.'''
            if not isinstance(afc, bool):
                raise TypeError('afc must be a bool')
            self.client.main.set_afc(bool(afc))

        @property
        def squelch(self):
            '''Returns the squelch state'''
            return bool(self.client.main.get_squelch())

        @squelch.setter
        def squelch(self, squelch):
            '''Returns the old state'''
            if not isinstance(squelch, bool):
                raise TypeError('squelch state must be a bool')
            return self.client.main.set_squelch(bool(squelch))

        @property
        def squelch_level(self):
            '''Returns the squelch level'''
            return self.client.main.get_squelch_level()

        @squelch_level.setter
        def squelch_level(self, level):
            '''Sets the squelch level. Returns the old level'''
            self.client.main.set_squelch_level(float(level))

        def increment_squelch_level(self, inc):
            '''main.inc_squelch_level  d:d Increments the squelch level. Returns the new level'''
            return self.client.main.inc_squelch_level(float(inc))

        @property
        def reverse(self):
            '''Returns the Reverse Sideband state'''
            return bool(self.client.main.get_reverse())

        @reverse.setter
        def reverse(self, state):
            '''Sets the Reverse Sideband state.'''
            self.client.main.set_reverse(bool(state))

        @property
        def lock(self):
            '''Returns the Transmit [frequency] Lock state'''
            return bool(self.client.main.get_lock())

        def set_lock(self, lock=True):
            '''Sets the Transmit [frequency] Lock state.'''
            self.client.main.set_lock(bool(lock))

        @lock.setter
        def lock(self, value):
            '''Sets the Transmit [frequency] Lock state.'''
            self.set_lock(value)

        @property
        def rsid(self):
            '''Returns the RSID state'''
            return bool(self.client.main.get_rsid())

        @rsid.setter
        def set_rsid(self, value):
            '''Sets the RSID state.'''
            self.client.main.set_rsid(bool(value))

        def get_trx_status(self):
            '''Returns transmit/tune/receive status
            returns: ['tx', 'rx', 'tune'] ??'''
            return self.client.main.get_trx_status()

        def get_trx_state(self):
            '''Returns T/R state
            returns ['RX', 'TX']'''
            return self.client.main.get_trx_state()

        def rx(self):
            '''Receives'''
            return self.client.main.rx()

        def tx(self):
            '''Transmits'''
            return self.client.main.tx()

        def tune(self):
            '''Tunes'''
            return self.client.main.tune()

        def abort(self):
            '''main.abort  n:n Aborts a transmit or tune'''
            return self.client.main.abort()

        def run_macro(self, macroNum):
            '''Runs a macro'''
            return self.client.main.run_macro(int(macroNum))

        def get_max_macro_id(self):
            '''Returns the maximum macro ID number'''
            return self.client.main.get_max_macro_id()

    class Flmsg(object):

        def __init__(self, client):
            self.client = client

        @property
        def online(self):
            '''flmsg online indication'''
            return bool(self.client.main.flmsg_online())

        @property
        def available(self):
            '''flmsg data available'''
            return bool(self.client.main.flmsg_available())

        def transfer(self):
            '''data transfer to flmsg'''
            return bool(self.client.main.flmsg_transfer())

        @property
        def squelch(self):
            '''Returns the squelch state.'''
            return bool(self.client.main.flmsg_squelch())

    class Rig(object):

        def __init__(self, client):
            self.client = client

        @property
        def name(self):
            '''Returns the rig name previously set via rig.set_name'''
            return self.client.rig.get_name()

        @name.setter
        def name(self, name):
            '''Sets the rig name for xmlrpc rig'''
            return self.client.rig.set_name(str(name))

        def set_frequency(self, freq):
            '''Sets the RF carrier frequency. Returns the old value'''
            return self.client.rig.set_frequency(float(freq))

        @property
        def modes(self):
            '''Returns the list of available rig modes'''
            return self.client.rig.get_modes()

        @modes.setter
        def modes(self, value):
            '''Sets the list of available rig modes'''
            self.client.rig.set_modes(value)

        @property
        def mode(self):
            '''Returns the name of the current transceiver mode'''
            return self.client.rig.get_mode()

        @mode.setter
        def mode(self, value):
            '''Selects a mode previously added by rig.set_modes'''
            self.client.rig.set_mode(str(value))

        @property
        def bandwidths(self):
            '''Returns the list of available rig bandwidths'''
            return self.client.rig.get_bandwidths()

        @bandwidths.setter
        def bandwidths(self, bandwidths):
            '''Sets the list of available rig bandwidths'''
            self.client.rig.set_bandwidths(bandwidths)

        @property
        def bandwidth(self):
            '''rig.get_bandwidth   s:n Returns the name of the current transceiver bandwidth'''
            return self.client.rig.get_bandwidth()

        @bandwidth.setter
        def bandwidth(self, bandwidth):
            '''Selects a bandwidth previously added by rig.set_bandwidths'''
            self.client.rig.set_bandwidth(bandwidth)

        def take_control(self):
            '''rig.take_control    n:n Switches rig control to XML-RPC'''
            return self.client.rig.take_control()

        def release_control(self):
            '''rig.release_control n:n Switches rig control to previous setting'''
            return self.client.rig.release_control()

    class Log(object):

        def __init__(self, client):
            self.client = client

        # def get_frequency(self):
        #     '''log.get_frequency   s:n Returns the Frequency field contents'''
        #     return self.client.log.get_frequency()

        # def get_time_on(self):
        #     '''log.get_time_on s:n Returns the Time-On field contents'''
        #     return self.client.log.get_time_on()

        # def get_time_off(self):
        #     '''log.get_time_off    s:n Returns the Time-Off field contents'''
        #     return self.client.log.get_time_off()

        # def get_call(self):
        #     '''log.get_call    s:n Returns the Call field contents'''
        #     return self.client.log.get_time_off()

        # def get_name(self):
        #     '''log.get_name    s:n Returns the Name field contents'''
        #     return self.client.log.get_name()

        # def get_rst_in(self):
        #     '''log.get_rst_in  s:n Returns the RST(r) field contents'''
        #     return self.client.log.get_rst_in()

        # def get_rst_out(self):
        #     '''log.get_rst_out s:n Returns the RST(s) field contents'''
        #     return self.client.log.get_rst_out()

        # def get_serial_number(self):
        #     '''log.get_serial_number   s:n Returns the serial number field contents'''
        #     return self.client.log.get_serial_number()

        # def set_serial_number(self):
        #     '''log.set_serial_number   n:s Sets the serial number field contents'''
        #     return self.client.log.set_serial_number()

        # def get_serial_number_sent(self):
        #     '''log.get_serial_number_sent  s:n Returns the serial number (sent) field contents'''
        #     return self.client.log.get_serial_number_sent()

        # def get_exchange(self):
        #     '''log.get_exchange    s:n Returns the contest exchange field contents'''
        #     return self.client.log.get_exchange()

        # def set_exchange(self):
        #     '''log.set_exchange    n:s Sets the contest exchange field contents'''
        #     return self.client.log.set_exchange()

        # def get_state(self):
        #     '''log.get_state   s:n Returns the State field contents'''
        #     return self.client.log.get_state()

        # def get_province(self):
        #     '''log.get_province    s:n Returns the Province field contents'''
        #     return self.client.log.get_province()

        # def get_country(self):
        #     '''log.get_country s:n Returns the Country field contents'''
        #     return self.client.log.get_country()

        # def get_qth(self):
        #     '''log.get_qth s:n Returns the QTH field contents'''
        #     return self.client.log.get_qth()

        # def get_band(self):
        #     '''log.get_band    s:n Returns the current band name'''
        #     return self.client.log.get_band()

        # def get_notes(self):
        #     '''log.get_notes   s:n Returns the Notes field contents'''
        #     return self.client.log.get_notes()

        # def get_locator(self):
        #     '''log.get_locator s:n Returns the Locator field contents'''
        #     return self.client.log.get_locator()

        # def get_az(self):
        #     '''log.get_az  s:n Returns the AZ field contents'''
        #     return self.client.log.get_az()

        # def clear(self):
        #     '''log.clear   n:n Clears the contents of the log fields'''
        #     return self.client.log.clear()

        # def set_call(self):
        #     '''log.set_call    n:s Sets the Call field contents'''
        #     return self.client.log.set_call()

        # def set_name(self):
        #     '''log.set_name    n:s Sets the Name field contents'''
        #     return self.client.log.set_name()

        # def set_qth(self):
        #     '''log.set_qth n:s Sets the QTH field contents'''
        #     return self.client.log.set_qth()

        # def set_locator(self):
        #     '''log.set_locator n:s Sets the Locator field contents'''
        #     return self.client.log.set_locator()

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
            '''Returns all RX data received since last query.'''
            resp = self.client.rx.get_data()
            if isinstance(resp, str):
                self.buff += resp

        def clear(self):
            '''Clears the RX text widget'''
            self.client.text.clear_rx()
            self.buff = ''

    class Tx(object):

        def __init__(self, client):
            self.client = client
            self.buff = ''

        def __str__(self):
            return self.buff

        def __iadd__(self, other):
            '''Adds a string to the TX text widget'''
            if isinstance(other, bytes):
                return self.client.text.add_tx_bytes(other)
            elif isinstance(other, str):
                return self.client.text.add_tx(other)
            else:
                raise TypeError('text must be in bytes or str format')

        def clear(self):
            '''Clears the TX text widget'''
            return self.client.text.clear_tx()

        def get_tx_data(self):
            '''Returns all TX data transmitted since last query.'''
            return self.client.tx.get_data()

        def send(self, text):
            '''Blocking call to 'send'''
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
            '''main.abort  n:n Aborts a transmit or tune'''
            return self.client.main.abort()

    class Spot(object):

        def __init__(self, client):
            self.client = client

        @property
        def auto(self):
            '''spot.get_auto   b:n Returns the autospotter state'''
            return self.client.spot.get_auto()

        @auto.setter
        def auto(self, state):
            '''spot.set_auto   n:b Sets the autospotter state. Returns the old state'''
            return self.client.spot.set_auto(bool(state))

        @property
        def pskrep_count(self):
            '''spot.pskrep.get_count   i:n Returns the number of callsigns spotted in the current session'''
            return self.client.spot.pskrep.get_count()

    class Io(object):

        def __init__(self, client):
            self.client = client

        def in_use(self):
            '''Returns the IO port in use (ARQ/KISS).'''
            return self.client.io.in_use()

        def enable_kiss(self):
            '''Switch to KISS I/O'''
            self.client.io.enable_kiss()

        def enable_arq(self):
            '''Switch to ARQ I/O'''
            self.client.io.enable_arq()
