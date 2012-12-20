from twisted.web import server
from twisted.web import resource
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
import os
import json
import requests

server_ip = '192.168.0.100'
server_url = 'http://%s/api/YourAppName/lights/' % server_ip

#def authenticate():
#  a = requests.get(server_url+'3')
#  print json.loads(a.text)
#  return requests.post(server_url, {})

class HueServer(resource.Resource):
  isLeaf = True

  def render_GET(self, request):
    print 'GET state of light',
    light_number = request.uri.split('/')[-1]
    print light_number
    status = requests.get(server_url+light_number)
    res = json.loads(status.text)
    if isinstance(res,list):
      if 'error' in res[0]:
        print 'ERROR connecting to light',light_number
        return '-1,-1,-1'
    else:
      state = res['state']
      h,s,b = state['hue'],state['sat'],state['bri']
      return ','.join(map(str,[h,s,b]))

  def render_POST(self, request):
    print request.args
    print request.uri
    print request.content.read()
    return "POST:"


site = server.Site(HueServer())
reactor.listenTCP(8080, site)
reactor.run()
