import requests
from requests import get
from threading import Thread
#


class Zoom(object):

    #URL with users
    url_name = 'https://api.zoom.us/v2/users/'

    #List Zoom users
    ZoomUsers = []

    #Init
    def __init__(self, key = 'None'):
        self.key = {'authorization': 'Bearer ' + key}
        self.ZoomGET = requests.get(self.url_name, headers = self.key)

    #Get status
    def GetState(self):
        if int(self.ZoomGET.status_code) == 200:
            return 'True'
        else:
            return [self.ZoomGET.status_code, self.ZoomGET.json()['message']]

    #Init zoom users
    def InitUsers(self):
        for user in self.ZoomGET.json()['users']:
            self.ZoomUsers.append(
                ZoomUser(user['id'],
                          str(user['first_name']) + ' ' + str(user['last_name']),
                          user['status'], user['timezone'], user['email'], self.key
                )
            )

class ZoomUser(Zoom):
    #
    def __init__(self, id,  name, status, timezone, email, key):
        self.id = id
        self.name = name
        self.status = status
        self.timezone = timezone
        self.email = email
        self.url_name = self.url_name + id + '/' + 'meetings'
        self.key = key

        self.getResult = None

    #
    def GetAllConference(self, type='upcoming'):
        self.ZoomGET = requests.get(self.url_name, headers=self.key, params={'type': type})
        if str(self.ZoomGET.json()['meetings']) == '[]':
            self.getResult = 'None'
        else:
            self.getResult = self.ZoomGET.json()['meetings']

    #Метод создания новой конференции(Create conference function)
    def SetConference(self, topic, type, start_time, duration, participant_video,  auto_recording = 'none', timezone = ''):

        if timezone == '':
            timezone = str(self.timezone)

        return requests.post(self.url_name, headers=self.key,

                params={ 'userId': str(self.id) },

                json={
                    'topic': str(topic),
                    'type': type,
                    'start_time': str(start_time),
                    'duration': int(duration),
                    'timezone': str(timezone),
                    'settings': {

                        'host_video': False,
                        'participant_video': participant_video,
                        'join_before_host': True,
                        'auto_recording': str(auto_recording)

                    }
                }

            )


#q.InitUsers()
#print(q.ZoomUsers[3].name)
#print(q.ZoomUsers[3].GetAllConference())
#kek = q.ZoomUsers[3].SetConference('test', 2, '2022-02-14T16:00:00', 120, True, 'cloud')
#print(kek.status_code, kek.json())
#print(q.GetState())
#print(q.ZoomUsers[3].id, q.ZoomUsers[3].timezone)
#print(q.GetState()[0], q.GetState()[1])

