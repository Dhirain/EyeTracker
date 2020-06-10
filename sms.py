from ipaddress import IPv4Address  # for your IP address
from pyairmore.request import AirmoreSession  # to create an AirmoreSession
from pyairmore.services.messaging import MessagingService  # to send messages
import constants

class SMSSender(object):
    def __init__(self,number,message):
        self.ip = IPv4Address("192.168.***.***")  # let's create an IP address object
        # now create a session
        self.session = AirmoreSession(self.ip)
        self.connection = self.session.is_server_running  # True if Airmore is running

        if self.connection:
            was_accepted = self.session.request_authorization()
            service = MessagingService(self.session)
            service.send_message(str(number), message)
            print("SMS send: " + message)

# SMSSender(constants.number, "Test")