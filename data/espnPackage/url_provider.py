
"""Provide actual URL based on queried params."""

from __future__ import annotations
from typing import *

from data.espnPackage.constants import cricket_const


class url_segments_cricket:
    """
    Class: To provide and construct url based on query parameters.
    following functions can used to fetch url:-
    1.get_relative_url
    2.get_absolute_url
    """

    def __init__(
        self,
        category_sub_1: str,
        category_sub_2: str,
        subclass_query: str,
        country: str
    ) -> None:
        self._category_sub_1 = category_sub_1
        self._category_sub_2 = category_sub_2
        self._subclass_query = subclass_query
        self._country = country

    def _data_binding(self, pre_html1: str, class_segment: str, country_key: str) -> str:
        # Get error for keywords defined in constants.py.
        return cricket_const.country_url_str(pre_html1, class_segment, country_key)

    def _get_subclass_number(self) -> str:
        return cricket_const.subclass_const(self._subclass_query)

    def _get_category(self) -> str:
        return cricket_const.category_const(self._category_sub_1, self._category_sub_2)

    def _get_url_class_segment(self) -> str:
        self._subclass_query_num = self._get_subclass_number()
        return f"class={self._subclass_query_num};"

    def get_relative_url(self) -> str:
        """
        Returns: relative generated url of site, for which query is requested.
        """
        class_segment = self._get_url_class_segment()
        pre_html = self._get_category()

        return self._data_binding(pre_html, class_segment, self._country)

    def get_absolute_url(self) -> str:
        """
        Returns: absolute generated url of site, for which query is requested.
        """
        class_segment = self._get_url_class_segment()
        pre_html = self._get_category()

        return 'https://stats.espncricinfo.com' + self._data_binding(pre_html, class_segment, self._country)
