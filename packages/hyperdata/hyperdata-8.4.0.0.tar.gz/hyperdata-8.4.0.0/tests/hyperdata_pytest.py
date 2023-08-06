from mlplatform_lib.pre_check_base import PreCheckBase

import pytest


@pytest.mark.usefixtures("get_server_config_path")
def test_pre_check_hyperdata(get_server_config_path):
    server_config_path = get_server_config_path
    pre_check_base = PreCheckBase(
        server_config_path=server_config_path
    )
    pre_check_base.run()
