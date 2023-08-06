"""Utilities"""

from typing import Dict, List


def insert_tags_into_snippets(prospect: Dict, tags: List[str]) -> None:
    """
    Function takes in a list of tags and inserts
    them into snippets, there can only be 15 of them..

    Args:
        prospect (Dict): Woodpecker prospect object, where snippets should be added
        tags (List[str]): List of tags, that should be inserted into snippets
    Returns:
        None: Function makes changes in place
    """

    for idx, technology in enumerate(tags):
        if idx > 14:
            break
        prospect[f"snippet{idx+1}"] = technology
