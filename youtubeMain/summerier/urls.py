
from django.urls import path
from .views import adminView,ExportAsPdf,SummeryView,summary,summary_delete,register,homeView,login_view,logout_view,dashboard_view
urlpatterns = [
    path('summary/', SummeryView.as_view(),name='summizeapi'),
    path('sum/', summary,name='summizeui'),
    path('reg/',register,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('dash/',dashboard_view,name='dashboard'),
    path('del/<int:summary_id>/',summary_delete.as_view(),name='delete'),
    path('',homeView,name='home'),
    path('export/<int:pk>/',ExportAsPdf,name='pdf'),
    path('admin/',adminView,name='admin'),

]
