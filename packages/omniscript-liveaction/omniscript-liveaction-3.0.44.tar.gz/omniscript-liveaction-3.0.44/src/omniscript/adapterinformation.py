"""AdapterInfo class.
"""
#Copyright (c) LiveAction, Inc. 2022. All rights reserved.
#Copyright (c) Savvius, Inc. 2013-2019. All rights reserved.
#Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.

import six

from .omniaddress import EthernetAddress
from .omniid import OmniId


adapter_types = ['Network Interface Card', 'File Adapter', 'Plugin Adapter']

adapter_find_attributes = ['name', 'id', 'device_name']


class AdapterInformation(object):
    """The Adapter Information class has the attributes of an adapter.
    The 
    :func:`get_adapter_info_list() 
    <omniscript.omniengine.OmniEngine.get_adapter_info_list>`
    function returns a list of Adapter Information objects.
    """

    adapter_type = 0
    address = None
    channel_list = None
    characteristics = 0
    description = ''
    enumerator = ''
    extended_description = ''
    features = None
    flags = 0
    id = None
    interface_fatures = None
    interface_version = None
    link_speed = 0
    media_type = 0
    media_sub_type = 0
    product_name = None
    service_name = None
    symbolic_link = None
    title = None
    versions = None
    option_hidden = False
    option_valid = True
    optoin_valid_advanced = True
    option_virtual = True

    def __init__(self, engine, props):
        self._engine = engine
        self.logger = engine.logger
        self.adapter_type = AdapterInformation.adapter_type
        self.address = AdapterInformation.address
        self.channel_list = AdapterInformation.channel_list
        self.characteristics = AdapterInformation.characteristics
        self.description = AdapterInformation.description
        self.enumerator = AdapterInformation.enumerator
        self.extended_description = AdapterInformation.extended_description
        self.features = AdapterInformation.features
        self.flags = AdapterInformation.flags
        self.id = AdapterInformation.id
        self.link_speed = AdapterInformation.link_speed
        self.media_type = AdapterInformation.media_type
        self.media_sub_type = AdapterInformation.media_sub_type
        self.product_name = AdapterInformation.product_name
        self.service_name = AdapterInformation.service_name
        self.symbolic_link = AdapterInformation.symbolic_link
        self.title = AdapterInformation.title
        self.versions = AdapterInformation.versions
        self.option_hidden = AdapterInformation.option_hidden
        self.option_valid = AdapterInformation.option_valid
        self.optoin_valid_advanced = AdapterInformation.optoin_valid_advanced
        self.option_virtual = AdapterInformation.option_virtual
        self._load(props)

    def __repr__(self):
        return f'AdapterInformation: {self.description}'

    def __str__(self):
        return f'Adapter: {self.description}'

    def _load(self, props):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            for k,v in props.items():
                if k == 'type':
                    self.adapter_type = int(v)
                elif k == 'address':
                    self.address = EthernetAddress(v)
                elif k == 'channel_list':
                    self.channel_list = []
                    if isinstance(v, dict):
                        if 'enumChannels' in v:
                            ch = v.get('enumChannels')
                        elif 'wirelessChannels' in v:
                            wch = v.get('wirelessChannels')
                elif k == 'characteristics':
                    self.channel_list = v
                elif k == 'description':
                    self.description = v
                elif k == 'enumerator':
                    self.enumerator = v
                elif k == 'descriptionExtended':
                    self.extended_description = v
                elif k == 'features':
                    self.features = v
                elif k == 'flags':
                    self.flags = int(v)
                elif k == 'id':
                    self.id = OmniId(v)
                elif k == 'interfaceFeatures':
                    self.interface_fatures = v
                elif k == 'interfaceVersion':
                    self.interface_version = v
                elif k == 'link_speed':
                    self.link_speed = int(v)
                elif k == 'mediaType':
                    self.media_type = int(v)
                elif k == 'mediaSubType':
                    self.media_sub_type = int(v)
                elif k == 'productName':
                    self.product_name = v
                elif k == 'serviceName':
                    self.service_name = v
                elif k == 'symbolicLink':
                    self.symbolic_link = v
                elif k == 'title':
                    self.title = v
                elif k == 'versions':
                    if v:
                        try:
                            self.versions = dict(
                                    (x.strip(),
                                    y.strip() if not y.strip().isnumeric() else int(y))
                                for x,y in (e.split(':')
                                for e in v.split(', ')))
                        except Exception:
                            self.versions = [v]
                elif k == 'hidden':
                    self.option_hidden = v
                elif k == 'valid':
                    self.option_valid = v
                elif k == 'validAdvanced':
                    self.optoin_valid_advanced = v
                elif k == 'supportsVirtual':
                    self.option_virtual = v

    @property
    def name(self):
        """The name/description of the adapter. (Read Only)"""
        return self.description


def _create_adapter_information_list(engine, resp):
    lst = []
    adapters = resp['adapters']
    if isinstance(adapters, list):
        for a in adapters:
            lst.append(AdapterInformation(engine, a))
    lst.sort(key=lambda x: x.description)
    return lst


def find_adapter_information(adapters, value, attrib=adapter_find_attributes[0]):
    """Finds an Adapter Information in the list."""
    if (not adapters) or (attrib not in adapter_find_attributes):
        return None

    if len(adapters) == 0:
        return None

    if isinstance(value, AdapterInformation):
        _value = value.id
        attrib = 'id'
    else:
        _value = value

    return next((i for i in adapters if getattr(i, attrib) == _value), None)
