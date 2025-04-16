from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Student Cohorts
    path('cohorts/', views.cohorts_view, name='cohorts'),
    path('download_students/<int:year>/', views.download_students_by_year, name='download_students_by_year'),

    # Other sections
    path('tithe-offerings/', views.tithe_offerings_view, name='tithe_offerings'),
    path('events-programs/', views.events_programs_view, name='events_programs'),
    path('promotions/', views.promotions_view, name='promotions'),
    path('settings/', views.settings_view, name='settings'),

    # Catch-all for other templates (keep last)
    path('<path:template>', views.pages, name='pages'),
]
