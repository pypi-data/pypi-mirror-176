from paho.mqtt import client as paho

from homesolar.utils import mqtt
from loguru import logger


def initialize(mqtt_service_queue, relay_host, relay_port, relay_username, relay_password):
    try:
        def on_message(cli: paho.Client, userdata, msg):
            mqtt_service_queue.put({
                "name": "publish",
                "topic": msg.topic,
                "payload": msg.payload
            })

        def on_connect(cli: paho.Client, userdata, flags, rc):
            cli.subscribe(mqtt.MqttTopic.SENSORS)

        client = paho.Client()

        client.reconnect_delay_set(max_delay=120)
        client.on_message = on_message
        client.on_connect = on_connect
        client.username_pw_set(relay_username, relay_password)
        client.connect(relay_host, relay_port, 60)

        # Start MQTT main loop
        client.loop_forever()
    except Exception as e:
        logger.exception(f"There is something wrong when executing relayer operation [{e}]")
    finally:
        return
