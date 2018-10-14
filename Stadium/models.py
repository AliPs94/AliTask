# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from enum import Enum
from django.core.validators import MaxValueValidator

from django.db import models


class WeekDayChoice(Enum):
    SU = "SUNDAY"
    MO = "MONDAY"
    TU = "TUESDAY"
    WE = "WEDNESDAY"
    TH = "THURSDAY"
    FR = "FRIDAY"
    SA = "SATURDAY"

class Owner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null= True, unique= True)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null= True, unique= True)
    join_date = models.DateTimeField(default=timezone.now())


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE)


class Parts(models.Model):
    stadium = models.ForeignKey(Stadium,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Availability(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=2, choices=[(tag, tag.value) for tag in WeekDayChoice])
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Orders(models.Model):
    customer = models.ForeignKey(Customer)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    number_of_parts = models.PositiveIntegerField(validators=[MaxValueValidator(4),])
    price = models.PositiveIntegerField(default=10)
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(default=timezone.now())
    create_time = models.DateTimeField(default=timezone.now())

class Rental(models.Model):
    order = models.ForeignKey(Orders)
    part = models.ForeignKey(Parts)


