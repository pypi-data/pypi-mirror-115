"""Module provides functionalities for the Woodpecker API."""

from typing import Optional, List, Dict
import base64
import requests


class Woodpecker:
    """
    Handles prospects and campaigns management.

        Args:
            api_key (str): Api key generated on your account
    """

    URL_API = "https://api.woodpecker.co/rest/v1/"
    URL_PROSPECTS = "prospects"
    URL_ADD_PROSPECTS_LIST = "add_prospects_list"
    URL_ADD_PROSPECTS_CAMPAIGN = "add_prospects_campaign"
    URL_CAMPAIGNS = "campaign_list"

    def __init__(self, api_key: str) -> None:
        self.api_key = base64.b64encode(api_key.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {self.api_key}"
        }

    def get_prospects(self,
                      per_page: Optional[int] = None,
                      page: Optional[int] = None,
                      sort: Optional[str] = None) -> Optional[List[Dict]]:
        """
        Returns list of all prospects in the database.

        Args:
            per_page (int): Defines a number of results per page.
            page (int): Defines a page number you want access to.
            sort (str): Defines the sort order, as well as the field on which sorting will be based.
                        Usage: +/- and a parameter
        Returns:
            list_of_prospects (Optional[List[Dict]]): Lit of all prospects filtered by given criteria
        """

        params = self.args_to_url_params({
            "per_page": per_page,
            "page": page,
            "sort": sort
        })
        url = self.URL_API + self.URL_PROSPECTS + params

        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code != 204 else None

    def get_single_prospect(self,
                            prospect_id: int,
                            campaigns_details: bool = False) -> Optional[List[Dict]]:
        """
        Returns details of a single prospect.

        Args:
            prospect_id (int): Prospect's ID
            campaigns_details (bool): Show campaign details for a specific prospect
        Returns:
            single_prospect (Optional[List[Dict]]): Single prospect's details
        """

        params = self.args_to_url_params({
            "id": prospect_id,
            "campaigns_details": campaigns_details
        })
        url = self.URL_API + self.URL_PROSPECTS + params

        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code != 204 else None

    def add_prospects_list(self, prospects_list: List[Dict], update: bool = True) -> Optional[Dict]:
        """
        Adds a list of new prospects to the database.

        Args:
            prospects_list (List[Dict]): List containing prospect's details
            update (bool): Defines if prospects, who already are in database should be overwritten
        Returns:
            response (Optional[Dict]): Contains emails of added prospects and status
        """

        body = {
            "update": str(update).lower(),
            "prospects": prospects_list
        }
        url = self.URL_API + self.URL_ADD_PROSPECTS_LIST

        response = requests.post(url, headers=self.headers, json=body)
        return response.json() if response.status_code != 204 else None

    def add_prospects_campaign(self,
                               campaign_id: int, prospects_list: List[Dict]) -> Optional[Dict]:
        """
        Adds a list of new prospects to the certain campaign. If any of the prospects is not in the
        database yet, also inserts him there.

        Args:
            campaign_id (int): Id of the campaign, which you want to add the prospects to
            prospects_list (List[Dict]): List containing prospect's details
        Returns:
            response (Optional[Dict]): Contains emails of added prospects and status
        """

        body = {
            "campaign": {
                "campaign_id": campaign_id
            },
            "update": "true",
            "prospects": prospects_list
        }
        url = self.URL_API + self.URL_ADD_PROSPECTS_CAMPAIGN

        response = requests.post(url, headers=self.headers, json=body)
        return response.json() if response.status_code != 204 else None

    def delete_prospect(self, prospect_id: int, campaign_id: Optional[int] = None) -> Dict:
        """
        Deletes certain prospect from a campaign or database.

        Args:
            prospect_id (int): Id of the prospect, that should be deleted
            campaign_id (Optional[int]): Id of campaign, which you want to remove the prospect from.
              If this param is not specified, then the prospect is deleted from the entire database.
        Returns:
            status_code (Dict): Status code returned by the request
        """

        params = self.args_to_url_params({
            "id": prospect_id,
            "campaigns_id": campaign_id
        })
        url = self.URL_API + self.URL_PROSPECTS + params

        response = requests.delete(url, headers=self.headers)
        return {"status_code": response.status_code}

    def get_campaigns(self) -> Optional[List[Dict]]:
        """
        Returns list of all campaigns

        Returns:
            list_of_campaigns (Optional[List[Dict]]): List of all available campaigns
        """

        url = self.URL_API + self.URL_CAMPAIGNS

        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code != 204 else None

    def get_single_campaign(self, campaign_id: Optional[int] = None,
                            status: Optional[str] = None) -> Optional[List[Dict]]:
        """
        Returns details of a certain campaign.

        Args:
            campaign_id (Optional[int]): id of a specific campaign
            status (Optional[str]): status of a specific campaign
        Returns:
            campaign_details (Optional[List[Dict]]): Single campaign details
        """

        params = self.args_to_url_params({
            "id": campaign_id,
            "status": status
        })
        url = self.URL_API + self.URL_CAMPAIGNS + params

        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code != 204 else None

    @staticmethod
    def args_to_url_params(args: Dict) -> str:
        """
        Converts a dict containing url path arguments into a valid url-like string.

        Args:
            args (dict): Contains url path params with their values
        Returns:
            url_path (str): Args converted to valid url path
        """

        params = [f"{key}={value}" for key, value in args.items() if value]
        return "?" + "&".join(params) if params else ""
