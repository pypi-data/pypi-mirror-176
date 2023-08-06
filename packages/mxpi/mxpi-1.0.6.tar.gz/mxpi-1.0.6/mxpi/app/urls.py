from django.urls import path
from . import views

app_name='app'

urlpatterns = [

path('',views.home,name='home'),
path('upfile_Ajax',views.upfile,name='upfile'),
path('runcmd_Ajax',views.run_cmd,name='run_cmd'),
path('cmd_msg',views.cmd_msg,name='cmd_msg'),
path('file_list',views.file_list,name='file_list'),
path('file_remove',views.file_remove,name='file_remove'),
path('files',views.files,name='files'),
path('get_c',views.get_c,name='get_c'),
path('read_model_list',views.read_model_list,name='read_model_list'),
path('get_upmodel',views.get_upmodel,name='get_upmodel'),
path('downModel',views.downModel,name='downModel'),
]
