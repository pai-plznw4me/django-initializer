from django.db import models

from bankbook.models import Bankbook
from department.models import Department
from employee.models import Employee


class Card(models.Model):
	name = models.CharField(max_length=100)
	desacription = models.TextField(null=True, blank=True)
	code = models.CharField(max_length=20)
	bank = models.ForeignKey(Bankbook, on_delete=models.SET_NULL, null=True, blank=True)
	owner = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
	department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
