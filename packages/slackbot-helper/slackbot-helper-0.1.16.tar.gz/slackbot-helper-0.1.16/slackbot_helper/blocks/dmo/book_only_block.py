#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Display Book Results with a Book Name and Book URL only """


from typing import List, Optional

from baseblock import BaseObject


class BookOnlyBlock(BaseObject):
    """ Display Book Results with a Book Name and Book URL only

    This is often useful when the 'book' is a short 2-3 page article

    View Sample Output:
        ???
    """

    def __init__(self):
        """ Change Log

        Created:
            15-Nov-2022
            craigtrim@gmail.com
            *   created in pursuit of
                https://github.com/craigtrim/slackbot-helper/issues/2

        Args:
            web_client (WebClient): an instantiation of the slack client
        """
        BaseObject.__init__(self, __name__)

    def _book_name_text(self,
                        book_name: str) -> str:
        """ Format the Provenance Description

        Args:
            book_name (str): the name of the book (label form)

        Returns:
            str: the provenance output
            Sample Output:
                :notebook: SDG 13:
        """
        return ':notebook: *#BOOKNAME*'.replace("#BOOKNAME", book_name)

    @ staticmethod
    def _primary_text_only(primary_text: str,
                           book_name: str,
                           book_button_text: str,
                           book_url: str) -> list:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": primary_text
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": book_name
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": book_button_text
                        },
                        "url": book_url
                    }
                ]
            }
        ]

    @staticmethod
    def _secondary_text(primary_text: str,
                        secondary_text: List[str],
                        book_name: str,
                        book_button_text: str,
                        book_url: str) -> list:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": primary_text
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": secondary_text
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": book_name
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": book_button_text
                        },
                        "url": book_url
                    }
                ]
            }
        ]

    def process(self,
                primary_text: str,
                secondary_text: Optional[List[str]],
                book_url: str,
                book_name: str,
                book_button_text: str,
                slack_channel_id: str,
                slack_thread_ts: Optional[str] = None) -> dict:
        """ Entry Point

        Args:
            primary_text (str): the primary output text to display to the user
            secondary_text (Optional[List[str]]): the secondary output text for the user
            book_url (str): the S3 Chapter URL
            book_name (str): the name of the book (label form)
            book_button_text (str): the name to display on the button
            slack_channel_id (str): the Slack Channel ID
            slack_thread_ts (Optional[str], optional): the Slack Thread timestamp. Defaults to None.

        Returns:
            dict: the display block
        """

        book_name = self._book_name_text(book_name)

        def decide() -> list:
            if secondary_text and len(secondary_text):
                return self._secondary_text(
                    book_url=book_url,
                    book_name=book_name,
                    book_button_text=book_button_text,
                    primary_text=primary_text,
                    secondary_text=secondary_text)

            return self._primary_text_only(
                book_url=book_url,
                book_name=book_name,
                book_button_text=book_button_text,
                primary_text=primary_text)

        blocks = decide()

        d_event_outgoing = {
            'blocks': blocks,
            'channel': slack_channel_id,
            'thread_ts': slack_thread_ts,
        }

        return d_event_outgoing
