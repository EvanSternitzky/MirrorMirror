
from googleapiclient.discovery import build
import google.oauth2.credentials

class Google:
    def __init__(self, *access_token, ref_token, scope):
        if(access_token is not None):
            self.configure(access_token, ref_token, scope)

    def configure(self, access_token, ref_token, scope):
        self.access_token = access_token[0]
        print(self.access_token)
        self.credentials = google.oauth2.credentials.Credentials(self.access_token, refresh_token=ref_token, scopes=scope.split(" "))
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

    def MessageList(self):
        MessageArray = []
        try:
            response = self.ListMessagesMatchingQuery()
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




