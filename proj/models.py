from django.db import models
class Proj(models.Model):
	name = models.CharField(max_length=100, unique=True)
	desc = models.TextField(null=True, blank=True)
