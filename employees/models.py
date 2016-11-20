from django.db import models

class Department(models.Model):
	name = models.CharField(max_length=128,unique=True)

	def __str__(self):
		return self.name


class Employee(models.Model):
	name = models.CharField(max_length=512)
	email = models.EmailField(max_length=255,unique=True)
	department = models.ForeignKey(Department,related_name='department')

	def __str__(self):
		return self.name

