from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('penguins/', views.penguins_index, name='index'),
  path('penguins/<int:penguin_id>/', views.penguins_detail, name='detail'),
  path('penguins/create/', views.PenguinCreate.as_view(), name='penguins_create'),
  path('penguins/<int:pk>/update/', views.PenguinUpdate.as_view(), name='penguins_update'),
  path('penguins/<int:pk>/delete/', views.PenguinDelete.as_view(), name='penguins_delete'),
]