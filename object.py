import requests
from requests import get
import json
#
class Zoom(object):

    #URL with users
    url_name = 'https://api.zoom.us/v2/users/'

    #List Zoom users
    ZoomUsers = []

    #Init
    def __init__(self, key = 'None'):
        self.key = {'authorization': 'Bearer ' + key}
        self.ZoomGET = requests.get(self.url_name, headers=self.key)

    #Get status
    def GetState(self):
        if int(self.ZoomGET.status_code) == 200:
            return True
        else:
            return [self.ZoomGET.status_code, self.ZoomGET.json()['message']]

    #Init zoom users
    def InitUsers(self):
        for user in self.ZoomGET.json()['users']:
            self.ZoomUsers.append(
                ZoomUser(user['id'],
                          str(user['first_name']) + ' ' + str(user['last_name']),
                          user['status'], user['timezone'], self.key
                )
            )

class ZoomUser(Zoom):
    #
    def __init__(self, id,  name, status, timezone, key):
        self.id = id
        self.name = name
        self.status = status
        self.timezone = timezone
        self.url_name = self.url_name + id + '/' + 'meetings'
        self.key = key

    #
    def GetAllConference(self, type='upcoming'):
        self.ZoomGET = requests.get(self.url_name, headers=self.key, params={'type': type})
        if str(self.ZoomGET.json()['meetings']) == '[]':
            return 'None'
        else:
            return self.ZoomGET.json()['meetings']

    #Метод создания новой конференции(Create conference function)
    def SetConference(self, topic, type, start_time, duration, timezone = ''):
        if timezone == '':
            timezone = self.timezone

        meetingdetails = {"topic": "The title of your zoom meeting",
                          "type": 2,
                          "start_time": "2022-02-14T10:21:57",
                          "duration": "45",
                          #'schedule_for': self.id,
                          "timezone": "Europe/Madrid",
                          'default_password': 'true',

                          "settings": {"host_video": "true",
                                       "participant_video": "true",
                                       "join_before_host": "False",
                                       "mute_upon_entry": "False",
                                       "auto_recording": "local"
                                       }
                          }

        sett = {
            'host_video': False,
            'participant_video': True,
            'join_before_host': True,
            'jbh_time': 0,
            'auto_recording': 'local',
            'waiting_room': False,
            'registrants_confirmation_email': False,
            'authentication_option': False
        }

        return requests.post(self.url_name, headers=self.key,

                params={ 'userId': self.id },

                data=json.dumps(meetingdetails)

                #{
                #    'topic': str(topic),
                #   'type': int(type),
                #    'start_time': str(start_time),
                #    'duration': int(duration),
                    #'schedule_for': self.id,
                #    'timezone': str(timezone),
                #    'default_password': 'true',
                    #'settings': sett

                #}

            )


q.InitUsers()
print(q.ZoomUsers[3].name)
print(q.ZoomUsers[3].GetAllConference())
kek = q.ZoomUsers[3].SetConference('test', 2, '2020-02-11T16:00:00', 120)
print(kek.status_code, kek.content)
#print(q.GetState()[0], q.GetState()[1])

