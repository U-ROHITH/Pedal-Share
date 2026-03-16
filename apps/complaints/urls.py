from django.urls import path
from apps.complaints import views

app_name = 'complaints'

urlpatterns = [
    path('raise/', views.raise_complaint, name='raise'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('detail/<int:complaint_id>/', views.complaint_detail, name='detail'),
]
