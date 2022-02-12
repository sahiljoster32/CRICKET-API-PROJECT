
from __future__ import annotations
from bs4 import BeautifulSoup
from data.espnPackage.url_provider import url_segments_cricket
from typing import *

import requests
import json
import datetime
import pprint  # should only be used for print


class cricket_data():

    """
    DOC: Returns API ready data in json format, 
    this data is fetch and parsed from site "stats.espncricinfo.com"
        following are the properties to be used for fetching the data:
            1. get_json_data
                To get data in simple string without any indentation format.
            2. get_parsed_data
                To get data in complex string with indentation equals to 4 units format.
    RETURNS: Data is returned in following format:
                {
                "meta_data":{
                    "current_stamp":"XXX",
                    "field_description":{
                        .
                        .
                        .
                        .
                    "player_url":"relative link of each player"
                    },
                    "source_url":"https://stats.espncricinfo.comXXXXX",
                    "data_length":50,
                    "keys":[
                    .
                    .
                    .
                    "player_url"
                    ],
                    "keys_length":....
                    },
                "data":{
                    "player_1":{.......
                        },
                    "player_2":{.......
                        },
                    .
                    .,
                    "player_X":{......
                }}}
    """

    def __init__(
            self,
            main_category: str,
            main_sub_category: str,
            subclass: str,
            country: str) -> None:
        """
        DOC: Initializes all private attributes of parsed object.
        """

        first_url: url_segments_cricket = url_segments_cricket(
            main_category,
            main_sub_category,
            subclass,
            country
        )

        self.source_url = first_url.get_absolute_url()
        self.batting_data = []
        self.headings_values = []
        self.headings_description = []
        self.main_data_dict = {}
        self.meta_data_dict = {}
        self.raw_data = {}

        batting_oneDayInternationals_fetch_url: str = self.source_url
        requested_data = requests.get(batting_oneDayInternationals_fetch_url)
        self.unparsed_data = BeautifulSoup(requested_data.text, 'html.parser')

        self._main_run()

    def _cricket_data_parser(self, unparsed_data: list) -> None:
        """
        DOC: Function to fetch actual raw-data from site and
        supply it into the form of list.
        """

        batting_data_unparsed: list = unparsed_data.find_all(class_="data1")

        for player_elem in batting_data_unparsed:

            player_data: list = []
            player_data_elem = player_elem.find_all(nowrap="nowrap")
            player_link = player_data_elem[0].a["href"]
            player_data.append(player_link)

            for data in player_data_elem:
                player_data.append(data.get_text())

            self.batting_data.append(player_data)

    def _cricket_data_heading(self, unparsed_data: list) -> None:
        """
        DOC: Function to parse and fetch headings of each columns.
        """

        main_table_ele = unparsed_data.find("thead")
        heading_elements: List = main_table_ele.find_all("th")

        for head_element in heading_elements:

            head_text = head_element.get_text()
            if head_text != '':
                head_title_txt = head_element.get('title')

                self.headings_values.append(head_element.get_text())
                self.headings_description.append(head_title_txt)

    def _mainData_binder(self, headings: List, batting_data: List) -> None:
        """
        DOC: Binds the data with their respective field and supply it into dictionary format.
        """
        headingsLen = len(headings)
        basicDataLen = len(batting_data[0])

        if headingsLen == (basicDataLen - 1):
            for player_id, data in enumerate(batting_data):
                temp_player_data = {}

                for index in range(headingsLen + 1):
                    if index == 0:
                        temp_player_data["player_url"] = data[index]
                    elif index != 0:
                        temp_player_data[headings[index - 1]] = data[index]

                self.main_data_dict[f"player_{player_id + 1}"] = temp_player_data

    def _metaData_binder(self, headings: List, headings_description: List) -> None:
        """
        DOC: This function fetch and populate meta data from site.
        """

        fields_description = {}
        current_date = datetime.datetime.now()

        self.meta_data_dict["current_stamp"] = f"{current_date}"

        if len(headings_description) == len(headings):
            for index, value in enumerate(headings):
                fields_description[headings[index]
                                   ] = headings_description[index]
            fields_description['player_url'] = 'relative link of each player'

        self.meta_data_dict['field_description'] = fields_description
        self.meta_data_dict['source_url'] = self.source_url
        self.meta_data_dict['data_length'] = len(self.batting_data)
        self.meta_data_dict['keys'] = headings
        self.meta_data_dict['keys'].append('player_url')
        self.meta_data_dict['keys_length'] = len(headings)

    def _get_rawData(self, meta_data: Dict[str, Any], main_data: Dict[str, str]) -> None:
        """
        DOC: This returns raw data which was in python format.
        """
        self.raw_data['meta_data'] = meta_data
        self.raw_data['data'] = main_data

    def _get_json_data(self, raw_data: Dict[str, Dict[str, Any]]) -> str:
        """
        DOC: This function gives json formatted data, without any indentation 
        to send further.
        """
        return json.dumps(raw_data)

    def _get_Json_parsed_data(self, data: str) -> str:
        """
        Return: Data formatted acc. to json documentation, with proper indentation.
        """
        return json.dumps(data, indent=4)

    @property
    def get_json_data(self) -> str:
        """
        Returns: cricket current data in json format.
        """
        return self._get_json_data(self.raw_data)

    @property
    def get_parsed_data(self) -> str:
        """
        Returns: cricket data in json format with indentation 4 units.
        """
        return self._get_Json_parsed_data(self.raw_data)

    @property
    def get_raw_data(self) -> str:
        """Returns: whole raw data to console"""
        return self.raw_data

    @property
    def get_meta_data(self) -> str:
        """Return: get meta data about fetch api data"""
        return self.meta_data_dict

    @property
    def get_main_data(self) -> str:
        """Returns: get main data about fetch api data"""
        return self.main_data_dict

    def _main_run(self):
        """
        DOC: Runs all functions accordingly to populate respective properties of cricket_data object.
        """
        self._cricket_data_parser(self.unparsed_data)
        self._cricket_data_heading(self.unparsed_data)
        self._mainData_binder(self.headings_values, self.batting_data)
        self._metaData_binder(self.headings_values, self.headings_description)
        self._get_rawData(self.meta_data_dict, self.main_data_dict)


if __name__ == "__main__":

    cricket_Api_obj = cricket_data(
        "batting",
        "high_scores",
        "test_match",
        "India"
    )

    print(cricket_Api_obj.get_json_data)
