#!/usr/bin/env python
# -*- coding: utf-8 -*-

# queueapp.py
# QueueApp for Asterisk integrated with XMPP Server for PubSub use
#
# Marcelo H. Terres <mhterres@mundoopensource.com.br>
# 2016-04-11
#

import os
import ari
import sys
import time
import uuid
import logging
import requests
import sleekxmpp
import threading
import ConfigParser

import psycopg2
import psycopg2.extras

from sleekxmpp.xmlstream import ET, tostring

#logging.basicConfig()

# Python versions before 3.0 do not use UTF-8 encoding 
# by default. To ensure that Unicode is handled properly 
# throughout SleekXMPP, we will set the default encoding 
# ourselves to UTF-8. 
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

configFile='%s/queueapp.conf' % os.path.dirname(sys.argv[0])

try:

  configuration = ConfigParser.RawConfigParser()
  configuration.read(configFile)

  # queue config
  queue_id=configuration.get('queue','id')
  queue_name=configuration.get('queue','name')
  queue_strategy=configuration.get('queue','strategy')
  queue_timeout="%s/Asterisk" % configuration.get('queue','timeout')
  queue_ringtimeperexten=configuration.get('queue','ringtimeperexten')
  queue_extension=configuration.get('queue','extension')

  # xmpp config
  xmppUser=configuration.get('xmpp','xmppUser')
  xmppSecret=configuration.get('xmpp','xmppSecret')
  pubsubDomain=configuration.get('xmpp','pubsubDomain')

  # asterisk ari config
  ari_user=configuration.get('ari','user')
  ari_secret=configuration.get('ari','secret')

  # db config
  db_name=configuration.get('db','name')
  db_host=configuration.get('db','host')
  db_user=configuration.get('db','user')
  db_secret=configuration.get('db','secret')

except:

  print "Config file %s not found." % configFile
  sys.exit(1)

# DEBUG
log = open('/tmp/queueapp.log', 'a')
sys.stderr = log

class XMPP(sleekxmpp.ClientXMPP):

  def __init__(self, jid, password, pubsubDomain):
    sleekxmpp.ClientXMPP.__init__(self, jid, password)

    self.pubsub=pubsubDomain
    self.register_plugin('xep_0060')

    # The session_start event will be triggered when
    # the bot establishes its connection with the server
    # and the XML streams are ready for use. We want to
    # listen for this event so that we we can initialize
    # our roster.
    self.add_event_handler("session_start", self.start)

  def start(self, event):
    """
    Process the session_start event.
    """
    self.send_presence()

  def publish(self,data,node):

	    # publish data in pubsub node
		
      #print "publish item %s in node %s on %s"	 % (data,node,self.pubsub)

      payload = ET.fromstring("<test xmlns='test'>%s</test>" % data)
      try:
          result = self['xep_0060'].publish(self.pubsub, node, payload=payload)
          id = result['pubsub']['publish']['item']['id']
          print('Published at item id: %s' % id)
      except:
          print('Could not publish to: %s on %s' % (node,self.pubsub))

class DBPgsql:

  def __init__(self,db_name,db_host,db_user,db_secret):

    self.dsn = 'dbname=%s host=%s user=%s password=%s' % (db_name,db_host,db_user,db_secret)

    self.conn = psycopg2.connect(self.dsn)

  def updateData(self,queue_id,extension):

    # update last hangup time of queue member

    curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    #print "Updating queue data in database - extension %s" % extension

    sql = "SELECT id FROM sip WHERE extension = '%s';" % extension
    curs.execute(sql)

    if not curs.rowcount:
      print("Can't find extension %s" % extension)
    else:

      sip_id = curs.fetchone()['id']

      sql = "SELECT * FROM queue_sip WHERE queue_id=%s and sip_id=%s;" % (queue_id,sip_id)
      curs.execute(sql)

      if curs.rowcount:

          sql="UPDATE queue_sip SET lasthangup='%s' WHERE queue_id=%s and sip_id=%s;" % (time.strftime("%Y-%m-%d %H:%M:%S"),queue_id,sip_id)
          curs.execute(sql)
          self.conn.commit()

  def selectExten(self,queue_id):

    # select extension to redirect call

    curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    #print "Selecting extension to redirect call"

    sql = "SELECT sip.extension as exten FROM sip,queue_sip WHERE  queue_sip.queue_id=%s AND queue_sip.logged=True AND sip.id=queue_sip.sip_id ORDER BY lasthangup LIMIT 1;" % queue_id
    curs.execute(sql)

    if not curs.rowcount:
      print("Can't find valid extension to queue %s" % queue_id)
    else:

      exten=curs.fetchone()['exten']

      self.conn.commit()
      return exten

