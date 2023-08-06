from loraspi.LoRaTransparent import LoRaTransparentBM
import paho.mqtt.client as mqtt
import dataset as ds
from time import time
from loguru import logger as log


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