from django.contrib import admin
  
# import the model Todo
from .models import Usuario
  
# create a class for the admin-model integration
class UsuarioAdmin(admin.ModelAdmin):
  
    # add the fields of the model here
    list_display = ("usu_rut","usu_password","usu_nombre","usu_rol")
  
# we will need to register the
# model class and the Admin model class
# using the register() method
# of admin.site class
admin.site.register(Usuario,UsuarioAdmin)