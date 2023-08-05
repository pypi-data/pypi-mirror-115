import os
from unittest import mock

import pytest
from django.test import Client

from example_project.settings import LOG_FILE_PATH


@pytest.mark.django_db
@pytest.mark.parametrize('excepted_log_data', [(
        r"""***** Request *****
GET /test/
user: AnonymousUser
remote_addr: 127.0.0.1
Cookie: =
X-Request-Id: static_for_testing


***** Response *****
GET /test/
user: AnonymousUser
remote_addr: 127.0.0.1
Content-Type: text/html; charset=utf-8
X-Request-Id: static_for_testing
status_code: 200
response body is excluded from the log
"""
)]
                         )
def test_init(client: Client, excepted_log_data):
    lof_file_path = LOG_FILE_PATH
    if os.path.isfile(lof_file_path):
        os.remove(lof_file_path)

    with mock.patch('uuid.UUID') as uuid_patch:
        uuid_patch.return_value.hex = "static_for_testing"
        response = client.get('/test/')
        # result_data = json.loads(response.content)

        assert response.status_code == 200
        assert open(lof_file_path).read() == excepted_log_data
