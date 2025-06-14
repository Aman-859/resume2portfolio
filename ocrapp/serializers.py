from rest_framework import serializers
from .models import OCRRecord

class OCRRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRRecord
        fields = ['id', 'image', 'extracted_text', 'created_at']