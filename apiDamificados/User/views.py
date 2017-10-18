# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User
from .serializer import UserSerializer

from django.shortcuts import render
import requests
import json

# Create your views here.
class UserRegister(APIView):
	permission_classes = (AllowAny,)

	def get(self, request):
		Users = User.objects.all()
		#serializer = PeopleGetName(people, many=True)
		serializer = UserSerializer(user, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = UserSerializer(data=request.data)
		#print(serializer)
		#print(serializer.is_valid())
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)