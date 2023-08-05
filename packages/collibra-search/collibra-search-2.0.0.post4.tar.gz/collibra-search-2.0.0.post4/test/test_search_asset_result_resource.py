# coding: utf-8

"""
    Collibra Search API

    <p>The Search API allows you to create your own integration with the Collibra Search Engine.<br /> Find your data!</p>  # noqa: E501

    The version of the OpenAPI document: 2.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import collibra_search
from collibra_search.models.search_asset_result_resource import SearchAssetResultResource  # noqa: E501
from collibra_search.rest import ApiException

class TestSearchAssetResultResource(unittest.TestCase):
    """SearchAssetResultResource unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SearchAssetResultResource
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = collibra_search.models.search_asset_result_resource.SearchAssetResultResource()  # noqa: E501
        if include_optional :
            return SearchAssetResultResource(
                display_name = 'Simple display name', 
                type = collibra_search.models.search_result_type.SearchResultType(
                    id = '0', 
                    name = '0', ), 
                tags = [
                    '0'
                    ], 
                status = collibra_search.models.search_result_status.SearchResultStatus(
                    id = '0', 
                    name = '"Approved"', )
            )
        else :
            return SearchAssetResultResource(
        )

    def testSearchAssetResultResource(self):
        """Test SearchAssetResultResource"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
