
# Slixmpp: The Slick XMPP Library
# Copyright (C) 2011  Nathanael C. Fritz
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.
from slixmpp.plugins.base import register_plugin

from slixmpp.features.feature_sasl2mechanisms.mechanisms import FeatureSASL2Mechanisms
from slixmpp.features.feature_sasl2mechanisms.stanza import SASL2Mechanisms
from slixmpp.features.feature_sasl2mechanisms.stanza import SASL2Auth
from slixmpp.features.feature_sasl2mechanisms.stanza import SASL2Success
from slixmpp.features.feature_sasl2mechanisms.stanza import SASL2Failure


register_plugin(FeatureSASL2Mechanisms)
