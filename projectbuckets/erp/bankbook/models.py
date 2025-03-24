from django.db import models
class Bankbook(models.Model):
	owner = models.CharField(max_length=50, verbose_name='예금주')
	description = models.TextField()
	bank_name = models.CharField(max_length=50, verbose_name='은행명')
	code = models.CharField(max_length=50, verbose_name='통장번호')
	alias = models.CharField(max_length=50, verbose_name='통장별명')
