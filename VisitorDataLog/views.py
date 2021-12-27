from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
import csv
from itertools import chain
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView, View
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import VisitorUser
from .serializers import VisitorUserSerializer


# For importing data from csv file  ########################
def importdata(request):
    print('path i/p')
    path = 'F:\Tnewrep\Tvisitdata.csv'
    print('before')
    with open(path) as filenm:
        read = csv.reader(filenm)
        for i in read:
            if i[0] != 'UserID':
                _, created = VisitorUser.objects.get_or_create(
                    usernm=i[0],
                    signupdt=i[1],
                    u_segmt=i[2],
                    )

    print('after')
    return HttpResponse('<h1>Welcome ImportData</h1>')
#########################################################################


def index(request):
    return HttpResponse('<h1>Welcome index</h1>')


@api_view(['GET', 'POST'])
def api_detail_all(request):
    if request.method == 'GET':
        rdata = VisitorUser.objects.all()
        serializer = VisitorUserSerializer(rdata, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = VisitorUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_detail_one(request, uid):
    try:
        visit = VisitorUser.objects.get(pk=uid)
    except VisitorUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VisitorUserSerializer(visit)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = VisitorUserSerializer(visit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def json_detail(request):

    if request.method == 'GET':
        rdata = VisitorUser.objects.all()
        serializer = VisitorUserSerializer(rdata, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        rdata = JSONParser().parse(request)
        serializer = VisitorUserSerializer(rdata, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class GenericListAndDetails(GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    queryset = VisitorUser.objects.all()
    serializer_class = VisitorUserSerializer
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class VisitDataList(APIView):

    def get(self, request):
        rdata = VisitorUser.objects.all()
        serializer = VisitorUserSerializer(rdata, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VisitorUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitDataDetail(APIView):

    def get_object(self, uid):
        try:
            return VisitorUser.objects.get(pk=uid)
        except VisitorUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, uid):
        visit = self.get_object(uid)
        serializer = VisitorUserSerializer(visit)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uid):
        visit = self.get_object(uid)
        serializer = VisitorUserSerializer(visit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid):
        visit = self.get_object(uid)
        visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VisitListDetailviewset(viewsets.ViewSet):

    def list(self, request):
        rdata = VisitorUser.objects.all()
        serializer = VisitorUserSerializer(rdata, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = VisitorUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = VisitorUser.objects.all()
        visit = get_object_or_404(queryset, pk=pk)
        serializer = VisitorUserSerializer(visit)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = VisitorUser.objects.get(pk=pk)
        serializer = VisitorUserSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = VisitorUser.objects.all()
        visit = get_object_or_404(queryset, pk=pk)
        visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VisitViewsetGeneric(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin,
                          mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    queryset = VisitorUser.objects.all()
    serializer_class = VisitorUserSerializer


class VisitViewsetModel(viewsets.ModelViewSet):

    queryset = VisitorUser.objects.all()
    serializer_class = VisitorUserSerializer


class VisitDataFilter(APIView):

    def post(self, request):
        print(request)
        print('-----------------------------')
        print(request.body)
        print('-----------------------------')
        print(request.data)
        segment = request.data.get('u_segmt')
        print(segment)
        usrnm = request.data.get('usernm')
        '''
        '''''' Some Query types:
        
        # rdata = VisitorUser.objects.all()
        # rdata = VisitorUser.objects.filter(u_segmt__in=[segment])
        # rdata = {}
        # for i in segment:
        #    rdata= (rdata | set(rdata.filter(u_segmt=i)))

        #    rdata.update({i:VisitorUser.objects.filter(u_segmt=i)})
        # rdata = rdata.filter(u_segmt__in=segment).order_by('- u_segmt')
        
        # rdata = VisitorUser.objects.values_list('id', 'u_segmt') 
        <QuerySet [(1, 'B'), (2, 'D'), ...]>
        
        # rdata = VisitorUser.objects.values_list('u_segmt', flat=True) 
        <QuerySet ['B', 'C', 'D', ...]>
        
        # rdata = VisitorUser.objects.filter(u_segmt__in=segment).values_list('id', 'usrnm').order_by('- usrnm')
        
        # rdata = VisitorUser.objects.values_list('u_segmt', flat=True).get(id=3)
        # o/p: D
        
        '''''
        rdata = VisitorUser.objects.filter(u_segmt__in=segment).order_by('- u_segmt')
        print("""""""""""""""""""""""""""""""""---""""")
        print(rdata)
        serializer = VisitorUserSerializer(rdata, many=True)
        print('--------------------------')
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

