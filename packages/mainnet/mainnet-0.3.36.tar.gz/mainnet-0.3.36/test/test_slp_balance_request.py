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
import datetime

import mainnet
from mainnet.models.slp_balance_request import SlpBalanceRequest  # noqa: E501
from mainnet.rest import ApiException

class TestSlpBalanceRequest(unittest.TestCase):
    """SlpBalanceRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SlpBalanceRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = mainnet.models.slp_balance_request.SlpBalanceRequest()  # noqa: E501
        if include_optional :
            return SlpBalanceRequest(
                wallet_id = 'wif:testnet:cNfsPtqN2bMRS7vH5qd8tR8GMvgXyL5BjnGAKgZ8DYEiCrCCQcP6', 
                token_id = '132731d90ac4c88a79d55eae2ad92709b415de886329e958cf35fdd81ba34c15'
            )
        else :
            return SlpBalanceRequest(
                wallet_id = 'wif:testnet:cNfsPtqN2bMRS7vH5qd8tR8GMvgXyL5BjnGAKgZ8DYEiCrCCQcP6',
        )

    def testSlpBalanceRequest(self):
        """Test SlpBalanceRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
