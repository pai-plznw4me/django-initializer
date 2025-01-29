from django.db import models
from proj.models import Proj


class Basicapp(models.Model):
	name = models.CharField(max_length=100, verbose_name='앱 이름')
	desc = models.TextField(null=True, blank=True, verbose_name='앱 설명')
	proj = models.ForeignKey(Proj, on_delete=models.CASCADE, verbose_name='앱이 설치 될 프로젝트')
