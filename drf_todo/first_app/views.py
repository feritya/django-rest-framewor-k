from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import ToDoModel
from .serializers import ToDoSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend



class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
   
    authentication_classes = [TokenAuthentication       ]
    permission_classes = [IsAuthenticated]

    serializer_class=ToDoSerializer
    queryset = ToDoModel.objects.all()
    # lookup_field= "pk"
    def get(self, request,pk):
        if pk:
            return self.retrieve(request,pk)
        return self.list(request)
    def post(self,request,pk):
        return self.create(request)
    def put(self,request,pk):
        return self.update(request,pk)
    def delete(self,request,pk):
        return self.destroy(request, pk)


    
    


class ToDoView(APIView):
     authentication_classes = [BasicAuthentication,SessionAuthentication]
     permission_classes = [IsAuthenticated]

     def get(self,request):

         obj= ToDoModel.objects.all()
         serializer = ToDoSerializer(obj,many = True)

         return Response(serializer.data)
     def post(self,request):
         serializer = ToDoSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ToDoDetailView(APIView):
    authentication_classes = [BasicAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            to = ToDoModel.objects.get(pk=pk)

        except ToDoModel.DoesNotExist:    
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,pk):
        to = self.get_object(pk)
        serializer = ToDoSerializer(to)
        return Response(serializer.data)
    def put(self,request,pk):
        to = self.get_object(pk)
        serializer=ToDoSerializer(to,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        to = self.get_object(pk)
        to.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        









@api_view(["GET","POST"])
def todo_list(request):
    if request.method == "GET":
        obj= ToDoModel.objects.all()
        serializer = ToDoSerializer(obj,many = True)
        return Response(serializer.data)

    elif request.method == "POST":
        # # data = JSONParser().parse(request)#requestten gelen bilgiyi dataya atacak
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT","DELETE"])
def todo_detail(request,pk):
    try:
       to = ToDoModel.objects.get(pk=pk)

    except ToDoModel.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serializer = ToDoSerializer(to)
        return Response(serializer.data)

    elif request.method == "PUT":
        # data = JSONParser().parse(request)
        serializer=ToDoSerializer(to,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        to.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



