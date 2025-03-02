from django.db import models

from proj.models import Proj


class Basicauth(models.Model):
	desc = models.TextField(null=True, blank=True, verbose_name='앱 설명')
	proj = models.ForeignKey(Proj, on_delete=models.CASCADE, verbose_name='앱이 설치 될 프로젝트')
