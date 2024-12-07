
from django.urls import include, path
from . import views
from .more_views import students, academics, rooms, adminrequests, faculty, edit_endpoints, delete_endpoints
from . import firebase


urlpatterns = [
    path('signup/', views.signup), # Base User signup
    path('login/', views.login), # Base User login
    path('login/student/', views.login_student), # Student login
    path('login/faculty/', views.login_faculty), # Faculty login
    path('login/admin/', views.login_admin), # Admin login

    path('user/get/', views.get_user), # Get user details

    # path('student/create/', students.student_create), # Signup + Student create
    # path('student/login/', students.student_login), # Login + Student get
    # path('student/update/', students.student_update),
    # path('student/delete/', students.student_delete),
    path('student/get/', students.student_get),
    path('student/timetable/', students.student_time_table),
    path('student/makeuplectures/', students.student_makeup_lectures),
    
    path('student/attendance/', students.student_attendance),

    path('calendar/', academics.get_academic_calendar), # Academic calendar
    path('calendar/addevent/', academics.add_academic_calendar_event), # Create an event in the calendar
    path('calendar/edit/', edit_endpoints.edit_academic_calendar_event), # Delete an event in the calendar
    path('calendar/delete/', delete_endpoints.delete_academic_calendar_event), # Delete an event in the calendar

    path('news/', academics.get_news), # Get news
    path('news/create/', academics.create_news), # Create news
    path('news/edit/', edit_endpoints.edit_news), # Edit news
    path('news/delete/', delete_endpoints.delete_news), # Delete news
    
    path('events/', academics.get_events), # Get events
    path('events/create/', academics.create_event), # Create event
    path('events/edit/', edit_endpoints.edit_event),
    path('events/delete/', delete_endpoints.delete_event),


    path('extracurricularactivities/', academics.get_extra_curricular_activities), # Get extra curricular activities


    path('pcs/get/', rooms.get_pcs), # Get PCs
    path('pcs/book/', rooms.book_pc), # Book a PC

    # Admin requests
    path('pcs/pcrequests/', adminrequests.get_pc_requests), # Get PC reservation requests
    path('pcs/accept/', adminrequests.accept_pc_request), # Accept PC reservation request
    path('pcs/reject/', adminrequests.reject_pc_request), # Reject PC reservation request

    # makeup lectures reject/accept
    path('makeuplectures/requests/', adminrequests.get_makeup_lecture_requests), # Get makeup lectures
    path('makeuplectures/accept/', adminrequests.accept_makeup_lecture_request), # Accept makeup lecture
    path('makeuplectures/reject/', adminrequests.reject_makeup_lecture_request), # Reject makeup lecture


    # Faculty endpoints
    path('faculty/profile/get/', faculty.get_faculty_profile), # Get faculty profile
    path('faculty/requestmakeuplecture/', faculty.request_makeup_lecture), # Request a makeup lecture
    path('faculty/alllectures/', faculty.faculty_time_table), # Get faculty timetable
    path('faculty/studentsinlecture/', faculty.get_students_in_lecture), # Get students in a lecture
    path('faculty/markattendance/', faculty.mark_attendance), # Mark attendance of students in a lecture



# Register fcm token for unique devices
    path('registerfcmtoken/', firebase.register_fcm_token),

]
