from google.oauth2 import service_account
from googleapiclient.discovery import build

# Authenticate using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account-file.json',
    scopes=['https://www.googleapis.com/auth/calendar.readonly']
)
service = build('calendar', 'v3', credentials=credentials)

# Specify the calendar ID you want to retrieve information for
calendar_id = 'alfredom@elevateconstructionist.com'

# Retrieve information about the specified calendar
calendar_list_entry = service.calendarList().get(calendarId=calendar_id).execute()

# Print the summary of the calendar
print('Calendar Summary:', calendar_list_entry['summary'])
