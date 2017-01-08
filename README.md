# simpleMQTTlogger
simple python based mqtt logger client

## help

```
$ ./simpleLogger.py -h
Usage: simpleLogger.py [options]

simple logger - A simple MQTT logger to show or save mqtt data.

Options:
  -h, --help            show this help message and exit

  MQTT settings:
    -s SERVER, --server=SERVER
                        mqtt server, default 127.0.0.1
    --port=PORT         mqtt server port, default 1883
    -k KEEPALIVE, --keepalive=KEEPALIVE
                        keepalive option for mqtt server, default 60
    -t TOPIC, --topic=TOPIC
                        topic to subscribe to, default #
    -u USERNAME, --username=USERNAME
                        connection username
    -p PASSWORD, --password=PASSWORD
                        connection password

  Basic settings:
    -f FILENAME, --filename=FILENAME
                        destination for mqtt message
    --newline=NEWLINE   newline character for logging file, default \n
    -v, --verbose       show debug messages
```
