"""
Guardian API websocket utilities.
"""
import os
import json
import asyncio
import logging
import requests
import websockets
from dotenv import load_dotenv
from dataclasses import dataclass, asdict
import socket

from .config import settings
load_dotenv()


class GuardianAPI:
    """Main Guardian API client."""

    def __init__(self, debug: bool = True) -> None:
        self.ws_identifier = settings.WS_IDENTIFIER
        self.rest_api_get_url = settings.REST_API_URL_GET
        self.rest_api_login_url = settings.REST_API_LOGIN

        self.debug: bool = debug
        self.send_to_cloud: bool = True

        self.ping_timeout: int = 10
        self.retry_time: int = 5

        self.last_message_check = False
        self.first_message_check = True

        self.SENTINEL = object()

    def unpack_from_queue(self, package):
        """Unpack data from the queue filled with BLE data

        Args:
            package (dict): _description_

        Returns:
            _type_: _description_
        """
        return (
            package["timestamp"],
            package["device_id"],
            package["data"],
            package["stop"],
        )

    async def connect_ws_api(
        self,
        data_queue: asyncio.Queue,
        deviceID: str = "deviceMockID",
        recordingID: str = "dummy_recID",
    ) -> None:
        """_summary_

        Args:
            data_queue (asyncio.Queue): Data queue from the BLE client
        """

        # init data model
        data_model = GuardianDataModel("", deviceID, recordingID, "", False)

        data = []

        while True:
            if self.debug:
                logging.info("Connecting to WS API...")

            websocket_resource_url = (
                f"wss://{self.ws_identifier}.execute-api.eu-central-1.amazonaws.com/v1"
            )

            try:
                async with websockets.connect(websocket_resource_url) as websocket:
                    # log the websocket resource url
                    self.first_message_check = True
                    if self.debug:
                        logging.info(
                            f"[API]: Connected to websocket resource url: {websocket_resource_url}"
                        )
                        logging.info("Sending data to the cloud")
                    while True:
                        try:
                            # forward data to the cloud
                            if self.send_to_cloud:

                                package = await data_queue.get()
                                (
                                    device_timestamp,
                                    device_id,
                                    data,
                                    stop,
                                ) = self.unpack_from_queue(package)

                                if data is not None:
                                    data_model.deviceTimestamp = device_timestamp
                                    data_model.deviceID = device_id
                                    data_model.payload = data
                                    data_model.stop = stop

                                # print("Sending to the cloud ", asdict(data_model))
                                await websocket.send(json.dumps(asdict(data_model)))
                                package_receipt = await websocket.recv()

                                if self.debug and self.first_message_check:
                                    self.first_message_check = False
                                    logging.info(
                                        "[API]: First package sent: %s",
                                        asdict(data_model),
                                    )
                                    logging.info(
                                        "[API]: First package receipt: %s",
                                        package_receipt,
                                    )

                                if (stop and self.debug) or self.last_message_check:
                                    self.last_message_check = True
                                    logging.info(
                                        "[API]: Final package sent: %s",
                                        asdict(data_model),
                                    )
                                    logging.info(
                                        "[API]: Last package receipt: %s",
                                        package_receipt,
                                    )
                                    logging.info(
                                        "[API]: Cloud connection sucesfully terminated .."
                                    )

                        except (
                            asyncio.TimeoutError,
                            websockets.exceptions.ConnectionClosed,
                        ) as error:
                            logging.error(
                                "[API]: Error in sending data to the cloud: %s", error
                            )
                            try:
                                if self.debug:
                                    logging.info(
                                        "[API]: ws client connection closed or asyncio Timeout"
                                    )
                                pong = await websocket.ping()
                                await asyncio.wait_for(pong, timeout=self.ping_timeout)
                                logging.info(
                                    "Ping successful, connection alive and continue.."
                                )
                                print("Try to ping websocket successful")
                                continue
                            except:
                                logging.error(
                                    f"[API]: Ping failed, connection closed, trying to reconnect in {self.retry_time} seconds"
                                )
                                logging.error("[API]: Ping failed - will retry...")
                                await asyncio.sleep(self.ping_timeout)
                                break
                        except asyncio.CancelledError:
                            async with websockets.connect(
                                websocket_resource_url
                            ) as websocket:
                                await asyncio.sleep(5)
                                logging.info(
                                    "[API]: Websocket connection terminated ..."
                                )
                                logging.info("[API]: Fetching last package from queue")
                                package = await data_queue.get()
                                (
                                    device_timestamp,
                                    device_id,
                                    data,
                                    stop,
                                ) = self.unpack_from_queue(package)

                                logging.info("[API]: Terminating cloud connection ..")
                                if data is not None:
                                    data_model.deviceTimestamp = device_timestamp
                                    data_model.deviceID = device_id
                                    data_model.payload = "STOP_CANCELLED"
                                    data_model.stop = True

                                await websocket.send(json.dumps(asdict(data_model)))
                                package_receipt = await websocket.recv()
                                if self.debug:
                                    logging.info(
                                        "[API]: Final package sent: %s",
                                        asdict(data_model),
                                    )
                                    logging.info(
                                        "[API]: Last package receipt: %s",
                                        package_receipt,
                                    )
                                    logging.info(
                                        "[API]: Cloud connection sucesfully terminated .."
                                    )
                                try:
                                    sys.exit(0)
                                except SystemExit:
                                    os._exit(0)

            except socket.gaierror:
                logging.info(
                    "[API]: Socket error - retrying connection in {} sec (Ctrl-C to quit)".format(
                        self.retry_time
                    )
                )
                print("Websocket connection error - trying to reconnect again....")
                await asyncio.sleep(self.retry_time)
                continue

            except ConnectionRefusedError:
                logging.error(
                    "Cannot connect to API endpoint. Please check the URL and try again."
                )
                logging.error(
                    "Retrying connection in {} seconds".format(self.retry_time)
                )
                await asyncio.sleep(self.retry_time)
                continue

            # TODO: receive response from websocket and handle it, later with bidirectional streaming

    def get_recordings_all(self, device_id: str = "mock-device-0") -> list:
        recordings_url = f"{self.rest_api_login_url}recordings"
        print(recordings_url)
        with requests.Session() as session:
            r = session.get(recordings_url, auth=(device_id, ""))
            if r.status_code == 200:
                print("Recording list retrieved successfully")
                print(r.json())
                return r.json
            else:
                print("Loading recording list failed")

    def get_recordings_by_id(
        self, device_id: str, recording_id: str = "recordingId-0"
    ) -> None:

        recordings_url = f"{self.rest_api_login_url}recordings/{recording_id}"

        with requests.Session() as session:
            r = session.get(recordings_url, auth=(device_id, ""))
            if r.status_code == 200:
                print("Recording ID file found! Downloading...")
                print(r.json())
                return r.json
            else:
                print("Data download failed")
                print(r.status_code)
                print(r.json())

    def download_recording_by_id(
        self, device_id: str, recording_id: str = "recordingId-0"
    ) -> None:

        recordings_url = f"{self.rest_api_login_url}recordings/{recording_id}/download"
        with requests.Session() as session:
            r = session.get(recordings_url, auth=(device_id, ""))
            if r.status_code == 200:
                print("Recording ID file found! Downloading...")
                print(r.json())
                # get url from response
                url = r.json()["downloadUrl"]
                r = session.get(url)

                filename = f"{recording_id}.json"
                with open(filename, "wb") as f:
                    # giving a name and saving it in any required format
                    # opening the file in write mode
                    f.write(r.content)

                print("Downloading complete for recording ID: ", recording_id)
            else:
                print("Data download failed")
                print(r.status_code)
                print(r.json())


@dataclass
# TODO: break it out into separate scripts for better readability and alignment
class GuardianDataModel:
    """Data model for Guardian data"""

    deviceTimestamp: str
    deviceID: str
    recordingID: str
    payload: str  # This is a base64 encoded bytearray as a string
    stop: bool
