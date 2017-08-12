from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import Owner, Secretary, Instructor, Class, Building, Housemaster, Visitor, Room, Mark, Fee, FeeRecord, Student, EnterApply, QuitApply, LiveRecord, Maintenance, Repair
def user_login(request):
    return render(request, 'dorm/login.html')

def confirm(request):
    username = request.POST['userAccount']
    password = request.POST['userPwd']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            tab = {'宿舍管理员': 'housemaster',
                   '辅导员': 'instructor',
                   '学生': 'student',
                   '书记': 'secretary',
                   '维修人员': 'maintenance'}
            if hasattr(user, 'owner') and user.owner.user_type in tab:
                return render(request, 'dorm/confirm.html', {'user_type': user.owner.user_type, 'dir': tab[user.owner.user_type]})
            else:
                return redirect('dorm:user_login')
        else:
            return render(request, 'dorm/confirm.html', {'error_message': '帐户不可用！'})
    else:
        return render(request, 'dorm/confirm.html', {'error_message': '用户名或密码错误！'})

def housemaster__add_visitor(request):
    return render(request, 'dorm/housemaster/add_visitor.html')

def housemaster__new_visitor(request):
    user = get_object_or_404(Owner, user=request.user)
    housemaster = get_object_or_404(Housemaster, user=user)
    visitor = Visitor(name=request.POST['name'], sex=request.POST['sex'], document_type=request.POST['type'], documentno=request.POST['id'], contact=request.POST['contact'], dt=timezone.now(), housemasterid=housemaster)
    visitor.save()
    return redirect('dorm:housemaster__visitor')

def housemaster__building(request):
    class RoomItem(object):
        pass
    user = get_object_or_404(Owner, user=request.user)
    housemaster = get_object_or_404(Housemaster, user=user)
    building = housemaster.buildingid
    housemaster_set = Housemaster.objects.filter(buildingid=building)
    room_set = Room.objects.filter(buildingid=building)
    empty = building.amount - len(room_set)
    full = 0
    room_tab = []
    for room in room_set:
        tmp = RoomItem()
        tmp.id = room.id
        tmp.name = room.name
        tmp.room_type = room.room_type
        tmp.capacity = room.capacity
        tmp.occupant = 0
        tmp.class_set = set()
        for student in Student.objects.filter(roomid=room):
            tmp.occupant += 1
            tmp.class_set.add(student.classid)
        if room.capacity == len(Student.objects.filter(roomid=room)):
            full += 1
            tmp.is_full = True
        room_tab.append(tmp)
    return render(request, 'dorm/housemaster/building.html', {'building': building, 'housemaster_set': housemaster_set, 'empty': empty, 'full': full, 'not_full': building.amount-empty-full, 'room_tab': room_tab})

def housemaster__checkin(request):
    user = get_object_or_404(Owner, user=request.user)
    housemaster = get_object_or_404(Housemaster, user=user)
    building = housemaster.buildingid
    rec_set = set()
    for rec in EnterApply.objects.all():
        if rec.roomid.buildingid == building:
            rec.occupant = 0
            for student in Student.objects.filter(roomid=rec.roomid):
                rec.occupant += 1
            rec_set.add(rec)
    return render(request, 'dorm/housemaster/checkin.html', {'rec_set': rec_set})

def housemaster__checkin_result(request):
    for id in request.POST.getlist('checked'):
        rec = EnterApply.objects.get(pk=id)
        rec.housemaster_check = True
        rec.save()
        if rec.instructor_check and rec.secretary_check:
            live_record = LiveRecord(sno=rec.sno, roomid=rec.roomid, enter_time=timezone.now(), quit_time=None)
            live_record.save()
            rec.delete()
    return redirect('dorm:housemaster__checkin')

def housemaster__index(request):
    user = get_object_or_404(Owner, user=request.user)
    housemaster = get_object_or_404(Housemaster, user=user)
    building = housemaster.buildingid
    housemaster_set = Housemaster.objects.filter(buildingid=building)
    room_set = Room.objects.filter(buildingid=building)
    empty = building.amount - len(room_set)
    full = 0
    for room in room_set:
        if room.capacity == len(Student.objects.filter(roomid=room)):
            full += 1
    return render(request, 'dorm/housemaster/index.html', {'housemaster': housemaster, 'building': building, 'housemaster_set': housemaster_set, 'empty': empty, 'full': full, 'not_full': building.amount-empty-full})

def housemaster__lookup(request):
    return render(request, 'dorm/housemaster/lookup.html')

def housemaster__lookup_result(request):
    student_set = Student.objects.filter(name=request.POST['name'])
    return render(request, 'dorm/housemaster/lookup_result.html', {'student_set': student_set})

