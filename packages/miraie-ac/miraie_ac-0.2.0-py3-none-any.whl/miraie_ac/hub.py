import aiohttp
import asyncio
from . import constants
from .broker import MirAIeBroker
from .user import User
from .topic import MirAIeTopic
from .home import Home
from .device import Device, DeviceDetails


class MirAIeHub:
    def __init__(self):
        self.http = aiohttp.ClientSession()
        self.topics_map: dict[str, MirAIeTopic] = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self.http.close()

    def __build_headers__(self):
        return {
            "Authorization": f"Bearer {self.user.access_token}",
            "Content-Type": "application/json",
        }

    async def init(self, mobile: str, password: str, broker: MirAIeBroker):
        self._broker = broker

        await self._authenticate(mobile, password)
        await self._get_home_details()
        self._init_broker(broker)

    def _init_broker(self, broker: MirAIeBroker):
        topics = self.get_device_topics()
        broker.set_topics(topics)
        broker.connect(self.home.id, self.user.access_token)

    @property
    def broker(self):
        return self._broker

    def get_device_topics(self):
        device_topics = list(
            map(
                lambda device: [device.status_topic, device.connection_status_topic],
                self.home.devices,
            )
        )
        miraie_topics = [topic for topics in device_topics for topic in topics]
        return miraie_topics

    # Authenticate with the MirAIe API
    async def _authenticate(self, mobile: str, password: str):
        data = {
            "clientId": constants.httpClientId,
            "mobile": mobile,
            "password": password,
            "scope": "an_14214235325",
        }

        response = await self.http.post(constants.loginUrl, json=data)

        if response.status == 200:
            json = await response.json()
            self.user = User(
                access_token=json["accessToken"],
                refresh_token=json["refreshToken"],
                user_id=json["userId"],
                expires_in=json["expiresIn"],
            )
            return True

        raise Exception("Authentication failed")

    # Get device details
    async def _get_device_details(self, deviceIds: str):
        response = await self.http.get(
            constants.deviceDetailsUrl + "/" + deviceIds,
            headers=self.__build_headers__(),
        )
        return await response.json()

    # Process the home details
    async def _process_home_details(self, json_data):
        devices: list[Device] = []

        for space in json_data["spaces"]:
            for device in space["devices"]:
                item = Device(
                    id=device["deviceId"],
                    name=str(device["deviceName"]).lower().replace(" ", "-"),
                    friendly_name=device["deviceName"],
                    control_topic=str(device["topic"][0]) + "/control",
                    status_topic=str(device["topic"][0]) + "/status",
                    connection_status_topic=str(device["topic"][0])
                    + "/connectionStatus",
                    broker=self._broker,
                )
                devices.append(item)
                topic = MirAIeTopic(
                    control_topic=item.control_topic,
                    status_topic=item.status_topic,
                    connection_status_topic=item.connection_status_topic,
                )
                self.topics_map[item.id] = topic

        device_ids = ",".join(list(map(lambda device: device.id, devices)))
        device_details = await self._get_device_details(device_ids)

        for dd in device_details:
            device = next(d for d in devices if d.id == dd["deviceId"])

            details = DeviceDetails(
                model_name=dd["modelName"],
                mac_address=dd["macAddress"],
                category=dd["category"],
                brand=dd["brand"],
                firmware_version=dd["firmwareVersion"],
                serial_number=dd["serialNumber"],
                model_number=dd["modelNumber"],
                product_serial_number=dd["productSerialNumber"],
            )

            device.set_details(details)

        self.home = Home(id=json_data["homeId"], devices=devices)
        return self.home

    # Get home details
    async def _get_home_details(self):
        response = await self.http.get(
            constants.homesUrl, headers=self.__build_headers__()
        )
        resp = await response.json()
        await self._process_home_details(resp[0])

    # Get device status
    async def _get_device_status(self, device_id: str):
        response = await self.http.get(
            constants.statusUrl.replace("{deviceId}", device_id),
            headers=self.__build_headers__(),
        )
        return await response.json()

    # Get all device status
    async def get_all_device_status(self):
        results = await asyncio.gather(
            *[self._get_device_status(device.id) for device in self.home.devices],
            return_exceptions=True,
        )
        return results
