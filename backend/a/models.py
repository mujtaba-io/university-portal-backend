# your_app/models.py
from django.utils import timezone # use django's timezone instead of python's datetime
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password


# User - auth system

class User(AbstractUser):

    # Default fields of AbstractUser:
    # username, first_name, last_name, email, password
    # is_staff, is_active, date_joined

    phone = models.CharField(max_length=32, default='+92 000 000-0000')

    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False) DEFINED IN BASE CLASS, FOR ADMIN
    # is_staff = models.BooleanField(default=False) DEFINED IN BASE CLASS, FOR STAFF (read: admin)

    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Hash the password before saving
    def save(self, *args, **kwargs):
        # Hash the password if it's not hashed already
        if self.pk is None or not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        
        potential_student = Student.objects.filter(user=self)
        if potential_student.exists():
            self.is_student = True
        
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    father_name = models.CharField(max_length=128, default='Father Name')
    father_occupation = models.CharField(max_length=128 , default='Father Occupation')
    guardian_name = models.CharField(max_length=128, default='Guardian Name')
    guardian_occupation = models.CharField(max_length=128, default='Guardian Occupation')
    date_of_birth = models.DateField(default=timezone.now)
    nic = models.CharField(max_length=16, default='00000-0000000-0')
    blood_group = models.CharField(max_length=4 , default='A+')

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
    
    # Get semester name such as 'SP22', 'FA21', etc. from the admission time
    def get_semester_name(self):
        if self.admission_time.month in [1, 2, 3, 4, 5, 6]:
            return f"SP{str(self.admission_time.year)[2:]}"
        elif self.admission_time.month in [7, 8, 9, 10, 11, 12]:
            return f"FA{str(self.admission_time.year)[2:]}"
        else:
            return "Unknown"
    
    # When saving a student, make sure its username is: semester name + program + roll number
    def save(self, *args, **kwargs):
        self.user.username = self.get_semester_name() +'-'+ self.program +'-'+ self.roll_number
        self.user.save()
        super().save(*args, **kwargs)





# Time table


class Course(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=16)
    credit_hours = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name




class Block(models.Model):
    name = models.CharField(max_length=16)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name



class Room(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
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
    is_makeup_approved = models.BooleanField(default=False) # If makeup, is it approved by the admin?
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
    def is_reserved(self, given_time_slot):
        # Delete the reservations which are older than 1 day
        self.pc_reservations.filter(created_at__lt=timezone.now()-timedelta(days=1)).delete()
        # Check if the PC is reserved at the given time
        return self.pc_reservations.filter(slot=given_time_slot).exists()


class PCReservation(models.Model):
    pc = models.ForeignKey(PC, related_name='pc_reservations', on_delete=models.CASCADE)
    reserved_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    
    SLOT_CHOICES = [
        ('08:30-10:00', '08:30 to 10:00'),
        ('10:00-11:30', '10:00 to 11:30'),
        ('11:30-01:00', '11:30 to 01:00'),
        ('01:00-02:30', '01:00 to 02:30'),
        ('02:30-04:00', '02:30 to 04:00'),
        ('04:00-05:30', '04:00 to 05:30')
    ]

    slot = models.CharField(
        max_length=11,  # Adjust length based on the longest value
        choices=SLOT_CHOICES,
        default='08:00-10:00',  # Optional: set a default value
    )

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pc} - {self.slot}"









# Academic calendar

class AdacemicCalendarEvent(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        semester_name = "No Semester"
        semester = AcademicCalendar.objects.all()
        for sem in semester:
            if self in sem.events.all():
                semester_name = sem.semester_name
                break
        return semester_name + ' - ' + self.title + ' - ' + str(self.start_date)


class AcademicCalendar(models.Model):
    semester_name = models.CharField(max_length=128, default="SP22") # FA32, SP22, FA21, etc.
    events = models.ManyToManyField(AdacemicCalendarEvent, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.semester_name)













# News

class News(models.Model):
    title = models.CharField(max_length=256, default='News Title')
    content = models.TextField(default="News content")
    youtube_link = models.URLField(default='https://www.youtube.com')
    image_url = models.URLField(default='https://www.nist.gov/sites/default/files/styles/2800_x_2800_limit/public/images/2018/07/10/mass_spec_cd_scan.jpg')
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
    image_url = models.CharField(max_length=256, default='https://www.nist.gov/sites/default/files/styles/2800_x_2800_limit/public/images/2018/07/10/mass_spec_cd_scan.jpg')
    description = models.TextField(default="Event description")
    link = models.URLField(default='https://www.example.com')

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    venue = models.CharField(max_length=256, default='Venue')

    registration = models.URLField(default='https://www.example.com')
    participation_registration = models.URLField(default='https://www.example.com')
    linkedin = models.URLField(default='https://www.linkedin.com')

    created_at = models.DateField(auto_now_add=True)

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
    
