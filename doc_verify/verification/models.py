from statistics import mode
from django.db import models
import hashlib

# Create your models here.

class Document(models.Model):

    def pdf_upload_path(instance, filename):
        print(instance)
        return f'documents/{instance.uploaded_at.strftime("%d-%m-%y_%H-%M-%S")}_{filename}'

    # def save(self, *args, **kwargs):
    #     with self.document.open('rb') as f:
    #         sha = hashlib.sha256(f.read())
            
    #     self.doc_hash = sha.digest()
    #     super(Document, self).save(*args, **kwargs)

    institute_name = models.CharField(max_length=100)
    holder_name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to=pdf_upload_path, blank=False)
    # doc_hash = models.CharField(max_length=256, blank=True, editable=False)
