# Companion Class
class MqttTopic:
    SENSORS = "homesolar/sensors/#"
    ACTUATORS = "homesolar/actuators/#"
    CLIENT = "homesolar/app/clients/#"
    REQUEST = "homesolar/app/clients/+/request"
    RESPONSE = "homesolar/app/clients/+/response"
    SUMMARY = "homesolar/summary"
    BATTERY = "homesolar/battery"

