from rest_framework import viewsets, status
from rest_framework.response import Response
from .db import MongoDB
from bson import ObjectId
import json
import os

class IncidentViewSet(viewsets.ViewSet):
    def get_collection(self):
        return MongoDB.get_collection('incidents')

    def list(self, request):
        incidents = list(self.get_collection().find())
        for inc in incidents:
            inc['_id'] = str(inc['_id'])
        return Response(incidents)

    def create(self, request):
        data = request.data
        result = self.get_collection().insert_one(data)
        return Response({'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        incident = self.get_collection().find_one({'_id': ObjectId(pk)})
        if incident:
            incident['_id'] = str(incident['_id'])
            return Response(incident)
        return Response(status=status.HTTP_404_NOT_FOUND)

class LookupViewSet(viewsets.ViewSet):
    def list(self, request):
        # We'll stick to the JSON file for now, but easily moved to Mongo
        lookup_path = 'neris_lookups.json'
        if os.path.exists(lookup_path):
            with open(lookup_path, 'r') as f:
                return Response(json.load(f))
        return Response({'error': 'lookups not synced'}, status=status.HTTP_404_NOT_FOUND)
