'''
'''


class Log(object):

    '''
    .. note:: An instance of this class automatically gets created under :py:class:`pyfldigi.client.client.Client` when it is constructed.
    '''

    def __init__(self, clientObj):
        self.clientObj = clientObj
        self.client = clientObj.client

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
