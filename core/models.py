from django.db import models


class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    doi = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='papers/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True, null=True)
    audio = models.FileField(upload_to='audios/', blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    citation = models.TextField(blank=True, null=True)  # Added citation field
