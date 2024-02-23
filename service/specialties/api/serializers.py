from rest_framework import serializers
from .models import *


class SpecialtyCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ('specialty',)


class SpecialtyDetailSerializer(serializers.ModelSerializer):
    comments = SpecialtyCommentSerializer(many=True, read_only=True, required=False)
    url = serializers.HyperlinkedIdentityField(view_name='specialty-detail', lookup_field='slug')
    university = serializers.CharField(source='university.name')

    class Meta:
        model = Specialty
        exclude = ['id']


class SpecialtyListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='specialty-detail', lookup_field='slug')
    university = serializers.CharField(source='university.name')

    class Meta:
        model = Specialty
        exclude = ['id']


class UniversityDetailSerializer(serializers.ModelSerializer):
    specialty_list = SpecialtyListSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='university-detail')

    class Meta:
        model = University
        exclude = ['slug', 'id']


class UniversityListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='university-detail')

    class Meta:
        model = University
        exclude = ['slug', 'id']
