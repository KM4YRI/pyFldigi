import http
import time
# import queue
import logging
import threading


STATES = ['TX', 'RX', 'TUNE', 'ERROR']


class _State(object):

    def __init__(self, state):
        self.state = state
        self.start()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value not in STATES:
            raise ValueError('value ({}) must be one of: {}'.format(value, STATES))
        self._state = value

    def start(self):
        self.start_time = time.time()
        self.end_time = None

    def end(self):
        self.end_time = time.time()
        return self.duration

    @property
    def duration(self):
        if self.end_time is None:
            return time.time() - self.start_time
        else:
            return self.end_time - self.start_time

    def __str__(self):
        if self.end_time is None:
            end_time = time.time()
        else:
            end_time = self.end_time
        return '\'{}\' for {:.3f}s (from {:.3f} to {:.3f})'.format(self.state, self.duration, self.start_time, end_time)


class _TxData(object):

    def __init__(self, data):
        self.time = time.time()
        self.data = data

    def __str__(self):
        if isinstance(self.data, bytes):
            data = self.data.decode('iso-8859-1')
        else:
            data = str(self.data)
        if len(self.data) > 25:
            data = '\'{}\'... (length={})'.format(data[0:25], len(data))
        else:
            data = '\'{}\''.format(data)
        return 'T={:.3f}s: {}'.format(self.time, data)


class _History(object):

    def __init__(self, initialState='RX', max_history=900):
        self.logger = logging.getLogger('pyfldigi.client._History')
        self.max_history = max_history
        self.state_history = [_State(initialState)]  # Start the history with the initial state
        self.txdata_history = []

    def __str__(self):
        s = 'State History:\n{}\n'.format('\n'.join(['  {}'.format(str(i)) for i in self.state_history]))
        s += 'TX data History:\n{}\n'.format('\n'.join(['  {}'.format(str(i)) for i in self.txdata_history]))
        s += 'Last TX time was: {}\n'.format(self.get_last_txdata_time())
        return s

    def __repr__(self):
        return str(self)

    def chop(self):
        t = time.time() - self.max_history
        if len(self.txdata_history) > 0:
            if self.state_history[0].end_time is not None:
                if self.state_history[0].end_time <= t:
                    h = []
                    for i in self.state_history:
                        if i.end_time is not None:
                            if i.end_time >= t:
                                h.append(i)
                        else:
                            h.append(i)
                    self.state_history = h
                    # self.state_history = [i for i in self.state_history if (i.end_time >= t)]

        if len(self.txdata_history) > 0:
            if self.txdata_history[0].time <= t:
                self.txdata_history = [i for i in self.txdata_history if (i.time >= t)]

    def update_state(self, new_state):
        if not isinstance(new_state, _State):
            raise TypeError('expected state type to be _State but got {}'.format(type(new_state)))
        last_state = self.state_history[-1].state
        if new_state.state != last_state:
            self.logger.info('STATE CHANGE to {}'.format(new_state.state))
            self.state_history[-1].end()
            self.state_history.append(new_state)
            self.chop()

    def get_duty_cycle(self, sample_period=60):
        '''Returns the duty cycle over a given sample period'''
        on_time = sum([i.duration for i in self.state_history if (i.state == 'TX')])
        off_time = sum([i.duration for i in self.state_history if (i.state != 'TX')])
        # print('on_time: {}s'.format(on_time))
        # print('off_time: {}s'.format(off_time))
        return (on_time / (on_time + off_time)) * 100

    def get_state(self):
        '''Returns the last state'''
        return self.state_history[-1].state

    def append_txdata(self, txdata):
        if txdata is None:
            return  # no data to append
        if not isinstance(txdata, _TxData):
            raise TypeError('expected type to be _TxData but got {}'.format(type(txdata)))
        self.txdata_history.append(txdata)
        self.chop()

    def get_last_txdata_time(self):
        if len(self.txdata_history) > 0:
            return time.time() - self.txdata_history[-1].time
        else:
            return None


class TxMonitor(threading.Thread):

    def __init__(self, clientObj):
        super().__init__()
        self.logger = logging.getLogger('pyfldigi.client.txmonitor')
        self.clientObj = clientObj
        self.client = clientObj.client

        # Modal properties
        self.interval = 1  # Default interval is 1 second
        self.transmitting = False
        self.max_duty_cycle = 95  # percent
        self.max_xmit_time = 2 * 60  # seconds.  should be enough for a modicum amount of ragchewing
        self.max_length = 10000   # characters
        self.xmit_timeout = 1.5  # Timeout after last bit of transmitted data

        self.history = _History()
        self.last_state = None

        # Set up the thread
        self.daemon = True
        self.heartbeat = time.time()
        self.start()

    def run(self):
        self.logger.debug('TXMONITOR: Thread started.')
        while(1):
            try:
                # Get TRX Status
                state = self.clientObj.main.get_trx_state()
                self.last_state = state
                self.history.update_state(_State(state))

                # Get TX Data
                data = self.clientObj.text.get_tx_data(suppress_errors=True)
                if data is not None:
                    if len(data) > 0:
                        self.logger.debug('TXMONITOR: TX DATA: {}'.format(data))
                        self.history.append_txdata(_TxData(data))

                if state == 'TX':
                    self.interval = 0.15  # Speed up the thread rate while transmitting
                    # Check transmitted bytes, see if it's time to change state to RX
                    t = self.history.get_last_txdata_time()
                    if t is None:
                        self.transmitting = True
                    else:
                        if t <= self.xmit_timeout:
                            # bytes are still being transmitted
                            self.transmitting = True
                        else:
                            self.clientObj.main.rx()  # put the state back into receive
                            self.transmitting = False
                            # print('txdata_time = {}'.format(t))
                            self.logger.info('Changing state back to RX... (last transmitted byte was {} seconds ago'.format(t))
                elif state == 'ERROR':
                    break
                else:
                    self.interval = 1  # Speed up the thread rate while transmitting
                    self.transmitting = False

            except Exception as e:
                raise
                print('TXMONITOR: Exception: {}'.format(e))
                pass  # Daemon threads might run after python starts shutting down.  Ignore errors.
            self.heartbeat = time.time()
            time.sleep(self.interval)
        self.logger.debug('TXMONITOR: Thread stopped.')

    def get_state(self):
        return self.history.get_state()

    def get_last_txdata_time(self):
        return self.history.get_last_txdata_time()
