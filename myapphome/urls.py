from django.contrib import admin
from django.urls import path,include
from myapphome import views
from .views import chat_with_gemini, chatbot_interaction
from django.contrib.auth import views as auth_views
# from .views import company_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index,name='home'),
    path("searchcompanies",views.my_view, name='searchcompanies'),
    path("sendemail",views.sendemail, name='sendemail'),
    path("contact",views.contact, name='contact'),
    path("mockinterview",views.yourimprovement, name='yourimprovement'),
    path('company_list/<str:search_uqid>/', views.company_list, name='company_list'),
    path('export_to_excel/<str:search_uqid>/', views.export_to_excel, name='export_to_excel'),
    path('chatbot/', chat_with_gemini, name='chatbot'),
    path('chatbot/interact/', chatbot_interaction, name='chatbot_interaction'),
    path('show-data/', views.show_data, name='show_data'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('feedback/success/', views.feedback_success, name='feedback_success'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.account_section, name='account_section'),
    path('logout/', views.logout_view, name='logout'),
    path('upload-avatar/', views.upload_avatar, name='upload_avatar'),
    # path('accounts/upload-avatar/', views.profile_view, name='upload_avatar'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)