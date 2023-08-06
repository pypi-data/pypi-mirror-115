"""Module provides webhooks subscribing/unsubscribing"""

import base64
from typing import Optional
import requests


class WoodpeckerHook:
    """Subscribing/unsubscribing to certain events"""

    URL_API = "https://api.woodpecker.co/rest/v1/"
    URL_SUBSCRIBE = "webhooks/subscribe"
    URL_UNSUBSCRIBE = "webhooks/unsubscribe"

    def __init__(self, api_key: str) -> None:
        self.api_key = base64.b64encode(api_key.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {self.api_key}"
        }

    def subscribe(self, target_url: str, event: str, to_subscribe: Optional[bool] = True) -> None:
        """
        Args:
            target_url (str): User defined endpoint
            event (str): type of event, on which action should be triggered
            to_subscribe (bool): Determines whether to subscribe or unsubscribe
        """

        body = {
            "target_url": target_url,
            "event": event
        }
        url = self.URL_API
        url += self.URL_SUBSCRIBE if to_subscribe else self.URL_UNSUBSCRIBE

        response = requests.post(url, headers=self.headers, json=body)
        print(response.status_code)
        return response.json() if response.status_code != 204 else None

    def unsubscribe(self, target_url: str, event: str) -> None:
        """
            Args:
                target_url (str): User defined endpoint
                event (str): type of event, on which action should be triggered
            """
        self.subscribe(target_url, event, to_subscribe=False)
