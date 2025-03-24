from tabnanny import verbose
from tkinter.constants import CASCADE

from django.db import models

from bank.models import Bank
from department.models import Department


class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name='이름')
    identification = models.CharField(max_length=100, verbose_name='사번')
    join = models.DateField(verbose_name='입사 날짜')
    quit = models.DateField(verbose_name='퇴직 날짜', null=True, blank=True)
    STATE_CHOICES = (('Active', '재직중'), ('Absence', '휴직중'), ('Departure', '퇴사'))
    state = models.CharField(max_length=20, verbose_name='재직여부', choices=STATE_CHOICES)
    address = models.CharField(max_length=100, verbose_name='주소')
    phone = models.CharField(max_length=20, verbose_name='전화번호')
    responsibility = models.CharField(max_length=20, verbose_name='직무', null=True, blank=True)

    RANK_CHOICES = (('Staff', '사원'), ('Junior', '주임'), ('Assistant', '대리'), ('Manager', '과장'),
                    ('Senior', '차장'), ('Deputy', '부장'),
                    ('Director', '이사'), ('ExecutiveDirector', '상무'), ('ManagingDirector', '전무'),
                    ('VicePresident', '부사장'), ('President', '사장'))
    rank = models.CharField(max_length=20, verbose_name='직위', choices=RANK_CHOICES)

    ROLE_CHOICES = (('CEO', '최고경영자'), ('COO', '최고운영책임자'), ('CFO', '최고재무책임자'), ('CMO', '최고마케팅책임자'),
                    ('CTO', '최고기술책임자'), ('CSO', '최고전략책임자'), ('Team Leader', '팀장'), ('Team Member', '팀원'))
    role = models.CharField(max_length=20, verbose_name='직책', choices=ROLE_CHOICES)

    level = models.CharField(max_length=20, verbose_name='직급', null=True, blank=True)
    resident_no = models.CharField(max_length=20, verbose_name='주민등록번호')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='부서')
    TYPE_CHOICE = (('full time', '정규직'), ('part time', '계약직'), ('freelancer', '프리랜서'))
    type = models.CharField(max_length=20, verbose_name='근로 계약 형식', choices=TYPE_CHOICE)
    bank_account = models.ForeignKey(Bank, on_delete=models.SET_NULL, verbose_name='계좌', null=True, blank=True)


    def __str__(self):
        return self.name