from django.db import models

from bankbook.models import Bankbook
from card.models import Card
from company.models import Company
from department.models import Department
from employee.models import Employee
from project.models import Project


class Purchase(models.Model):
	idx = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='품의번호')
	department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='부서')
	date = models.DateField(null=True, blank=True, verbose_name='구매날짜') # 구매 시기
	customer = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='거래처')
	METHOD_CHOICES = (('카드', '카드'), ('계좌이체', '계좌이체'), ('현금', '현금'), ('기타', '기타'))
	method = models.CharField(max_length=100, choices=METHOD_CHOICES)
	customer_account = models.ForeignKey(Bankbook, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='이체계좌')
	card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='사용카드')
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='프로젝트')
	employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='구매자')
	METHOD_CHOICES = (('식비', '식비'), ('교통비', '교통비'), ('장비비', '장비비'), ('인건비', '인건비'), ('기타', '기타'))
	category = models.CharField(max_length=100, choices=METHOD_CHOICES, verbose_name='사용 비목')
	cost = models.IntegerField(default=0, verbose_name='사용금액')
	decision = models.BooleanField(default=False)
	result = models.BooleanField(default=False)
	result_code = models.CharField(max_length=100, null=True, blank=True, verbose_name='이체번호')
