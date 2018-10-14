# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from datetime import date
from django.shortcuts import render
from serializer import PartsSerialiser
from django.http import HttpResponse
from dateutil import parser
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Stadium.models import *
import pytz

utc=pytz.UTC

def checkWorkigTime(stadium_id,start_time,end_time):
    availabilitys = Availability.objects.filter(stadium_id=stadium_id)
    weekday = start_time.weekday()
    for availability in availabilitys:
        if availability.weekday == "MO":
            if start_time.replace(tzinfo=utc) > availability.start_time.replace(tzinfo=utc): #and end_time < availability.end_time:
                return True
    return False


def checkRentalStatus(part_id,start_time,end_time):
    rentals = Rental.objects.filter(part_id=part_id)
    for rental in rentals:
        order = Orders.objects.get(id=rental.order_id)
        if (start_time.replace(tzinfo=utc) < order.start_time and start_time.replace(tzinfo=utc) > order.end_time) or \
                (end_time.replace(tzinfo=utc) < order.start_time and end_time.replace(tzinfo=utc) > order.end_time):
            return
    return Parts.objects.get(pk=part_id)


@api_view(['GET'])
def checkstadium(request):
    start_time = parser.parse(request.GET['start_time'])
    end_time = parser.parse(request.GET['end_time'])
    stadiums = Stadium.objects.all()
    part_list = []
    for stadium in stadiums:
        if checkWorkigTime(stadium.id, start_time, end_time):
            for part in Parts.objects.filter(stadium_id=stadium.id):
                part_list.append(checkRentalStatus(part.id,start_time,end_time))
    stadiums_dic={}
    for part in part_list:
        stadium_id = Stadium.objects.get(pk=part.stadium_id).id
        if stadium_id in stadiums_dic.keys():
            stadiums_dic[stadium_id]=stadiums_dic[stadium_id]+1
        else:
            stadiums_dic[stadium_id]=1

    return Response(stadiums_dic)

    #return HttpResponse(part_list, content_type='application/json')


@api_view(['POST'])
def reserve(request):

    stadium = Stadium.objects.get(pk=request.data['stadium_id'])
    customer = Customer.objects.get(pk=request.data['customer_id'])
    number_of_parts = request.data['number_of_parts']
    start_time = parser.parse(request.data['start_time'])
    end_time = parser.parse(request.data['end_time'])
    if checkWorkigTime(stadium.id, start_time, end_time):
        for part in Parts.objects.filter(stadium_id=stadium.id):
            part_id = checkRentalStatus(part.id,start_time,end_time)
    order = Orders(customer=customer, stadium=stadium, number_of_parts =number_of_parts,start_time=start_time,end_time=end_time)
    order.save()
    rental = Rental(order=order,part=part_id)
    rental.save()

    return HttpResponse("done",status=status.HTTP_201_CREATED)

