# models.py
import uuid
from django.db import models

class OCRRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='uploads/')
    extracted_text = models.TextField()
    template_choice = models.CharField(max_length=100,   default='modern_minimal')

    created_at = models.DateTimeField(auto_now_add=True)
