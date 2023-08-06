import logging
import json
from nalkinscloud_mqtt_python_client.mqtt_handler import NalkinscloudDevice, CONNECTION_RETURN_STATUS

logger = logging.getLogger(__name__)


class SwitchDevice(NalkinscloudDevice):

    def __init__(self, set_data_function):
        """
        :param set_data_function: function that will physically set switch state,
            function must implement return of updated state
        """
        super().__init__()

        self._switch_state = False
        self._set_data_function = set_data_function

    def on_connect(self, client, userdata, flags, rc, *extra_params):
        logger.info("client {} connection, user_data: {}, flags: {}, result code: {}".format(
            client, userdata, flags, str(rc)
        ))
        if rc != 0:
            logger.error("Error: " + self._device_id + ", " + CONNECTION_RETURN_STATUS.get(rc))
            exit(1)
        else:
            logger.info(CONNECTION_RETURN_STATUS.get(rc))
            self.subscribe(topic="v1/devices/me/rpc/request/+")
            # Sending current GPIO status
            self.publish('v1/devices/me/attributes', self.get_switch_state())

    def on_message(self, client, userdata, message):
        logger.info('message received: {{ "topic": {0}, "payload": {1}, "qos": {2}, "retain": {3} }}'.format(
            message.topic, message.payload, message.qos, message.retain))
        logger.info("client: {}, userdata: {}".format(client, userdata))

        # Decode JSON request
        data = json.loads(message.payload)
        # Check request method
        if data['method'] == 'getValue':
            # Reply with GPIO status
            self.publish(topic=message.topic.replace('request', 'response'),
                         payload=self.get_switch_state())
        elif data['method'] == 'setValue':
            # Update GPIO status and reply
            self.set_switch_state(data['params'])

            self.publish(topic=message.topic.replace('request', 'response'),
                         payload=self.get_switch_state())
            self.publish(topic="v1/devices/me/attributes",
                         payload=self.get_switch_state())

    def set_switch_state(self, state):
        # send desired state to set_date function
        self._switch_state = self._set_data_function(state)

    def get_switch_state(self):
        return json.dumps({"state": self._switch_state})


class DHTDevice(NalkinscloudDevice):
    def __init__(self, get_data_function):
        super().__init__()
        self._data = get_data_function()

        self._get_data_function = get_data_function

    def on_connect(self, client, userdata, flags, rc, *extra_params):
        logger.info("client {} connection, user_data: {}, flags: {}, result code: {}".format(
            client, userdata, flags, str(rc)
        ))
        if rc != 0:
            logger.error("Error: " + self._device_id + ", " + CONNECTION_RETURN_STATUS.get(rc))
            exit(1)
        else:
            # Subscribing to receive RPC requests
            self.subscribe(topic="v1/devices/me/rpc/request/+")
            # Sending current GPIO status
            self.publish(topic='v1/devices/me/telemetry',
                         payload=json.dumps(self._data))

    def on_message(self, client, userdata, message):
        logger.info('message received: {{ "topic": {0}, "payload": {1}, "qos": {2}, "retain": {3} }}'.format(
            message.topic, message.payload, message.qos, message.retain))
        logger.info("client: {}, userdata: {}".format(client, userdata))

        # Decode JSON request
        data = json.loads(message.payload)
        # Check request method
        if data['method'] == 'getData':
            self.publish(topic="v1/devices/me/telemetry",
                         payload=json.dumps(self._data))
