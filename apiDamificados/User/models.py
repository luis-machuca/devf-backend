# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
	def _create_user(self, email, password, **extra_fields):
		if not email or not password:
			raise ValueError('Los datos estan incompletos')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password, **extra_fields):
		return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
	email = models.CharField(unique=True, max_length=50)
	objects = UserManager()
	USERNAME_FIELD = 'email'
