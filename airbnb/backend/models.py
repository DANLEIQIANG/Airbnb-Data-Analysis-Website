# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Book(models.Model):
    book_name = models.CharField(max_length=64)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.book_name


class GeneralByCity(models.Model):
    city = models.CharField(max_length=64,primary_key=True)
    long_rent = models.IntegerField()
    short_rent = models.IntegerField()
    Entire_home_Or_apt = models.CharField(max_length=64)
    Private_room = models.CharField(max_length=64)
    Shared_room = models.CharField(max_length=64)
    Average_price = models.IntegerField()
    #add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.city, self.long_rent,self.short_rent,self.Entire_home_Or_apt,self.Private_room,self.Shared_room,self.Average_price)

class Avgscore(models.Model):
    city = models.CharField(max_length=64)
    avg_review_score = models.IntegerField()
    neighbourhood = models.CharField(max_length=64,primary_key=True)

    def __unicode__(self):
        return (self.city, self.avg_review_score,self.neighbourhood)



class TopAvgscoreByNeighbor(models.Model):
    city = models.CharField(max_length=64)
    neighborhood = models.CharField(max_length=64)
    review_scores_average = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    #name = models.CharField(max_length=128)
    def __unicode__(self):
        return (self.city, self.neighborhood,self.review_scores_average,self.id)


class AvgPerPrice(models.Model):
    neighbourhood_cleansed = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    avg_val = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return (self.neighbourhood_cleansed, self.city, self.country, self.avg_val)


class MedianPerPrice(models.Model):
    neighbourhood_cleansed = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    med_val = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return (self.neighbourhood_cleansed, self.city, self.country, self.med_val)


class PopularDescription(models.Model):
    country = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return (self.country, self.city, self.word, self.count)