from django.db import models

from bank.models import Bank
from department.models import Department
from employee.models import Employee


class Card(models.Model):
	name = models.CharField(max_length=100)
	desacription = models.TextField()
	code = models.CharField(max_length=20)
	bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True)
	owner = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
	department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
