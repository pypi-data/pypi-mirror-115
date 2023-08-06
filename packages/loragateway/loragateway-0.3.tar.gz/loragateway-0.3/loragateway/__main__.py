from loraspi.LoRaTransparent import LoRaTransparentBM
import paho.mqtt.client as mqtt
from loguru import logger as log
import dataset as ds
from time import time
from argparse import ArgumentParser


class Gateway(LoRaTransparentBM):
    mqtt_client = None
    db: ds.Database = None
    db_tbl_lora_recv: ds.Table = None

    def __init__(self, host: str, port: int = 1883, mqtt_id: str = "LoRa Gateway",
                 database_path: str = "loragateway.db"):
        LoRaTransparentBM.__init__(self)
        self.db = ds.connect(f"sqlite:///{database_path}")
        self.db_tbl_lora_recv = self.db["lora_recv"]
        self.mqtt_client = mqtt.Client(mqtt_id)
        self.mqtt_client.connect(host, port)
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message

    def on_mqtt_connect(self, client, userdata, flags, rc):
        log.info("MQTT Connect:", rc)
        client.subscribe("LoRaSendQueue")

    def on_mqtt_message(self, client, userdata, msg):
        log.info("MQTT Message:", msg)
        self.send_message(msg)

    def on_msg(self):
        log.info("Publishing:", self._buffer)
        self.db_tbl_lora_recv.insert({
            "timestamp": time(),
            "message": self._buffer
        })
        self.mqtt_client.publish("LoRaReceivedQueue", self._buffer)


def main():
    ap = ArgumentParser()
    ap.add_argument("-a", "--address", help="MQTT server address", type=str)
    ap.add_argument("-p", "--port", help="MQTT server port", type=int, default=1883)
    ap.add_argument("-i", "--id", help="MQTT client id", type=str, default="LoRa Gateway")
    ap.add_argument("-d", "--database", help="Path to sqlite database", type=str, default="loragateway.db")
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
