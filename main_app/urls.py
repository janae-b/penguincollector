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
  path('penguins/<int:penguin_id>/add_feeding/', views.add_feeding, name='add_feeding'),
  path('penguins/<int:penguin_id>/add_photo/', views.add_photo, name='add_photo'),
  path('penguins/<int:penguin_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
  path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
  path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
  path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
  path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
  path('toys/', views.ToyList.as_view(), name='toys_index'),
]