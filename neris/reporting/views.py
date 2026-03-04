from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .db import MongoDB
from bson import ObjectId
import json
import os

from .validation import NerisValidator

class CADFeedViewSet(viewsets.ViewSet):
    def list(self, request):
        events = list(MongoDB.get_collection('cad_feed').find())
        for e in events: e['_id'] = str(e['_id'])
        return Response(events)

class UnitViewSet(viewsets.ViewSet):
    def list(self, request):
        units = list(MongoDB.get_collection('units').find())
        for u in units: u['_id'] = str(u['_id'])
        return Response(units)

class PersonnelViewSet(viewsets.ViewSet):
    def list(self, request):
        staff = list(MongoDB.get_collection('personnel').find())
        for s in staff: s['_id'] = str(s['_id'])
        return Response(staff)

class IncidentViewSet(viewsets.ViewSet):
    def get_collection(self):
        return MongoDB.get_collection('incidents')

    @action(detail=True, methods=['get'])
    def validate(self, request, pk=None):
        incident = self.get_collection().find_one({'_id': ObjectId(pk)})
        if not incident:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        validator = NerisValidator()
        errors = validator.validate_incident(incident.get('data', {}))
        
        return Response({
            'incident_id': str(incident['_id']),
            'valid': len([e for e in errors if e['level'] == 'error']) == 0,
            'errors': errors
        })

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
