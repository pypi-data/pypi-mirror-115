import paho.mqtt.client as mqtt
import ssl
import logging

logger = logging.getLogger(__name__)

CONNECTION_RETURN_STATUS = {
    0: 'Connection successful',
    1: 'Connection refused - incorrect protocol version',
    2: 'Connection refused - invalid client identifier',
    3: 'Connection refused - server unavailable',
    4: 'Connection refused - bad username or password',
    5: 'Connection refused - not authorised'
}


class NalkinscloudDevice(object):

    def __init__(self):
        logger.info("creating new client {}".format(self))
        self._broker_host = None
        self._broker_port = None
        self._broker_cert = None
        self._broker_tls = None
        self._broker_tls_skip = None

        self._device_id = None
        self._device_type = None
        self._qos = None
        self._mqtt_client = None

    def init_broker(self, broker_host='127.0.0.1', broker_port=1883,
                    broker_tls=False, broker_cert=None, broker_tls_skip=False):
        logger.info("initializing client {} with broker: '{}:{}'".format(self, broker_host, broker_port))
        self._broker_host = broker_host
        self._broker_port = broker_port
        self._broker_cert = broker_cert
        self._broker_tls = broker_tls
        self._broker_tls_skip = broker_tls_skip

    def init_device(self, device_id, device_type, device_password, qos):
        """
        initialize a device, set its connection values, and on_connect / on_message
        :param device_id:
        :param device_type:
        :param device_password:
        :param qos:
        :return:
        """
        logger.info("initializing client {} with id: {}".format(self, device_id))
        self._device_id = device_id
        self._device_type = device_type
        self._qos = qos

        # Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv31)
        self._mqtt_client = mqtt.Client(client_id=self._device_id,
                                        clean_session=True,
                                        userdata={'device_id': self._device_id,
                                                  'device_type': device_type,
                                                  'qos': qos})

        # Using password under username parameter since passing access token
        self._mqtt_client.username_pw_set(username=device_password)

        if self._broker_tls:
            if self._broker_tls_skip:
                self._mqtt_client.tls_set(ca_certs=self._broker_cert,
                                          tls_version=ssl.PROTOCOL_TLSv1_2,
                                          cert_reqs=ssl.CERT_NONE)
                self._mqtt_client.tls_insecure_set(True)
            else:
                self._mqtt_client.tls_set(ca_certs=self._broker_cert,
                                          tls_version=ssl.PROTOCOL_TLSv1_2)

        self._mqtt_client.on_connect = self.on_connect
        self._mqtt_client.on_message = self.on_message

    def get_mqtt_client(self):
        return self._mqtt_client

    # thingsboard currently does not support LWT
    # https://github.com/thingsboard/thingsboard/issues/416
    # https://github.com/thingsboard/thingsboard/issues/3165
    # TODO set LWT back when implemented mosquitto bridge broker
    # Set a Will (LWT) to be sent to the broker. If the client disconnects without calling disconnect(),
    # the broker will publish the message on its behalf.
    def set_lwt(self, device_id, device_type, qos, is_retained):  # Last Will and Testament
        self._mqtt_client.will_set(device_id + "/" + device_type + '/status',
                                   payload='offline',
                                   qos=qos,
                                   retain=is_retained)

    # connect the client to the broker, this is a blocking function.
    def connect(self):
        logger.info("client connecting to: {0}:{1}".format(self._broker_host, self._broker_port))
        try:
            self._mqtt_client.connect(host=self._broker_host, port=self._broker_port, keepalive=60)
            return True
        except Exception as exc:
            logger.error('Connection Error: {}'.format(str(exc)) +
                         '. Host: ' + self._broker_host +
                         '. Port: ' + str(self._broker_port))
            return False

    def subscribe(self, topic):
        logger.info("Subscribing to: " + topic)
        return self._mqtt_client.subscribe(topic, qos=self._qos)

    def publish(self, topic, payload):
        logger.info("Publish: {} to: {}".format(topic, payload))
        self._mqtt_client.publish(topic, payload=payload, qos=self._qos, retain=False)

    def publish_retained(self, topic, payload, qos):
        # publish(topic, payload=None, qos=0, retain=False)
        logger.info("Publish RETAINED: " + topic)
        self._mqtt_client.publish(topic, payload=payload, qos=self._qos, retain=True)

    @staticmethod
    def on_message(client, userdata, message):
        logger.info('message received: {{ "topic": {0}, "payload": {1}, "qos": {2}, "retain": {3} }}'.format(
            message.topic, message.payload, message.qos, message.retain))
        logger.info("client: {}, userdata: {}".format(client, userdata))

    def on_connect(self, mqtt_client, userdata, flags, rc):
        logger.info("client {} connection, user_data: {}, flags: {}, result code: {}".format(
            mqtt_client, userdata, flags, str(rc)
        ))
        if rc != 0:
            logger.error("Error: " + self._device_id + ", " + CONNECTION_RETURN_STATUS.get(rc))
            exit(1)
        else:
            logger.info(CONNECTION_RETURN_STATUS.get(rc))
            # self.publish_retained(topic=self._device_id + '/' + self._device_type + '/status',
            #                      payload="online",
            #                      qos=self._qos)
            self.subscribe(topic="v1/devices/me/rpc/request/+")

    # Disconnect from the broker cleanly.
    # Using disconnect() will not result in a will (LWT) message being sent by the broker
    def __del__(self):
        self._mqtt_client.disconnect()

    # This is a blocking form of the network loop and will not return until the client calls disconnect().
    # It automatically handles reconnecting.
    def do_loop_forever(self):
        # loop_forever(timeout=1.0, max_packets=1)
        self._mqtt_client.loop_forever()

    def do_loop(self):
        self._mqtt_client.loop_start()


def is_valid_topic(topic):
    if type(topic) is not str:
        return False

    parsed_topic = topic.split('/')
    for i in range(len(parsed_topic)):
        if not parsed_topic[i]:  # Check if string inside each array cell is not null or empty
            return False
    return len(parsed_topic) == 3
