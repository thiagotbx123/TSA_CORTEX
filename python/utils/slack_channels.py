"""
Slack Channel Utils - Channel to theme mapping.

Provides utilities for:
- Mapping Slack channels to worklog themes
- Channel categorization
- User role inference

Ported from TypeScript: src/spinehub/utils/slack-channels.ts
Used by bridge.py handle_slack() handler.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ChannelInfo:
    """Basic Slack channel information."""
    id: str
    name: str
    is_private: bool = False
    num_members: int = 0


@dataclass
class ChannelMappingResult:
    """Result of mapping a channel to TSA context."""
    channel: str
    channel_id: str
    tsa_members: list[str] = field(default_factory=list)
    eng_members: list[str] = field(default_factory=list)
    gtm_members: list[str] = field(default_factory=list)
    external_members: list[str] = field(default_factory=list)


# Known channel mappings for TSA projects
CHANNEL_THEME_MAP: dict[str, dict[str, str]] = {
    # Customer Projects
    "intuit-internal": {"theme": "Intuit WFS Project", "category": "customer"},
    "testbox-intuit-wfs-external": {"theme": "WFS External Coordination", "category": "customer"},
    "testbox-intuit-mailchimp-external": {"theme": "Mailchimp Integration", "category": "customer"},
    "external-testbox-apollo": {"theme": "Apollo Project", "category": "customer"},
    "brevo-internal": {"theme": "Brevo Integration", "category": "customer"},
    "archer-internal": {"theme": "Archer Project", "category": "customer"},
    # Team Channels
    "tsa-data-engineers": {"theme": "TSA Team Sync", "category": "team"},
    "team-koala": {"theme": "Koala Team", "category": "team"},
    "dev-on-call": {"theme": "Engineering Support", "category": "ops"},
    # Company Channels
    "product": {"theme": "Product Discussions", "category": "internal"},
    "go-to-market": {"theme": "GTM Strategy", "category": "internal"},
    "engineering": {"theme": "Engineering", "category": "internal"},
    "general": {"theme": "General", "category": "internal"},
}

# Known TSA team roles
TSA_ROLES: dict[str, str] = {
    "thiago": "tsa_lead",
    "diego": "tsa",
    "gabrielle": "tsa",
    "carlos": "tsa",
    "alexandra": "tsa",
    "lucas": "engineering",
    "sam": "engineering",
    "waki": "engineering",
}


class SlackChannelMapper:
    """Maps Slack channels to worklog themes and categories."""

    def __init__(
        self,
        token: Optional[str] = None,
        company_domain: str = "@testbox.com",
        channel_prefixes: Optional[list[str]] = None,
    ):
        self.token = token
        self.company_domain = company_domain
        self.channel_prefixes = channel_prefixes or [
            "intuit", "testbox", "brevo", "archer",
            "tsa", "team", "dev", "product", "go-to-market",
        ]

    def list_channels(self, prefixes: Optional[list[str]] = None) -> list[ChannelInfo]:
        """
        List channels matching prefixes.
        Note: Without a live Slack token, returns known channels from theme map.
        """
        target_prefixes = prefixes or self.channel_prefixes
        channels: list[ChannelInfo] = []

        for channel_name, mapping in CHANNEL_THEME_MAP.items():
            if any(channel_name.startswith(p) or p in channel_name for p in target_prefixes):
                channels.append(ChannelInfo(
                    id=f"C_{channel_name.upper().replace('-', '')}",
                    name=channel_name,
                    is_private="-internal" in channel_name,
                    num_members=0,
                ))

        return channels

    def map_channel(self, channel: ChannelInfo) -> ChannelMappingResult:
        """Map a channel to its TSA context (members, roles)."""
        return ChannelMappingResult(
            channel=channel.name,
            channel_id=channel.id,
            tsa_members=[],
            eng_members=[],
            gtm_members=[],
            external_members=[],
        )

    def get_user_role(self, name: str) -> str:
        """Get the role of a user by name."""
        lower_name = name.lower().strip()
        for known_name, role in TSA_ROLES.items():
            if known_name in lower_name:
                return role
        return "unknown"


def get_channel_theme(channel_name: str) -> str:
    """Get theme for a channel."""
    if channel_name in CHANNEL_THEME_MAP:
        return CHANNEL_THEME_MAP[channel_name]["theme"]

    lower = channel_name.lower()
    for pattern, mapping in CHANNEL_THEME_MAP.items():
        if pattern.lower() in lower:
            return mapping["theme"]

    return f"Channel: #{channel_name}"


def get_channel_category(channel_name: str) -> str:
    """Get category for a channel."""
    if channel_name in CHANNEL_THEME_MAP:
        return CHANNEL_THEME_MAP[channel_name]["category"]

    lower = channel_name.lower()
    for pattern, mapping in CHANNEL_THEME_MAP.items():
        if pattern.lower() in lower:
            return mapping["category"]

    if "external" in lower or "client" in lower:
        return "customer"
    if "team" in lower or "squad" in lower:
        return "team"
    if "oncall" in lower or "ops" in lower or "incident" in lower:
        return "ops"

    return "internal"
