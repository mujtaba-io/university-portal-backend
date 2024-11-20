from django.contrib import admin
from .models import *


# Cusomize the admin panel
admin.site.site_header = "Portal Admin"
admin.site.site_title = "Portal Admin Area"
admin.site.index_title = "Welcome to Portal Admin Area"

# Register your models here.
admin.site.register(User)
admin.site.register(Student)

admin.site.register(Lecture)
admin.site.register(Course)

admin.site.register(Block)
admin.site.register(Room)

admin.site.register(TimeTable)
admin.site.register(Class)


admin.site.register(AcademicCalendar)
admin.site.register(AdacemicCalendarEvent)


admin.site.register(News)
admin.site.register(Event)
admin.site.register(ExtraCurricularActivity)


admin.site.register(HeldLecture)


admin.site.register(PC)
admin.site.register(PCReservation)