def housemaster__member(request, roomid):
    room = Room.objects.get(pk=roomid)
    student_set = Student.objects.filter(roomid=room)
    return render(request, 'dorm/housemaster/member.html', {'room': room, 'student_set': student_set})

def housemaster__unsubscribe(request):
    user = get_object_or_404(Owner, user=request.user)
    housemaster = get_object_or_404(Housemaster, user=user)
    building = housemaster.buildingid
    rec_set = set()
    for rec in QuitApply.objects.all():
        if rec.roomid.buildingid == building:
            rec.occupant = 0
            for student in Student.objects.filter(roomid=rec.roomid):
                rec.occupant += 1
            rec_set.add(rec)
    return render(request, 'dorm/housemaster/unsubscribe.html', {'rec_set': rec_set})

def housemaster__unsubscribe_result(request):
    for id in request.POST.getlist('checked'):
        rec = QuitApply.objects.get(pk=id)
        rec.housemaster_check = True
        rec.save()
        if rec.instructor_check and rec.secretary_check:
            live_record = LiveRecord.objects.filter(sno=rec.sno, roomid=rec.roomid).order_by('-enter_time')[0]
            live_record.quit_time = timezone.now()
            live_record.save()
            rec.delete()
    return redirect('dorm:housemaster__unsubscribe')

def housemaster__visitor(request):
    user = get_object_or_404(Owner, user=request.user)
    housemaster = get_object_or_404(Housemaster, user=user)
    building = housemaster.buildingid
    visitor_set = Visitor.objects.filter(housemasterid=housemaster)
    return render(request, 'dorm/housemaster/visitor.html', {'building': building, 'visitor_set': visitor_set})

def housemaster__mark(request):
    return render(request, 'dorm/housemaster/mark.html')

def housemaster__new_mark(request):
    user = get_object_or_404(Owner, user=request.user)
    housemaster = get_object_or_404(Housemaster, user=user)
    room = Room.objects.get(name=request.POST['room'], buildingid=housemaster.buildingid)
    mark = Mark(roomid=room, dt=timezone.now(), score=request.POST['score'], housemasterid=housemaster, remark=request.POST['remark'])
    mark.save()
    return redirect('dorm:housemaster__mark')

def instructor__building(request):
    return render(request, 'dorm/instructor/building.html')

def instructor__checkin(request):
    user = get_object_or_404(Owner, user=request.user)
    instructor = get_object_or_404(Instructor, user=user)
    rec_set = set()
    for rec in EnterApply.objects.all():
        if rec.sno.classid.instructorid == instructor:
            rec.occupant = 0
            for student in Student.objects.filter(roomid=rec.roomid):
                rec.occupant += 1
            rec_set.add(rec)
    return render(request, 'dorm/instructor/checkin.html', {'rec_set': rec_set})

def instructor__checkin_result(request):
    for id in request.POST.getlist('checked'):
        rec = EnterApply.objects.get(pk=id)
        rec.instructor_check = True
        rec.save()
        if rec.housemaster_check and rec.secretary_check:
            live_record = LiveRecord(sno=rec.sno, roomid=rec.roomid, enter_time=timezone.now(), quit_time=None)
            live_record.save()
            rec.delete()
    return redirect('dorm:instructor__checkin')

def instructor__class(request, classid):
    cls = Class.objects.get(pk=classid)
    student_set = Student.objects.filter(classid=cls)
    building_set = set()
    room_set = set()
    for student in student_set:
        room_set.add(student.roomid)
        building_set.add(student.roomid.buildingid)
    return render(request, 'dorm/instructor/class.html', {'cls': cls, 'student_set': student_set, 'student_amount': len(student_set), 'building_amount': len(building_set), 'room_amount': len(room_set)})

def instructor__index(request):
    user = get_object_or_404(Owner, user=request.user)
    instructor = get_object_or_404(Instructor, user=user)
    class_set = Class.objects.filter(instructorid=instructor)
    return render(request, 'dorm/instructor/index.html', {'instructor': instructor, 'class_set': class_set})

def instructor__lookup(request):
    return render(request, 'dorm/instructor/lookup.html')

def instructor__lookup_result(request):
    student_set = Student.objects.filter(name=request.POST['name'])
    return render(request, 'dorm/instructor/lookup_result.html', {'student_set': student_set})

def instructor__member(request, sno):
    student = Student.objects.get(pk=sno)
    student_set = Student.objects.filter(roomid=student.roomid)
    return render(request, 'dorm/instructor/member.html', {'room': student.roomid, 'student_set': student_set, 'classid': student.classid.id})

def instructor__student(request):
    return render(request, 'dorm/instructor/student.html')

