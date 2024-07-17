from django.urls import path, include

from main import views
from main.views import Register

# from django.contrib.auth.urls

urlpatterns = [
   path('', include('django.contrib.auth.urls')),
   path('profile/auth', views.login_view, name='auth'),
   path('register/', Register.as_view(), name='register'),
   path('profile/', views.get_profile_page, name='profile'),
   path('profile/settings', views.get_profile_settings_page, name='settings'),
   path('profile/res_tests', views.get_tests_page, name='tests'),
   path('profile/child/', views.get_childs_page, name='childs'),
   path('profile/child/medical_card/<str:child_code>', views.get_child_vew_page, name='child_view'),
   path('profile/test1/<str:child_code>', views.get_test1_page, name='test1'),
   path('profile/test2/<str:child_code>', views.get_test2_page, name='test2'),
   path('profile/test3/<str:child_code>', views.get_test3_page, name='test3'),
   path('profile/test_1_creation', views.test_1_creation, name='test_1_creation'),
   path('profile/test_2_creation', views.test_2_creation, name='test_2_creation'),
   path('profile/test_3_creation', views.test_3_creation, name='test_3_creation'),
   path('user/<int:user_id>/child/add/', views.save_child, name='save_child'),


]