def safe_hangup(channel,extension):
    """Safely hang up the specified channel"""
    db.updateData(queue_id,extension.split("/")[1])
    print "Call ended at %s\n" % time.strftime("%c")
    try:
        channel.hangup()
        print "Hung up {}".format(channel.json.get('name'))
    except requests.HTTPError as e:
        if e.response.status_code != requests.codes.not_found:
            raise e

def safe_bridge_destroy(bridge):
    """Safely destroy the specified bridge"""
    try:
        bridge.destroy()
    except requests.HTTPError as e:
        if e.response.status_code != requests.codes.not_found:
            raise e

def stasis_start_cb(channel_obj, ev):
    """Handler for StasisStart"""

    def playback_finished(playback, ev):
        """Callback when the playback have finished"""

        target_uri = playback.json.get('target_uri')
        channel_id = target_uri.replace('channel:', '')
        channel = client.channels.get(channelId=channel_id)

        channel.ring()

        exten=db.selectExten(queue_id)
        extension='PJSIP/%s' % exten
        nodeName="extension%s" % exten

        xmpp.publish(args[0],nodeName)

        try:
            print "Dialing %s - Origin %s" % (extension,callerid)
            outgoing = client.channels.originate(endpoint=extension,
                                                 app='queueapp',
                                                 appArgs='dialed',
																								 callerId=callerid)

        except requests.HTTPError:
            print "Whoops, pretty sure %s wasn't valid" % extension
            channel.hangup()
            return

        channel.on_event('StasisEnd', lambda *args: safe_hangup(outgoing,extension))
        outgoing.on_event('StasisEnd', lambda *args: safe_hangup(channel,extension))

        def outgoing_start_cb(channel_obj, ev):
            """StasisStart handler for our dialed channel"""

            print "{} answered; bridging with {}".format(outgoing.json.get('name'),
                                                         channel.json.get('name'))
				 
            channel.answer()

            bridge = client.bridges.create(type='mixing')
            bridge.addChannel(channel=[channel.id, outgoing.id])

            # Clean up the bridge when done
            channel.on_event('StasisEnd', lambda *args:
                             safe_bridge_destroy(bridge))
            outgoing.on_event('StasisEnd', lambda *args:
                             safe_bridge_destroy(bridge))
    
        outgoing.on_event('StasisStart', outgoing_start_cb)

    channel = channel_obj.get('channel')
    callerid = channel.json.get('caller')['number']

    # provide callerid (in case of receiving iax calls)
    if len(callerid)==0:
       callerid="Asterisk"

    channel_name = channel.json.get('name')
    args = ev.get('args')

    # get data received from Asterisk Stasis App (dialplan)
    pubsubData=args[0]

    print "%s - {} entered our application".format(channel_name) % time.strftime("%c")
    print "Pubsub data: %s" % pubsubData

    channel.answer()

    channel.on_event('StasisEnd', lambda *args: safe_hangup(outgoing,""))

    chanType=channel.json.get('name').split('-')[0] 	# get CHANTYPE/EXTEN
    #chanType=channel.json.get('name').split('/')[0] 	# get CHANTYPE

		# Normally you will avoid process of a call when channel is PJSIP/SIP
		# I did this because I want to process only external calls
		# Also, I want to avoid that the originate call be processed too (loop)

	  #if chanType != "PJSIP":					# avoid process when channel type is PJSIP

    # I'm using PJSIP/2000 for my tests, but you should consider using ChanType != "PJSIP"
    if chanType == "PJSIP/2000":			# process when channel is PJSIP/2000

        playback_id = str(uuid.uuid4())
        playback = channel.playWithId(playbackId=playback_id,media='sound:poc/support_team')
        playback.on_event('PlaybackFinished', playback_finished)

print "queueapp started at %s" % time.strftime("%c")

print "Asterisk ARI - connecting"
client = ari.connect('http://localhost:8088', ari_user, ari_secret)
client.on_channel_event('StasisStart', stasis_start_cb)

print "XMPP Server - connecting"
xmpp=XMPP(xmppUser,xmppSecret,pubsubDomain)
xmpp.connect()
xmpp.process(block=False)

print "DB PostgreSQL - connecting"
db=DBPgsql(db_name,db_host,db_user,db_secret)

print "Waiting for calls..."

client.run(apps='queueapp')




