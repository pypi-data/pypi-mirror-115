from mlplatform_lib.hyperdata_client import HyperdataUserAuth
from mlplatform_lib.pre_check_base import PreCheckBase
import yaml


class PreCheckPredefinedAI(PreCheckBase):
    def __init__(self, server_config_path: str):
        super().__init__(server_config_path)
        server_config = yaml.safe_load(open(server_config_path))

        try:
            self.train_do_name = server_config["train_do_name"]
            self.inference_do_name = server_config["inference_do_name"]
        except KeyError as e:
            print(f'Cannot found "{str(e)}" in server_config.yaml')
            exit(1)

    def _check_train_do_exist(self):
        self._print_header(f'check is train do "{self.train_do_name}" exist.')
        self.auth = HyperdataUserAuth(
            project_id=self.mlplatform_request_header["projectId"],
            authorization=self.mlplatform_request_header["Authorization"],
            user_id=self.mlplatform_request_header["userId"],
        )
        do_list = self.hyperdata_client.get_do_list(self.auth)
        for do_info in do_list:
            if do_info.name == self.train_do_name:
                self.train_do_id = do_info.id
                print("check train do end.\n")
                return

        print("cannot found train do")
        exit(1)

    def _check_inference_do_exist(self):
        self._print_header(f'check is inference do "{self.inference_do_name}" exist.')
        do_list = self.hyperdata_client.get_do_list(self.auth)

        for do_info in do_list:
            if do_info.name == self.inference_do_name:
                print("check inference do end.\n")
                self.inference_do_id = do_info.id
                return

        print("cannot found inference do")
        exit(1)

    def run(self):
        super().run()
        self._check_train_do_exist()
        self._check_inference_do_exist()
