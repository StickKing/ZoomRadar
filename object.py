import requests
from requests import get

#
class Zoom:
    #URL with users
    url_name = 'https://api.zoom.us/v2/users/'
    #List Zoom users
    ZoomUsers = []
    #
    Zoom = ''
    #Init
    def __init__(self, key):
        self.key = {'authorization': 'Bearer ' + key}
        self.Zoom = requests.get( self.url_name, headers = self.key )
    #
    def GetState(self):
        if int( self.Zoom.status_code ) == 401:
            print('Fasle')
        else: print('True')

    def InitUsers(self):
        for user in self.Zoom.json()['users']:
            self.ZoomUsers.append(
                ZoomUser( user['id'],
                          str(user['first_name']) + ' ' + str(user['last_name']),
                          user['status'], user['timezone'], self.key
                )
            )

class ZoomUser:
    #Конференции пользователя (User Conference)
    Conference = []
    #Инициализация класса (Create class)
    def __init__(self, id,  name, status, timezone, url, key):
        self.idd = id
        self.name = name
        self.status = status
        self.timezone = timezone
        self.meetingsURL = url + id + '/' + 'meetings'
        self.key = key

    def InitUpcomingConference(self):
        return[ requests.get( self.meetingsURL, headers = key, params = {'type': 'upcoming'} ) ]

    def InitScheduledConference(self):
        return[ requests.get( self.meetingsURL, headers = key, params = {'type': 'scheduled'} ) ]

    #Метод создания новой конференции(Create conference function)
    def CreateConference(self, topic, type, pre_shedule, dateTime, duration, videoOrganizator, videoParticipant, allTimeConnect, offSound, record ):
        return[

            requests.post( self.meetingsURL, headers = key,

                params = {

                    'topic': str(topic),
                    'type': int(type),
                    'pre_shedule': pre_shedule,
                    'start_time' : str(dateTime),
                    'duration': int(duration):
                    'schedule_for':
                    'timezone': str(),
                    'password':
                    'default_password':

                }

            )

        ]



