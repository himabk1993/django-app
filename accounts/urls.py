from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name = 'signup'),
    path('index/', views.index, name = 'index'),
    path('quest/', views.quest, name = 'quest'),
    path('questAdd/', views.questAdd, name = 'questAdd'),
    path('<int:question_id>/', views.detail, name = 'detail'),
    path('<int:question_id>/results/', views.results, name = 'results'),
    path('<int:question_id>/vote/', views.vote, name = 'vote'),  
]