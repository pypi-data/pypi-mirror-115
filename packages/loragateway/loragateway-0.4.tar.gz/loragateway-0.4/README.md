# loragateway

## features

- [X] logging incoming messages into sqlite db
- [X] publishing incoming messages to broker
- [X] sending lora messages which come into channel 'LoRaSendQueue'

## usage

```shell
pi@hq:~ $ loragw --help
usage: loragw [-h] [-a ADDRESS] [-p PORT] [-i ID] [-d DATABASE]

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        MQTT server address
  -p PORT, --port PORT  MQTT server port
  -i ID, --id ID        MQTT client id
  -d DATABASE, --database DATABASE
                        Path to sqlite database
```