def instructor__unsubscribe(request):
    user = get_object_or_404(Owner, user=request.user)
    instructor = get_object_or_404(Instructor, user=user)
    rec_set = set()
    for rec in QuitApply.objects.all():
        if rec.sno.classid.instructorid == instructor:
            rec.occupant = 0
            for student in Student.objects.filter(roomid=rec.roomid):
                rec.occupant += 1
            rec_set.add(rec)
    return render(request, 'dorm/instructor/unsubscribe.html', {'rec_set': rec_set})

def instructor__unsubscribe_result(request):
    for id in request.POST.getlist('checked'):
        rec = QuitApply.objects.get(pk=id)
        rec.instructor_check = True
        rec.save()
        if rec.housemaster_check and rec.secretary_check:
            live_record = LiveRecord.objects.filter(sno=rec.sno, roomid=rec.roomid).order_by('-enter_time')[0]
            live_record.quit_time = timezone.now()
            live_record.save()
            rec.delete()
    return redirect('dorm:instructor__unsubscribe')

def maintenance__index(request):
    fixed_list = []
    unfixed_list = []
    for repair in Repair.objects.all():
        if repair.fix_dt is None and repair.maintenanceid is None:
            unfixed_list.append(repair)
        else:
            fixed_list.append(repair)
    return render(request, 'dorm/maintenance/index.html', {'fixed_list': fixed_list, 'unfixed_list': unfixed_list})

def maintenance__repair(request, repairid):
    repair = Repair.objects.get(pk=repairid)
    return render(request, 'dorm/maintenance/repair.html', {'repair': repair})

def maintenance__repair_result(request, repairid):
    repair = Repair.objects.get(pk=repairid)
    repair.fix_dt = timezone.now()
    user = get_object_or_404(Owner, user=request.user)
    maintenance = get_object_or_404(Maintenance, user=user)
    repair.maintenanceid = maintenance
    repair.remark = request.POST['remark']
    repair.save()
    return redirect('dorm:maintenance__index')

def secretary__building(request):
    return render(request, 'dorm/secretary/building.html')

def secretary__checkin(request):
    user = get_object_or_404(Owner, user=request.user)
    secretary = get_object_or_404(Secretary, user=user)
    rec_set = set()
    for rec in EnterApply.objects.all():
        if rec.sno.classid.collegeid == secretary.collegeid:
            rec.occupant = 0
            for student in Student.objects.filter(roomid=rec.roomid):
                rec.occupant += 1
            rec_set.add(rec)
    return render(request, 'dorm/secretary/checkin.html', {'rec_set': rec_set})

def secretary__checkin_result(request):
    for id in request.POST.getlist('checked'):
        rec = EnterApply.objects.get(pk=id)
        rec.secretary_check = True
        rec.save()
        if rec.housemaster_check and rec.instructor_check:
            live_record = LiveRecord(sno=rec.sno, roomid=rec.roomid, enter_time=timezone.now(), quit_time=None)
            live_record.save()
            rec.delete()
    return redirect('dorm:secretary__checkin')

def secretary__class(request, classid):
    cls = Class.objects.get(pk=classid)
    student_set = Student.objects.filter(classid=cls)
    building_set = set()
    room_set = set()
    for student in student_set:
        room_set.add(student.roomid)
        building_set.add(student.roomid.buildingid)
    return render(request, 'dorm/secretary/class.html', {'cls': cls, 'student_set': student_set, 'student_amount': len(student_set), 'building_amount': len(building_set), 'room_amount': len(room_set)})

def secretary__index(request):
    user = get_object_or_404(Owner, user=request.user)
    secretary = get_object_or_404(Secretary, user=user)
    class_set = Class.objects.filter(collegeid=secretary.collegeid)
    student_amount = 0
    for cls in class_set:
        student_amount += len(Student.objects.filter(classid=cls))
    return render(request, 'dorm/secretary/index.html', {'secretary': secretary, 'class_set': class_set, 'class_amount': len(class_set), 'student_amount': student_amount})

def secretary__lookup(request):
    return render(request, 'dorm/secretary/lookup.html')

def secretary__lookup_result(request):
    student_set = Student.objects.filter(name=request.POST['name'])
    return render(request, 'dorm/secretary/lookup_result.html', {'student_set': student_set})

def secretary__member(request, sno):
    student = Student.objects.get(pk=sno)
    student_set = Student.objects.filter(roomid=student.roomid)
    return render(request, 'dorm/secretary/member.html', {'room': student.roomid, 'student_set': student_set, 'classid': student.classid.id})

def secretary__student(request):
    return render(request, 'dorm/secretary/student.html')

