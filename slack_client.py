import os
from slackclient import SlackClient
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# instantiate Slack client
slack_token = os.environ['SLACK_TOKEN']
slack_client = SlackClient(slack_token)