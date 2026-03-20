from django.urls import path
from apps.cycles import views

app_name = 'cycles'

urlpatterns = [
    path('', views.available_cycles, name='available'),
    path('detail/<int:cycle_id>/', views.cycle_detail, name='detail'),
    path('add/', views.add_cycle, name='add'),
    path('edit/<int:cycle_id>/', views.edit_cycle, name='edit'),
    path('delete/<int:cycle_id>/', views.delete_cycle, name='delete'),
    path('my-cycles/', views.my_cycles, name='my_cycles'),
    path('toggle-availability/<int:cycle_id>/', views.toggle_cycle_availability, name='toggle_availability'),
]
