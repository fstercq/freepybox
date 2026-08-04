class NetworkControl:

    def __init__(self, access):
        self._access = access


    def list_profiles(self):
        """List network control profiles.

        Freebox OS v15+ uses `network_control/` for per-profile access control.

        Returns a list of profiles (dicts).
        """
        return self._access.get('network_control/')


    def get_profile(self, profile_id):
        """Get a single network control profile by id."""
        return self._access.get('network_control/{0}'.format(profile_id))


    def update_profile(self, profile_id, payload):
        """Update a network control profile.

        Note: Freebox OS expects a payload that includes fields like `macs`.
        If you only send the override fields you may get an error.
        """
        return self._access.put('network_control/{0}'.format(profile_id), payload)


    def set_override(self, profile_id, enabled, mode=None, until=None):
        """Enable/disable manual override for a profile.

        The Freebox API requires including some fields on update (notably `macs`).
        This helper fetches the current profile, merges required fields, and
        applies the requested override.

        Args:
            profile_id (int): profile id
            enabled (bool): whether override should be enabled
            mode (str|None): "allowed" or "denied" when enabling override
            until (int|None): epoch seconds (0 for unlimited) when enabling override

        Returns:
            dict: updated profile
        """
        current = self.get_profile(profile_id)

        payload = {
            # Common required fields
            'macs': current.get('macs', []),
            'cdayranges': current.get('cdayranges', []),
            'resolution': current.get('resolution'),

            # Current override state
            'override': bool(current.get('override')),
            'override_mode': current.get('override_mode'),
        }

        payload['override'] = bool(enabled)

        if enabled:
            if mode is not None:
                payload['override_mode'] = mode
            if until is not None:
                payload['override_until'] = until
        # When disabling override, omit override_until (server recomputes next_change).

        return self.update_profile(profile_id, payload)
