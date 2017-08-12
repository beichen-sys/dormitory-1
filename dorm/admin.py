from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Owner, Secretary, College, Instructor, Class, Building, Housemaster, Visitor, Room, Mark, Fee, FeeRecord, Student, EnterApply, QuitApply, LiveRecord, Maintenance, Repair

class OwnerInline(admin.StackedInline):
    model = Owner
    can_delete = False
    verbose_name_plural = 'owner'

class UserAdmin(UserAdmin):
    inlines = (OwnerInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class StudentInline(admin.TabularInline):
    model = Student
    extra = 4

class ClassAdmin(admin.ModelAdmin):
    fieldsets = [
        ('班级名称', {'fields': ['name']}),
        ('辅导员', {'fields': ['instructorid']}),
        ('学院', {'fields': ['collegeid']}),
    ]
    inlines = [StudentInline]
    list_display = ('name', 'instructorid', 'collegeid')
    list_filter = ['collegeid', 'name']
    search_fields = ['collegeid', 'name', 'instructorid']

admin.site.register(Class, ClassAdmin)

class ClassInline(admin.TabularInline):
    model = Class
    extra = 4

class InstructorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('用户', {'fields': ['user']}),
        ('姓名', {'fields': ['name']}),
        ('联系方式', {'fields': ['contact']}),
    ]
    inlines = [ClassInline]
    list_display = ('name', 'contact')
    list_filter = ['name']
    search_fields = ['name', 'contact']

admin.site.register(Instructor, InstructorAdmin)

class SecretaryInline(admin.TabularInline):
    model = Secretary
    extra = 3

class CollegeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('学院名称', {'fields': ['name']}),
    ]
    inlines = [ClassInline, SecretaryInline]
    list_display = ('name', )
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(College, CollegeAdmin)

class RoomInline(admin.TabularInline):
    model = Room
    extra = 5

class HousemasterInline(admin.TabularInline):
    model = Housemaster
    extra = 2

class BuildingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('楼栋名称', {'fields': ['name']}),
        (None, {'fields': ['amount']}),
    ]
    inlines = [RoomInline, HousemasterInline]
    list_display = ('name', 'amount')
    list_filter = ['amount']
    search_fields = ['name']

admin.site.register(Building, BuildingAdmin)

class VisitorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('姓名', {'fields': ['name']}),
        ('性别', {'fields': ['sex']}),
        ('证件类型', {'fields': ['document_type']}),
        ('证件号', {'fields': ['documentno']}),
        ('联系方式', {'fields': ['contact']}),
        ('时间', {'fields': ['dt']}),
        ('宿管', {'fields': ['housemasterid']}),
    ]
    list_display = ('name', 'sex', 'document_type', 'documentno', 'contact', 'dt', 'housemasterid')
    list_filter = ['housemasterid', 'dt', 'name']
    search_fields = ['name', 'housemasterid', 'documentno', 'contact', 'dt']

admin.site.register(Visitor, VisitorAdmin)

class RepairInline(admin.TabularInline):
    model = Repair
    extra = 2

class MaintenanceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('用户', {'fields': ['user']}),
        ('姓名', {'fields': ['name']}),
        ('联系方式', {'fields': ['contact']}),
    ]
    inlines = [RepairInline]
    list_display = ('name', 'contact')
    list_filter = ['name']
    search_fields = ['name', 'contact']

admin.site.register(Maintenance, MaintenanceAdmin)

class FeeInline(admin.TabularInline):
    model = Fee

class FeeRecordInline(admin.TabularInline):
    model = FeeRecord
    extra = 2

class MarkInline(admin.TabularInline):
    model = Mark
    extra = 2

class RoomAdmin(admin.ModelAdmin):
    fieldsets = [
        ('房间名称', {'fields': ['name']}),
        ('房间类型', {'fields': ['room_type']}),
        ('容纳人数', {'fields': ['capacity']}),
        ('所属楼栋', {'fields': ['buildingid']}),
    ]
    inlines = [StudentInline, FeeInline, FeeRecordInline, MarkInline, RepairInline]
    list_display = ('name', 'room_type', 'capacity', 'buildingid')
    list_filter = ['buildingid', 'room_type', 'capacity']
    search_fields = ['name', 'room_type']

admin.site.register(Room, RoomAdmin)

class EnterApplyInline(admin.TabularInline):
    model = EnterApply
    extra = 2

class QuitApplyInline(admin.TabularInline):
    model = QuitApply
    extra = 2

class LiveRecordInline(admin.TabularInline):
    model = LiveRecord
    extra = 2

class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('学号', {'fields': ['sno']}),
        ('用户', {'fields': ['user']}),
        ('姓名', {'fields': ['name']}),
        ('性别', {'fields': ['sex']}),
        ('班级', {'fields': ['classid']}),
        ('房间', {'fields': ['roomid']}),
        ('联系方式', {'fields': ['contact']}),
    ]
    inlines = [EnterApplyInline, QuitApplyInline, LiveRecordInline]
    list_display = ('sno', 'user', 'name', 'sex', 'classid', 'roomid', 'contact')
    list_filter = ['classid', 'name']
    search_fields = ['sno', 'name', 'classid', 'roomid', 'contact']

admin.site.register(Student, StudentAdmin)
