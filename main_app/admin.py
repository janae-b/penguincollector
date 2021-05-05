from django.contrib import admin

from .models import Penguin, Feeding, Toy, Photo

# Register your models here.
admin.site.register(Penguin)
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)