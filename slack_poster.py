# slack_poster.py

import os
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackPoster:
    def post_results(self, results_json, token, channel_id):
        client = WebClient(token=token)
        results_json_str = json.dumps(results_json)
        try:
            response = client.chat_postMessage(channel=channel_id, text=results_json_str)
            print("Message posted successfully:", response["ts"])
        except SlackApiError as e:
            print("Error:", e.response)
