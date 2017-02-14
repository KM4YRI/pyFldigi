'''

.. TODO:: Currently, the 'save' functionality does not work.  To preserve comments and other formatting, a bit of work
      will be needed to write a custom regex-based string subset modifier.

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

    '''Placeholder for fldigi.prefs config read/write

      :param config_dir: The directory in which fldigi reads and writes its config files.  e.g. 'C:/Users/njansen/fldigi.files/'
      :type config_dir: str
      :param read_now: If True, read() is called immediately at the end of the constructor.  Otherwise, a read is not done until explicitly called.
      :type read_now: bool

    :Example:

    >>> import pyfldigi
    >>> xc = pyfldigi.XmlConfig(config_dir)

    .. automethod:: pyfldigi.xmlconfig.XmlConfig.__getitem__
    .. automethod:: pyfldigi.xmlconfig.XmlConfig.__setitem__
    .. automethod:: pyfldigi.xmlconfig.XmlConfig.__str__

    '''

    def __init__(self, config_dir, read_now=True):
        # TODO: Check to make sure that the location is valid, and that the name is fldigi_def.xml
        self.config_dir = config_dir
        self.location = os.path.join(config_dir, 'fldigi_def.xml')
        self.settings = {}
        self.dirty = False
        if read_now is True:
            self.read()

    def read(self):
        '''Open and parse the config XML file.
        :Example:

        >>> import pyfldigi
        >>> xc = pyfldigi.XmlConfig(config_dir, read_now=False)
        >>> # do some other stuff
        >>> xc.read()
        >>> xc['baz']  # Read some random setting named 'baz'
        42
        '''
        self.settings = {}
        self.dirty = False
        self.tree = ElementTree.parse(self.location)
        self.root = self.tree.getroot()
        if not self.root.tag == 'FLDIGI_DEFS':
            raise Exception('Expected root tag to be \'FLDIGI_DEFS\' but got {}'.format(self.root.tag))
        for child in self.root:
            self.settings[str(child.tag).lower()] = child.text

    def save(self):
        '''Save the config.  Will only write to the file if changes have been made (self.dirty is True)

        :Example:

        >>> import pyfldigi
        >>> xc = pyfldigi.XmlConfig(config_dir)
        >>> xc['baz'] = 42
        >>> xc.save()
        '''
        if self.dirty is True:
            # Delete the xml-old, if present
            pass

    def __str__(self):
        '''Prints out all of the settings in a manner of: '{name} : {value}\n'

        :Example:

        >>> import pyfldigi
        >>> xc = pyfldigi.XmlConfig(config_dir)
        >>> str(xc)
        SETTING1 : 0
        SETTING2 : 1
        # and so on
        '''
        s = ''
        for key, value in self.settings.items():
            s += ('{} : {}\n'.format(key, value))
        return s

    def __getitem__(self, key):
        '''Get a setting from the XML config, by its XML tag name

        :Example:

        >>> import pyfldigi
        >>> xc = pyfldigi.XmlConfig(config_dir)
        >>> xc['XMLRIGDEVICE']
        'COM1'
        '''
        return self.settings[str(key).lower()]  # case insensitive

    def __setitem__(self, key, value):
        '''Update a setting value.

          :param key: The XML tag name
          :type key: str
          :param value: description
          :type value: str, bool, int, or float.

        .. note:: Settings aren't written until save() is called!

        .. note:: Strings will be escaped because this is an XML file.  '<', '>', etc. will be replaced as required.

        .. todo:: boolean values will be encoded as '1' or '0'

        :Example:

        >>> import pyfldigi
        >>> xc = pyfldigi.XmlConfig(config_dir)
        >>> xc['XMLRIGDEVICE']
        'COM1'
        >>> xc['XMLRIGDEVICE'] = 'COM5'
        >>> xc['XMLRIGDEVICE']
        'COM5'
        >>> xc.save()  # Settings aren't written until save() is called!
        '''

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

    def set_serial_port(self, comport):
        '''Sets the serial port device in the config.

          :param comport: The com port, e.g. 'COM1' or '/dev/ttys1'
          :type comport: str

        .. note::
            There are two COM ports in the config (XMLRIGDEVICE and HAMRIGDEVICE).
            One for XML-RPC (flrig) and one for HamRig.
            Set both because they're mutually exclusive.
        '''
        self['XMLRIGDEVICE'] = str(comport)
        self['HAMRIGDEVICE'] = str(comport)

    def set_sound_card(self):
        '''
        PORTINDEVICE is None if not defined.  Or a str (e.g. 'Microphone (USB Audio Codec)' if defined)
        PORTININDEX is -1 if not defined.  Or the current index of the sound card (9)
        PORTOUTDEVICE is None if not defined.  Or a str (e.g. 'Speakers (High Definition Audio to Speakers (USB Audio Codec)')
        AUDIOIO ?? changed from 3 to 1
        PORTOUTINDEX -1 or a valid index.
        '''
        pass



class XmlMonitor(object):

    '''A useful tool for figuring out which XML parameter is correlated with a particular
    setting in the FLDIGI GUI.  It will monitor for changes to the config file, and print
    any changes to the console as they happen.  Make sure to press 'save settings' after
    making your setting!  The actual monitoring happens in a thread, so it is non-blocking.

    :param config_dir: The directory in which fldigi reads and writes its config files.  e.g. 'C:/Users/njansen/fldigi.files/'
    :type config_dir: str (path to folder)
    :param start: If True, the monitoring will start immediately.  if False, start() must be called.
    :type start: bool

    .. note::
        All changed settings are logged by default using the Python logger framework, to the
        configuration directory, as 'XmlMonitor.log'

    .. note:: Press Ctrl-C to stop, or set a timeout before running.

    :Example:

    >>> import pyfldigi
    >>> xc = pyfldigi.XmlMonitor(config_dir)
    2017-02-05 16:36:29,129 : XmlMonitor : Monitoring C:/Users/jeff/fldigi.files/fldigi_def.xml...
    2017-02-05 16:36:47,252 : XmlMonitor : MYANTENNA changed from 'dipole' to 'yagi'
    2017-02-05 16:36:51,279 : XmlMonitor : MYANTENNA changed from 'yagi' to 'magloop'
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
        '''Start monitoring the XML.  This launches a monitoring thread, therefore start() is non-blocking.'''
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._threadworker)
            self._timer.start()
            self.is_running = True

    def stop(self):
        '''Stop monitoring the XML.  Stops the thread.  Can be restarted with start().'''
        self._timer.cancel()
        self.is_running = False

    def _threadworker(self):
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
