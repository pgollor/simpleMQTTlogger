#!/usr/bin/python3

## 
# @brief simple MQTT logger
# @author Pascal Gollor
# @date 2017-01-08
#
# Project repository on: 
# 

import optparse, signal, logging
import paho.mqtt.client as mqtt


DEFAULT_MQTT_SERVER = "127.0.0.1"
DEFAULT_MQTT_PORT = 1883
DEFAULT_TOPIC = "#"



## detecting kill signal
# source:	http://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
class GracefulKiller:
	def __init__(self):
		self.kill_now = False
		
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)
	# end __init__

	def exit_gracefully(self,signum, frame):
		self.kill_now = True
	# end exit_gracefully
	
# end class GracefulKiller



#def on_connect(client, userdata, flags, rc):
#	logging.debug("Connected with result code %i", rc)
#
#	client.subscribe("#")
# end on_connect

def on_message(client, userdata, msg):
	if ('saveLogger' in userdata):
		userdata['saveLogger'].info("%s%s%s", msg.topic, userdata['newline'], msg.payload.decode())
	# end if
	
	userdata['logger'].info("%s\r\n%s", msg.topic, msg.payload.decode())
# end on_message


def main():
	parser = optparse.OptionParser(
		usage = "%prog [options]",
		description = "simple logger - A simple MQTT logger to show or save mqtt data."
	)
	
	group = optparse.OptionGroup(parser, "MQTT settings")
	group.add_option("-s", "--server",
		dest = "server",
		help = "mqtt server, default %default",
		default = DEFAULT_MQTT_SERVER
	)
	group.add_option("--port",
		dest = "port",
		action = "store",
		type = 'int',
		help = "mqtt server port, default %default",
		default = DEFAULT_MQTT_PORT
	)
	group.add_option("-k", "--keepalive",
		dest = "keepalive",
		action = "store",
		type = 'int',
		help = "keepalive option for mqtt server, default %default",
		default = 60
	)
	group.add_option("-t", "--topic",
		dest = "topic",
		help = "topic to subscribe to, default %default",
		default = DEFAULT_TOPIC
	)
	group.add_option("-u", "--username",
		dest = "username",
		help = "connection username",
		default = ""
	)
	group.add_option("-p", "--password",
		dest = "password",
		help = "connection password",
		default = ""
	)
	parser.add_option_group(group)
	
	group = optparse.OptionGroup(parser, "Basic settings")
	group.add_option("-f", "--filename",
		dest = "filename",
		help = "destination for mqtt message",
		default = ""
	)
	group.add_option("--newline",
		dest = "newline",
		help = "newline character for logging file, default \\n",
		default = "\n"
	)
	group.add_option("-v", "--verbose",
		dest = "verbose",
		action = "store_true",
		help = "show debug messages",
		default = False
	)
	parser.add_option_group(group)
	
	# parse options
	(options, _) = parser.parse_args()
	
	
	# init logging
	loglevel = logging.WARN
	if (options.verbose):
		loglevel = logging.DEBUG
	# end if
	logger = logging.getLogger("simpleLogger")
	logger.setLevel(loglevel)
	ch = logging.StreamHandler()
	ch.setLevel(loglevel)
	formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
	formatter.datefmt = '%Y-%m-%d %H:%M:%S'
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	
	
	# createing save logger
	userdata = dict()
	userdata['logger'] = logger
	if (options.filename != ""):
		saveLogger = logging.getLogger('mqtt logger')
		saveLogger.setLevel(logging.INFO)
		ch = logging.FileHandler(options.filename, mode="w")
		ch.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s' + options.newline + '%(message)s' + options.newline)
		formatter.datefmt = '%Y-%m-%d %H:%M:%S'
		ch.setFormatter(formatter)
		saveLogger.addHandler(ch)
		
		userdata['saveLogger'] = saveLogger
		userdata['newline'] = options.newline
	# end if
	
	
	# add killer
	killer = GracefulKiller()
	
	# add mqtt client
	client = mqtt.Client()
	#client.on_connect = on_connect
	client.on_message = on_message
	client.user_data_set(userdata)
	
	# check username and password
	if (len(options.username) > 0):
		if (len(options.password) == 0):
			raise ValueError("please do not use username without password")
		# end if
		
		client.username_pw_set(options.username, options.password)
	# end if
	
	
	# debug output
	logger.debug("server: %s" ,options.server)
	logger.debug("port: %i", options.port)
	logger.debug("topic: %s", options.topic)
	
	# connect to mqttclient
	logger.debug("connect to mqtt client")
	client.connect(options.server, options.port, options.keepalive)
	client.subscribe(options.topic, qos=1)
	
	# loop forever
	try:
		logger.debug("start mqtt loop")
		
		while (1):
			#client.loop_forever()
			client.loop(0.1)
			
			if (killer.kill_now):
				raise KeyboardInterrupt
			# end if
		# end while
	except KeyboardInterrupt:
		logger.debug("exit mqtt loop")
	# end try
	
	# disconnecting
	logger.debug("disconnecting from mqtt server")
	client.disconnect()
# end main


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		logging.error(str(e))
	# end try
# end if