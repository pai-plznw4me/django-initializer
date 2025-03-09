from django.db import models

from company.models import Company


class Project(models.Model):
	name = models.CharField(max_length=100, verbose_name='프로젝트명')
	description = models.TextField(verbose_name='설명', null=True, blank=True)
	alias = models.CharField(max_length=100, verbose_name='별명', null=True, blank=True)
	code = models.CharField(max_length=50, verbose_name='프로젝트코드')
	start = models.DateField(verbose_name='시작일', null=True, blank=True)
	end = models.DateField(verbose_name='종료일', null=True, blank=True)
	certificate = models.FileField(null=True, blank=True, verbose_name='실적증명서')
	STATE_CHOICE = (('BTS', '시작전'), ('WIP', '진행중'), ('EOB', '종료')) # work in progress
	state = models.CharField(max_length=50, verbose_name='상태', choices=STATE_CHOICE)
	TYPE_CHOICES = (('EDU', '교육'),('DEV', '개발'),('ETC','기타'))
	type = models.CharField(max_length=10, verbose_name='타입', choices=TYPE_CHOICES)
	size = models.IntegerField(verbose_name='규모', default=0, null=True, blank=True)
	customer = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
