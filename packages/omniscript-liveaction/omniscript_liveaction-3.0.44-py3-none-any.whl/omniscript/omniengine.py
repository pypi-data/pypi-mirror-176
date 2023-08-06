"""OmniEngine class.
"""
#Copyright (c) LiveAction, Inc. 2022. All rights reserved.
#Copyright (c) Savvius, Inc. 2013-2019. All rights reserved.
#Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.

import os
import fileinput
import json
import logging
import re
import requests
import six
import time
import xml.etree.ElementTree as ET

from contextlib import closing
from pathlib import PurePath

import omniscript

from .invariant import (BYTES_PER_MEGABYTE, BYTES_PER_GIGABYTE, DEFAULT_PORT,
    ID_FLAG_BRACES, OMNI_FLAG_NO_HTTPS_WARNINGS, OMNI_GET_LOG_MSGS)

from .capture import Capture
from .capturesession import CaptureSession
from .capturetemplate import CaptureTemplate
from .directory import Directory
from .enginestatus import EngineStatus
from .eventlog import EventLog, EventLogEntry
from .fileinformation import FileInformation
from .filter import Filter
from .filternode import FilterNode
from .forensicsearch import ForensicSearch, find_forensic_search
from .forensictemplate import ForensicTemplate
from .graphtemplate import GraphTemplate
from .invariant import (DatabaseOperation, Diagnostics, EngineOperation as EO,
    EngineDataFormat as DF)
from .omniaddress import OmniAddress, IPv4Address, IPv6Address
from .omnierror import OmniError
from .omniid import OmniId
from .omniport import OmniPort
from .peektime import PeekTime
from .performancelogger import PerformanceLogger

from .adapter import _create_adapter_list, find_adapter, adapter_find_attributes
from .adapterinformation import _create_adapter_information_list
from .alarm import _create_alarm_list
from .analysismodule import _create_analysis_module_list
from .application import _create_application_list
from .authenticationtoken import _create_authentication_token_list
from .capture import _create_capture_list, find_capture
from .capturesession import _create_capture_session_list
from .capturetemplate import _create_capture_template_list, find_capture_template
from .country import _create_country_list
# from .directory import _create_file_system
# from .fileinformation import _create_file_information_list
from .filter import _create_filter_list, find_filter
from .forensicsearch import _create_forensic_search_list
from .graphtemplate import _create_graph_template_list, find_graph_template
from .packetfileinformation import PacketFileInformation, _create_packet_file_information_list


ENGINECONFIG = '/etc/omni/engineconfig.xml'
OMNI_CONF = '/etc/omni/omni.conf'
CTD_RATIO = 75

find_attributes = ('name', 'id')

_tag_results = 'results'

jtrue = 'true'
jfalse = 'false'

def jbool(b):
    """Returns 'true' if 'b' is True else 'false'.
    """
    return jtrue if b else jfalse


def _capture_id_list(captures):
    """Returns a list of OmniId.
    """
    capturelist = captures if isinstance(captures, list) else [captures]
    ids = []
    for c in capturelist:
        if isinstance(c, six.string_types):
            id = OmniId(c)
            if id != OmniId.null_id:
                ids.append(id)
        elif isinstance(c, OmniId):
            ids.append(c)
        elif isinstance(c, Capture):
            ids.append(c.id)
        else:
            raise TypeError("capture must be or contain a GUID.")
    return ids


def _capture_session_list(session):
    """Returns a list of session ids.
    """
    session_list = session if isinstance(session, list) else [session]
    lst = []
    for s in session_list:
        if isinstance(s, (int, six.string_types)):
            lst.append(int(s))
        elif isinstance(s, CaptureSession):
            lst.append(s.session_id)
        else:
            raise TypeError('session must be or contain an integer session id.')
    return lst


def _capture_template_list(template):
    """Returns a list of template ids.
    """
    template_list = template if isinstance(template, list) else [template]
    lst = []
    for t in template_list:
        if isinstance(t, (int, six.string_types)):
            lst.append(OmniId(t))
        elif isinstance(t, CaptureTemplate):
            lst.append(t.id)
        else:
            raise TypeError('template must be or contain an integer template id.')
    return lst


def _success(props):
    return isinstance(props, dict) and (_tag_results in props) and \
        isinstance(props[_tag_results], list) and \
        (len(props[_tag_results]) > 0) and (props[_tag_results][0] == 0)


def _almost_success(props):
    # Start Capture sometimes returns: {'returns': []}
    if isinstance(props, dict) and (_tag_results in props):
        return isinstance(props[_tag_results], list)
    return False


