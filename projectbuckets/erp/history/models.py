from django.db import models

from employee.models import Employee


class History(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	join = models.DateField()
	quit = models.DateField()
	job = models.CharField(max_length=100, null=True)
	position = models.CharField(max_length=100, null=True)
	rank = models.CharField(max_length=100, null=True)
	responsibility = models.CharField(max_length=100, null=True)
