pyFldigi
========

Summary / Context
-----------------

pyFldigi is a small Python library that can control the Fldigi
application via XML-RPC.

Fldigi is a digital modem application that is widely used in the amateur
radio community. It acts as a digital modem, intended to be coupled with
a standard SSB or FM transceiver radio.

Features
--------

-  Full implementation of the available `XML-RPC client`_ commands]
-  Get FLDIGI version, name, etc.
-  **Modem**: Get and set the modem type, carrier frequency, bandwidth,
   etc.
-  **Modem**: Get and set various modem configuration options for
   Olivia, WEFAX, and NAVTEX
-  **Transmit**: Set RX/TX mode to Transmit, Receive, or Tune.
-  Abort a transmit or tune.
-  **Squelch**: Get or set the squelch
-  **Rig control**: Get or set various rig controls, such as frequency,
   mode, etc.
-  **Logging**: Get and set various log field contents. This is in the
   context of ham contact logs, not debug logs.
-  **Text**: Send text to FLdigi to be transmitted
-  **Text**: Get text from FLdigi that has been received
-  **Terminate the Program**: Terminate the program gracefully by asking
   it to close.
-  Application monitoring and launching. It is possible to launch FLdigi
   from a Python command, and monitor it. Also the program can be killed
   if it refuses to shut down gracefully.
-  **Configuration**: TBD. Reading and writing of the configuration
   file(s). Requires a restart of FLdigi.

Applications and Intended Usage
-------------------------------

-  Remote weather stations.
-  Portable HF setups. Typically, HF digital setups are bulky and
   require several interconnected pieces of hardware, usually via audio
   cables. This library, along with some custom hardware, could allow a
   walkie-talkie sized HF digital radio that’s completely integrated.
-  Emcomm
-  ‘Headless’ operation on a Raspberry Pi, BeagleBone, or any number of
   other Linux-based single-board computers.
-  Putting a more ‘user-friendly’ GUI on top of FLdigi.
-  Web enabled FLDIGI via HTML5 and some Javascript, that could be
   accessed from anywhere. Python’s Flask / Django along with Bootstrap,
   and a few REST calls, for example.
-  Allow a phone or tablet to send and receive FLDIGI messages via a
   custom app. There is an Android version of FLDIGI, but that might not
   be the best approach for every problem. A more custom application
   could be created to use only a particular mode and send pre-formatted
   data, for example, with considerably less work than it would be to
   fork the FLDIGI mobile application and update it.

Documentation
=============

API Documentation
-----------------

-  TBD

Useful FLDIGI documentation
---------------------------

-  `FLDIGI Wikipedia page`_
-  `FLDIGI Users Manual - XML-RPC Control`_
-  `FLDIGI Users Manual - Modems`_
-  [FLDIGI Users Manual -
   Configuration](http://www.w1hkj.com/FldigiHelp-3.21/html/conf

.. _XML-RPC client: http://www.w1hkj.com/FldigiHelp-3.21/html/configuration_page.html
.. _FLDIGI Wikipedia page: https://en.wikipedia.org/wiki/Fldigi
.. _FLDIGI Users Manual - XML-RPC Control: http://www.w1hkj.com/FldigiHelp-3.21/html/xmlrpc_control_page.html
.. _FLDIGI Users Manual - Modems: http://www.w1hkj.com/FldigiHelp-3.21/html/modems_page.html