"""AuthenticationToken class.
"""
#Copyright (c) LiveAction, Inc. 2022. All rights reserved.
#Copyright (c) Savvius, Inc. 2013-2019. All rights reserved.
#Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.


find_attribs = ['name', 'code']

class AuthenticationToken(object):
    """An Authentication Token object."""

    authentcaion_token_id = None
    client = ''
    expiration_time = None
    label = ''
    last_activity_time = None
    user_domain = ''
    user_id = ''
    user_information_id = ''
    user_name = ''
    option_authentication = False
    option_enabled = False

    # Tags
    _json_authentcaion_token_id = 'authTokenId'
    _json_client = 'client'
    _json_expiration_time = 'expirationTime'
    _json_label = 'label'
    _json_last_activity_time = 'lastActivityTime'
    _json_user_domain = 'userDomain'
    _json_user_id = 'userId'
    _json_user_information_id = 'userInfoId'
    _json_user_name = 'userName'
    _json_option_authentication = 'authentication'
    _json_option_enabled = 'enabled'

    _tag_authentcaion_token_id = 'authentcaion_token_id'
    _tag_client = 'client'
    _tag_expiration_time = 'expiration_time'
    _tag_label = 'label'
    _tag_last_activity_time = 'last_activity_time'
    _tag_user_domain = 'user_domain'
    _tag_user_id = 'user_id'
    _tag_user_information_id = 'user_information_id'
    _tag_user_name = 'user_name'
    _tag_option_authentication = 'option_authentication'
    _tag_option_enabled = 'option_enabled'

    auth_token_prop_dict = {
        _json_authentcaion_token_id: _tag_authentcaion_token_id,
        _json_client: _tag_client,
        _json_expiration_time: _tag_expiration_time,
        _json_label: _tag_label,
        _json_last_activity_time: _tag_last_activity_time,
        _json_user_domain: _tag_user_domain,
        _json_user_id: _tag_user_id,
        _json_user_information_id: _tag_user_information_id,
        _json_user_name: _tag_user_name,
        _json_option_authentication: _tag_option_authentication,
        _json_option_enabled: _tag_option_enabled
    }

    def __init__(self, props):
        self.authentcaion_token_id = AuthenticationToken.authentcaion_token_id
        self.client = AuthenticationToken.client
        self.expiration_time = AuthenticationToken.expiration_time
        self.label = AuthenticationToken.label
        self.last_activity_time = AuthenticationToken.last_activity_time
        self.user_domain = AuthenticationToken.user_domain
        self.user_id = AuthenticationToken.user_id
        self.user_information_id = AuthenticationToken.user_information_id
        self.user_name = AuthenticationToken.user_name
        self.option_authentication = AuthenticationToken.option_authentication
        self.option_enabled = AuthenticationToken.option_enabled
        self._load(props)

    def _load(self, props):
        if not isinstance(props, dict):
            return
        for k,v in props.items():
            a = AuthenticationToken.auth_token_prop_dict.get(k)
            if a == AuthenticationToken._tag_authentcaion_token_id:
                self.authentcaion_token_id = v
            elif a == AuthenticationToken._tag_client:
                self.client = v
            elif a == AuthenticationToken._tag_expiration_time:
                self.expiration_time = v
            elif a == AuthenticationToken._tag_label:
                self.label = v
            elif a == AuthenticationToken._tag_last_activity_time:
                self.last_activity_time = v
            elif a == AuthenticationToken._tag_user_domain:
                self.user_domain = v
            elif a == AuthenticationToken._tag_user_id:
                self.user_id = v
            elif a == AuthenticationToken._tag_user_information_id:
                self.user_information_id = v
            elif a == AuthenticationToken._tag_user_name:
                self.user_name = v
            elif a == AuthenticationToken._tag_option_authentication:
                self.option_authentication = v
            elif a == AuthenticationToken._tag_option_enabled:
                self.option_enabled = v


def _create_authentication_token_list(props):
    lst = []
    if isinstance(props, dict):
        if 'tokens' in props:
            tokens = props.get('tokens')
            if isinstance(tokens, list):
                for t in tokens:
                    lst.append(AuthenticationToken(t))
    return lst
