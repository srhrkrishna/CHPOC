from django.contrib.auth.models import User, Group
from rest_framework import serializers


class cdx_compositesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ()


#class GroupSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Group
#        fields = ('url', 'name')
