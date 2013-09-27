from django.conf.urls.defaults import *

urlpatterns = patterns('graphite.device.views',
  ('^find/', 'find'),
  ('', 'find'),
)