class OmniEngine(object):
    """The OmniEngine class provides access to an OmniEngie.
    The function
    :func:`create_engine() <omniscript.omniscript.OmniScript.create_engine>`
    returns an OmniEngine object.
    Then use the function
    :func:`login() <omniscript.omniscript.OmniEngine.login>`
    to enter user credentials to login to the engine.
    """

    logger = None
    """The logging object for the engine."""

    host = ''
    """The address of the host system."""

    port = DEFAULT_PORT
    """The port, https (443)."""

    timeout = 600000
    """The default timeout, in milliseconds, for issuing commands.
    The default is 10 minutes.
    """

    _omni = None
    """The parent OmniScript object of self."""

    _base_url = ''
    """The base URL for the REST API."""

    _session = None
    """The HTTP Session for the REST API."""

    _connected = False
    """Is the client connected and logged in?"""

    _filter_list = None
    """Cached Filter List: (
    :class:`Filter <omniscript.filter.Filter>`,
    :class:`PeekTime <omniscript.peektime.PeekTime>`).
    """

    _filter_timeout = 120 * 1000000000
    """The timeout, in nanoseconds, for refreshing the Filter List.
    Default 2 minutes.
    """

    _last_status = None
    """The last EngineStatus object. Cached for performance."""

    _file_system = None
    """The file system of the host system. A tree of Directory object"""

    _perf_logger = None
    """The engine's Performance Log file."""

    def __init__(self, omni, host, port=DEFAULT_PORT, secure=True):
        self._omni = omni
        self.logger = omni.logger
        self.host = host if host else 'localhost'
        self.port = port if port else OmniEngine.port
        self.timeout = OmniEngine.timeout
        self._connected = False
        self._filter_list = None
        self._filter_timeout = OmniEngine._filter_timeout
        self._last_status = None
        self._file_system = Directory(self, 'root')
        self._perf_logger = OmniEngine._perf_logger

        # if isinstance(self.host, (OmniAddress, IPv4Address, IPv6Address)):
        #     _host = self.host.format()
        # else:
        #     _host = self.host

        # if isinstance(self.port, OmniPort):
        #     _port = self.port.port
        # else:
        #     _port = int(port)

        # _base_url must end with a '/'.
        protocol = 'https' if secure else 'http'
        self._base_url = f'{protocol}://{self.host}:{int(self.port)}/api/v1/'
        self._session = requests.Session()
        self._session.keep_alive = True

    def __repr__(self) -> str:
        return f'OmniEngine: {self._last_status.name}' if self._last_status else 'OmniEngine'

    def __str__(self) -> str:
        return f'OmniEngine: {self._last_status.name}' if self._last_status else 'OmniEngine'

    def _operate_url(self, operation, url, params=None, data=None):
        if operation == EO.GET:
            return self._session.get(url, verify=False, params=params, data=data)
        elif operation == EO.POST:
            return self._session.post(url, verify=False, params=params, data=data)
        elif operation == EO.PUT:
            return self._session.put(url, verify=False, params=params, data=data)
        elif operation == EO.DELETE:
            return self._session.delete(url, verify=False, params=params, data=data)
        return None

    def _pr_operate_url(self, pr, operation, url, params=None, data=None):
        resp = None
        if operation == EO.GET:
            pr.start = PeekTime()
            resp = self._session.get(url, verify=False, params=params, data=data)
            pr.end = PeekTime()
        elif operation == EO.POST:
            pr.start = PeekTime()
            resp = self._session.post(url, verify=False, params=params, data=data)
            pr.end = PeekTime()
        elif operation == EO.PUT:
            pr.start = PeekTime()
            resp = self._session.put(url, verify=False, params=params, data=data)
            pr.end = PeekTime()
        elif operation == EO.DELETE:
            pr.start = PeekTime()
            resp = self._session.delete(url, verify=False, params=params, data=data)
            pr.end = PeekTime()
        return resp

    def _retry_operate_url(self, operation, url, params=None, data=None):
        retries = 3
        resp = self._operate_url(operation, url, params, data)
        while (resp.status_code == 503) and (retries > 0):
            time.sleep(1)
            retries -= 1
            resp = self._operate_url(operation, url)
        return resp

    def _pr_retry_operate_url(self, pr, operation, url, params=None, data=None):
        retries = 3
        resp = self._pr_operate_url(pr, operation, url, params, data)
        while (resp.status_code == 503) and (retries > 0):
            time.sleep(1)
            retries -= 1
            resp = self._pr_operate_url(pr, operation, url)
        return resp

    def _issue_command(self, command, pr=None, operation=EO.GET,
            format=DF.JSON, params=None, data=None):
        """Issue the command and return the response data.
        The OmniEngine object must have a connection to an OmniEngine. 

        Args:
            command (str): the command to issue.

        Returns:
            Success: response data or None on failure.
        """
        _text = None
        if self.is_connected:
            if format == DF.JSON:
                self._session.headers.update({'accept':'application/json'})
            elif format == DF.PLAIN:
                self._session.headers.update({'accept':'text/plain'})
            elif format == DF.HTML:
                self._session.headers.update({'accept':'text/html'})
            elif format == DF.TAG_STREAM:
                self._session.headers.update(
                    {'accept':'application/octet-stream'})
            else:
                raise OmniError('Unrecognized format parameter.')
            url = self._base_url + command
            if pr:
                resp = self._pr_retry_operate_url(pr, operation, url, params=params, data=data)
            else:
                resp = self._retry_operate_url(operation, url, params=params, data=data)

            if format != DF.JSON:
                self._session.headers.update({'accept':'application/json'})

            if resp is None:
                raise OmniError(f'REST API Command failed: Invalid operation.')                
            if resp.status_code == 200:
                if format == DF.JSON:
                    _text = json.loads(resp.text)
                elif format == DF.TAG_STREAM:
                    _text = resp.text.encode()
                else:
                    _text = resp.text
            elif resp.status_code == 204:
                _text = { 'results': [0] }
            elif resp.status_code == 503:
                # 503 - Service temporarily unavailable
                raise OmniError('REST API Command failed: ' \
                    f'{resp.status_code}: {resp.reason}.')
            else:
                raise OmniError(f'REST API Command failed: {resp.status_code}', code=resp.status_code)
        return _text

    def add_capture_template(self, template):
        """Add a Capture Template to the OmniEngine.

        Return:
            bool: True on success, False on failure.
        """
        if isinstance(template, CaptureTemplate):
            t = template.store(encapsulate=True)
        else:
            raise ValueError('A CaptureTemplate is required.')
        pr = self.perf('add_capture_template')
        resp = self._issue_command('capture-templates/', pr, EO.POST, data=t)
        return _success(resp)

    def add_events(self, events):
        """Add one or more entries to the OmniEngine's Event Log.

        Args:
            event (EventLogEntry or a list of EventLogEntry): 
        """
        evt_props = []
        _events = [events] if isinstance(events, EventLogEntry) else events
        if not isinstance(_events, list):
            raise TypeError("The events parameter must be an EventLogEntry or a list.")
        for evt in _events:
            if isinstance(evt, EventLogEntry):
                props = {
                    'longMessage': '',
                    'severity': evt.severity,
                    'shortMessage': evt.message,
                    'sourceId': str(OmniId.null_id),
                    'sourceKey': 0
                }
                if isinstance(evt.capture_id, OmniId):
                    props['contextId'] = evt.capture_id.format()
                if isinstance(evt.timestamp, PeekTime):
                    props['timestamp'] = evt.timestamp.iso_time()
                evt_props.append(props)
        req_props = {
            'events': evt_props
        }
        pr = self.perf('add_events')
        data = json.dumps(req_props)
        resp = self._issue_command('events/', pr, EO.PUT, data=data)
        return resp

    def add_filter(self, omnifilter):
        """Add one to the engine's filter set.

        Args:
            omnifilter (str, Filter): the filter to add.
        """
        item = None
        if isinstance(omnifilter, six.string_types):
            item = Filter(criteria=omnifilter)
        elif isinstance(omnifilter, Filter):
            item = omnifilter
        else:
            raise TypeError('omnifilter must be or contain a Filter.')

        pr = self.perf('add_filter')
        props = item._store()
        cmd = f'filters/{item.id.format()}'
        resp = self._issue_command(cmd, pr, EO.PUT, data=props)
        if not _success(resp):
            raise OmniError('Failed to add filter.')
        return self.get_filter(item.id)

    def create_capture(self, template):
        """Create a new Capture from a
        :class:`CaptureTemplate <omniscript.capturetemplate.CaptureTemplate>`
        object.
        
        Args:
            template(str or
            :class:`CaptureTemplate <omniscript.capturetemplate.CaptureTemplate>`
            ): the capture template.

        Returns:
            A :class:`Capture <omniscript.capture.Capture>` 
            object of the new capture or None.
        """
        if isinstance(template, six.string_types):
            ct = template
        elif isinstance(template, CaptureTemplate):
            ct = template.store(self, True)
        pr = self.perf('create_capture')
        cmd = f'captures/'
        resp = self._issue_command(cmd, pr, EO.POST, data=ct)
        if not resp:
            raise OmniError('Failed to create capture.')
        if isinstance(resp, dict):
            if 'id' in resp:
                id = resp['id']
                cl = self.get_capture_list()
                return find_capture(cl, id, 'id')
        return None

    def create_forensic_search(self, template):
        """Create a new Forensic Search from a
        :class:`ForensicTemplate 
        <omniscript.forensictemplate.ForensicTemplate>`
        object.

        Args:
            template(str or
            :class:`ForensicTemplate 
            <omniscript.forensictemplate.ForensicTemplate>`
            ): the settings of the search.

        Returns:
            A :class:`ForensicSearch 
            <omniscript.forensicsearch.ForensicSearch>`
            object or None."""
        if isinstance(template, six.string_types):
            fst = template
        elif isinstance(template, ForensicTemplate):
            fst = template.store(self, True)
        pr = self.perf('create_forensic_search')
        cmd = f'forensic-searches/'
        resp = self._issue_command(cmd, pr, EO.POST, data=fst)
        if not resp:
            raise OmniError('Failed to create Forensic Search.')
        if isinstance(resp, dict):
            if 'id' in resp:
                id = resp['id']
                return self.get_forensic_search(id)
        return None

    def delete_all_capture_sessions(self):
        """ Delete all the Capture Sessions from the engine.

        Note that 'Capture Sessions' are different from Captures.
        See the Details tab at the bottom of an OmniEngine's
        Forensics tab.
        """
        pr = self.perf('delete_all_capture_sessions')
        props = self._issue_command('capture-sessions/', pr, EO.DELETE)
        if not _success(props):
            raise OmniError('Command failed: 0x80004005')

    def delete_all_filters(self):
        """ Delete all the Filters from the engine.
        """
        pr = self.perf('delete_all_filters')
        props = self._issue_command('filters/', pr, EO.DELETE)
        if not _success(props):
            raise OmniError('Command failed: 0x80004005')

    def delete_all_forensic_searches(self):
        """ Delete all the Forensic Searches from the engine.
        """
        pr = self.perf('delete_all_forensic_searches')
        props = self._issue_command('forensic-searches/', pr, EO.DELETE)
        # if there are no Forensic Searches, then {return:[]} is returned.
        if not _almost_success(props):
            raise OmniError('Command failed: 0x80004005')

    def delete_capture(self, capture, retry=3):
        """Delete a Capture from the OmniEngine.

        Args:
            capture (str,
            :class:`OmniId <omniscript.omniid.OmniId>` or
            :class:`Capture <omniscript.capture.Capture>`
            ): the capture's id or a Capture object.
            Or a list of captures.
        """
        ids = _capture_id_list(capture)
        for id in ids:
            pr = self.perf('delete_capture')
            cmd = f'captures/{id.format()}'
            props = self._issue_command(cmd, pr, EO.DELETE)
            if not _success(props):
                raise OmniError('Command failed: 0x80004005')

    def delete_capture_session(self, session):
        """Deletes Capture Sessions from the OmniEngine.

        Args:
            session (int, str,
            :class:`CaptureSession <omniscript.capturesession.CaptureSession>`
            ): the session's id or a CaptureSession object.
            Or a list of sessions.
        """
        ids = _capture_session_list(session)
        for id in ids:
            pr = self.perf('delete_capture_session')
            cmd = f'capture-sessions/{id}'
            props = self._issue_command(cmd, pr, EO.DELETE)
            if not _success(props):
                raise OmniError('Command failed: 0x80004005')

    def delete_capture_template(self, template):
        """Deletes Capture Templates from the OmniEngine.

        Args:
            template (int, str,
            :class:`CaptureTemplate <omniscript.capturetemplate.CaptureTemplate>`
            ): the template's id or a CaptureTemplate object.
            Or a list of templates.
        """
        ids = _capture_template_list(template)
        for id in ids:
            pr = self.perf('delete_capture_template')
            cmd = f'capture-templates/{id.format()}'
            props = self._issue_command(cmd, pr, EO.DELETE)
            if not _success(props):
                raise OmniError('Command failed: 0x80004005')

    def delete_event_log(self, capture=None, compact=False):
        """Delete the OmniEngine's Event Log.

        Args:
            capture (OmniId, str, Capture, CaptureSession): 
            Delete the entries for just this 'capture'.
            compact (bool): compact the Event Log after deleting
            entries.
        """
        if isinstance(capture, OmniId):
            _context_id = capture
        elif isinstance(capture, six.string_types):
            _context_id = OmniId(capture)
        elif isinstance(capture, Capture):
            _context_id = capture.id
        elif isinstance(capture, CaptureSession):
            _context_id = capture.capture_id
        else:
            _context_id = OmniId()
        req_props = {
            'contextId': _context_id.format(),
            'compact': jbool(compact)
        }
        pr = self.perf('delete_event_log')
        cmd = f'events/'
        resp = self._issue_command(cmd, pr, EO.DELETE, params=req_props)
        if not isinstance(resp, dict):
            raise OmniError('Failed to Delete Event Log.')

    def delete_file(self, target):
        """Delete a list of files from the OmniEngine.
        
        Args:
            target (str): one or more files to delete. If not fully qualified
                          then target will be relative to the engine's
                          data directory.

        Failure:
            Raises an OmniError with results as the list of failures.
        """
        _target = target if isinstance(target, list) else [target]
        req_props = []
        for _t in _target:
            if isinstance(_t, PacketFileInformation):
                _name = _t.path
            elif isinstance(_t, FileInformation):
                _name = _t.name
            else:
                _name = _t
            req_props.append( ('files', _name) )
        if not req_props:
            raise TypeError('No files specified.')
        pr = self.perf('delete_files')
        cmd = f'files/'
        resp = self._issue_command(cmd, pr, EO.DELETE, params=req_props)
        if isinstance(resp, dict):
            results = resp.get('results')
            failures = []
            if isinstance(results, list):
                for r in results:
                    if isinstance(r, dict):
                        code = r.get('result')
                        if code != 0:
                            failures.append(r)
                if failures:
                    raise OmniError('Failed to delete 1 or more files.', result=failures)

    def delete_filter(self, omnifilter):
        """Delete a filter from the OmniEngine's filter set.

        Args:
            omnifilter (str,
            :class:`OmniId <omniscript.omniid.OmniId>` or
            :class:`Filter <omniscript.filter.Filter>`
            ): the id of the filter or a Filter object.
        """
        if not omnifilter:
            return
        idlist = []
        filterlist = omnifilter \
            if isinstance(omnifilter, list) else [omnifilter]
        for f in filterlist:
            if isinstance(f, Filter):
                idlist.append(f.id)
            elif isinstance(f, OmniId):
                idlist.append(f)
            elif isinstance(f, six.string_types):
                idlist.append(OmniId(f))
            elif f is not None:
                raise TypeError('omnifilter must be a Filter.')
        if idlist:
            fl = self.get_filter_list()
            for id in idlist:
                if find_filter(fl, id, 'id'):
                    pr = self.perf('delete_filter')
                    cmd = f'filters/{id.format()}'
                    props = self._issue_command(cmd, pr, EO.DELETE)
                    if not _success(props):
                        raise OmniError('Command failed: 0x80004005')

    def delete_forensic_search(self, search):
        """Delete a 
        :class:`ForensicSearch <omniscript.forensicsearch.ForensicSearch>`
        for the specified id.
        
        Returns:
            A
            :class:`ForensicSearch <omniscript.forensicsearch.ForensicSearch>`
            object.
        """
        if isinstance(search, ForensicSearch):
            id = search.id
        else:
            id = OmniId(search)
        pr = self.perf('delete_forensic_search')
        props = self._issue_command(f'forensic-searches/{id.format()}', pr, EO.DELETE)
        if not _success(props):
            raise OmniError('Command failed: 0x80004005')

    def disconnect(self):
        """Disconnect from the OmniEngine
        """
        return self.logout()

    def file_database_operation(self, operation=DatabaseOperation.SYNC):
        """Perform one of the file database maintenance operations.

        Input:
            operation : Must be one of the DATABASE_ constants.
        """
        if operation == DatabaseOperation.SYNC:
            pr = self.perf('synchronize_file_databases')
            props = self._issue_command('database-sync/', pr, EO.POST)
        elif operation == DatabaseOperation.INDEX:
            pr = self.perf('file_databases_index')
            props = self._issue_command('database-index/', pr, EO.POST)
        elif operation == DatabaseOperation.MAINTENANCE:
            pr = self.perf('file_databases_maintenance')
            props = self._issue_command('database-maintenance/', pr, EO.POST, DF.PLAIN)
        else:
            raise OmniEngine('Illeagal operation, must be one of the DATABASE_ constants.')

    def find_adapter(self, value, attrib=adapter_find_attributes[0]):
        """Find an :class:`Adapter <omniscript.adapter.Adapter>`
        in the OmniEngine's list of adapters.

        Args:
            value (str or :class:`Adapter <omniscript.adapter.Adapter>`
            ): the search key.
            attrib ('name' or 'id'): what attribute to search on.

        Returns:
            An :class:`Adapter <omniscript.adapter.Adapter>`
            object of the adapter.

        Note:
            If value is an :class:`Adapter <omniscript.adapter.Adapter>`,
            then the search is performed on the Adapter's id.
        """
        adapters = self.get_adapter_list()
        return find_adapter(adapters, value, attrib)

    def find_capture(self, value, attrib=find_attributes[0]):
        """Find an :class:`Capture <omniscript.capture.Capture>`
        in the OmniEngine's list of captures.

        Args:
            value (str or :class:`Capture <omniscript.capture.Capture>`
            ): the search key.
            attrib ('name' or 'id'): what attribute to search on.

        Returns:
            An :class:`Capture <omniscript.capture.Capture>`
            object of the capture.

        Note:
            If value is an :class:`Capture <omniscript.capture.Capture>`,
            then the search is performed on the Capture's id.
        """
        captures = self.get_capture_list()
        return find_capture(captures, value, attrib)

    def find_filter(self, value, attrib=find_attributes[0]):
        """Find a :class:`Filter <omniscript.filter.Filter>`
        in the OmniEngine's filter set.

        Args:
            value (str or :class:`Filter <omniscript.filter.Filter>`
            ): the search key.
            attrib ('name' or 'id'): what attribute to search on.

        Returns:
            A :class:`Filter <omniscript.filter.Filter>` object
            of the filter or None.
        """
        filters = self.get_filter_list()
        return omniscript.find_filter(filters, value, attrib)

    def find_forensic_search(self, value, attrib=find_attributes[0]):
        """Find a
        :class:`ForensicSearch <omniscript.forensicsearch.ForensicSearch>`
        in the OmniEngine's Forensic Search list.

        Args:
            value (str or
            :class:`ForensicSearch <omniscript.forensicsearch.ForensicSearch>`
            ): the search key.
            attrib ('name' or 'id'): what attribute to search on.

        Returns:
            A
            :class:`ForensicSearch <omniscript.forensicsearch.ForensicSearch>`
            object or None.
        """
        searches = self.get_forensic_search_list()
        return find_forensic_search(searches, value, attrib)

    def get_adapter_list(self):
        """Get the OmniEngine's list of
        :class:`Adapter <omniscript.adapter.Adapter>`.
        
        Returns:
            A list of
            :class:`Adapter <omniscript.adapter.Adapter>`
            objects.
        """
        pr = self.perf('get_adapter_list')
        props = self._issue_command('adapters/', pr)
        return _create_adapter_list(self, props) if props else None
 
    def get_adapter_information_list(self):
        """Get the OmniEngine's list of
        :class:`AdapterInformation <omniscript.adapterinformation.AdapterInformation>`.
        
        Returns:
            A list of
            :class:`AdapterInformation <omniscript.adapterinformation.AdapterInformation>`
            objects.
        """
        pr = self.perf('get_adapter_information_list')
        props = self._issue_command('adapters/info/', pr)
        return _create_adapter_information_list(self, props) if props else None
 
    def get_alarm_list(self):
        """Get the OmniEngine's list of alarms.
        
        Returns:
            A list of :class:`Alarm <omniscript.alarm.Alarm>` objects.
        """
        pr = self.perf('get_alarm_list')
        props = self._issue_command('alarms/', pr)
        return _create_alarm_list(props) if props else None

    def get_analysis_module_list(self):
        """Get the OmniEngine's list of Analysis Modules.

        Returns:
            A list of
            :class:`AnalysisModule <omniscript.analysismodule.AnalysisModule>`
            objects.
        """
        pr = self.perf('get_analysis_module_list')
        props = self._issue_command('capabilities/', pr)
        return _create_analysis_module_list(self, props.get('pluginsInfo')) if (
            props and 'pluginsInfo' in props) else None

    def get_application_list(self):
        """The the list of Applications.
        """
        pr = self.perf('get_application_list')
        props = self._issue_command('applications/', pr)
        return _create_application_list(props)

    def get_capture_list(self):
        """Get the OmniEngine's list of
        :class:`Capture <omniscript.capture.Capture>`.
        
        Returns:
            A list of
            :class:`Capture <omniscript.capture.Capture>`
            objects.
        """
        pr = self.perf('get_capture_list')
        props = self._issue_command('captures/', pr)
        return _create_capture_list(self, props) if props else None

    def get_capture_session_list(self):
        """Get the OmniEngine's list of
        :class:`CaptureSession <omniscript.capturesession.CaptureSession>`.
        
        Returns:
            A list of
            :class:`CaptureSession <omniscript.capturesession.CaptureSession>`
            objects.
        """
        pr = self.perf('get_capture_session_list')
        props = self._issue_command('capture-sessions/', pr)
        return _create_capture_session_list(self, props) if props else None

    def get_capture_template(self, obj):
        """Get one of the stored Capture Templates.

        Returns:
            A :class:`CaptureTemplate <omniscript.capturetemplate.CaptureTemplate>`
            object.
        """
        if isinstance(obj, CaptureTemplate):
            id = obj.id
        else:
            id = OmniId(obj)
        pr = self.perf('get_capture_template')
        cmd = f'capture-templates/{id.format()}/'
        props = self._issue_command(cmd, pr)
        return CaptureTemplate(props=props, engine=self) if props else None

    def get_capture_template_list(self):
        """Get the OmniEngine's list of stored 
        :class:`CaptureTemplates <omniscript.capturetemplate.CaptureTemplate>`.
        
        Returns:
            A list of
            :class:`Capture <omniscript.capturetemplate.CaptureTemplate>`
            objects.
        """
        pr = self.perf('get_capture_template_list')
        props = self._issue_command('capture-templates/', pr)
        return _create_capture_template_list(self, props) if props else None

    def get_country_list(self):
        """Return the list of Country Names and Codes.
        """
        pr = self.perf('get_country_list')
        props = self._issue_command('countries/', pr)
        return _create_country_list(props)

    def get_diagnostics(self, command=Diagnostics.DEFAULT, verbose=False):
        """Get diagnostice information from the Engine.
        """
        cmd_labels = 'default', 'drives', 'processes', 'raid', 'system-log'
        if command not in Diagnostics:
            raise TypeError('command must be one of the Diagnostics constants.')
        req_props = {
            'verbose': jbool(verbose)
        }
        pr = self.perf('get_diagnostics')
        cmd = f'diagnostics/{cmd_labels[command]}/'
        txt = self._issue_command(cmd, pr, EO.POST, DF.PLAIN, params=req_props)
        return txt

    def get_directory(self, path=None, files=True, hidden=False):
        """Get a :class:`Directory <omniscript.directory.Directory>`
        object of the host system's File System.

        Default path is the engine's data directory.
        
        Returns:
            A
            :class:`Directory <omniscript.directory.Directory>`
            object.
        """
        if path:
            _path = path
        elif self._last_status is not None:
            _path = self._last_status.data_directory
        else:
            _path = '/var/lib/omni/data'
        req_props = {
            'path': _path,
            'showFiles': jbool(files),
            'showHiddenFiles': jbool(hidden)
        }
        pr = self.perf('get_directory')
        cmd = f'directory-list/'
        resp = self._issue_command(cmd, pr, params=req_props)
        return Directory(self, resp)
    
    def get_event_log(self, first=None, count=None, capture=None, query=None, time_span=None):
        """Get the OmniEngine's Event Log.

        Args:
            first (int): the index of the first entry to retrieve.
            count (int): the maximum number of entries to retrieve.
            capture (OmniId, str, Capture, CaptureSession): 
            Get entries for just this 'capture'.
            query (str): only entries whos message contains query.

        Returns:
            A :class:`EventLog <omniscript.eventlog.EventLog>` object.
        """
        if isinstance(capture, OmniId):
            _context_id = capture
        elif isinstance(capture, six.string_types):
            _context_id = OmniId(capture)
        elif isinstance(capture, Capture):
            _context_id = capture.id
        elif isinstance(capture, CaptureSession):
            _context_id = capture.capture_id
        else:
            _context_id = None

        req_props = {
            'informational': jtrue,
            'major': jtrue,
            'minor': jtrue,
            'severe': jtrue,
            'messages': jtrue,
            'sourceId': str(OmniId.null_id),
            'sourceKey': 0,
        }

        if first is not None:
            req_props['offset'] = int(first)
        if count is not None:
            req_props['limit'] = int(count)
        if _context_id:
            req_props['contextId'] = _context_id.format()
        if query:
            req_props['search'] = query
        if isinstance(time_span, (tuple, list, dict)) and len(time_span) == 2:
            req_props['startTime'] = time_span[0].iso_time()
            req_props['stopTime'] = time_span[1].iso_time()

        pr = self.perf('get_event_log')
        data = json.dumps(req_props)
        cmd = f'events/'
        resp = self._issue_command(cmd, pr, params=req_props)
        return EventLog(self, resp, _context_id, query)

    def get_file(self, source):
        """Get a file from the OmniEngine.
        
        Args:
            source (str): name of the file to get. If not fully qualified
                          then source will be relative to the engine's
                          data directory.

        Returns:
            The contents of the file as an array of bytes.
        """
        if isinstance(source, PacketFileInformation):
            _source = source.path
        elif isinstance(source, FileInformation):
            _source = source.name
        else:
            _source = source

        req_props = {
            'file': _source,
            'delete': jfalse
        }
        pr = self.perf('get_file')
        cmd = f'files/'
        resp = self._issue_command(cmd, pr, params=req_props, format=DF.PLAIN)
        return resp
    
    # def get_file_system(self, path='/', files=True, hidden=False):
    #     """Get host system's File System as a tree of Directory
    #     objects.
        
    #     Returns:
    #         A list of
    #         :class:`Directory <omniscript.directory.Directory>`
    #         objects.
    #     """
    #     p = self._last_status.data_directory
    #     req_props = {
    #         'path': path,
    #         'showFiles': jbool(files),
    #         'showHiddenFiles': jbool(hidden)
    #     }
    #     pr = self.perf('get_file_system')
    #     cmd = f'directory-list/'
    #     resp = self._issue_command(cmd, pr, params=req_props)
    #     if resp.status_code != 200:
    #         return None
    #     props = json.loads(resp.text)
    #     return _create_file_system(self, props)
    
    def get_filter(self, omnifilter):
        """Get :class:`Filter <omniscript.filter.Filter>` from the engine.
        
        Args:
            omnifilter (str, id, Filter): id of the Filter
        Returns:
            A  :class:`Filter <omniscript.filter.Filter>` object.
        """
        if isinstance(omnifilter, Filter):
            id = omnifilter.id
        elif isinstance(omnifilter, OmniId):
            id = omnifilter
        elif isinstance(omnifilter, six.string_types):
            id = OmniId(omnifilter)
        elif omnifilter is not None:
            raise TypeError('omnifilter must be an OmniId.')
        else:
            return None

        pr = self.perf('get_filter')
        cmd = f'filters/{id.format()}'
        props = self._issue_command(cmd, pr)
        filter_list = _create_filter_list(props)
        return filter_list[0] if filter_list else None

    def get_filter_list(self, refresh=True):
        """Get the OmniEngine's :class:`Filter <omniscript.filter.Filter>`
        set.
        
        Args:
            refresh(bool): If True will force a refresh, else refresh
                           if the timeout has expired.
        Returns:
            A list of
            :class:`Filter <omniscript.filter.Filter>`
            objects.
        """
        do_refresh = refresh
        if not refresh and self._filter_list:
            delta_time = PeekTime() - self._filter_list[1]
            do_refresh = delta_time.value > self._filter_timeout
        if not self._filter_list or do_refresh:
            pr = self.perf('get_filter_list')
            props = self._issue_command('filters/', pr)
            filter_list = _create_filter_list(props)
            self._filter_list = (filter_list, PeekTime())
        return self._filter_list[0]

    def get_forensic_search(self, search):
        """Get a 
        :class:`ForensicSearch <omniscript.forensicsearch.ForensicSearch>`
        for the specified id.
        
        Returns:
            A
            :class:`ForensicSearch <omniscript.forensicsearch.ForensicSearch>`
            object.
        """
        if isinstance(search, ForensicSearch):
            id = search.id
        else:
            id = OmniId(search)
        pr = self.perf('get_forensic_template')
        props = self._issue_command(f'forensic-searches/{id.format()}', pr)
        return ForensicSearch(props, self) if props else None

    def get_forensic_file_list(self):
        return None

    def get_forensic_search_list(self):
        """Get the OmniEngine's list of
        :class:`ForensicSearch <omniscript.forensicsearch.ForensicSearch>`.
        
        Returns:
            A list of
            :class:`ForensicSearch <omniscript.forensicsearch.ForensicSearch>`
            objects.
        """
        pr = self.perf('get_forensic_search_list')
        props = self._issue_command('forensic-searches/', pr)
        return _create_forensic_search_list(self, props) if props else None

    def get_graph_template_list(self):
        """Get the OmniEngine's list of
        :class:`GraphTemplate <omniscript.graphtemplate.GraphTemplate>`.
        
        Returns:
            A list of :class:`GraphTemplate <omniscript.graphtemplate.GraphTemplate>`
            objects.
        """
        pr = self.perf('get_graph_template_list')
        props = self._issue_command('graphs/', pr)
        return _create_graph_template_list(props) if props else None

    def get_packet_file_list(self):
        """Get a list of packet files and their attributes.
        
        Returns:
            A list of
            :class:`PacketFileInformation <omniscript.packetfileinformation.PacketFileInformation>`
            objects.
        """
        pr = self.perf('get_packet_file_list')
        props = self._issue_command('files-list/', pr)
        return _create_packet_file_information_list(props) if props else None

    def get_session_token(self):
        """Return the current Session Token.
        """
        if 'authorization' in self._session.headers:
            token = self._session.headers['authorization']
            if len(token) > 11:
                return token[11:]
        return None

    def get_status(self):
        """Return the current OmniEngine Status.
        """
        pr = self.perf('get_status')
        data = self._issue_command('status/', pr)
        self._last_status = EngineStatus(self, data)
        return self._last_status

    def get_token_list(self):
        pr = self.perf('get_token_list')
        props = self._issue_command('token/', pr)
        return _create_authentication_token_list(props)

    def get_version(self):
        """Get the OmniEngine's version string.
        
        Returns:
            The OmniEngine's version as a string.
        """
        pr = self.perf('get_version')
        props = self._issue_command('version/', pr)
        return props['engineVersion'] if isinstance(props, dict) and (
            'engineVersion' in props) else None

    def is_connected(self):
        """Get the connection status of the OmniEngine object.
        
        Returns:
            True if OmniEngine object is connected to an OmniEngine,
            otherwise False.
        """
        return self._connected

    def login(self, user, password, session_token=None):
        """Login and connect to the OmniEngine.
        """
        try:
            if session_token:
                # TODO: rewrite with f-string.
                token = ('authToken: '
                    + session_token.decode('utf-8')).encode('utf-8')
                self._session.headers.update({'authorization':token})
                status_url = f'{self._base_url}status/'
                resp = self._session.get(status_url, verify=False)
                if resp.status_code == 200:
                    self._connected = True
                    self.get_status()
                    return True
            url = f'{self._base_url}login/'
            cred_dict = {
                'username': user,
                'password': password,
                'client': 'OmniScript',
                'attempt': 0
            }
            credentials = json.dumps(cred_dict)
            self._session.headers.update({'accept':'application/json'})
            self._session.headers.update({'Content-Type':'application/json'})
            resp = self._session.post(url, verify=False, data=credentials)
            if (resp is None) or (resp.status_code != 200):
                self.logger.debug('Could not login. Retrying')
                retry = True
                while retry and (cred_dict['attempts'] < 6) and (resp.status_code != 200):
                    cred_dict['attempts'] += 1
                    self.logger.debug(f'Attempt No: {cred_dict["attempts"]}')
                    credentials = json.dumps(cred_dict)
                    time.sleep(5)
                    resp = self._session.post(url, verify=False, data=credentials)
                    if resp.status_code == 200:
                        self.logger.debug(f'Retry Succeeded after {cred_dict["attempts"]} attempts.')
                        retry = False
                if cred_dict['attempts'] > 5:
                    if resp.status_code == 502:
                        self.logger.debug(f'Could not connect to engine. Please Check if engine is running and then retry. Response code : {resp.status_code}')
                    else:
                        self.logger.debug(f'Could not connect to engine. Response code : {resp.status_code}')
                    return False
            resp_data = json.loads(resp.text)
            token = ('authToken: ' + resp_data['authToken']).encode('utf-8')
            self._session.headers.update({'authorization':token})
            self._connected = True
            self.get_status()
        except Exception as e:
            self.logger.debug(f'Exception while logging in. {e}')
        return self._connected

    def logout(self):
        """logout and disconnect from the OmniEngine.
        """
        self._connected = False
        errors = []
        if 'authorization' not in self._session.headers:
            return errors
        url = f'{self._base_url}logout/'
        token = self._session.headers['authorization'].decode('utf-8')
        # TODO: rewrite with f-string.
        data = "{\"authToken\":\"" + token + "\"}"
        try:
            resp = self._session.post(url, verify=False, data=data)
        except Exception as e:
            errors.extend(['Exception while logging out'])
            self.logger.debug('Exception while logging out')
        return errors

    def perf(self, msg):
        """Log a performance message.
        """
        return self._perf_logger.perf(msg) if self._perf_logger else None

    def restart(self):
        """Request the OmniEngine to Restart itself.
        The user will be logged off and the connection will be lost.
        """
        url = f'{self._base_url}restart/'
        try:
            resp = self._session.post(url, verify=False)
        except Exception as e:
            self.logger.debug('Exception while restarting the engine.')

    def send_file(self, path):
        """Send a file to the OmniEngine.
        
        Args:
            path (str): name of the name of the file to send. If not fully qualified
                          then a relative path will be used.

        Returns:
            The number of bytes transfered.
        """
        if isinstance(path, PacketFileInformation):
            _path = path.path
        elif isinstance(path, FileInformation):
            _path = path.name
        else:
            _path = path
        if not os.path.isfile(_path):
            raise OmniError(f'File not found: {_path}')
        with open(_path, 'rb') as data_file:
            data = data_file.read()

        p = PurePath(_path)
        kind = ''   # magic.from_file(_path, mime=True)
        req_props = {
            'file': p.name,
            'type': kind
        }
        pr = self.perf('send_file')
        cmd = f'files/'
        resp = self._issue_command(cmd, pr, EO.POST, params=req_props, data=data)
        count = 0
        if isinstance(resp, dict):
            count = int(resp.get('size'))
        return count

    def set_filter_list_timeout(self, timeout):
        """Set the Filter List refresh timeout in seconds.
        """
        self._filter_timeout = int(timeout) * 1000000000    # to nanoseconds.

    def start_capture(self, capture, retry=3):
        """Signal a Capture, or list of Captures, to begin
        capturing packets.

        Args:
            capture (str,
            :class:`OmniId <omniscript.omniid.OmniId>` or
            :class:`Capture <omniscript.capture.Capture>`
            ): the capture's id or a Capture object.
            Or a list of captures.
        """
        ids = _capture_id_list(capture)
        for id in ids:
            pr = self.perf('start_capture')
            command = f'running-captures/{id.format()}/'
            props = self._issue_command(command, pr, EO.POST)
            if not _almost_success(props):
                raise OmniError('Command failed: 0x80004005')

    def start_performance_logging(self, filename, mode='a'):
        """Start loggin the time it takes for the OmniEngine to perform
        each command.

        Args:
            filename: the name of the file to write the log entries.
            mode: open the file in append 'a', or create/overwrite 'c'.
        """
        if self._perf_logger:
            self.stop_performance_logging()
        self._perf_logger = PerformanceLogger(filename, mode)

    def stop_capture(self, capture, retry=3):
        """Signal a Capture, or list of Captures, to
        stop capturing packets.

        Args:
            capture (str,
            :class:`OmniId <omniscript.omniid.OmniId>` or
            :class:`Capture <omniscript.capture.Capture>`
            ): the capture's id or a Capture object.
            Or a list of captures.
        """
        ids = _capture_id_list(capture)
        for id in ids:
            pr = self.perf('stop_capture')
            command = f'running-captures/{id.format()}/'
            props = self._issue_command(command, pr, EO.DELETE)
            if not _almost_success(props):
                raise OmniError('Command failed: 0x80004005')

    def stop_performance_logging(self):
        """Stop Performance Logging.
        """
        if self._perf_logger:
            self._perf_logger = None

    def update_capture_template(self, template):
        """Update an existing Capture Template to the OmniEngine.

        Return:
            bool: True on success, False on failure.
        """
        if isinstance(template, CaptureTemplate):
            t = template.store()
        else:
            raise ValueError('A CaptureTemplate is required.')
        pr = self.perf('update_capture_template')
        cmd = f'capture-templates/{template.id.format()}/'
        resp = self._issue_command(cmd, pr, EO.PUT, data=t)
        return _success(resp)
