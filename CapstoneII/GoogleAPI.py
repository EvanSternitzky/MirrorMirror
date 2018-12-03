
from googleapiclient.discovery import build
import google.oauth2.credentials


class Google:
    def __init__(self, access_token):

        self.access_token = access_token
        self.credentials = google.oauth2.credentials.Credentials(access_token)
        self.mail_service = build('gmail', 'v1', credentials=self.credentials)
        self.calendar_service = build('calendar', 'v3', credentials=self.credentials)

        try:
            response = self.authed_session.get("https://www.googleapis.com/gmail/v1/users/me/profile").json()
            self.email = response["emailAddress"]
            print(self.email)

        except:
            print("Error: Invalid Access Token")

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

            return messages
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
            events = self.calendar_service.events().list(calendarId='primary', pageToken=page_token).execute()
            return events

            page_token = events.get('nextPageToken')
            if not page_token:
                break


#Sample usage
# thisaccess_token = "ya29.GltnBpKroMR4lRe9CIqo29GV17ddkXxmwrTwl6YxY" \
#                    "19nBQO_dMaoCyM_1_xcOjivGodnHppUsRRBlwOguauB4MYeMBehcKDOzUkSKDhOoFUNzj96ZkUPU5xOYgKR"
# google = Google(thisaccess_token)
# response = google.ListMessagesMatchingQuery()
# print(response)
#
# for message in response:
#     print(google.GetMessage(message['id']))
#
# Getting titles of calendar events
# events = google.ListCalendatItems()
#
# for item in events['items']:
#     print(item['summary'])



