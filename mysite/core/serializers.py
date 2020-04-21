from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Book
        fields = "__all__"

class FileSerializer(serializers.Serializer):

    file = serializers.CharField()


       

