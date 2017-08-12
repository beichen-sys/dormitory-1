from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Owner(models.Model):
    user = models.OneToOneField(User)
    user_type = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.user.username

class College(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Secretary(models.Model):
    user = models.ForeignKey(Owner)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=200, null=True)
    collegeid = models.ForeignKey(College)
    def __str__(self):
        return self.name

class Instructor(models.Model):
    user = models.ForeignKey(Owner)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=20)
    instructorid = models.ForeignKey(Instructor, null=True)
    collegeid = models.ForeignKey(College, null=True)
    def __str__(self):
        return self.name

class Building(models.Model):
    name = models.CharField(max_length=20)
    amount = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.name

class Housemaster(models.Model):
    user = models.ForeignKey(Owner)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=200, null=True)
    buildingid = models.ForeignKey(Building, null=True)
    def __str__(self):
        return self.name

class Visitor(models.Model):
    name = models.CharField(max_length=20)
    sex = models.BooleanField()
    document_type = models.CharField(max_length=20, null=True)
    documentno = models.CharField(max_length=20, null=True)
    contact = models.CharField(max_length=200, null=True)
    dt = models.DateTimeField()
    housemasterid = models.ForeignKey(Housemaster)
    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20, null=True)
    capacity = models.IntegerField(default=0, null=True)
    buildingid = models.ForeignKey(Building)
    def __str__(self):
        return self.name

class Mark(models.Model):
    roomid = models.ForeignKey(Room)
    dt = models.DateTimeField()
    score = models.FloatField()
    housemasterid = models.ForeignKey(Housemaster)
    remark = models.TextField(null=True)
    class Meta:
        unique_together = ('roomid', 'dt')

class Fee(models.Model):
    roomid = models.OneToOneField(Room, primary_key=True)
    remain = models.FloatField()

class FeeRecord(models.Model):
    roomid = models.ForeignKey(Room)
    dt = models.DateTimeField()
    amount = models.FloatField()
    class Meta:
        unique_together = ('roomid', 'dt')

class Student(models.Model):
    sno = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(Owner)
    name = models.CharField(max_length=20)
    sex = models.NullBooleanField(null=True)
    classid = models.ForeignKey(Class, null=True)
    roomid = models.ForeignKey(Room, null=True)
    contact = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class EnterApply(models.Model):
    sno = models.ForeignKey(Student)
    roomid = models.ForeignKey(Room)
    dt = models.DateTimeField()
    housemaster_check = models.NullBooleanField(null=True)
    instructor_check = models.NullBooleanField(null=True)
    secretary_check = models.NullBooleanField(null=True)
    class Meta:
        unique_together = ('sno', 'roomid', 'dt')

class QuitApply(models.Model):
    sno = models.ForeignKey(Student)
    roomid = models.ForeignKey(Room)
    dt = models.DateTimeField()
    reason = models.TextField()
    housemaster_check = models.NullBooleanField(null=True)
    instructor_check = models.NullBooleanField(null=True)
    secretary_check = models.NullBooleanField(null=True)
    class Meta:
        unique_together = ('sno', 'roomid', 'dt')

class LiveRecord(models.Model):
    sno = models.ForeignKey(Student)
    roomid = models.ForeignKey(Room)
    enter_time = models.DateTimeField()
    quit_time = models.DateTimeField(null=True)
    class Meta:
        unique_together = ('sno', 'roomid', 'enter_time')

class Maintenance(models.Model):
    user = models.ForeignKey(Owner)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Repair(models.Model):
    item = models.CharField(max_length=20)
    roomid = models.ForeignKey(Room)
    book_dt = models.DateTimeField()
    reason = models.TextField(null=True)
    fix_dt = models.DateTimeField(null=True)
    maintenanceid = models.ForeignKey(Maintenance, null=True)
    remark = models.TextField(null=True)
    class Meta:
        unique_together = ('item', 'roomid', 'book_dt')
    def __str__(self):
        return self.item
