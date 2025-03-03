from django.db import models
from django.db.models import CharField

from employee.models import Employee

class Education(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='직원명')
	name = models.CharField(max_length=100, verbose_name='학교명')
	LEVEL_CHOICES = (('high', '고졸'), ('bachelor', '학사'), ('master', '석사'), ('doctor', '박사'))
	level = models.CharField(max_length=100,verbose_name='학위')

	department = models.CharField(max_length=100,verbose_name='학과')
	acquisition = models.DateField(null=True, blank=True, verbose_name='취득일')
	certificate = models.FileField(null=True, blank=True,verbose_name='증명서')
	STATE_CHOICES = (('active', '재학중'), ('absence', '휴학'), ('graduate', '졸업'), ('dismissal', '제적'))
	state = CharField(max_length=100, choices=STATE_CHOICES, default='graduate', verbose_name='상태')
	final = models.BooleanField(default=False,verbose_name='최종')

	# TODO: final 은 오직 개인당 오직 하나만 True 을 갖습니다.


def __str__(self):
	return self.name