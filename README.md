# Notion Keylogger

Python keylogger that saves logs in a Notion database. It's recommended to have knowledge about:

- Python
- [Basic Notion](https://youtube.com/playlist?list=PLzyqWC0hTxc-4cuvDjb1eTMes0OoFV2B_)
- [Notion's databases](https://youtu.be/mAJOpO73d8Y)
- [Notion's API](https://developers.notion.com/docs)

## Installation

1. Install requirements: `pip3 install -r requirements.txt`

2. Create a new Notion page and import the [CSV file](./database.csv) as database.

3. In your new Notion database, create a Notion integration by following steps 1-3 from the [Notion's official guide.](https://developers.notion.com/docs/create-a-notion-integration) Remember to save the **database ID** and the **secret API token** in the [Python script.](./notion_klog.py#L9)

## Usage

> :warning: Do not modify the imported database properties for the script to properly work. In case of changing them, apply the respective modifications from [line 118](./notion_klog.py#L118) to [line 139](./notion_klog.py#L139) to keep it working.

After the [installation steps,](#installation) run `python3 notion_klog.py` and logs will be placed inside the database every 60 seconds by default.
