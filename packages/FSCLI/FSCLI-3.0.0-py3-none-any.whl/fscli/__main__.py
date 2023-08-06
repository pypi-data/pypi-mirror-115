import argparse
import os
import sys

import requests

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from config import *
from set_key import SetKey

class fscli:

    def __init__(self):
        """
        [INFO]: ABOUT FSCLI
        FSCLI is a module that simplifies starting, stopping & deleting servers based on server_id and email.

        [INFO]: HOW TO RUN THIS CLASS
            python3 -m FSCLI --start --email <email> --server_id <server id>
            python3 -m FSCLI --stop_all --email <email>
            python3 -m FSCLI --stop --email <email> --server_id <server id>
            python3 -m FSCLI --destroy_all --email <email>
            python3 -m FSCLI --destroy --email <email> --server_id <server_id>
            python3 -m FSCLI --fraud_set --email <email>
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-st', '--start', help="Arg for starting one server given the ID",
                                 action='store_true')
        self.parser.add_argument('-sa', '--stop_all', help="Arg for stopping all servers given the email",
                                 action='store_true')
        self.parser.add_argument('-so', '--stop', help="Arg for stopping one server given the ID",
                                 action='store_true')
        self.parser.add_argument('-da', '--destroy_all',
                                 help="Arg for destroying all servers given the email",
                                 action='store_true')
        self.parser.add_argument('-d', '--destroy', help="Arg for destroying one server given the ID",
                                 action='store_true')
        self.parser.add_argument('-f', '--fraud_set',
                                 help="Arg for stopping all servers in one's account and setting their account to fraud"
                                      " given the email.",
                                 action='store_true')
        self.parser.add_argument('-e', '--email',
                                 help="The email of the user who is under review.", required=True)
        self.parser.add_argument('-sid', '--server_id',
                                 help="The server id of a particular server.")
        self.parser.add_argument('-c', '--change_key', action='store_true',
                                 help="Change the Airtable API Key")
        self.args = self.parser.parse_args()
        self.check_airtable_key()
        self.email: str = self.args.email
        self.api_key, self.api_token = self.get_api_key_and_token(self.email)
        self.server_id: list = self.get_server_id()
        self.check_if_servers_exist(self.email, self.server_id)

    def determine_action(self) -> None:
        """Determine the action to be taken based on the arguments given by the user.

        Raises:
            Exception: If the user does not input the correct arguments.
        """
        if self.args.change_key:
            self.change_key()
        elif self.args.start:
            self.start(self.server_id[0])
        elif self.args.stop_all:
            self.stop_all()
        elif self.args.stop:
            print(self.server_id)
            self.stop(self.server_id[0])
        elif self.args.destroy_all:
            self.destroy_all()
        elif self.args.destroy:
            self.destroy(self.server_id[0])
        elif self.args.fraud_set:
            self.fraud_set()
        else:
            raise Exception("Please specify an action")

    @staticmethod
    def check_if_servers_exist(email: str, server_id: list) -> None:
        """Check if the server ids provided by the user exist.

        Args:
            email (str): The email of the user.
            server_id (list): A list of server ids retrieved via the email provided.

        Raises:
            Exception: If the user does not any active servers, then a exception is raised.
        """
        if len(server_id) == 0:
            raise Exception("The user by the email of {} does not have any running servers currently.".format(email))

    def get_api_key_and_token(self, email: str) -> tuple:
        """Retrieve the API key and API token from the user's account.

        Args:
            email (str): The email of the user.

        Returns:
            tuple: The tuple contains the API key and API token.
        """
        url = f'{AT_URL_USERS}&filterByFormula=Email%3D"{email}"'
        headers = {"Authorization": "Bearer " + self.AT_KEY}
        machines_dict = requests.get(url, headers=headers).json()
        l_api_key = machines_dict['records'][0]['id']
        l_api_token = machines_dict['records'][0]['fields']['API Token']
        return l_api_key, l_api_token

    def change_key(self) -> None:
        """Change the Airtable API key.
        """
        set_key_inst = SetKey()
        set_key_inst.change_key()

    def check_airtable_key(self):
        try:
            from config import AT_KEY
            if AT_KEY == "":
                raise ImportError("Airtable Key is empty.")
            self.AT_KEY = AT_KEY
        except ImportError:
            set_key_inst = SetKey()
            set_key_inst.main()
            self.AT_KEY = set_key_inst.get_key()

    def destroy(self, server_id: str) -> None:
        """Destroy one server using the Fluidstack API. If the server is still running, the server is first stopped and
        then destroyed.

        Args:
            server_id (str): The server id of the server to be destroyed.

        Raises:
            Exception: If there is an error in the API call.
        """
        url = "https://infinity.fluidstack.io/api/delete/single?api_key={}&api_token={}&server={}" \
            .format(self.api_key, self.api_token, server_id)
        response = requests.get(url).json()
        if response['success']:
            print("Email: {}\nServer ID: {}\nSuccessfully Deleted".format(self.email, server_id))
        else:
            if response['error'] == "You cannot delete a server that is not running or not stopped.":
                self.stop(server_id)
                self.destroy(server_id)
            raise Exception('Error: {}'.format(response['error']))

    def start(self, server_id: str) -> None:
        """Start one server using the Fluidstack API.

        Args:
            server_id (str): The server id of the server to be started.

        Raises:
            Exception: If there is an error in the API call.
        """
        url = "https://infinity.fluidstack.io/api/start/single?api_key={}&api_token={}&server={}" \
            .format(self.api_key, self.api_token, server_id)
        response = requests.get(url).json()
        if response['success']:
            print("Email: {}\nServer ID: {}\nSuccessfully Started".format(self.email, server_id))
        else:
            raise Exception('Error: {}'.format(response['error']))

    def stop(self, server_id: str) -> None:
        """Stop one server using the FluidStack API.

        Args:
            server_id (str): The server id of the server to be stopped.

        Raises:
            Exception: If there is an error in the API call.
        """
        print(server_id)
        url = "https://infinity.fluidstack.io/api/stop/single?api_key={}&api_token={}&server={}" \
            .format(self.api_key, self.api_token, server_id)
        print(url)
        response = requests.get(url).json()
        if response['success']:
            print("Email: {}\nServer ID: {}\nSuccessfully Stopped".format(self.email, server_id))
        else:
            raise Exception('Error: {}'.format(response['error']))

    def stop_all(self) -> None:
        """Stop all servers using the Fluidstack API.

        Raises:
            Exception: If there are not any active servers for the user.
        """
        if self.server_id is not None:
            for machine in self.server_id:
                self.stop(machine)
        else:
            raise Exception("No machines found for the user. Make sure to input the email.")

    def destroy_all(self) -> None:
        """Destroy all servers using the Fluidstack API.

        Raises:
            Exception: If there are not any active servers for the user.
        """
        if self.server_id is not None:
            for machine in self.server_id:
                self.destroy(machine)
        else:
            raise Exception("No machines found for the user. Make sure to input the email.")

    def flag_user(self) -> None:
        """Flag the user's account for review.
        """
        url = AT_URL_USERS + '&filterByFormula=Email%3D"' + self.email + '\"'
        headers = {"Authorization": "Bearer " + self.AT_KEY}
        users_dict = requests.get(url, headers=headers).json()
        url = AT_URL_SINGLE_USER + users_dict["records"][0]["id"]
        headers = {"Authorization": "Bearer " + self.AT_KEY, }
        patch_data = {
            "fields": {
                "Flagged": "Yes"
            }
        }
        requests.patch(url, headers=headers, json=patch_data)

    def fraud_set(self) -> None:
        """Flag the user's account for review and destroy all servers that the user has running.
        """
        self.destroy_all()
        self.flag_user()

    def get_server_id(self) -> list:
        """Retrieve all of the ids of the active servers for the user. 

        Raises:
            Exception: If an argument that requires a server id is not given, an exception is raised.

        Returns:
            list: A list containing all of the active server ids.
        """
        if self.args.server_id is not None:
            return [self.args.server_id]
        else:
            if self.args.start or self.args.stop or self.args.destroy:
                raise Exception("Please provide a server id.")
            else:
                url = "https://infinity.fluidstack.io/api/list?api_key={}&api_token={}" \
                    .format(self.api_key, self.api_token)
                servers = requests.get(url).json()
                server_id_list = []
                for servers in servers['servers']:
                    if servers['status'] == 'Running' and (self.args.stop or self.args.stop_all or self.args.destroy or self.args.destroy_all or self.args.fraud_set):
                        server_id_list.append(servers['id'])
                    elif servers['status'] == 'Stopped' and (self.args.start or self.args.destroy or self.args.destroy_all or self.args.fraud_set):
                        server_id_list.append(servers['id'])
                return server_id_list

    def main(self) -> None:
        """Determine the action to be taken based on the arguments provided.
        """
        self.determine_action()


if __name__ == '__main__':
    fscli_inst = fscli()
    fscli_inst.main()
