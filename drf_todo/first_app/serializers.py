from rest_framework import serializers
from .models import ToDoModel

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoModel
        fields =["craeted","user","title","description","complate"]