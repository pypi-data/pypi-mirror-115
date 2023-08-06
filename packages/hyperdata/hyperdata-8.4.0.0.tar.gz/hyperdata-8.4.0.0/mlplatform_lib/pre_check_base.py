from mlplatform_lib.hyperdata_client import HyperdataHttpClient
import yaml
import requests
import json


class PreCheckBase:
    def __init__(self, server_config_path: str):
        server_config = yaml.safe_load(open(server_config_path))
        try:
            self.hyperdata_addr = server_config["hyperdata_addr"]
            self.mlplatform_addr = server_config["mlplatform_addr"]
            self.proauth_addr = server_config["proauth_addr"]
            self.user_id = server_config["user_id"]
            self.user_password = server_config["user_password"]
            self.project_name = server_config["project_name"]
        except KeyError as e:
            print(f'Cannot found "{str(e)}" in server_config.yaml')
            exit(1)

        self.hyperdata_client = HyperdataHttpClient(self.hyperdata_addr)

    def _print_header(self, msg: str):
        print("-" * len(msg))
        print(msg)
        print("-" * len(msg))

    def _check_hyperdata_proauth_server_connect(self):
        self._print_header(f'check proauth server "{self.proauth_addr}" connection.')
        res = requests.post(
            url=self.proauth_addr + "/proauth/oauth/authenticate",
            headers={"Content-Type": "application/json;charset=UTF-8"},
            data=json.dumps({"user_id": self.user_id, "password": self.user_password}),
        )
        if res.status_code != 200:
            print(
                "cannot connect to %s. proauth server returns status code %d"
                % (self.proauth_addr, res.status_code)
            )
            raise Exception(res)

        response = json.loads(res.text)
        if response["result"] == "false":
            raise Exception(response["error"])
        self.access_token = response["token"]
        self.hyperdata_request_header = {"Authorization": self.access_token}
        print("check proauth server connection end.\n")

    def _check_hyperdata_project(self):
        self._print_header(f'check is hyperdata project "{self.project_name}" exist.')

        project_get_url = self.hyperdata_addr + "/hyperdata/web-service/projects"
        res = requests.get(project_get_url, headers=self.hyperdata_request_header)
        if res.status_code != 200:
            print(
                "cannot connect to %s. hyperdata server returns status code %d"
                % (self.hyperdata_addr, res.status_code)
            )
            raise Exception(res)

        project_infos = json.loads(res.text)["dto"]["project"]
        project_id = None
        for project_info in project_infos:
            if project_info["name"] == self.project_name:
                project_id = project_info["id"]
                break
        if project_id is None:
            print(f"Cannot found project {self.project_name}. Please check hyperdata.")
            raise Exception("_check_hyperdata_project failed.")
        else:
            self.project_id = project_id

        print("check hyperdata server connection end.\n")

    def _check_mlplatform_server_connect(self):
        self._print_header(
            f'check mlplatform server "{self.mlplatform_addr}" connection.'
        )
        self.mlplatform_request_header = {
            "projectId": str(self.project_id),
            "Authorization": self.access_token,
            "userId": self.user_id,
            "authorizationType": "hyperdata",
            "Content-Type": "application/json"
        }
        res = requests.get(self.mlplatform_addr, headers=self.mlplatform_request_header)
        if res.status_code != 200:
            print(
                "cannot connect to %s. mlplatform server returns status code %d"
                % (self.mlplatform_addr, res.status_code)
            )
            raise Exception(res)
        print("check mlplatform server connection end.\n")

    def run(self):
        self._check_hyperdata_proauth_server_connect()
        self._check_hyperdata_project()
        self._check_mlplatform_server_connect()