def secretary__unsubscribe(request):
    user = get_object_or_404(Owner, user=request.user)
    secretary = get_object_or_404(Secretary, user=user)
    rec_set = set()
    for rec in QuitApply.objects.all():
        if rec.sno.classid.collegeid == secretary.collegeid:
            rec.occupant = 0
            for student in Student.objects.filter(roomid=rec.roomid):
                rec.occupant += 1
            rec_set.add(rec)
    return render(request, 'dorm/secretary/unsubscribe.html', {'rec_set': rec_set})

def secretary__unsubscribe_result(request):
    for id in request.POST.getlist('checked'):
        rec = QuitApply.objects.get(pk=id)
        rec.secretary_check = True
        rec.save()
        if rec.housemaster_check and rec.instructor_check:
            live_record = LiveRecord.objects.filter(sno=rec.sno, roomid=rec.roomid).order_by('-enter_time')[0]
            live_record.quit_time = timezone.now()
            live_record.save()
            rec.delete()
    return redirect('dorm:secretary__unsubscribe')

def student__checkin(request, roomid):
    room = Room.objects.get(pk=roomid)
    user = get_object_or_404(Owner, user=request.user)
    student = get_object_or_404(Student, user=user)
    rec = EnterApply(sno=student, roomid=room, dt=timezone.now())
    rec.save()
    return redirect('dorm:student__index')

def student__building(request, buildingid):
    class RoomItem(object):
        pass
    building = Building.objects.get(pk=buildingid)
    housemaster_set = Housemaster.objects.filter(buildingid=building)
    room_set = Room.objects.filter(buildingid=building)
    empty = building.amount - len(room_set)
    full = 0
    room_tab = []
    for room in room_set:
        tmp = RoomItem()
        tmp.id = room.id
        tmp.name = room.name
        tmp.room_type = room.room_type
        tmp.capacity = room.capacity
        tmp.occupant = 0
        tmp.class_set = set()
        for student in Student.objects.filter(roomid=room):
            tmp.occupant += 1
            tmp.class_set.add(student.classid)
        if room.capacity == len(Student.objects.filter(roomid=room)):
            full += 1
            tmp.is_full = True
        room_tab.append(tmp)
    return render(request, 'dorm/student/building.html', {'building': building, 'housemaster_set': housemaster_set, 'empty': empty, 'full': full, 'not_full': building.amount-empty-full, 'room_tab': room_tab})

def student__building_select(request):
    building_set = Building.objects.all()
    return render(request, 'dorm/student/building_select.html', {'building_set': building_set})

def student__fee(request):
    user = get_object_or_404(Owner, user=request.user)
    student = get_object_or_404(Student, user=user)
    fee_record_set = FeeRecord.objects.filter(roomid=student.roomid).order_by('dt')
    return render(request, 'dorm/student/fee.html', {'student': student, 'fee_record_set': fee_record_set})

def student__index(request):
    user = get_object_or_404(Owner, user=request.user)
    student = get_object_or_404(Student, user=user)
    fee = Fee.objects.get(pk=student.roomid)
    mark = Mark.objects.filter(roomid=student.roomid).order_by('-dt')[0]
    secretary_set = Secretary.objects.filter(collegeid=student.classid.collegeid)
    housemaster_set = Housemaster.objects.filter(buildingid=student.roomid.buildingid)
    content = {'student': student,
               'fee': fee,
               'mark': mark,
               'secretary_set': secretary_set,
               'housemaster_set': housemaster_set}
    return render(request, 'dorm/student/index.html', content)

def student__mark(request):
    user = get_object_or_404(Owner, user=request.user)
    student = get_object_or_404(Student, user=user)
    mark_set = Mark.objects.filter(roomid=student.roomid).order_by('dt')
    return render(request, 'dorm/student/mark.html', {'student': student, 'mark_set': mark_set})

def student__repair(request):
    return render(request, 'dorm/student/repair.html')

def student__new_repair(request):
    user = get_object_or_404(Owner, user=request.user)
    student = get_object_or_404(Student, user=user)
    rep = Repair(item=request.POST['item'], roomid=student.roomid, book_dt=timezone.now(), reason=request.POST['reason'])
    rep.save()
    return redirect('dorm:student__repair_record')

def student__repair_record(request):
    user = get_object_or_404(Owner, user=request.user)
    student = get_object_or_404(Student, user=user)
    repair_set = Repair.objects.filter(roomid=student.roomid).order_by('book_dt')
    return render(request, 'dorm/student/repair_record.html', {'student': student, 'repair_set': repair_set})

def student__unsubscribe(request):
    return render(request, 'dorm/student/unsubscribe.html')

def student__unsubscribe_result(request):
    user = get_object_or_404(Owner, user=request.user)
    student = get_object_or_404(Student, user=user)
    rec = QuitApply(sno=student, roomid=student.roomid, dt=timezone.now(), reason=request.POST['reason'])
    rec.save()
    return redirect('dorm:student__index')
