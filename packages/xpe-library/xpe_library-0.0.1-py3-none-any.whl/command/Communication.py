import threading
from http.server import HTTPServer
from typing import Optional
from typing import List, Dict

from src.command.EventServer import ProcessEvent
from src.request.HttpRequest import HttpRequest
from src.models.Relay import Relay
from src.models.FactoryModel import factory_model_from_json
from src.models.FactoryModel import factory_model_to_dict
from src.models.Input import Input
from src.models.User import User
from src.models.DialPlan import DialPlan
from enum import Enum


class _CommunicationAction(Enum):
    GET = "get"  # get info using post method
    ADD = "add"  # add resource
    SET = "set"  # update resource
    INFO = "info"
    DEL = "del"  # delete resource
    REBOOT = "reboot"
    CLEAR = "clear"


class Communication:
    """
    Class to call the most important endpoints of the device XPE
    """
    __SUCCESS_MESSAGE = "OK"
    __MESSAGE_FIELD = "message"
    __RETCODE_FIELD = "retcode"
    __DATA_FIELD = "data"
    __DATA_ARRAY_FIELD = "item"
    __TARGET_FIELD = "target"
    __ACTION_FIELD = "action"
    __USER_KEY = "rfkey"
    __DIAL_PLAY_KEY = "dialreplace"
    __event_list: list = []
    __CODE_FAILED_STATUS = [401, 400, 0]

    def __init__(self, ip: str, login: str, password: str, port: int = 5832):
        """
        :param ip: ip of device
        :param login: username to authentication
        :param password: password to authentication
        """
        self.__http_server_port: int = port
        self.__http_server: HTTPServer = HTTPServer(("", self.__http_server_port), ProcessEvent)
        self.__requester = HttpRequest(login=login, password=password)
        self.__base_url = "http://" + ip + "/api/"
        self.__server_running: bool = False

    def get_relay_info(self) -> Optional[Relay]:
        """
        Get all info about relay from the device

        :return: Relay class
        """
        endpoint: str = "relay/get"
        _, body = self.__get_request(endpoint)
        relay = factory_model_from_json(Relay, body)

        return relay

    def set_relay_info(self, relay: Relay):
        """
        Set relay config

        :param relay: Input class
        :return: Success or fail
        """
        payload: dict = factory_model_to_dict(relay)
        executed, _ = self.__post_request(_CommunicationAction.SET, "relay", payload)
        return executed

    def get_all_user(self) -> Optional[List[User]]:
        """
        Get all card users of the device

        :return: A list with all Users or None
        """
        endpoint: str = "rfkey/get"
        _, body = self.__get_request(endpoint)

        return self.__convert_list_dict_2_model(body, User)

    def add_users(self, users: List[User]) -> Optional[List[User]]:
        """
        Send new card users to device.

        :param users: A list with all users to create
        :return: A list with all users created or None if a error happened
        """
        created = self.__send_users(_CommunicationAction.ADD, users)

        return self.__convert_list_dict_2_model(created, User)

    def update_users(self, users: List[User]) -> Optional[List[User]]:
        """
        Update a card user
        :param users: A list with all users to update
        :return: A list with all users updated or None if a error happened
        """
        updated = self.__send_users(_CommunicationAction.SET, users)
        return self.__convert_list_dict_2_model(updated, User)

    def del_users(self, users: List[User]) -> Optional[List[User]]:
        """
        Delete  card users.

        :param users: A list with all users to create
        :return: A list with all users deleted or None if a error happened
        """
        deleted = self.__send_users(_CommunicationAction.DEL, users)
        return self.__convert_list_dict_2_model(deleted, User)

    def del_all_users(self) -> bool:
        """
        Clear all card users
        :return: success or fail
        """
        executed, _ = self.__post_request(_CommunicationAction.CLEAR, "rfkey", None)
        return executed

    def get_input(self) -> Optional[Input]:
        """
        Get all info about input
        :return: Input class
        """
        endpoint: str = "input/get"
        _, body = self.__get_request(endpoint)

        return factory_model_from_json(Input, body)

    def set_input(self, input_value: Input) -> bool:
        """
        Set input config

        :param input_value: Input class
        :return: Success or fail
        """
        payload: dict = factory_model_to_dict(input_value)
        executed, _ = self.__post_request(_CommunicationAction.SET, "input", payload)
        return executed

    def reboot_system(self) -> bool:
        """
        Reboot system
        :return: Success or fail
        """
        sent, _ = self.__post_request(_CommunicationAction.REBOOT, "system", None)
        return sent

    def add_dial_plans(self, dial_plans: List[DialPlan]) -> Optional[List[DialPlan]]:
        """
        Create many dial plans
        :param dial_plans: List with all dial plans to add
        :return: List of all dial plans added
        """
        created = self.__send_dial_plans(_CommunicationAction.ADD, dial_plans)
        return self.__convert_list_dict_2_model(created, DialPlan)

    def update_dial_plans(self, dial_plans: List[DialPlan]) -> Optional[List[DialPlan]]:
        """
        Update many dial plans
        :param dial_plans: List with all dial plans to update
        :return: List of all dial plans updated
        """
        updated = self.__send_dial_plans(_CommunicationAction.SET, dial_plans)
        return self.__convert_list_dict_2_model(updated, DialPlan)

    def delete_dial_plans(self, dial_plans: List[DialPlan]) -> Optional[List[DialPlan]]:
        """
        Delete many dial plans
        :param dial_plans: List with all dial plans to delete
        :return:  List of all dial plans deleted
        """
        deleted = self.__send_dial_plans(_CommunicationAction.DEL, dial_plans)
        return self.__convert_list_dict_2_model(deleted, DialPlan)

    def del_all_dial_plans(self) -> bool:
        """
        Delete all dial plans
        :return: Success or fail
        """
        executed, _ = self.__post_request(_CommunicationAction.CLEAR, self.__DIAL_PLAY_KEY)
        return executed

    def __get_request(self, endpoint: str) -> Optional[tuple]:
        """

        :param endpoint: URL sufix
        :return: A dictionary with the response
        """
        _, body = self.__requester.get(self.__base_url + endpoint)
        return self.__check_request(body)

    def __post_request(self, action: _CommunicationAction, target: str, payload: dict = None) -> Optional[tuple]:
        """

        :param action: Kind of request
        :param target: kind of resource wanted
        :param payload: Info to send
        :return: A tuple with dictionary with the response and success or fail
        """
        request: dict = {
            self.__ACTION_FIELD: action.value,
            self.__TARGET_FIELD: target,
        }
        if payload is not None:  # add payload if exists
            request[self.__DATA_FIELD] = payload
        _, body = self.__requester.post(self.__base_url, request)
        return self.__check_request(body)

    def __check_request(self, body: dict) -> Optional[tuple]:
        """
        Check success or fail of request
        :param body: body returned
        :return: A dictionary with the response or None and if success or fail
        """
        if body is not None and body[self.__MESSAGE_FIELD] == self.__SUCCESS_MESSAGE:
            return True, body.get(self.__DATA_FIELD, None)
        else:
            return False, None

    def __send_users(self, action: _CommunicationAction, users: List[User]) -> Optional[dict]:
        """
        Generic command to send a list of users

        :param action: What do with the users list
        :param users: List of users to send
        :return:
        """
        target: str = self.__USER_KEY
        payload_users = self.__prepare_payload_users(users)
        _, request = self.__post_request(action, target, payload_users)
        return request

    def __prepare_payload_users(self, users: List[User]) -> Optional[dict]:
        """

        :param users: List of users to send
        :return: payload with information about users
        """
        all_users: List[Dict] = []
        payload_users = None
        for user in users:
            user_dict: dict = factory_model_to_dict(user)
            if user_dict is not None:
                all_users.append(user_dict)

        if len(all_users) > 0:
            payload_users = {self.__DATA_ARRAY_FIELD: all_users}

        return payload_users

    def __send_dial_plans(self, action: _CommunicationAction, dial_plans: List[DialPlan]) -> Optional[dict]:
        """

        :param action: Action to send a dial plan
        :param dial_plans: List with all dial plans
        :return: the request
        """
        target: str = self.__DIAL_PLAY_KEY
        payload: dict = self.__prepare_payload_dial_plans(dial_plans)
        _, request = self.__post_request(action, target, payload)
        return request

    def __prepare_payload_dial_plans(self, dial_plans: List[DialPlan]) -> Optional[dict]:
        """
        Build a payload to send many dial plans
        :param dial_plans: List of dial plan to send
        :return: payload with information about dial plan
        """
        all_dial_plans: List[Dict] = []
        payload: dict = None
        for dial_plan in dial_plans:
            dial_plan_dict = factory_model_to_dict(dial_plan)
            if dial_plan_dict is not None:
                all_dial_plans.append(dial_plan_dict)

        if len(all_dial_plans) > 0:
            payload = {self.__DATA_ARRAY_FIELD: all_dial_plans}

        return payload

    def __convert_list_dict_2_model(self, payload: dict, type_model) -> Optional[list]:
        """
        Convert the request of list dictionary to a model list

        :param payload: Body of the request
        :param type_model: type of model
        :return: A list of model type
        """
        if payload is None:
            return payload
        models = []
        for model_dict in payload[self.__DATA_ARRAY_FIELD]:
            model = factory_model_from_json(type_model, model_dict)
            models.append(model)

        return models

    def run_server(self):
        """
        Start running the server
        """
        if not self.__server_running:
            self.__server_running = True
            self.__server_thread = threading.Thread(target=self.__http_server.serve_forever, args=())
            self.__server_thread.start()

    def stop_server(self):
        """
        Stop running server
        """
        if self.__server_running:
            self.__http_server.shutdown()
            self.__server_running = False

    def get_event_list(self) -> Optional[list]:
        """
        Get the list that contains all requests received

        :return: list of events
        """
        try:
            # Get list with all events received we are using ProcessEvent to get all request
            # and RequestHandlerClass is the type of ProcessEvent because of this we can access event_list
            events: List[dict] = self.__http_server.RequestHandlerClass.event_list
            events_copy = events.copy()  # create a copy of list of events for avoiding direct manipulation
            events.clear()
            return events_copy
        except:
            return None

    def test_connection(self, login: str = None, password: str = None) -> bool:
        """
        Test connection with the device
        :return: Connected or not
        """
        if login is not None and password is not None:
            self.__requester.change_auth(login, password)
        endpoint: str = "system/status"
        status, _ = self.__requester.get(self.__base_url + endpoint)

        if status in self.__CODE_FAILED_STATUS:
            return False
        else:
            return True

    def is_connected(self):
        """
        Return if is connected
        :return: Connected or not
        """
        return self.test_connection()
