from django.db import models
from proj.models import Proj
from proj.project_wizard import default_url


class Layout(models.Model):
	NAME_CHOICES = (('doctris_base', 'doctris_base'), ('colorlib', 'colorlib'),)
	name = models.CharField(max_length=100, choices=NAME_CHOICES)
	favicon = models.ImageField(null=True, blank=True)
	logo = models.ImageField(null=True, blank=True)
	proj = models.ForeignKey(Proj, on_delete=models.CASCADE, verbose_name='프로젝트')
