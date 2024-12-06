# from django.urls import path
# from . import views

# urlpatterns = [
#     path('upload/', views.upload_inventory, name='upload_inventory'),
# ]



from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_inventory, name='upload_inventory'),
    path('edit/<str:site_name>/', views.edit_inventory, name='edit_inventory'),
    path('inventory_history/<str:site_name>/', views.inventory_history, name='inventory_history'),
    path('notifications/', views.view_notifications, name='view_notifications'),
    path('notification_list/',views.notification_list, name='notification_list'),

    path('', views.redirect_to_home),  # Redirect root URL to /home/
    path('home/', views.home_page, name='home'),
    path('superuser/signup/', views.signup_view, name='signup'),
    path('user/login/', views.login_view, name='login'),  
    path('superuser/login/',views.login1_view,name="login1"),
    path('superuser/services/', views.admin_page, name='admin'),
    path('user/services/', views.user_page, name='user'),
]
