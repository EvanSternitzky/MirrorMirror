
from googleapiclient.discovery import build
import google.oauth2.credentials
import requests
import json

class Google:
    refresh_url = "https://www.googleapis.com/oauth2/v4/token"
    def __init__(self, *args):
        if(args is not None):
            self.access_token = args[0]
            if args[1] != None:
                self.refresh_token = args[1]
            if self.client_id == None:
                with open('credentials.json') as f:
                    self.client_id = json.load(f)['clientid']
            self.configure(self.access_token)
            print('ARGS SUPPLIED: ', args)

    def configure(self, *args):
        print(self.access_token)
        self.credentials = google.oauth2.credentials.Credentials(self.access_token)
        #self.credentials = google.oauth2.credentials.Credentials.from_authorized_user_file('credentials.json', scopes=['https://www.googleapis.com/auth/plus.me', 'https://mail.google.com/', 'https://www.googleapis.com/auth/calendar.readonly'])
        #self.credentials.refresh_token = args[1]
        self.mail_service = build('gmail', 'v1', credentials=self.credentials)
        self.calendar_service = build('calendar', 'v3', credentials=self.credentials)
    def ListMessagesMatchingQuery(self, query=''):
        """List all Messages of the user's mailbox matching the query.

        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          query: String used to filter messages returned.
          Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
          List of Messages that match the criteria of the query. Note that the
          returned list contains Message IDs, you must use get with the
          appropriate ID to get the details of a Message.
        """

        user_id = "me"
        try:
            response = self.mail_service.users().messages().list(userId=user_id, q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.mail_service.users().messages().list(userId=user_id, q=query,
                                                                     pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages[:5]
        except:
            print("Error: List Messages")

    def GetMessage(self,  msg_id):
        """Get a Message with given ID.

        Args:
          msg_id: The ID of the Message required.

        Returns:
          A Message.
        """

        user_id = "me"

        try:
            message = self.mail_service.users().messages().get(userId=user_id, id=msg_id).execute()

            print
            'Message snippet: %s' % message['snippet']

            return message
        except:
            print("Error: Get Message")

    def ListCalendatItems(self):
        page_token = None
        while True:
            events = self.calendar_service.events().list(calendarId='primary', pageToken=page_token, maxResults=10).execute()
            return events

            page_token = events.get('nextPageToken')
            if not page_token:
                break
    def send_refresh(self):
        r = requests.post(self.refresh_url, data={'client_id': self.client_id, 'refresh_token': self.refresh_token, 'grant_type': 'refresh_token'})
        self.access_token = json.loads(r.text)['access_token']
        self.configure(self.access_token)

    def MessageList(self):
        MessageArray = []
        try:
            if self.credentials.expired():
                print("Refreshing access token.")
                self.send_refresh()
            response = self.ListMessagesMatchingQuery()
            print("RESPONSE FOR MESSAGES: ", response)
            for message in response:
                full_message = self.GetMessage(message['id'])
                headers = full_message['payload']['headers']
                for item in headers:
                    if (item['name'] == "From"):
                        NewDictionaryItem = {
                            'from': item['value'],
                            'summary' : full_message['snippet'][0:30]
                        }
                        MessageArray.append(NewDictionaryItem)

        except Exception as ex:
            print("Error: MessageList {0}".format(ex))

        return MessageArray

    def EventList(self):
        EventArray =[]
        try:
            if self.credentials.expired():
                print("Refreshing access token.")
                self.send_refresh()
            events = self.ListCalendatItems()

            for i in range(0,5):
                item = events['items'][i]
                NewDictionaryItem = {
                    'summary': item.get('summary', 'No Description'),
                    'location': item.get('location', 'No Location'),
                    'time': item.get('start', 'No Time')
                }
                EventArray.append(NewDictionaryItem)
        except Exception as ex:
            print("Error: EventList {0}".format(ex))
        return EventArray

        
# Sample usage
#thisaccess_token = "ya29.GltrBt6Z38EXSpkETvrn3GYZYbXbvJC6f9cJqJM54A__57zB1mI1I2cLvwockccCRnvyCCnq9X3grxJWCMu-BV4ObYdvJKPaEjVGszy_QtYSDOIc-YDHPoDXl1f_"
#goog = Google()

#print("check")

#goog.configure(thisaccess_token)

#print(goog.MessageList())
#print(goog.EventList())




