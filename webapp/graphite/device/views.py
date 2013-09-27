from os import listdir, path
from django.shortcuts import render_to_response
from django.http import HttpResponse, QueryDict
from django.conf import settings
from graphite.util import json

def find(request):
  query = request.REQUEST.get('query','').lower()
  results = []
  flist = []

  for dir in settings.METRICS_DIRS:
    if path.isdir(dir):
      flist += sorted(listdir(dir))

  if len(query) < 1:
    for dir in flist:
      results.append(dict(name=dir))
  else:
    for dir in flist:
      if query in dir:
        results.append(dict(name=dir))

  return json_response(dict(devices=results))

def json_response(obj):
  return HttpResponse(mimetype='application/json', content=json.dumps(obj))
