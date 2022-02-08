from rest_framework import serializers
from files.models import File, Link


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)
    class Meta:
        model = File
        fields = ['file']



class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['link']