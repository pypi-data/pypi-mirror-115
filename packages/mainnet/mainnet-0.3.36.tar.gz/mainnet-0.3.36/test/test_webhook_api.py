# coding: utf-8

"""
    Mainnet Cash

    A developer friendly bitcoin cash wallet api  This API is currently in *active* development, breaking changes may be made prior to official release of version 1.0.0.   # noqa: E501

    The version of the OpenAPI document: 0.3.35
    Contact: hello@mainnet.cash
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import mainnet
from mainnet.api.webhook_api import WebhookApi  # noqa: E501
from mainnet.rest import ApiException


class TestWebhookApi(unittest.TestCase):
    """WebhookApi unit test stubs"""

    def setUp(self):
        self.api = mainnet.api.webhook_api.WebhookApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_watch_address(self):
        """Test case for watch_address

        Create a webhook to watch cashaddress balance and transactions.   # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
