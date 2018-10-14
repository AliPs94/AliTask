from rest_framework import serializers
from models import Parts
from rest_framework import viewsets, status

class PartsSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parts
        fields = ('id','name','stadium')

class PartsViewSet(viewsets.ModelViewSet):
    queryset = Parts.objects.all()
    serializer_class = PartsSerialiser