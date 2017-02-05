'''

'''

import time
import logging
import xmlrpc.client
from .main import Main
from .modem import Modem
from .rig import Rig
from .log import Log
from .inputbuff import Inputbuff
from .outputbuff import Outputbuff
from .ioconfig import Io
from .flmsg import Flmsg
from .pskreporter import Spot


class Client(object):

    '''A client that can read/write settings to FLDIGI via XML-RPC protocol

    `Official FLDIGI XML-RPC Protocol Documentation page <http://www.w1hkj.com/FldigiHelp-3.21/html/xmlrpc_control_page.html/>`_
    '''

    def __init__(self, hostname='127.0.0.1', port=7362):
        '''Client() constructor

        :param hostname: IP address of the xml-rpc FLDIGI interface (usually 127.0.0.1)
        :type hostname: str

        :param port: The port of the xml-rpc FLDIGI interfac (usually 7362)
        :type port: int

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client(hostname='127.0.0.1', port=7362)  # <-- Constructor call
        >>> fldigi.name
        'fldigi'
        '''
        self.logger = logging.getLogger('pyfldigi.Client')
        self.ip_address = hostname
        self.port = port
        self.logger.debug('Attempting to connect to connect to fldigi at IP address={}, port={}, via XMP-RPC'.format(self.ip_address, self.port))
        self.client = xmlrpc.client.ServerProxy('http://{}:{}/'.format(self.ip_address, self.port))
        self.main = Main(self.client)
        self.modem = Modem(self.client)
        self.rig = Rig(self.client)
        self.log = Log(self.client)
        self.rx = Inputbuff(self.client)
        self.tx = Outputbuff(self.client)
        self.spot = Spot(self.client)
        self.flmsg = Flmsg(self.client)
        self.io = Io(self.client)

    @property
    def methods(self):
        '''Returns the list of methods in which fldigi can handle via the xml-rpc interface

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
        bitmask = int('0b{}{}{}'.format(int(save_macros), int(save_log), int(save_options)), 0)
        self.client.fldigi.terminate(bitmask)

    def delay(self, milliseconds):
        '''Simple delay / blocking call

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.delay(100)  # 100 millisecond delay
        '''
        time.sleep(int(milliseconds / 1000.0))

    def send(self, text):
        '''Blocking call to transmit a given block of text using the current modem

        TBD
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
        '''Aborts a transmit or tune

        :Example:

        >>> import pyfldigi
        >>> fldigi = pyfldigi.Client()
        >>> fldigi.main.tune()
        >>> fldigi.delay(60)
        >>> fldigi.abort()  # abort the previous commanded tune
        '''
        return self.client.main.abort()

    def receive(self, ):
        '''TBD'''
        pass
