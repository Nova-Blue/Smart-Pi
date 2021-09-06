import logging
import os
import time
import requests
import socket
from WOL import WOLClient
from RokuTV import RokuClient
import RSDRemoteClient

from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.launch
def launch():
    speech_text = 'Welcome to Smart Pie'
    return question(speech_text).reprompt(speech_text)


@ask.intent('TVDayModeIntent')
def tv_day():
    tv.day_mode()
    speech_text = 'Done, enjoy your day'
    return statement(speech_text)


@ask.intent('TVNightModeIntent')
def tv_night():
    tv.night_mode()
    speech_text = 'Done, have a nice night'
    return statement(speech_text)


@ask.intent('WakePCIntent')
def wake_pc():
    wol.wake()
    speech_text = 'Okay, PC turning on'
    return statement(speech_text)


@ask.intent('ShutdownPCIntent')
def shutdown_pc():
    RSDRemoteClient.shutdown()
    speech_text = 'Done, PC is shutting down now'
    return statement(speech_text)


@ask.intent('AMAZON.HelpIntent')
def help_handler():
    speech_text = ("I can do things like change the brightness on your "
     "TV or turn on your computer")
    return question(speech_text).reprompt(speech_text)


@ask.intent('AMAZON.CancelIntent')
def cancel_handler():
    speech_text = "Goodbye!"
    return statement(speech_text)


@ask.intent('AMAZON.StopIntent')
def stop_handler():
    speech_text = "Goodbye!"
    return statement(speech_text)


@ask.default_intent
def default_handler():
    speech_text = "Sorry, I didn't understand that. Please try again"
    return question(speech_text).reprompt(speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200



if __name__ == '__main__':

    rokuIP = input('Roku TV IP Address: ')
    mac_addr = input('WOL PC MAC Address: ')
    netmask = input('LAN Subnet Mask: ')
    
    tv = RokuClient(rokuIP)
    
    # WOL accepts any valid IP address for the network, so rokuIP is used
    # however, mac_addr specifies the target device for WOL
    wol = WOLClient(rokuIP, netmask, mac_addr)
    
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run()
