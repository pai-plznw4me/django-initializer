from django.db import models
class Department(models.Model):
	name = models.CharField(max_length=100)
	desc = models.CharField(max_length=100)
