# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Personas
from .serializers import PeopleGetName,PersonasCreationSerlializer,TodosSerializer2, PersonasSerializer

from django.shortcuts import render
import requests
import json

# Create your views here.

class PersonasApi(APIView):

	def get(self, request):
		people = Personas.objects.all()
		#serializer = PeopleGetName(people, many=True)
		serializer = PersonasSerializer(people, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		print(request.data)
		serializer = PersonasSerializer(data=request.data)
		#print(serializer)
		#print(serializer.is_valid())
		if serializer.is_valid():
			serializer.save()
			self._sendPushNotification("Nueva persona creada", "c9V7Aiypink:APA91bEkNI-BnQd7gqnmatjOGgehE_aFehAFLEWB5jjkoR36y4gYMY92YHMWC86eZuB4gV9iGzAe4Wmz_C2ifnV5tvGrBeDeAOOUhmPnDuvfr7D1xRAGci2U8TQJJldfh91ROMWndTLa")
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def _sendPushNotification(self, message, deviceToken):
		baseUrl = "https://fcm.googleapis.com/fcm/send"
		headers= {"Authorization":"key=AIzaSyB0k006LxEMxjpcL1bgz6CkAtEhX2UjQdY","Content-Type":"application/json"}
		data = {"notification": {"title": message,"body": "5 to 1","icon": "firebase-logo.png","click_action": "http://localhost:8081"},"to":deviceToken}
		data = json.dumps(data)
		pushNotification= requests.post(baseUrl, headers=headers,data=data)
		pushNotificationJson = pushNotification.json()
		if pushNotification.status_code == 200 and "error" not in pushNotificationJson['results'][0]:
			return False
		else:
			return True
#class PersonaHasLugaresApi(APIView):
#	def get(self, request):
#	def post(self, request):
class PersonaApi(APIView):
	def _getPersona(self, pk):
		try:
			return Personas.objects.get(pk=pk)
		except Personas.DoesNotExist:
			raise Http404
	def get(self, request, pk):
		persona = self._getPersona(pk)
		serializer = PersonasSerializer(persona)
		return Response(serializer.data, status=status.HTTP_200_OK)
	def put(self, request, pk):
		persona = self._getPersona(pk)
		serializer = PersonasSerializer(persona, request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	def delete(self, request, pk):
		persona = self._getPersona(pk)
		persona.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)






