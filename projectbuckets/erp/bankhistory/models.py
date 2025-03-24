from django.db import models

from bankbook.models import Bankbook


class Bankhistory(models.Model):
	transaction_id = models.CharField(max_length=50, verbose_name='거래ID', unique=True, null=True, blank=True)
	bankbook = models.ForeignKey(Bankbook, on_delete=models.SET_NULL, null=True, blank=True)
	transaction_date = models.DateTimeField(verbose_name='거래시간',null=True, blank=True)
	summary = models.CharField(max_length=50, verbose_name='적요', null=True, blank=True)
	detail = models.CharField(max_length=50, verbose_name='기재내용', null=True, blank=True)
	payment = models.IntegerField(verbose_name='지급', null=True, blank=True, default=0)
	deposit = models.IntegerField(verbose_name='입금', null=True, blank=True, default=0)
	bat = models.IntegerField(verbose_name='거래후 잔액', null=True, blank=True, default=0)
	memo = models.CharField(max_length=200, verbose_name='메모', null=True, blank=True)
	NEGO_CHOICES = (('현금', '현금'), ('수표', '수표'), ('어음', '어음'), ('증권', '증권'))
	Negotiable_type = models.CharField(max_length=200, verbose_name='메모', null=True, blank=True, choices=NEGO_CHOICES, default='현금')
