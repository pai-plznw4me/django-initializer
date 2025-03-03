from django.db import models
class Project(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	start = models.DateField()
	end = models.DateField()
	certificate = models.FileField(null=True, black=True)
	state = models.CharField(max_length=50)
	type = models.CharField(max_length=10)
	alias = models.CharField(max_length=100)
	code = models.CharField(max_length=50)
