from rest_framework import serializers
from data.espnPackage.main import cricket_data

from typing import Any, Dict

class DataFieldSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    country = serializers.CharField(write_only=True)
    main_category = serializers.CharField(write_only=True)
    sub_category = serializers.CharField(write_only=True)
    sorting = serializers.CharField(write_only=True)

    meta = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    main = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Data is fetch from espn sports site in form of html and then html is 
        parsed accordingly to clean data. this cleaned data is then attached to 
        Api endpoint "cricket-data-api/get".  
        """

        main_category = validated_data['main_category']
        country = validated_data['country']
        sub_category = validated_data['sub_category']
        sorting = validated_data['sorting']

        cricket_data_object = cricket_data(
            main_category, sorting, sub_category, country)

        request = self.context.get('request', None)
        if request:
            user = request.user

        user_obj: Dict[str, Any] = {
            'name': user.name,
            'email': user.email
        }

        resource: Dict[str, Any] = {
            'user': user_obj,
            'meta': cricket_data_object.get_meta_data,
            'main': cricket_data_object.get_main_data
        }

        return resource
