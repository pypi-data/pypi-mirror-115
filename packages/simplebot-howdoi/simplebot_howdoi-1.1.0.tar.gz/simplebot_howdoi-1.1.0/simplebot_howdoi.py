"""Plugin's filters and commands definitions."""

import json

import simplebot
from deltachat import Message
from howdoi.howdoi import howdoi
from pkg_resources import DistributionNotFound, get_distribution
from simplebot.bot import Replies

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "0.0.0.dev0-unknown"


@simplebot.filter
def query_filter(message: Message, replies: Replies) -> None:
    """Send me a question in private to get an answer."""
    if not message.chat.is_group():
        _search(message.text, replies)


@simplebot.command(name="/howdoi")
def cmd_howdoi(payload: str, replies: Replies) -> None:
    """Instant coding answers.

    Example:
    /howdoi format date bash

    You can also send me the question direclty in private.
    """
    _search(payload, replies)


def _search(query: str, replies: Replies) -> None:
    try:
        res = json.loads(howdoi("{} -j".format(query)))[0]
        replies.add(text="{}\n\n↗️ {}".format(res["answer"], res["link"]))
    except (Exception, SystemExit):  # noqa
        replies.add(text="❌ Something went wrong.")


class TestPlugin:
    """Online tests"""

    def test_howdoi(self, mocker):
        msg = mocker.get_one_reply("/howdoi format date bash")
        assert "↗" in msg.text

        msg = mocker.get_one_reply("/howdoi -h")
        assert "❌" in msg.text

    def test_filter(self, mocker):
        msg = mocker.get_one_reply("format date bash")
        assert "↗" in msg.text

        # filter should work only in private/direct chat
        msgs = mocker.get_replies("format date bash", group="group1")
        assert not msgs
