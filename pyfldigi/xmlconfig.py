'''
'''
import os
import sys
import time
import signal
import logging
import threading
from xml.etree import ElementTree
from xml.sax.saxutils import escape


class XmlConfig(object):

    '''Placeholder for fldigi.prefs config read/write'''

    def __init__(self, config_dir, read_now=True):
        # TODO: Check to make sure that the location is valid, and that the name is fldigi_def.xml
        self.config_dir = config_dir
        self.location = os.path.join(config_dir, 'fldigi_def.xml')
        self.settings = {}
        self.dirty = False
        if read_now is True:
            self.read()

    def read(self):
        '''Open and parse the config XML file'''
        self.settings = {}
        self.dirty = False
        self.tree = ElementTree.parse(self.location)
        self.root = self.tree.getroot()
        if not self.root.tag == 'FLDIGI_DEFS':
            raise Exception('Expected root tag to be \'FLDIGI_DEFS\' but got {}'.format(self.root.tag))
        for child in self.root:
            self.settings[str(child.tag).lower()] = child.text

    def save(self):
        if self.dirty is True:
            # Delete the xml-old, if present
            pass

    def __str__(self):
        s = ''
        for key, value in self.settings.items():
            s += ('{} : {}\n'.format(key, value))
        return s

    def __getitem__(self, key):
        return self.settings[str(key).lower()]  # case insensitive

    def __setitem__(self, key, value):
        # TODO: Escape strings with XML safe values
        # TODO: Encode bool's as 1 or 0
        if isinstance(value, str):
            value = escape(value)
        elif isinstance(value, bool):
            value = str(int(value))
        elif isinstance(value, (int, float)):
            value = str(value)
        else:
            raise TypeError('Types supported are bool, str, float, or int.  If you are purposely setting another type, please cast it to one of these.')
        try:
            self.settings[key] = value
            self.dirty = True
        except KeyError:
            raise KeyError('Not a valid configuration item')

    # #####################################################################################
    # Highly used items have their own methods below

    def set_comport(self, comport):
        '''Note that there are two COM ports in the config.  One for XML-RPC (flrig) and one for HamRig.
        Set both because they're mutually exclusive.
        XMLRIGDEVICE
        HAMRIGDEVICE
        '''
        self['XMLRIGDEVICE'] = str(comport)
        self['HAMRIGDEVICE'] = str(comport)


class XmlMonitor(object):

    '''A useful tool for figuring out which XML parameter is correlated with a particular
    setting in the FLDIGI GUI.  It will monitor for changes to the config file, and print
    any changes to the console as they happen.  Make sure to press 'save settings' after
    making your setting!  The actual monitoring happens in a thread, so it is non-blocking.

    Note that all changed settings are logged by default, to the configuration directory,
    as 'XmlMonitor.log'

    Press Ctrl-C to stop, or set a timeout before running.
    '''

    def __init__(self, config_dir, start=True):
        self.config_dir = config_dir
        self.location = os.path.join(config_dir, 'fldigi_def.xml')
        self.mtime = os.path.getmtime(self.location)  # File modification time
        # Load the XML and get the settings
        self.settings = XmlConfig(config_dir).settings

        # Setup the logger
        self.logger = logging.getLogger('pyfldigi.config.XmlMonitor')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s : XmlMonitor : %(message)s')
        self.fh = logging.FileHandler(os.path.join(config_dir, 'XmlMonitor.log'))
        self.sh = logging.StreamHandler()
        self.fh.setLevel(logging.INFO)
        self.sh.setLevel(logging.INFO)
        self.fh.setFormatter(formatter)
        self.sh.setFormatter(formatter)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh)

        self.logger.info('Monitoring {}...'.format(self.location))

        # Setup the thread
        self._timer = None
        self.interval = 2
        self.is_running = False
        if start is True:
            self.start()

        # register SIGINT signal
        signal.signal(signal.SIGINT, self.stop)

    def start(self):
        '''Start monitoring the XML'''
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self.threadworker)
            self._timer.start()
            self.is_running = True

    def stop(self):
        '''Stop monitoring the XML'''
        self._timer.cancel()
        self.is_running = False

    def wait(self, timeout=None):
        self.timeout = timeout
        pass

    def threadworker(self):
        self.is_running = False
        self.start()
        mtime = os.path.getmtime(self.location)
        if mtime != self.mtime:
            # The file has been modified.  Parse the new settings
            new = XmlConfig(self.config_dir).settings
            old = self.settings
            for key, value in old.items():
                try:
                    if new[key] != value:
                        self.logger.info('{} changed from {} to {}'.format(key.upper(), value, new[key]))
                except KeyError:
                    pass  # TBD
            self.settings = new
            self.mtime = mtime

    def _isFileChanged(self):
        '''tbd'''
        return False
