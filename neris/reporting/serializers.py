from rest_framework import serializers
from .models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['_id', 'neris_id', 'internal_id', 'data', 'status', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_at', 'updated_at']

class LookupSerializer(serializers.Serializer):
    key = serializers.CharField()
    options = serializers.ListField()
