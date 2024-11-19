# your_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password


# User - auth system

class User(AbstractUser):

    # Default fields of AbstractUser:
    # username, first_name, last_name, email, password
    # is_staff, is_active, date_joined

    phone = models.CharField(max_length=32, default='+92 000 000-0000')

    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Hash the password before saving
    def save(self, *args, **kwargs):
        # Hash the password if it's not hashed already
        if self.pk is None or not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    admission_time = models.DateField() # Exact time of admission
    roll_number = models.CharField(max_length=10) # 001
    program = models.CharField(max_length=100) # BS, MS, PhD, MA, etc.

    cgpa = models.FloatField() # 0.0 - 4.0

    is_graduated = models.BooleanField(default=False)
    is_dropout = models.BooleanField(default=False)

    lectures = models.ManyToManyField('Lecture', blank=True) # Courses enrolled
    _class = models.ForeignKey('Class', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username





# Time table


class Course(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=16)
    credit_hours = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=16)
    is_lab = models.BooleanField(default=False) # Is this room a lab?
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# This is for timetable of a class. For held lectures, see HeldLecture model
class Lecture(models.Model):
    _class = models.ForeignKey('Class', on_delete=models.CASCADE, blank=True, null=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    day = models.CharField(max_length=16) # Monday, Tuesday, Wednesday, Thursday, Friday
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    start_time = models.TimeField()
    end_time = models.TimeField()

    is_makeup = models.BooleanField(default=False) # If makeup, ignore it in timetable & anywhere after end_time
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.course} - {self.teacher}"
    
    # When a lecture is created, add it to the timetable of the class and to the
    # lectures of the student who belongs to that class
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._class and self._class.time_table:
            self._class.time_table.lectures.add(self)
        for student in self._class.student_set.all():
            student.lectures.add(self)



class TimeTable(models.Model):
    lectures = models.ManyToManyField(Lecture)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"




# Such as BSE-4A, BSE-4B, BSE-4C...
class Class(models.Model):
    name = models.CharField(max_length=16)
    time_table = models.OneToOneField(TimeTable, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name










# PCs in Rooms which are labs
class PC(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - {self.pk}"

    # Check if the PC is reserved at a given time
    # @param current_time: Time to check if the PC is reserved (python datetime.time)
    def is_reserved(self, given_time):
        for reservation in self.pc_reservations.all():
            if reservation.start_time <= given_time <= reservation.end_time:
                return True
        return False


class PCReservation(models.Model):
    pc = models.ForeignKey(PC, related_name='pc_reservations', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.pc} reserved from {self.start_time} to {self.end_time}"









# Academic calendar

class AdacemicCalendarEvent(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class AcademicCalendar(models.Model):
    semester_name = models.CharField(max_length=128, default="SP22") # FA32, SP22, FA21, etc.
    events = models.ManyToManyField(AdacemicCalendarEvent)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"













# News

class News(models.Model):
    title = models.CharField(max_length=256, default='News Title')
    content = models.TextField(default="News content")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title









# Events of university
"""
day and date
time
venue
registration
participation registration
linkedin
"""
class Event(models.Model):
    title = models.CharField(max_length=256, default='Event Title')
    image = models.ImageField(upload_to='uploads/events/', default='uploads/events/default.jpg')
    description = models.TextField(default="Event description")
    link = models.URLField(default='https://www.example.com')

    created_at = models.DateField(auto_now_add=True)
    day = models.CharField(max_length=16, default='Monday')
    
    time = models.TimeField(auto_now_add=True)
    venue = models.CharField(max_length=256, default='Venue')

    registration = models.URLField(default='https://www.example.com')
    participation_registration = models.URLField(default='https://www.example.com')
    linkedin = models.URLField(default='https://www.linkedin.com')

    def __str__(self):
        return self.title




# Extra curricular activities (same as event , but clients pushed me to make it separate)
class ExtraCurricularActivity(models.Model):
    title = models.CharField(max_length=256, default='ExtraCurricularActivities Title')
    image = models.ImageField(upload_to='uploads/activities/', default='uploads/activities/default.jpg')
    description = models.TextField(default="description")
    link = models.URLField(default='https://www.example.com')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title









# HeldLecture - for attendance. Teacher creates it after each lecture
class HeldLecture(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.lecture} - {self.created_at}"