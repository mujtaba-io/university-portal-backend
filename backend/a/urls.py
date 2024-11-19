
from django.urls import include, path
from . import views
from .more_views import students, academics, rooms



urlpatterns = [
    path('signup/', views.signup), # Base User signup
    path('login/', views.login), # Base User login

    # path('student/create/', students.student_create), # Signup + Student create
    # path('student/login/', students.student_login), # Login + Student get
    # path('student/update/', students.student_update),
    # path('student/delete/', students.student_delete),
    path('student/get/', students.student_get),
    path('student/timetable/', students.student_time_table),
    path('student/makeuplectures/', students.student_makeup_lectures),
    
    path('student/attendance/', students.student_attendance),

    path('calendar/', academics.get_academic_calendar), # Academic calendar
    path('calendar/create/', academics.create_academic_calendar), # Create an event in the calendar

    path('news/', academics.get_news), # Get news
    path('news/create/', academics.create_news), # Create news
    
    path('events/', academics.get_events), # Get events
    path('extracurricularactivities/', academics.get_extra_curricular_activities), # Get extra curricular activities

    path('pcs/get/', rooms.get_pcs), # Get PCs
    path('pcs/book/', rooms.book_pc), # Book a PC
]
