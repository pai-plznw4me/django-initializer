from tabnanny import verbose

from django.db import models
class Company(models.Model):
	name = models.CharField(max_length=100, verbose_name='이름')
	description = models.TextField(null=True, blank=True, verbose_name='설명')
	logo = models.ImageField(null=True, blank=True, verbose_name='회사 로고')
	registration = models.FileField(null=True, blank=True, verbose_name='사업자등록증')
	registration_code = models.CharField(max_length=50, verbose_name='사업자번호', null=True, blank=True)
	phone = models.CharField(max_length=50, verbose_name='번호', null=True, blank=True)
	fax = models.CharField(max_length=50, verbose_name='팩스', null=True, blank=True)
	bank_name = models.CharField(max_length=50, verbose_name='은행명', null=True, blank=True)
	bank_account = models.CharField(max_length=50, verbose_name='은행계좌', null=True, blank=True)
	manager_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='행정 담당자')
	manager_phonenumber = models.CharField(max_length=50, null=True, blank=True, verbose_name='행정 담당자 번호')

	def __str__(self):
		return self.name
