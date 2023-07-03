# Notion Keylogger

Python keylogger that saves logs in a Notion database. It's recommended to have knowledge about:

- Python
- [Basic Notion](https://youtube.com/playlist?list=PLzyqWC0hTxc-4cuvDjb1eTMes0OoFV2B_)
- [Notion's databases](https://youtu.be/mAJOpO73d8Y)
- [Notion's API](https://developers.notion.com/docs)

## Installation

:one: Install [Python version 3.9 or more](https://www.python.org/downloads/) and the requirements with `pip3 install -r requirements.txt`

:two: Create a [Notion account.](https://www.notion.so/signup) Then, create an [internal integration](https://www.notion.so/my-integrations) and get the **Internal Integration Secret (secret token).**

:three: Create a Notion page and import the [CSV database file.](./database.csv) Then, add your integration as a connection and get the **database's URL or ID.**

> :information_source: Detailed steps :two: and :three: explained by Notion [here.](https://developers.notion.com/docs/create-a-notion-integration)

:four: **(optional):** In the database, change the *Date* property type from *Text* to *Created time.* Sort the database by *Date* in descending order for better view.

> :warning: Do not modify more the database properties for the script to properly work. In case of changing them, script should be modified from [line 118](./notion_klog.py#L118) to [line 139.](./notion_klog.py#L139)

:five: Insert your **secret token** and the **database's URL or ID** in the [Python script.](./notion_klog.py#L9)

## Usage

After the [installation steps,](#installation) run `python3 notion_klog.py` and logs will be placed inside the database every 60 seconds by default. To change the report time, modify [line 187.](./notion_klog.py#L187)
