"""
Guardian Bluetooth utils.
"""
import sys
import asyncio
import os
from codecs import utf_8_encode
import logging
import time
import base64
import datetime
from bleak import discover, BleakClient, BleakScanner, exc

from .config import settings


class GuardianBLE:
    """Main Guardian BLE client."""

    def __init__(self, address: str = "", debug: bool = True) -> None:

        self.address = address
        self.debug = debug
        self.write_to_file: bool = debug

        self.initialise_connection: bool = True
        self.client: BleakClient

        self.connection_established = False
        self.time_left = True
        self.initial_time = True

        self.original_time = time.time()
        self.reconnect_try_amount = 50
        self.try_to_connect_timeout = self.reconnect_try_amount

        self.get_ble_characteristic()

        if self.debug:
            logging.info("MEASUREMENT EEG ID: %s", self.meas_eeg_id)
            logging.info("COMMAND ID: %s", self.command_id)
            logging.info("START CMD: %s", self.start_cmd)
            logging.info("STOP CMD: %s", self.stop_cmd)

    def get_ble_characteristic(self) -> None:
        """Get the environment variables."""
        # General information
        self.battery_id = settings.UUID_BATT_GDK
        self.device_service = settings.UUID_DEVICE_SERVICE
        self.mac_uuid = settings.UUID_MAC_ID

        # EEG/IMU measurement
        self.meas_eeg_id = settings.UUID_MEAS_EEGIMU
        self.command_id = settings.UUID_CMD
        self.start_cmd = settings.START_CMD
        self.stop_cmd = settings.STOP_CMD

        # Impedance measurement
        self.meas_imp_id = settings.UUID_MEAS_IMP
        self.start_imp_cmd = settings.START_IMP_CMD
        self.stop_imp_cmd = settings.STOP_IMP_CMD

        # LED control
        self.led_id = settings.UUID_CFG
        self.led_on_cmd = settings.LED_ON_CFG
        self.led_off_cmd = settings.LED_OFF_CFG

    async def get_ble_devices(self) -> list:
        """
        Scan for devices and return a list of devices.
        """
        devices_dict: dict = {}
        ble_device_list: list = []
        devices = await discover()

        for device_idx, device in enumerate(devices):
            # print device discovered
            print(
                "[" + str(device_idx) + "]" + device.address,
                device.name,
                device.metadata["uuids"],
            )
            # put device information in list
            devices_dict[device.address] = []
            devices_dict[device.address].append(device.name)
            devices_dict[device.address].append(device.metadata["uuids"])
            ble_device_list.append(device.address)

        return ble_device_list

    async def stop_stream(self) -> None:
        """Stop the stream."""
        try:
            async with BleakClient(self.address) as client:
                await client.write_gatt_char(
                    self.command_id, utf_8_encode(self.stop_cmd)[0]
                )
                if self.debug:
                    logging.info("[BLE]: Recording successfully stopped")
        except exc.BleakError:
            logging.info("[BLE]: failed to stop measurement")

    async def get_device_mac(self) -> str:
        """Get the device MAC address.
        This is different from BLE device address
        (UUID on Mac or MAC address on Windows)

        Args:
            device_name (str): Device name

        Returns:
            str: MAC address
        """
        async with BleakClient(self.address) as client:
            logging.info("[BLE]: Searching for MAC address")

            value = bytes(await client.read_gatt_char(self.mac_uuid))
            # log the mac address of the device
            # convert bytes to string
            mac_address = value.decode("utf-8")
            mac_address = mac_address.replace(":", "-")
            logging.info("[BLE] Device ID (based on MAC address is): %s", mac_address)
            return mac_address  # convert bytes to string

    async def search_device(self) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """

        ble_device_list = await self.get_ble_devices()
        index_str = input(
            "Enter the index of the GDK device you want to connect to \
            \nIf cannot find the device, please restart the program and try again: "
        )
        index = int(index_str)
        self.address = ble_device_list[index]

        if self.debug:
            logging.info("[BLE]: Address is %s", self.address)
            logging.info("[BLE]: .............................................")
            logging.info("[BLE]: Connecting to %s", self.address)

        return self.address

    async def connect_to_device(self):
        """
        This function initialises the connection to the device.
        It finds the device using the address, sets up callback,
        and connects to the device.
        """
        if self.debug:
            logging.info("[BLE]: Trying to connect to %s.....", self.address)
        device = await BleakScanner.find_device_by_address(self.address, timeout=20.0)
        if not device:
            raise exc.BleakError(
                f"A device with address {self.address} could not be found."
            )
        self.client = BleakClient(
            device, disconnected_callback=self.disconnected_callback
        )
        if self.debug:
            logging.info("[BLE]: Connecting to %s", self.address)
        await self.client.connect()
        self.connection_established = True
        if self.debug:
            logging.info("[BLE]: Connected to %s", self.address)

    def disconnected_callback(self, client):  # pylint: disable=unused-argument
        """
        Callback function when device is disconnected.

        Args:
            client (BleakClient): BleakClient object
        """
        logging.info(
            "[BLE]: Callback function recognised a disconnection."
        )
        self.connection_established = False
        self.initialise_connection = True

    async def run_ble_record(
        self,
        data_queue: asyncio.Queue,
        record_time=60,
        mac_id="MAC_ID",
        led_sleep: bool = False,
    ) -> None:
        """_summary_

        Args:
            data_queue (asyncio.Queue): _description_
            record_time (_type_): _description_

        Raises:
            BleakError: _description_
        """
        # The initial time is set to true here so that you do not have to
        # initiate the class everytime to create new time
        async def data_handler(_, data):
            """Data handler for the BLE client.
                Data is put in a queue and forwarded to the API.

            Args:
                callback (handler Object): Handler object
                data (bytes): Binary data package
            """
            data_base_64 = base64.b64encode(data).decode("ascii")
            if self.write_to_file:
                self.data_recording_logfile.write(f"{data_base_64},\n")

            package = {
                "timestamp": datetime.datetime.now().astimezone().isoformat(),
                "device_id": mac_id,
                "data": data_base_64,
                "stop": False,
            }
            await data_queue.put(package)

        async def battery_handler(_, data):
            """Battery handler for the BLE client.
            Args:
                callback (handler Object): Handler object
                data (bytes): Battery Level as uint8_t
            """
            if self.debug:
                logging.info(
                    "[BLE]: Battery level: %d%%", int.from_bytes(data, byteorder="little")
                )

        async def send_start_commands_recording():
            """Send start commands to the device."""
            if self.debug:
                logging.info("[BLE]: Sending start commands")
            if led_sleep:
                await self.client.write_gatt_char(
                    self.led_id, utf_8_encode(self.led_off_cmd)[0]
                )
            # Notify the client that these two services are required
            await self.client.start_notify(self.meas_eeg_id, data_handler)
            await self.client.start_notify(self.battery_id, battery_handler)
            # sleep so that cleint can respond
            await asyncio.sleep(2)
            # send start command for recording data
            await self.client.write_gatt_char(
                self.command_id, utf_8_encode(self.start_cmd)[0]
            )

        async def stop_recording_timeout():
            """Stop recording gracefully."""
            await asyncio.sleep(2)
            # wait for the last data to be sent
            await self.client.write_gatt_char(
                self.command_id, utf_8_encode(self.stop_cmd)[0]
            )
            await asyncio.sleep(3)
            if led_sleep:
                await self.client.write_gatt_char(
                    self.led_id, utf_8_encode(self.led_on_cmd)[0]
                )
            # make sure the last data is now a stop command
            package = {
                "timestamp": datetime.datetime.now().astimezone().isoformat(),
                "device_id": mac_id,
                "data": "STOP_TIMEOUT",
                "stop": True,
            }
            # This gives time for the api to send last data before the stop command
            await asyncio.sleep(2)
            # pack the stop command
            await data_queue.put(package)
            if self.debug:
                logging.info("[BLE]: Sending stop command to the cloud")
            # This gives time for the API to receive the stop command
            await asyncio.sleep(2)
            if self.write_to_file:
                self.data_recording_logfile.close()
            if self.debug:
                logging.info("[BLE]: Recording successfully stopped")


        async def stop_recording_cancelled_script():
            """Stop recording abruptly."""
            if self.debug:
                logging.info("[BLE]: KeyboardInterrupt applied, terminating...")
            await asyncio.sleep(2)
            if self.debug:
                logging.info("[BLE]: Sending stop signal to device")
            await self.client.write_gatt_char(
                self.command_id, utf_8_encode(self.stop_cmd)[0]
            )
            await asyncio.sleep(3)
            if led_sleep:
                await self.client.write_gatt_char(
                    self.led_id, utf_8_encode(self.led_on_cmd)[0]
                )
            if self.debug:
                logging.info("[BLE]: Device successfully stopped")
            await asyncio.sleep(5)
            if self.write_to_file:
                self.data_recording_logfile.close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

        async def stop_recording_device_lost():
            """Stop recording device lost."""
            if self.debug:
                logging.info("[BLE]: Device lost, terminating...")
            package = {
                "timestamp": datetime.datetime.now().astimezone().isoformat(),
                "device_id": mac_id,
                "data": "STOP_DEVICE_LOST",
                "stop": True,
            }
            # pack the stop command
            await data_queue.put(package)
            await asyncio.sleep(2)
            if self.debug:
                logging.info("[BLE]: Sending stop command to the cloud")
            if self.write_to_file:
                self.data_recording_logfile.close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

        # ///////////////// Start of recording process /////////////////
        # Set everything to its default
        self.initial_time = True
        self.connection_established = False
        self.time_left = True
        self.initial_time = True
        self.original_time = time.time()
        self.try_to_connect_timeout = self.reconnect_try_amount


        if self.write_to_file:
            if not os.path.exists("./logs"):
                os.makedirs("logs")
            datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            recording_filename = f"./logs/IGEB-rec-{datestr}.txt"
            self.data_recording_logfile = open(
                recording_filename, "w", encoding="utf-8"
            )

        while True:
            try:
                if self.initialise_connection:
                    self.initialise_connection = False
                    await self.connect_to_device()

                if self.client.is_connected:
                    if self.debug:
                        logging.info("[BLE]: Device Connected")
                    await send_start_commands_recording()
                    if self.debug:
                        logging.info("[BLE]: Recording successfully started")
                    self.try_to_connect_timeout = (
                        self.reconnect_try_amount
                    )  # reset counter

                    # //////////////////// Main loop //////////////////////////
                    if self.initial_time:
                        self.initial_time = (
                            False  # record that this is the initial time
                        )
                        self.original_time = time.time()
                    while (
                        self.connection_established is True and self.time_left is True
                    ):
                        await asyncio.sleep(1)  # sleep so that everything can happen
                        time_left = record_time - (time.time() - self.original_time)
                        print(f"Time left: {round(time_left)}s")
                        if time_left <= 0:
                            self.time_left = False
                            if self.debug:
                                logging.info(
                                    "[BLE]: Recording stopped, time reached : %s",
                                    round(time.time() - self.original_time,2)
                                )
                    # //////////////////// Main loop //////////////////////////
                    await stop_recording_timeout()
                    if self.time_left:
                        if self.debug:
                            logging.info("[BLE]: Breaking loop of bluetooth client, timeout")
                        break

            except asyncio.CancelledError:
                await stop_recording_cancelled_script()

            except:
                self.try_to_connect_timeout = self.try_to_connect_timeout - 1
                if self.try_to_connect_timeout <= 0:
                    await stop_recording_device_lost()
                if self.debug:
                    logging.warning(
                        " [BLE] Connection lost, will try to reconnect %s more times",
                        self.try_to_connect_timeout,
                    )
                self.connection_established = False
                self.initialise_connection = True

            finally:
                if self.debug:
                    logging.info("[BLE]: Finally disconnecting")
                await self.client.disconnect()
                self.connection_established = False
                await asyncio.sleep(6)

    async def get_service_and_char(self) -> None:
        """Get the services and characteristics of the device."""
        try:
            async with BleakClient(self.address) as client:
                logging.info("BLE: Device connected")

                for service in client.services:
                    logging.info("[Service] %s: %s", service.uuid, service.description)
                    for char in service.characteristics:
                        if "read" in char.properties:
                            try:
                                value = bytes(await client.read_gatt_char(char.uuid))
                            except exc.BleakError as err:
                                value = str(err).encode()
                        else:
                            value = None
                        logging.info(
                            "\t[Characteristic] %s: (Handle: %s) (%s) \
                                | Name: %s, Value: %s ",
                            char.uuid,
                            char.handle,
                            ",".join(char.properties),
                            char.description,
                            value,
                        )
        except exc.BleakError as err:
            logging.error("[BLE]: Device connection failed - %s", err)

    async def read_battery_level(self, interval=10) -> None:
        """Read the battery level of the device given pre-defined interval."""
        if self.debug:
            logging.info("Reading battery level")

        async with BleakClient(self.address) as client:
            logging.info("[BLE]: Device connected")

            try:
                value = int.from_bytes(
                    (await client.read_gatt_char(self.battery_id)), byteorder="little"
                )
                await asyncio.sleep(interval)

                print(f"\nBattery level: {value}%\n")
                if self.debug:
                    logging.info("Battery level: %s", value)
            except exc.BleakError as err:
                # log the error
                logging.error("[BLE]: Device connection failed - %s", err)

    async def get_device_information(self) -> dict:
        """Read the device information of the device."""

        device_info = {}

        if self.debug:
            logging.info("[BLE]: Reading device information")

        async with BleakClient(self.address) as client:
            logging.info("[BLE]: Device connected")

            for service in client.services:
                if service.uuid == self.device_service:
                    for char in service.characteristics:
                        if "read" in char.properties:
                            try:
                                value = bytes(await client.read_gatt_char(char.uuid))
                            except exc.BleakError as err:
                                value = str(err).encode()
                        else:
                            value = None

                        print(f"{ char.description}:{str(value)}")
                        device_info[char.description] = str(value)
                        if self.debug:
                            logging.info("%s : %s", char.description, str(value))

        return device_info

    async def get_impedance_measurement(
        self,
        data_queue: asyncio.Queue,
        timer=5,
    ) -> None:
        """Get impedance measurement."""
        if self.debug:
            logging.info("[BLE]: Getting impedance measurement")

        if self.write_to_file:
            if not os.path.exists("./logs"):
                os.makedirs("logs")
            datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            local_impedance_recording = open(
                f"./logs/IGEB-imp-{datestr}.txt", "w", encoding="utf-8"
            )

        def write_impedance_to_local(data):
            """Write data to local file."""
            # convert data from bytes to int
            data = int.from_bytes(data, byteorder="little")
            print(f"[BLE]: Impedance value : {round(data/1000,2)} kOhms")
            local_impedance_recording.write(f"{data}\n")

        async def impedance_handler(_, data):
            """Impedance handler for the BLE client.
                Data is put in a queue and forwarded to the API.

            Args:
                callback (handler Object): Handler object
                data (bytes): Binary data package with impedance values
            """
            if self.write_to_file:
                write_impedance_to_local(data)
            # print impdance values which is just a string in kOhms by
            #  dividing by 1000 and rounding to 2 decimals
            await data_queue.put((time.time(), data))

        async with BleakClient(self.address) as client:
            logging.info("[BLE]: Device connected")
            logging.info("[BLE]: Starting impedance measurement")
            await client.start_notify(self.meas_imp_id, impedance_handler)
            await asyncio.sleep(2)

            await client.write_gatt_char(
                self.command_id, utf_8_encode(self.start_imp_cmd)[0]
            )
            await asyncio.sleep(timer)
            await client.write_gatt_char(
                self.command_id, utf_8_encode(self.stop_imp_cmd)[0]
            )
