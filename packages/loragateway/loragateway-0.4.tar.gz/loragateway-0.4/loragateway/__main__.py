from loguru import logger as log
from argparse import ArgumentParser
from loragateway.Gateway import Gateway


def main():
    ap = ArgumentParser()
    ap.add_argument("-a", "--address", help="MQTT server address", type=str, required=True)
    ap.add_argument("-p", "--port", help="MQTT server port", type=int, default=1883, required=True)
    ap.add_argument("-i", "--id", help="MQTT client id", type=str, default="LoRa Gateway", required=True)
    ap.add_argument("-d", "--database", help="Path to sqlite database", type=str, default="loragateway.db", required=True)
    a = ap.parse_args()

    gw = Gateway(a.address, a.port, a.id, a.database)
    gw.start()
    try:
        gw.join()
    except KeyboardInterrupt:
        gw.stop()
    log.info("\nExiting.")


if __name__ == '__main__':
    main()
