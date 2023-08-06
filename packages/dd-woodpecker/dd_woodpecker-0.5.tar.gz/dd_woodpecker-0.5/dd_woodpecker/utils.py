"""Utilities"""

from typing import Dict, List


def insert_tags_into_snippets(prospect: Dict, tags: List[str]) -> None:
    """
    Function takes technologies from tag property and
    puts then into snippets, there can only be 15 snippets.
    Args:
        prospect (Dict): Woodpecker prospect object, where snippets should be added
        tags (List[str]): List of tags, that should be inserted into snippets
    """

    for idx, technology in enumerate(tags):
        if idx > 14:
            break
        prospect[f"snippet{idx+1}"] = technology
