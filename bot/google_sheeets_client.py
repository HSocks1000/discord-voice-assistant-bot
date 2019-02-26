import gspread
import time

from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsClient:
    """
    Gets data from Google Sheets. Specifically, the guild's command channels and the bot's custom responses.
    """

    def __init__(self):
        print("Connecting to Google Sheets...")
        for i in range(24):
            self.refresh_records()

    def refresh_refresh(self):
        starttime = time.time()
        self.refresh_records()
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

    def refresh_records(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("./secret/cs350server1-f9905e0baf48.json", scope)
        client = gspread.authorize(credentials)
        master_sheet = client.open("SockBot Commands")

        self.command_channel_sheet = master_sheet.worksheet("Permissions")
        self.custom_response_sheet = master_sheet.worksheet("Custom Responses")
        self.command_channel_records = None
        self.custom_response_records = None

        self.command_channel_records = self.command_channel_sheet.get_all_records()
        self.custom_response_records = self.custom_response_sheet.get_all_records()

    def get_command_channel_id(self, server_id):
        for entry in self.command_channel_records:
            if str(entry["server_id"]) == server_id:
                return entry["command_channel_id"]
        #self.refresh_records()


    def get_custom_response(self, text):
        for entry in self.custom_response_records:
            trigger_phrases = str(entry["trigger_phrases"]).split(', ')

            for phrase in trigger_phrases:
                if phrase in text:
                    return entry["response"]
        #self.refresh_records()

    def is_command_channel(self, text_channel, server_id):
        for entry in self.command_channel_records:
            if str(entry["server_id"]) == server_id and entry["command_channel_name"] == text_channel:
                #self.refresh_records()
                return True

        return False
        #self.refresh_records()
