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

  def parse_response(self, response):
    if isinstance(response,list):
      if 'error' in response[0]:
        print 'ERROR connecting to light',light_number
        print response[0]
        return '-1,-1,-1'
    else:
      state = response['state']
      h,s,b = state['hue'],state['sat'],state['bri']
      return ','.join(map(str,[h,s,b]))

  def render_GET(self, request):
    light_number = request.uri.split('/')[-1]
    print 'GET state of light',
    print light_number
    status = requests.get(server_url+light_number)
    res = json.loads(status.text)
    return self.parse_response(res)

  def render_PUT(self, request):
    light_number = request.uri.split('/')[-1]
    data = request.content.read()
    print 'PUT change light',light_number,
    print 'data:',data
    status = requests.put(server_url+light_number+'/state', data)
    res = json.loads(status.text)
    return self.parse_response(res)

site = server.Site(HueServer())
reactor.listenTCP(8080, site)
reactor.run()
