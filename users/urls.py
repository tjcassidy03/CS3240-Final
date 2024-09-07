from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("", views.home, name='home'),
    path("logout", views.logout_view),
    path("report/file", views.file_report, name='file_report'),
    path("report/<int:reportID>/submitted", views.report_submitted, name='report_submitted'),
    path("admin_reports", views.admin_reports, name='admin_reports'),
    path("user_reports", views.user_reports, name='user_reports'),
    path("user_reports/<int:report_id>/retract/", views.retract_report, name='retract_report'),
    path('report/<int:reportID>/comment', views.admin_reports, name='admin_comment'),

]
