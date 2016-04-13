#!/usr/bin/env python
# -*- coding: utf-8 -*-

# software.py
# "customer service software"
# For pubsub testing
#
# Marcelo H. Terres <mhterres@mundoopensource.com.br>
# 2016-04-10
#
# Based on pubsub_events.py

import sys
import sleekxmpp
import ConfigParser
import xml.etree.cElementTree as ET
	
from sleekxmpp.xmlstream import ET, tostring
from sleekxmpp.xmlstream.matcher import StanzaPath
from sleekxmpp.xmlstream.handler import Callback

# Python versions before 3.0 do not use UTF-8 encoding 
# by default. To ensure that Unicode is handled properly 
# throughout SleekXMPP, we will set the default encoding 
# ourselves to UTF-8. 
if sys.version_info < (3, 0): 
    from sleekxmpp.util.misc_ops import setdefaultencoding 
    setdefaultencoding('utf8') 
else: 
    raw_input = input 

configFile='./software.conf' 

IDs=[]

try:

	configuration = ConfigParser.RawConfigParser()
	configuration.read(configFile)

  # xmpp config

	nodeName=configuration.get('general','nodeName')
	pubsubDomain=configuration.get('general','pubsubDomain')
	xmppUser=configuration.get('general','xmppUser')
	xmppSecret=configuration.get('general','xmppSecret')

except:

	print "Config file %s not found." % configFile
	sys.exit(1)

class SW_XMPP(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        super(SW_XMPP, self).__init__(jid, password)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0059')
        self.register_plugin('xep_0060')

        self.register_handler(
                Callback('Pubsub event',
                    StanzaPath('message/pubsub_event'),
                    self._handle_event))

        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.get_roster()
        self.send_presence()

        print('started connection on %s' % pubsubDomain)
        node = nodeName
        try:
            self['xep_0060'].subscribe(pubsubDomain,nodeName)
            print('subscribed to %s on %s' % (nodeName,pubsubDomain))
        except:
            print('failed to subscribe to %s on %s' % (nodeName,pubsubDomain))
            self.disconnect()

    def _handle_event(self, msg):
        data='''%s''' % msg['pubsub_event']
        tree=ET.fromstring(data)

        #print "pubsub Item: %s" % data
        print "Code: %s" % tree[0][0][0].text
        try:
            result = self['xep_0060'].purge(pubsubDomain, nodeName)
            #print('Purged all items from node %s on %s' % (nodeName,pubsubDomain))
        except:
            print('Could not purge items from node %s on %s' % (nodeName,pubsubDomain) )

print "Connecting as %s" % xmppUser

xmpp = SW_XMPP(xmppUser,xmppSecret)

if xmpp.connect():
	xmpp.process(block=True)
else:
	print 'Unable to connect'

