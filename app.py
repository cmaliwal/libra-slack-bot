
import re
import time
from termcolor import colored, cprint
from libra_actions import account, balance, mint, qr_create
from slack_client import slack_client
from utils import *
from constants import *


# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                user = event.get('user')
                return message, event["channel"], user
    return None, None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel, user):
    """
        Executes bot command if the command is known
    """
    user_mention = get_mention(user)

    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.lower().startswith(EXAMPLE_COMMAND) or command.lower().startswith('hi') or command.lower().startswith('hey'):
        response = "Hey *{}*  Thanks for your response. Please let me know how may I help you.\n Please select an option:\n create account\n import account\n check balance".format(user_mention)
    elif command.lower().startswith('create account'):
        response = account()
    elif command.lower().startswith('import account'):
        response = "Please give your wallet seed"
    elif command.lower().startswith('seed'):
        seed = command.split("seed: ",1)[1]
        response = account(seed)
    elif command.lower().startswith('check balance'):
        response = "Please give your wallet address"
    elif command.lower().startswith('wallet address'):
        address = command.split("wallet address: ",1)[1]
        bal = balance(address)
        response = "Your wallet {} balance is: {}".format(address, bal)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":

    # Make connection to slack_client
    if slack_client.rtm_connect(with_team_state=False):
        cprint("---"*11, "yellow")
        cprint("\nStarter Bot connected and running\n", "yellow")
        cprint("---"*11, "yellow")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, user = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel, user)
            time.sleep(RTM_READ_DELAY)
    else:
        cprint(f"Connection failed. Exception traceback printed above.", "red")