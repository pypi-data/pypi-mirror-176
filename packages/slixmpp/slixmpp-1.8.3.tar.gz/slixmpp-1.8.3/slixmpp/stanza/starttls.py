# Slixmpp: The Slick XMPP Library
# Copyright (C) 2021 Mathieu Pasquet
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

from slixmpp.xmlstream import StanzaBase
from typing import Optional


class Starttls(RootStanza):

    """
    Jabber protocol starttls
    """
    namespace = 'jabber:client'
    name = 'starttls'
