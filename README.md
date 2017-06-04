# simpleMQTTlogger
simple python based mqtt logger client

## requirements
- python 3
- paho mqtt for python 3

### Install mqtt
```
pip3 install paho-mqtt
```

## Help

```
$ ./simpleLogger.py -h
Usage: simpleLogger.py [options]

simple logger - A simple MQTT logger to show or save mqtt data.

Options:
  --version             show program's version number and exit
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
                        destination file for mqtt message
    -l LOGLEVEL, --loglevel=LOGLEVEL
                        50: critical  40: error  30: warning  20:info
                        10:debug
    --with-timestring   add timestring as suffix for filename
    --newline=NEWLINE   newline character for logging file, default \n
    -v, --verbose       show debug messages (overrites loglevel to debug)
```

## Usage
Log into ```mqtt.log```:
```
$ ./simpleLogger.py -f mqtt.log &
```

## License
[![cc-bc-sa](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)
