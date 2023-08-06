# Copyright Notice:
# Copyright 2016-2021 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link:
# https://github.com/DMTF/python-redfish-library/blob/master/LICENSE.md

# -*- coding: utf-8 -*-

# ---------Imports---------
import os
import sys
import ssl
import time
import json
import logging.config
import http.client
import argparse
import xml.dom.minidom
import urllib
from urllib.parse import urlparse

import requests
from requests_toolbelt import MultipartEncoder

# generate random integer values
from random import randint
import random
# ---------End of imports---------

class redfish_advantech:
    def __init__(self, hostname, port, username, password, nLogLevel=0, strProtocol='https://'):
        self.__logVerbose = nLogLevel
        # Load logging.conf
        logging.config.fileConfig('logging.conf')
        # create logger
        self.logger = logging.getLogger('redfish')
        if (self.get_logVerbose() >= 1):
            self.logger.debug('=== Start to of redfish_advantech.__init__ ===')

        self.logger.info('BMC=%s, port=%d', hostname, port)

		# ------------Avoid SSL error and ignore SSL Warning-------------
        requests.packages.urllib3.disable_warnings()
        ssl._create_default_https_context = ssl._create_unverified_context
		# ---------End of Avoid SSL error and ignore SSL Warning---------

		# ---------Proxy---------
        self.proxy_enable = False
        # ---------End of Proxy---------

        self.hostname = hostname
        self.root = "/redfish/v1"
        self.session = requests.Session()
        self.port = port
        self.username = username
        self.password = password
        self.strProtocol = strProtocol
        self.__redfishVersion = None
        self.payload = None
        self.theTimeout = 10
        self.connection = None
        self.authToken = None
        self.location = None
        self.method = ''
        self.urlThermal = ''
        self.urlThermalSubsystem = ''
        self.urlThermalSubsystemFans = ''
        self.urlThermalSubsystemThermalMetrics = ''
        self.lstURLThermalMetrics = dict()
        self.nCountThermalMetrics = 0
        self.nIndexThermalMetrics = 0
        self.urlPowerSubsystem = ''
        self.urlPowerSubsystemPowerSubsystem = ''
        self.urlPowerSubsystemPowerSubsystemSupplies = ''
        self.urlFans = ''
        self.urlPower = ''
        self.urlSensors = ''
        self.urlBios = ''
        self.urlProcessors = ''
        self.urlProcessorsAll = dict()
        self.urlSimpleStorage = ''
        self.urlMemory = ''
        self.urlEthernetInterfaces = ''
        self.urlLogServices = ''
        self.urlVirtualMedia = None
        self.strPowerState = ''
        self.urlRegistries = None
        self.lstURL1 = []
        self.nCount1 = 0
        self.nIndex1 = 0
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        self.lstURL3 = dict()
        self.nCount3 = 0
        self.nIndex3 = 0
        self.lstURL4 = dict()
        self.nCount4 = 0
        self.nIndex4 = 0
        self.lstEtag4 = []
        self.lstURL5 = None
        self.nCount5 = 0
        self.nIndex5 = 0
        self.lstURL6 = None
        self.nCount6 = 0
        self.nIndex6 = 0
        self.dictAccountService = dict()
        self.nAccountServiceCount = 0
        self.nAccountServiceIndex = 0
        self.urlLogEntries = ''
        self.bNextLogEntries = False
        self.ether_id = 0
        self.bFirstGetRoot = True
        self.urlFWUpdate = ''
        self.strFWPath = ''
        self.strSerialConsole = ''
        self.urlAccountCreated = ''
        self.strAccountID = ''
        self.strAccountName = ''
        self.strProtocol = strProtocol
        self.urlInsertMediaViaSMB = ''
        self.urlEjectMedia = ''

    def log(self, msg):
        self.logger.info("%s [hostname=%s port%d]",
                         msg, self.hostname, self.port)

    def get_logVerbose(self):
        """Return the level of log verbose"""
        return self.__logVerbose

    def set_logVerbose(self, logVerbose=0):
        """Set log Verbose level

        :param logVerbose: The level of log verbose to be set.
        :type logVerbose: int

        """
        self.__logVerbose = logVerbose

    def get_redfishVersion(self):
        """Return The redfish version number of Advantech BMC"""
        return self.__redfishVersion

    def set_redfishVersion(self, redfishVersion="1.3.1"):
        """Set Advantech redfish version

        :param version: The redfish version number of Advantech BMC to be set.
        :type version: str

        """
        self.__redfishVersion = redfishVersion

    def __del__(self):
        if (self.get_logVerbose() >= 1):
            self.logger.debug('=== Destroy of redfish_advantech.__del__ ===')

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.logout()
        self.disconnect()

    # Redfish http request
    def rfRequest(self, log=True, bXML = False):
        response = None
        if (self.authToken == None):  # No authToken since not login, yet. 
            if bXML:
                headers = {'Accept': 'application/xml', 'Accept-Encoding': 'identity',
                        'Connection': 'Keep-Alive', 'OData-Version': '4.0'}
            else:
                headers = {'Accept': 'application/json', 'Accept-Encoding': 'identity',
                        'Connection': 'Keep-Alive', 'OData-Version': '4.0'}
        else:  # for other requests than login
            if (self.method == "PATCH" and self.url.find("EthernetInterfaces") >= 0 ): # only for change EthernetInterface property of BMC
                headers = {'Accept': 'application/json', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'identity',
                           'OData-Version': '4.0', 'X-Auth-Token': self.authToken, 'IF-MATCH': self.lstEtag4[self.ether_id-1]}
            elif (self.method == "POST" and self.url.find("FWUpdate") >= 0): # only for update firmware
                headers = {'Accept': 'multipart/form-data', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'identity',
                           'OData-Version': '4.0', 'X-Auth-Token': self.authToken}
            else:
                if bXML:
                    headers = {'Accept': 'application/xml', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'identity',
                            'OData-Version': '4.0', 'X-Auth-Token': self.authToken}
                else:
                    headers = {'Accept': 'application/json', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'identity',
                            'OData-Version': '4.0', 'X-Auth-Token': self.authToken}
        try:
            if (self.get_logVerbose() >= 3 or (log and self.get_logVerbose() < 3)):
                if (self.payload == None):
                    self.logger.debug("headers=%s", headers)
                    self.logger.debug("self.payload=None")
                else:
                    self.logger.debug("headers=%s", headers)
                    self.logger.debug("self.payload=%s", self.payload)
            if (self.connection):
                if (self.payload == None):
                    if (self.method.upper() == "GET"):
                        response = self.session.get(
                            self.strProtocol + self.hostname + self.url, headers=headers, verify=False)						
                    elif (self.method.upper() == "POST"):
                        response = self.session.post(
                            self.strProtocol + self.hostname + self.url, headers=headers, verify=False)						
                    elif (self.method.upper() == "DELETE"):
                        response = self.session.delete(
                            self.strProtocol + self.hostname + self.url, headers=headers, verify=False)						
                else:
                    if (self.method.upper() == "POST"):
                        if self.url.find("FWUpdate") >= 0: # only for update firmware
                            response = self.session.post(
                                self.strProtocol + self.hostname + self.url, self.payload, headers=headers, verify=False)
                        else:
                            response = self.session.post(
                                self.strProtocol + self.hostname + self.url, data=json.dumps(self.payload), headers=headers, verify=False)
                    elif (self.method.upper() == "PATCH"):
                        response = self.session.patch(
                            self.strProtocol + self.hostname + self.url, data=json.dumps(self.payload), headers=headers, verify=False)
            else:
                self.logger.error("self.connection is None")
        except Exception as e:
            self.logger.error(e)
            return response

        if (self.get_logVerbose() >= 3 or (log and self.get_logVerbose() < 3)):
            self.logger.debug(
                "[%s %s] status_code=%d", self.method, self.url, response.status_code)
        return response

    # Set proxy
    def setProxy(self):
        host = ""
        try:
            self.logger.debug("os.name=%s", os.name)
            if (os.name == "nt"):
                windows_proxies = urllib.request.getproxies()
                https_proxy = windows_proxies["https"]
                if (https_proxy != ""):
                    self.logger.debug("Windows proxy %s: %s", urlparse(https_proxy).scheme, https_proxy)
                    host = urlparse(https_proxy).netloc
            else:
                https_proxy = os.environ['HTTPS_PROXY']
                self.logger.debug("Linux proxy HTTPS_PROXY=%s", https_proxy)
                host = urlparse(https_proxy).netloc
        except Exception as e:
            self.logger.info("No %s found in the OS env.", e)
        if (host != ""):
            self.proxy_enable = True
        url = urlparse(self.strProtocol + self.hostname)
        if (self.get_logVerbose() >= 2):
            self.logger.debug("url=%s", url)
        proxy = url.netloc
        ssl._create_default_https_context = ssl._create_unverified_context
        if (self.get_logVerbose() >= 2):
            self.logger.debug("self.hostname=%s, self.port=%d, self.theTimeout=%d", self.hostname, self.port, self.theTimeout)
        if self.strProtocol == "https://":
            self.connection = http.client.HTTPSConnection(
                self.hostname, self.port, timeout=self.theTimeout)
        else:
            self.connection = http.client.HTTPConnection(
                self.hostname, self.port, timeout=self.theTimeout)
        self.logger.debug("Start the http connection")
        if (self.proxy_enable):
            self.connection.set_tunnel(self, self.hostname)
            self.logger.info("Enable the https proxy(self.hostname) connection to %s via %s(host)", self.hostname, host)	

    # Get redfish major version
    def getRedfish(self):
        self.method = "GET"
        self.url = "/redfish"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        self.proxy_enable = False
        if (self.connection == None):
            self.setProxy()
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                self.logger.info("The major version of the redfish is %s: %s", i[0], i[1])

    # Get Redfish v1 service root
    def getRedfishV1(self):
        self.method = "GET"
        self.url = self.root
        if self.bFirstGetRoot:
            self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        self.proxy_enable = False
        if (self.connection == None):
            self.setProxy()
        response = self.rfRequest()
        # Get the next link of getRedfishV1
        self.lstURL1 = []
        self.nCount1 = 0
        self.nIndex1 = 0
        result = response.text
        if (response.status_code == 200):
            if self.bFirstGetRoot:
                self.logger.info("status=%d, result=\n%s", response.status_code, result)
                self.bFirstGetRoot = False
            else:
                self.logger.debug("status=%d, result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if (i[0] == "Vendor"):
                    if(i[1] != "Advantech"):
                        self.logger.warning("The vendor %s is not Advantech", i[1])
                        self.logout()
                        self.disconnect()
                        sys.exit()
                    if self.bFirstGetRoot:
                        self.logger.info("The %s is %s", i[0], i[1])
                elif i[0] in {"RedfishVersion", "Product", "UUID"}:
                    if (i[0] == "RedfishVersion"):
                        self.set_redfishVersion(i[1])
                    if self.bFirstGetRoot:
                        self.logger.info('"%s": "%s"', i[0], i[1])
                elif (i[0] in {"OData", "SessionService", "AccountService", "EventService", "Systems", "Chassis", "Managers", "Links"}):
                    json_data2 = i[1]
                    for ii in json_data2.items():
                        if ii[0] == '@odata.id':
                            self.lstURL1.append(ii[1])
                            self.nIndex1 += 1
                            self.nCount1 += 1
                            if (self.get_logVerbose() >= 2):
                                self.logger.debug("%s: %s", ii[0], ii[1])
                                self.logger.debug("Next link=%s", ii[1])
                elif (i[0] in {"Registries", "JsonSchemas", "Tasks", "UpdateService", "CertificateService"} and self.get_redfishVersion() >= "2.0.0"):
                    json_data2 = i[1]
                    for ii in json_data2.items():
                        if ii[0] == '@odata.id':
                            self.lstURL1.append(ii[1])
                            self.nIndex1 += 1
                            self.nCount1 += 1
                            if (self.get_logVerbose() >= 2):
                                self.logger.debug("%s: %s", ii[0], ii[1])
                                self.logger.debug("Next link=%s", ii[1])
                else:
                    if (self.get_logVerbose() >= 2):
                        self.logger.debug("%s: %s", i[0], i[1])
    
    # Get OData
    def getOData(self):
        self.method = "GET"
        self.url = "/redfish/v1/OData"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        self.proxy_enable = False
        if (self.connection == None):
            self.setProxy()
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'value':
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s=", i[0])
                    for ii in i[1]:
                        self.logger.debug(
                            "name: %s, kind: %s, url: %s", ii["name"], ii["kind"], ii["url"])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get /redfish/v1/$metadata
    def getMetadata(self):
        self.method = "GET"
        self.url = "/redfish/v1/$metadata"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        self.proxy_enable = False
        if (self.connection == None):
            self.setProxy()
        response = self.rfRequest(bXML = True)
        dom = xml.dom.minidom.parseString(response.text)
        result = dom.toprettyxml()
        self.logger.info("status=%d result=\n%s", response.status_code, result)

    # Login
    def login(self):
        """ Login and start a REST session.  Remember to call logout() when you are done. """
        self.url = "/redfish/v1/SessionService/Sessions"
        self.method = "POST"
        self.logger.info("Login [%s %s]", self.method, self.url)
        self.proxy_enable = False
        if (self.connection == None):
            self.setProxy()
        data = dict()
        data['UserName'] = self.username
        data['Password'] = self.password
        self.payload = data
        if (self.get_logVerbose() >= 2):
            self.logger.debug("self.payload=%s", self.payload)		

        response = self.rfRequest(self)
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        # Get Token and Location of session after login
        self.logger.debug("Login response headers=%s]", response.headers)
        self.authToken = response.headers['X-Auth-Token']
        self.logger.info("X-Auth-Token=%s]", self.authToken)
        # Get the next link of Chassis
        # 302 (found) for Advantech Redfish 1.3.1, 201 (created) for 2.1.1 & 2.0.0
        if (response.status_code in [201, 302]):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == '@odata.id':
                    self.location = i[1]
                    self.logger.info("Session=%s", self.location)
        self.payload = None

    # Logout
    def logout(self):
        """ Logout of session. YOU MUST CALL THIS WHEN YOU ARE DONE TO FREE UP SESSIONS"""
        if (self.authToken):
            self.url = self.location
            self.method = "DELETE"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            if response.status_code not in [200, 202, 204]:
                self.logger.info("Invalid session resource: %s, return code: %d" % (
                    self.url, response.status_code))
            self.logger.info("User logout response.status_code=%d",
                             response.status_code)
            self.authToken = None
            self.location = None

    # Disconnect
    def disconnect(self):
        if (self.get_logVerbose() >= 1):
            self.logger.debug(
                "=== Disconnecting http redfish_advantech.connection ===")
        if (self.connection):
            try:
                ret = self.connection.close()
                if (ret == None):
                    self.logger.info(
                        'http self.connection closed successfully')
                else:
                    logging.error(
                        'http self.connection closed failed with ', ret)
            except:
                logging.error(
                    'Unknown exception when close the http self.connection')
        else:
            self.logger.info(
                'http self.connection is not connected. No need to close it.')
        self.connection = None
        self.logger.debug('=== End to of redfish_advantech.disconnect ===')

    # Get SessionService
    def getSessionService(self):
        self.method = "GET"
        self.url = "/redfish/v1/SessionService"
        self.logger.info(
            "[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        # Get the next link of SessionService
        self.url = ''
        result = response.text
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        self.logger.info("status=%d, result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Sessions':
                    self.lstURL2.append(i[1]["@odata.id"])
                    self.nCount2 += 1
                    self.nIndex2 += 1
                    if (self.get_logVerbose() >= 1):
                        self.logger.info(
                            "Next link=%s", self.lstURL2[self.nIndex2-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get SessionService/Sessions
    def getSessionServiceSessions(self):
        self.lstURL3 = []
        self.nCount3 = 0
        self.nIndex3 = 0
        if (self.lstURL2[0] != ''):
            self.url = self.lstURL2[0]
            self.method = "GET"
            self.logger.info(
                "[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
        # Get the next link(s) of getSessionServiceSessions
        if (response.status_code == 200):
            self.logger.info(
                "status=%d, result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount3 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL3.append(iii[1])
                                self.nIndex3 += 1
                                if (self.get_logVerbose() >= 0):
                                    self.logger.debug(
                                        "Next link=%s", self.lstURL3[self.nIndex3-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get SessionService/Sessions/*
    def getSessionServiceSessionsAll(self):
        for i in range(self.nCount3):
            if (self.lstURL3[i] != ''):
                self.url = self.lstURL3[i]
                self.method = "GET"
                self.logger.info(
                    "[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                if (self.get_logVerbose() >= 0):
                    self.logger.info("status=%d result=\n%s", response.status_code, result)
                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Delete SessionService/Sessions/*
    def delSessionServiceSessionsAll(self):
        for i in range(self.nCount3):
            if (self.lstURL3[i] != '' and self.lstURL3[i] != self.location):
                self.url = self.lstURL3[i]
                self.method = "DELETE"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)
                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get AccountService

    def getAccountService(self):
        self.method = "GET"
        self.url = "/redfish/v1/AccountService"
        self.logger.info(
            "[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        # Get the next link of AccountService
        self.dictAccountService = dict()
        self.nAccountServiceCount = 0
        self.nAccountServiceIndex = 0
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if (i[0] in {"Accounts", "Roles", "PrivilegeMap"}):
                    json_data2 = i[1]
                    for ii in json_data2.items():
                        if ii[0] == '@odata.id':
                            self.dictAccountService[i[0]] = ii[1]
                            self.nAccountServiceCount += 1
                            self.nAccountServiceIndex += 1
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", ii[0], ii[1])
                                self.logger.debug("Next link of %s=%s", i[0], ii[1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get AccountService/Accounts
    def getAccountServiceAccounts(self):
        self.method = "GET"
        self.url = self.dictAccountService["Accounts"]
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        # Get the next link of AccountServiceAccounts
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        # Get the next link(s) of AccountServiceAccounts
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount2 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL2.append(iii[1])
                                self.nIndex2 += 1
                                if (self.get_logVerbose() >= 1):
                                    self.logger.debug(
                                        "Next link=%s", self.lstURL2[self.nIndex2-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Post AccountService/Accounts for testing purpose
    def postAccountServiceAccounts(self):
        self.method = "POST"
        self.url = self.dictAccountService["Accounts"]
        self.logger.info("[%s %s]", self.method, self.url)
        data = dict()
        data['Password'] = "advantech"
        data['UserName'] = "admin" + str(self.nCount2+100)
        data['RoleId'] = "Administrator"
        self.payload = data
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        self.urlAccountCreated = ''
        self.strAccountID = ''
        self.strAccountName = ''
        if (response.status_code == 201):
            json_data = json.loads(result)
            for i in json_data.items():
                if (i[0] in {"@odata.id", "Id", "UserName"}):
                    if i[0] == '@odata.id':
                        self.urlAccountCreated =i[1]
                    elif i[0] == 'Id':
                        self.strAccountID = i[1]
                    elif i[0] == 'UserName':
                        self.strAccountName = i[1]
                        self.logger.info("Test account [%s] has been created. Id=%s resource link=%s", 
                            self.strAccountName, self.strAccountID, self.urlAccountCreated)
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])
        self.payload = None

    # Delete AccountService/Accounts for testing purpose
    def delAccountServiceAccounts(self, nkeyAccountID=-1):
        if nkeyAccountID < 4:
            self.logger.info("System default user [%s] can't be deleted for testing purpose", self.lstURL2[nkeyAccountID])
            return
        self.method = "DELETE"
        self.url = self.lstURL2[nkeyAccountID]
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code in {200, 201, 204}):
            self.logger.debug("headers=%s]", response.headers)
        self.payload = None

    # Get AccountService/Accounts/*
    def getAccountServiceAccountsAll(self):
        for i in range(self.nCount2):
            if (self.lstURL2[i] != ''):
                self.url = self.lstURL2[i]
                self.method = "GET"
                self.logger.info(
                    "[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)
                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get AccountService/Roles
    def getAccountServiceRoles(self):
        self.method = "GET"
        self.url = self.dictAccountService["Roles"]
        self.logger.info(
            "[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        # Get the next link of getAccountServiceRoles
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        # Get the next link(s) of AccountServiceAccounts
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount2 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL2.append(iii[1])
                                self.nIndex2 += 1
                                self.logger.debug(
                                    "Next link=%s", self.lstURL2[self.nIndex2-1])
                else:
                    self.logger.debug("%s: %s", i[0], i[1])

    # Get AccountService/Roles/*
    def getAccountServiceRolesAll(self):
        for i in range(self.nCount2):
            if (self.lstURL2[i] != ''):
                self.url = self.lstURL2[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)
                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get AccountService/PrivilegeMap
    def getAccountServicePrivilegeMap(self):
        self.method = "GET"
        self.url = self.dictAccountService["PrivilegeMap"]
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        # Get the next link of getAccountServicePrivilegeMap
        result = response.text
        if (self.get_logVerbose() >= 3):
            self.logger.debug("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            self.logger.info("GET %s status=%d [OK]", self.url, response.status_code)

    # Get EventService
    def getEventService(self):
        self.method = "GET"
        self.url = "/redfish/v1/EventService"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        # Get the next link of EventService
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if (i[0] in {"Subscriptions"}):
                    json_data2 = i[1]
                    for ii in json_data2.items():
                        if ii[0] == '@odata.id':
                            self.lstURL2.append(ii[1])
                            self.nIndex2 += 1
                            self.nCount2 += 1
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", ii[0], ii[1])
                                self.logger.debug("Next link=%s", ii[1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get EventService/Subscriptions
    def getEventServiceSubscriptions(self):
        self.method = "GET"
        self.url = "/redfish/v1/EventService/Subscriptions"
        self.logger.info(
            "[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        # Get the next link of AccountService
        self.lstURL3 = []
        self.nCount3 = 0
        self.nIndex3 = 0
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        # Get the next link(s) of getEventServiceSubscriptions
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount3 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL3.append(iii[1])
                                self.nIndex3 += 1
                                if (self.get_logVerbose() >= 1):
                                    self.logger.debug(
                                        "Next link=%s", self.lstURL3[self.nIndex3-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get EventService/Subscription/*
    def getEventServiceSubscriptionsAll(self):
        for i in range(self.nCount3):
            if (self.lstURL3[i] != ''):
                self.url = self.lstURL3[i]
                self.method = "GET"
                self.logger.info(
                    "[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)
                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Post EventService/Actions/EventService.SubmitTestEvent
    def postEventServiceSubmitTestEvent(self):
        """ Submit a test event. """
        self.url = "/redfish/v1/EventService/Actions/EventService.SubmitTestEvent"
        self.method = "POST"
        self.logger.info("[%s %s]", self.method, self.url)
        data = dict()
        data['EventType'] = "Alert"
        self.payload = data
        response = self.rfRequest(self)
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code in {200, 204}):
            self.logger.debug("headers=%s]", response.headers)
        self.payload = None

    # Post EventService/Subscriptions
    def postEventServiceSubscriptions(self):
        """ Add Subscriptions. """
        self.url = "/redfish/v1/EventService/Subscriptions"
        self.method = "POST"
        self.logger.info("[%s %s]", self.method, self.url)
        data = dict()
        # seed random number generator
        t = int( time.time() * 1000.0 )
        random.seed( ((t & 0xff000000) >> 24) +
                    ((t & 0x00ff0000) >>  8) +
                    ((t & 0x0000ff00) <<  8) +
                    ((t & 0x000000ff) << 24)   )
        # generate some integers
        r1 = randint(0, 254)
        r2 = randint(1, 254)
        data['Destination'] = "172.17." + str(r1) + "." + str(r2)
        data['EventTypes'] = ["Alert"]
        data['Context'] = "Public"
        data['Protocol'] = "Redfish"
        self.payload = data

        response = self.rfRequest(self)
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code in {200, 302}):
            self.logger.debug("headers=%s]", response.headers)
        self.payload = None

    # Delete EventService/Subscription/*
    def delEventServiceSubscriptionsAll(self):
        for i in range(self.nCount3):
            if (self.lstURL3[i] != ''):
                self.url = self.lstURL3[i]
                self.method = "DELETE"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems
    def getSystems(self):
        self.url = "/redfish/v1/Systems"
        self.method = "GET"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text

        # Get the next link(s) of Systems
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        result = response.text
        if (response.status_code == 200):
            self.logger.info(
                "status=%d, result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members':
                    json_data2 = json.loads(json.dumps(i[1]))
                    for ii in json_data2:
                        self.lstURL2.append(ii["@odata.id"])
                        self.nCount2 += 1
                        self.nIndex2 += 1
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug(
                                "Next link=%s", self.lstURL2[self.nIndex2-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0
    def getSystems0(self):
        if (self.lstURL2[0] != ''):
            self.url = self.lstURL2[0]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

            if (response.status_code == 200):
                self.logger.info("status=%d result=\n%s", response.status_code, result)
                json_data = json.loads(result)
                self.lstURL3 = dict()
                self.nCount3 = 0
                self.nIndex3 = 0
                for i in json_data.items():
                    if i[0] in {"Bios", "Processors", "SimpleStorage", "Memory", "EthernetInterfaces", "LogServices", "VirtualMedia"}:
                        self.lstURL3[i[0]] = i[1]["@odata.id"]
                        self.nCount3 += 1
                        self.nIndex3 += 1
                        self.logger.info("%s: %s", i[0], i[1])
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])
                    elif i[0] == "SerialConsole":
                        for ii in i[1].items():
                            if ii[0] == "SSH":
                                for iii in ii[1].items():
                                    if iii[0] == "ConsoleEntryCommand":
                                        self.strSerialConsole = iii[1]
                                        self.logger.info("ConsoleEntryCommand=%s", self.strSerialConsole)


    # Get Systems/0/Bios
    def getSystems0Bios(self):
        if (self.lstURL3["Bios"] != ''):
            self.url = self.lstURL3["Bios"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

            # Get contents of Systems/Bios
            if (response.status_code == 200):
                if (self.get_logVerbose() >= 0):
                    self.logger.info("status=%d result=\n%s", response.status_code, result)
                json_data = json.loads(result)
                for i in json_data.items():
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/Processors (To support multi-processors)
    def getSystems0Processors(self):
        if (self.lstURL3["Processors"] != ''):
            self.url = self.lstURL3["Processors"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

        # Get the next link(s) of CPU*
        self.lstURL4 = []
        self.nCount4 = 0
        self.nIndex4 = 0
        if (response.status_code == 200):
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount4 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL4.append(iii[1])
                                self.nIndex4 += 1
                                self.logger.debug("Next link=%s", self.lstURL4[self.nIndex4-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/Processors/*
    def getSystems0ProcessorsAll(self):
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text

                if (response.status_code == 200):
                    self.logger.info("status=%d result=\n%s", response.status_code, result)
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/SimpleStorage
    def getSystems0SimpleStorage(self):
        if (self.lstURL3["SimpleStorage"] != ''):
            self.url = self.lstURL3["SimpleStorage"]
            self.method = "GET"
            self.logger.debug("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

        self.lstURL4 = []
        self.nCount4 = 0
        self.nIndex4 = 0
        # Get the next link(s) of SimpleStorage
        if (response.status_code == 200):
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount4 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL4.append(iii[1])
                                self.nIndex4 = self.nIndex4 + 1
                                self.logger.info("Next link=%s", self.lstURL4[self.nIndex4-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/SimpleStorage/*
    def getSystems0SimpleStorageAll(self):
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text

                if (response.status_code == 200):
                    self.logger.info("status=%d result=\n%s", response.status_code, result)
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/Memory
    def getSystems0Memory(self):
        if (self.lstURL3["Memory"] != ''):
            self.url = self.lstURL3["Memory"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

        # Get the next link(s) of Memory
        self.lstURL4 = []
        self.nCount4 = 0
        self.nIndex4 = 0
        if (response.status_code == 200):
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount4 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL4.append(iii[1])
                                self.nIndex4 += 1
                                self.logger.debug("Next link=%s", self.lstURL4[self.nIndex4-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/Memory/*
    def getSystems0MemoryAll(self):
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text

                if (response.status_code == 200):
                    self.logger.info("status=%d result=\n%s", response.status_code, result)
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/EthernetInterfaces
    def getSystems0EthernetInterfaces(self):
        if (self.lstURL3["EthernetInterfaces"] != ''):
            self.url = self.lstURL3["EthernetInterfaces"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

        # Get the next link(s) of EthernetInterfaces
        self.lstURL4 = []
        self.nCount4 = 0
        self.nIndex4 = 0
        if (response.status_code == 200):
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount4 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL4.append(iii[1])
                                self.nIndex4 = self.nIndex4 + 1
                                self.logger.info("Next link=%s", self.lstURL4[self.nIndex4-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/EthernetInterfaces/*
    def getSystems0EthernetInterfacesAll(self):
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                if (self.get_logVerbose() >= 0):
                    self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/LogServices
    def getSystems0LogServices(self):
        if (self.lstURL3["LogServices"] != ''):
            self.url = self.lstURL3["LogServices"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

        # Get the next link(s) of LogServices
        self.lstURL4 = []
        self.nCount4 = 0
        self.nIndex4 = 0
        if (response.status_code == 200):
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount4 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL4.append(iii[1])
                                self.nIndex4 = self.nIndex4 + 1
                                self.logger.info("Next link=%s", self.lstURL4[self.nIndex4-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/LogServices (Less info log)
    def getSystems0LogServicesLite(self):
        if (self.lstURL3["LogServices"] != ''):
            self.url = self.lstURL3["LogServices"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

        # Get the next link(s) of LogServices
        self.lstURL4 = []
        self.nCount4 = 0
        self.nIndex4 = 0
        if (response.status_code == 200):
            self.logger.debug("status=%d result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount4 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL4.append(iii[1])
                                self.nIndex4 = self.nIndex4 + 1
                                self.logger.debug("Next link=%s", self.lstURL4[self.nIndex4-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/LogServices/Log
    def getSystems0LogServicesLog(self):
        self.url = ''
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text

                if (response.status_code == 200):
                    self.logger.info("status=%d result=\n%s", response.status_code, result)
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if i[0] == 'Entries':
                            json_data2 = list(i[1].items())
                            if json_data2[0][0] == '@odata.id':
                                self.urlLogEntries = json_data2[0][1]
                                self.logger.info("Next link=%s", self.urlLogEntries)
                        else:
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/LogServices/Log (less info log)
    def getSystems0LogServicesLogLite(self):
        self.url = ''
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text

                if (response.status_code == 200):
                    self.logger.debug("status=%d result=\n%s", response.status_code, result)
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if i[0] == 'Entries':
                            json_data2 = list(i[1].items())
                            if json_data2[0][0] == '@odata.id':
                                self.urlLogEntries = json_data2[0][1]
                                self.logger.debug("Next link=%s", self.urlLogEntries)
                        else:
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/LogServices/Log/Entries (Enhanced for Advantech Redfish version >= 2.1.1 and backward compatible)
    def getSystems0LogServicesLogEntries(self):
        self.lstURL5 = []
        self.nCount5 = 0
        self.nIndex5 = 0
        while (self.urlLogEntries != ''):
            self.url = self.urlLogEntries
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            self.urlLogEntries = ''
            # Get the next link(s) of Entries
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount5 = i[1]
                        self.logger.info("Number of LogServicesLogEntries %d", self.nCount5)
                    elif i[0] == '@odata.nextLink':
                        self.urlLogEntries = i[1]
                        self.logger.info("More LogServicesLogEntries next link=%s", i[1])
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL5.append(iii[1])
                                    self.nIndex5 = self.nIndex5 + 1
                                    if (self.get_logVerbose() >= 2):
                                        self.logger.debug("Next link=%s", self.lstURL5[self.nIndex5-1])
                    else:
                        if (self.get_logVerbose() >= 2):
                            self.logger.debug("%s: %s", i[0], i[1])
        
    # Get Systems/0/LogServices/Log/Entries/*
    def getSystems0LogServicesLogEntriesAll(self):
        for i in range(self.nCount5):
            if (self.lstURL5[i] != ''):
                if (self.get_logVerbose() < 3):
                    if i < self.nCount5 - 1:
                        print("\rLogServicesLogEntries({})={}".format(
                            i+1, self.lstURL5[i]), end='')
                    else:
                        print("\rLogServicesLogEntries({})={}".format(
                            i+1, self.lstURL5[i]))
                self.url = self.lstURL5[i]
                self.method = "GET"
                self.payload = None
                response = self.rfRequest(False)
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 3):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/LogServices/Log/Entries (Only max to 50 entries for each query)
    def getSystems0LogServicesLogEntries50(self):
        self.lstURL5 = []
        self.nCount5 = 0
        self.nIndex5 = 0
        if (self.urlLogEntries != ''):
            self.url = self.urlLogEntries
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            self.urlLogEntries = ''
            # Get the next link(s) of Entries
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount5 = i[1]
                        self.logger.info("Number of LogServicesLogEntries %d", self.nCount5)
                    elif i[0] == '@odata.nextLink':
                        self.urlLogEntries = i[1]
                        self.bNextLogEntries = True
                        self.logger.info("More LogServicesLogEntries next link=%s", i[1])
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL5.append(iii[1])
                                    self.nIndex5 = self.nIndex5 + 1
                                    if (self.get_logVerbose() >= 2):
                                        self.logger.debug("Next link=%s", self.lstURL5[self.nIndex5-1])
                    else:
                        if (self.get_logVerbose() >= 2):
                            self.logger.debug("%s: %s", i[0], i[1])
        
    # Post Systems/0/LogServices/Log/Actions/LogService.Reset
    def postSystems0LogServicesLogActionsLogServiceReset(self):
        """ Clear the SEL log """
        self.url = "/redfish/v1/Systems/0/LogServices/Log/Actions/LogService.ClearLog" # For 3.1.0
        self.method = "POST"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None

        response = self.rfRequest(self)
        result = response.text
        if (self.get_logVerbose() >= 0):
            self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            self.logger.info("headers=%s]", response.headers)

    # Get Systems/0/VirtualMedia (New for Advantech redfish version >= "2.1.1")
    def getSystems0VirtualMedia(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/Systems/0/VirtualMedia Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        if (self.lstURL3["VirtualMedia"] != ''):
            self.url = self.lstURL3["VirtualMedia"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

            self.logger.info("status=%d result=\n%s", response.status_code, result)
            # Get the next link(s) of VirtualMedia
            self.lstURL4 = []
            self.nCount4 = 0
            self.nIndex4 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount4 = i[1]
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL4.append(iii[1])
                                    self.nIndex4 = self.nIndex4 + 1
                                    self.logger.info("Next link=%s", self.lstURL4[self.nIndex4-1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Systems/0/VirtualMedia/* (New for Advantech redfish version >= "2.1.1")
    def getSystems0VirtualMediaAll(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/Systems/0/VirtualMedia/* Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            self.nCount1 = 0
            return
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if i[0] == "Actions":
                            for ii in i[1].items():
                                if ii[0] == "#VirtualMedia.EjectMedia":
                                    self.urlEjectMedia = ii[1]["target"]
                                elif ii[0] == "Oem":
                                    self.urlInsertMediaViaSMB = ii[1]["#AdvantechManager.InsertMediaViaSMB"]["target"]
                        else:
                            if self.get_logVerbose() >= 1:
                                self.logger.debug("%s: %s", i[0], i[1])

    # Post /redfish/v1/Systems/0/VirtualMedia/usb1/Actions/Oem/AdvantechManager.InsertMediaViaSMB
    def postInsertMediaViaSMB(self, smbPath, smbDomainName, smbFilename, smbUsername, smbPassword):
        self.method = "POST"
        self.url = self.urlInsertMediaViaSMB
        self.logger.info("[%s %s]", self.method, self.url)
        data = dict()
        data['SambaShareAddress'] = smbPath
        data['SambaDomainName'] = smbDomainName
        data['ImagePath'] = smbFilename
        data['UserName'] = smbUsername
        data['Password'] = smbPassword
        self.payload = data
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 202):
            self.logger.info("HTTP 1.1 202 Accepted")
        self.payload = None

    # Post /redfish/v1/Systems/0/VirtualMedia/usb1/Actions/VirtualMedia.EjectMedia
    def postEjectMedia(self):
        self.method = "POST"
        self.url = self.urlEjectMedia
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 202):
            self.logger.info("HTTP 1.1 202 Accepted")
        self.payload = None

    # GracefulShutdown or Power on
    def postGracefulShutdownOrPowerOn(self, ResetType="GracefulShutdown"):
        self.logger.info("postGracefulShutdownOrPowerOn: %s", ResetType)
        if (self.strPowerState != ''):
            self.url = "/redfish/v1/Systems/0/Actions/ComputerSystem.Reset"
            self.method = "POST"
            self.logger.info("[%s %s]", self.method, self.url)
            data = dict()
            data['ResetType'] = ResetType
            self.payload = data
            self.logger.info('self.payload %s', ResetType)
            response = self.rfRequest()
            result = response.text
            if (self.get_logVerbose() >= 0):
                self.logger.info("status=%d result=\n%s", response.status_code, result)

        self.payload = None

    # Get Chassis
    def getChassis(self):
        self.method = "GET"
        self.url = "/redfish/v1/Chassis"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        self.url = ''
        result = response.text
        # Get the next link(s) of Chassis
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        result = response.text
        self.logger.info("status=%d, result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members':
                    json_data2 = json.loads(json.dumps(i[1]))
                    for ii in json_data2:
                        self.lstURL2.append(ii["@odata.id"])
                        self.nCount2 += 1
                        self.nIndex2 += 1
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug(
                                "Next link=%s", self.lstURL2[self.nIndex2-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u
    def getChassis1u(self):
        if (self.lstURL2[0] != ''):
            self.url = self.lstURL2[0]
            self.method = "GET"
            self.payload = None
            self.logger.info("[%s %s]", self.method, self.url)
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            self.lstURL3 = dict()
            self.nCount3 = 0
            self.nIndex3 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] in {"ThermalSubsystem", "PowerSubsystem", "Sensors"}:
                        json_data2 = json.loads(json.dumps(i[1]))
                        for ii in json_data2.items():
                            if ii[0] == '@odata.id':
                                self.lstURL3[i[0]] = ii[1]
                                self.nIndex3 += 1
                                self.nCount3 += 1
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", ii[0], ii[1])
                            self.logger.debug("Next link %s=%s", i[0], ii[1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u (this function only get the powerstate of the payload)
    def getPowerState(self):
        self.url = "/redfish/v1/Chassis/1u"
        self.method = "GET"
        self.payload = None
        self.logger.info("[%s %s]", self.method, self.url)
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == "PowerState":
                    self.strPowerState = i[1]
                    self.logger.info("Power State=%s", self.strPowerState)
                    return self.strPowerState

    # Get Chassis/1u/Thermal < version 3.1.0
    def getChassis1uThermal(self):
        if (self.urlThermal != ''):
            self.method = "GET"
            self.url = self.urlThermal
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == "Temperatures":
                        self.logger.debug("Temperatures")
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == 'Name':
                                    sensorName = iii[1]
                                elif iii[0] == 'ReadingCelsius':
                                    sensorValues = iii[1]
                                    self.logger.debug(
                                        "SensorName: %s = %s °C", sensorName, sensorValues)
                    elif i[0] == 'Fans':
                        self.logger.info("Fans")
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == 'Name':
                                    sensorName = iii[1]
                                elif iii[0] == 'Reading':
                                    sensorValues = iii[1]
                                    self.logger.info(
                                        "SensorName: %s=%s RPM", sensorName, sensorValues)
                    elif i[0] == 'Redundancy':
                        self.logger.info("Redundancy")
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/ThermalSubsystem >= version 3.1.0
    def getChassis1uThermalSubsystem(self):
        if (self.lstURL3["ThermalSubsystem"] != ''):
            self.method = "GET"
            self.url = self.lstURL3["ThermalSubsystem"]
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            self.lstURL4 = dict()
            self.nCount4 = 0
            self.nIndex4 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] in {"ThermalMetrics", "Fans"}:
                        self.logger.debug("%s link=%s", i[0], i[1]["@odata.id"])
                        if i[0] == "ThermalMetrics":
                            self.lstURL4["ThermalMetrics"] = i[1]["@odata.id"]
                        else:
                            self.lstURL4["Fans"] = i[1]["@odata.id"]
                            self.nCount4 += 1
                            self.nIndex4 += 1
                    elif i[0] == 'FanRedundancy':
                        self.logger.info("FanRedundancy")
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/ThermalSubsystem/Fans >= version 3.1.0
    def getChassis1uThermalSubsystemFans(self):
        if (self.lstURL4["Fans"] != ''):
            self.method = "GET"
            self.url = self.lstURL4["Fans"]
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            # Get the next link(s) of getChassis1uThermalSubsystemFans
            self.lstURL5 = []
            self.nCount5 = 0
            self.nIndex5 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount5 = i[1]
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL5.append(iii[1])
                                    self.nIndex5 += 1
                                    self.logger.debug("Next link=%s", self.lstURL5[self.nIndex5-1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/ThermalSubsystem/Fans/* >= version 3.1.0
    def getChassis1uThermalSubsystemFansAll(self):
        for i in range(self.nCount5):
            if (self.lstURL5[i] != ''):
                self.url = self.lstURL5[i]
                self.method = "GET"
                self.logger.debug("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                if (self.get_logVerbose() >= 2):
                    self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if i[0] == "SpeedPercent":
                            json_data2 = i[1]
                            for ii in json_data2.items():
                                if ii[0] == 'DataSourceUri':
                                    sensorUrl = ii[1]
                                elif ii[0] == 'SpeedRPM':
                                    sensorValues = ii[1]
                                    if (self.get_logVerbose() >= 2):
                                        self.logger.debug("sensorUrl: %s = %s RPM", sensorUrl, sensorValues)

                                    self.url = sensorUrl
                                    self.method = "GET"
                                    self.logger.debug("[%s %s]", self.method, self.url)
                                    self.payload = None
                                    response = self.rfRequest()
                                    result = response.text
                                    if (self.get_logVerbose() >= 2):
                                        self.logger.info("status=%d result=\n%s", response.status_code, result)

                                    if (response.status_code == 200):
                                        json_data3 = json.loads(result)
                                        for j in json_data3.items():
                                            if j[0] == "Name":
                                                self.logger.info("SensorName: %-16s = %4s RPM", j[1], sensorValues)
                        else:
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/ThermalSubsystem/ThermalMetrics >= version 3.1.0
    def getChassis1uThermalSubsystemThermalMetrics(self):
        if (self.lstURL4["ThermalMetrics"] != ''):
            self.method = "GET"
            self.url = self.lstURL4["ThermalMetrics"]
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            # Get the next link(s) of getChassis1uThermalSubsystemThermalMetrics
            self.lstURL5 = []
            self.nCount5 = 0
            self.nIndex5 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'TemperatureReadingsCelsius@odata.count':
                        self.nCount5 = i[1]
                    elif i[0] == 'TemperatureReadingsCelsius':
                        json_data2 = dict(enumerate(i[1]))
                        sensorName = None
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == 'DataSourceUri':
                                    self.lstURL5.append(iii[1])
                                elif iii[0] == 'DeviceName':
                                    sensorName = iii[1]
                                elif iii[0] == "Reading":
                                    self.nIndex5 += 1
                                    self.logger.debug("Next link=%s", self.lstURL5[self.nIndex5-1])
                                    self.logger.info('[%3s] %-16s: Reading=%3d°C', os.path.basename(self.lstURL5[self.nIndex5-1]), sensorName, iii[1])
                                else:
                                    self.logger.debug('"%s": "%s"', iii[0], iii[1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/ThermalSubsystem/ThermalMetrics/* >= version 3.1.0
    def getChassis1uThermalSubsystemThermalMetricsAll(self):
        for i in range(self.nCount5):
            if (self.lstURL5[i] != ''):
                self.url = self.lstURL5[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)
                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 2):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/PowerSubsystem >= version 3.1.0
    def getChassis1uPowerSubsystem(self):
        if (self.lstURL3["PowerSubsystem"] != ''):
            self.method = "GET"
            self.url = self.lstURL3["PowerSubsystem"]
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] in {"PowerSupplies"}:
                        self.logger.info("%s link=%s", i[0], i[1]["@odata.id"])
                        self.urlPowerSubsystemPowerSubsystemSupplies = i[1]["@odata.id"]
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/PowerSubsystem/PowerSupplies >= version 3.1.0
    def getChassis1uPowerSubsystemPowerSupplies(self):
        if (self.urlPowerSubsystemPowerSubsystemSupplies != ''):
            self.method = "GET"
            self.url = self.urlPowerSubsystemPowerSubsystemSupplies
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            # Get the next link(s) of getChassis1uPowerSubsystemPowerSupplies
            self.lstURL4 = []
            self.nCount4 = 0
            self.nIndex4 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount4 = i[1]
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL4.append(iii[1])
                                    self.nIndex4 = self.nIndex4 + 1
                                    self.logger.debug("Next link=%s", self.lstURL4[self.nIndex4-1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    def getChassis1uPowerSubsystemPowerSuppliesAll(self):
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                self.lstURL5 = []
                self.nCount5 = 0
                self.nIndex5 = 0
                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 2):
                            self.logger.debug("%s: %s", i[0], i[1])
                        if i[0] in {"Assembly", "Metrics"}:
                            self.lstURL5.append(i[1])
                            self.nCount5 += 1
                            self.nIndex5 += 1
                    for ii in range(self.nCount5):
                        if (self.lstURL5[ii] != ''):
                            self.url = self.lstURL5[ii]['@odata.id']
                            self.method = "GET"
                            self.logger.info("[%s %s]", self.method, self.url)
                            self.payload = None
                            response = self.rfRequest()
                            result = response.text
                            self.logger.info("status=%d result=\n%s", response.status_code, result)

                            self.lstURL6 = []
                            self.nCount6 = 0
                            self.nIndex6 = 0
                            if (response.status_code == 200):
                                json_data = json.loads(result)
                                for iii in json_data.items():
                                    if (self.get_logVerbose() >= 1):
                                        self.logger.debug("%s: %s", iii[0], iii[1])
                                    if i[0] in {"Metrics"}:
                                        self.lstURL6.append(iii[1])
                                        self.nCount6 += 1
                                        self.nIndex6 += 1

    # Get Chassis/1u/Power
    def getChassis1uPower(self):
        if (self.urlPower != ''):
            self.method = "GET"
            self.url = self.urlPower
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            if (self.get_logVerbose() >= 0):
                self.logger.info("status=%d result=\n%s", response.status_code, result)

            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == "Voltages":
                        self.logger.debug("Voltages")
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == 'Name':
                                    sensorName = iii[1]
                                elif iii[0] == 'ReadingVolts':
                                    sensorValues = iii[1]
                                    self.logger.info(
                                        "SensorName: %s=%s V(DC)", sensorName, sensorValues)
                    elif i[0] == 'PowerSupplies':
                        self.logger.info("PowerSupplies")
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == 'Name':
                                    sensorName = iii[1]
                                elif iii[0] == 'LineInputVoltage':
                                    sensorValues = iii[1]
                                    self.logger.info(
                                        "SensorName: %s=%s V(AC)", sensorName, sensorValues)
                    elif i[0] == 'Redundancy':
                        self.logger.info("Redundancy")
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/Sensors
    def getChassis1uSensors(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/Chassis/1u/Sensors Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        if (self.lstURL3["Sensors"] != ''):
            self.method = "GET"
            self.url = self.lstURL3["Sensors"]
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)
 
            # Get the next link(s) of getChassis1uSensors
            self.lstURL4 = []
            self.nCount4 = 0
            self.nIndex4 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount4 = i[1]
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL4.append(iii[1])
                                    self.nIndex4 = self.nIndex4 + 1
                                    self.logger.debug("Next link=%s", self.lstURL1[self.nIndex1-1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/Sensors/[sensorNumber]
    def getChassis1uSensorsNumber(self, sensorNumber=0):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/Chassis/1u/Sensors/* Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        self.url = self.lstURL4[sensorNumber]
        self.method = "GET"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if (self.get_logVerbose() >= 2):
                    self.logger.debug("%s: %s", i[0], i[1])

    # Get Chassis/1u/Sensors/*
    def getChassis1uSensorsAll(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/Chassis/1u/Sensors/* Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 2):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers
    def getManagers(self):
        self.url = "/redfish/v1/Managers"
        self.method = "GET"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        # Get the next link of getManagers
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount2 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL2.append(iii[1])
                                self.nIndex2 += 1
                                self.logger.info(
                                    "Next link=%s", self.lstURL2[self.nIndex2-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0
    def getManagers0(self):
        for i in range(self.nCount2):
            if (self.lstURL2[i] != ''):
                self.url = self.lstURL2[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                self.lstURL3 = dict()
                self.nIndex3 = 0
                self.nCount3 = 0
                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 0):
                            self.logger.debug("%s: %s", i[0], i[1])
                        if (i[0] == "Oem"):
                            json_data2 = json.dumps(i[1])
                            for ii in i[1].items():
                                if (ii[0] == "Advantech"):
                                    for iii in ii[1].items():
                                        if (iii[0] == "AdvantechManager"):
                                            for iiii in iii[1].items():
                                                if (iiii[0] == "@odata.id"):
                                                    self.lstURL3[iii[0]] = iiii[1]
                                                    self.nIndex3 += 1
                                                    self.nCount3 += 1
                                                    self.logger.info(
                                                        "Next link=%s", iiii[1])
                        elif (i[0] in {"EthernetInterfaces", "LogServices", "NetworkProtocol", "SerialInterfaces", "HostInterfaces"}):
                            json_data2 = json.dumps(i[1])
                            for ii in i[1].items():
                                if (ii[0] == "@odata.id"):
                                    self.lstURL3[i[0]] = ii[1]
                                    self.nIndex3 += 1
                                    self.nCount3 += 1
                                    self.logger.debug("'%s' link=%s", i[0], ii[1])

    # Get Managers/0/Oem/Advantech/AdvantechManager
    def getManagers0OemAdvantechAdvantechManager(self):
        url = self.lstURL3["AdvantechManager"]
        if (url != ''):
            self.url = url
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            if (self.get_logVerbose() >= 0):
                self.logger.info("status=%d result=\n%s", response.status_code, result)

            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/EthernetInterfaces
    def getManagers0EthernetInterfaces(self):
        if (self.lstURL3["EthernetInterfaces"] != ''):
            self.url = self.lstURL3["EthernetInterfaces"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            # Get the next link(s) of EthernetInterfaces
            self.lstURL4 = []
            self.nCount4 = 0
            self.nIndex4 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount4 = i[1]
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL4.append(iii[1])
                                    self.nIndex4 = self.nIndex4 + 1
                                    self.logger.debug("Next link=%s", self.lstURL4[self.nIndex4-1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/EthernetInterfaces/*
    def getManagers0EthernetInterfacesAll(self):
        self.lstEtag4 = []
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (i[0] == "@odata.etag"):
                            self.lstEtag4.append(i[1])
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Patch Managers/0/EthernetInterfaces/*
    def patchManagers0EthernetInterfaces(self, ether_id=2, address=None, subnetmask="255.255.255.0", gateway="0.0.0.0"):
        if (ether_id < 1 or ether_id > self.nCount4):
            self.logger.warning(
                "ether_id(%d) is not valid. it shall between [1, %d]", ether_id, self.nCount4)
            return

        self.url = self.lstURL4[ether_id-1]
        self.method = "PATCH"
        self.logger.info("[%s %s]", self.method, self.url)
        payload = dict()
        data = dict()
        list_dict = []
        if address == None:
            # seed random number generator
            t = int( time.time() * 1000.0 )
            random.seed( ((t & 0xff000000) >> 24) +
                        ((t & 0x00ff0000) >>  8) +
                        ((t & 0x0000ff00) <<  8) +
                        ((t & 0x000000ff) << 24)   )
            # generate some integers
            r1 = randint(1, 254)
            data["Address"] = "10.234.147." + str(r1)
        else:
            data["Address"] = address
        data["SubnetMask"] = subnetmask
        data["Gateway"] = gateway
        list_dict.append(data)
        payload["IPv4Addresses"] = list(list_dict)
        self.payload = payload
        self.ether_id = ether_id
        self.logger.info('Setup BMC IP[%d]', self.ether_id)
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if (self.get_logVerbose() >= 1):
                    self.logger.debug("%s: %s", i[0], i[1])
        self.payload = None

    # Get Managers/0/LogServices
    def getManagers0LogServices(self):
        if (self.lstURL3["LogServices"] != ''):
            self.url = self.lstURL3["LogServices"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

        # Get the next link(s) of LogServices
        self.lstURL4 = []
        self.nCount4 = 0
        self.nIndex4 = 0
        if (response.status_code == 200):
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount4 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL4.append(iii[1])
                                self.nIndex4 = self.nIndex4 + 1
                                self.logger.info("Next link=%s", self.lstURL4[self.nIndex4-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/LogServices (Less info log)
    def getManagers0LogServicesLite(self):
        if (self.lstURL3["LogServices"] != ''):
            self.url = self.lstURL3["LogServices"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text

        # Get the next link(s) of LogServices
        self.lstURL4 = []
        self.nCount4 = 0
        self.nIndex4 = 0
        if (response.status_code == 200):
            self.logger.debug("status=%d result=\n%s", response.status_code, result)
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount4 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL4.append(iii[1])
                                self.nIndex4 = self.nIndex4 + 1
                                self.logger.debug("Next link=%s", self.lstURL4[self.nIndex4-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/LogServices/Log
    def getManagers0LogServicesLog(self):
        self.url = ''
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text

                if (response.status_code == 200):
                    self.logger.info("status=%d result=\n%s", response.status_code, result)
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if i[0] == 'Entries':
                            json_data2 = list(i[1].items())
                            if json_data2[0][0] == '@odata.id':
                                self.urlLogEntries = json_data2[0][1]
                                self.logger.info("Next link=%s", self.urlLogEntries)
                        else:
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/LogServices/Log (less info log)
    def getManagers0LogServicesLogLite(self):
        self.url = ''
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text

                if (response.status_code == 200):
                    self.logger.debug("status=%d result=\n%s", response.status_code, result)
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if i[0] == 'Entries':
                            json_data2 = list(i[1].items())
                            if json_data2[0][0] == '@odata.id':
                                self.urlLogEntries = json_data2[0][1]
                                self.logger.debug("Next link=%s", self.urlLogEntries)
                        else:
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/LogServices/Log/Entries (Enhanced for Advantech Redfish version >= 2.1.1 and backward compatible)
    def getManagers0LogServicesLogEntries(self):
        self.lstURL5 = []
        self.nCount5 = 0
        self.nIndex5 = 0
        while (self.urlLogEntries != ''):
            self.url = self.urlLogEntries
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            self.urlLogEntries = ''
            # Get the next link(s) of Entries
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount5 = i[1]
                        self.logger.info("Number of LogServicesLogEntries %d", self.nCount5)
                    elif i[0] == '@odata.nextLink':
                        self.urlLogEntries = i[1]
                        self.logger.info("More LogServicesLogEntries next link=%s", i[1])
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL5.append(iii[1])
                                    self.nIndex5 = self.nIndex5 + 1
                                    if (self.get_logVerbose() >= 2):
                                        self.logger.debug("Next link=%s", self.lstURL5[self.nIndex5-1])
                    else:
                        if (self.get_logVerbose() >= 2):
                            self.logger.debug("%s: %s", i[0], i[1])
        
    # Get Managers/0/LogServices/Log/Entries/*
    def getManagers0LogServicesLogEntriesAll(self):
        for i in range(self.nCount5):
            if (self.lstURL5[i] != ''):
                if (self.get_logVerbose() < 3):
                    if i < self.nCount5 - 1:
                        print("\rLogServicesLogEntries({})={}".format(
                            i+1, self.lstURL5[i]), end='')
                    else:
                        print("\rLogServicesLogEntries({})={}".format(
                            i+1, self.lstURL5[i]))
                self.url = self.lstURL5[i]
                self.method = "GET"
                self.payload = None
                response = self.rfRequest(False)
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 3):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/LogServices/Log/Entries (Only max to 50 entries for each query)
    def getManagers0LogServicesLogEntries50(self):
        self.lstURL5 = []
        self.nCount5 = 0
        self.nIndex5 = 0
        if (self.urlLogEntries != ''):
            self.url = self.urlLogEntries
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            self.urlLogEntries = ''
            # Get the next link(s) of Entries
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount5 = i[1]
                        self.logger.info("Number of LogServicesLogEntries %d", self.nCount5)
                    elif i[0] == '@odata.nextLink':
                        self.urlLogEntries = i[1]
                        self.bNextLogEntries = True
                        self.logger.info("More LogServicesLogEntries next link=%s", i[1])
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL5.append(iii[1])
                                    self.nIndex5 = self.nIndex5 + 1
                                    if (self.get_logVerbose() >= 2):
                                        self.logger.debug("Next link=%s", self.lstURL5[self.nIndex5-1])
                    else:
                        if (self.get_logVerbose() >= 2):
                            self.logger.debug("%s: %s", i[0], i[1])
        
    # Post Managers/0/LogServices/Log/Actions/LogService.Reset
    def postManagers0LogServicesLogActionsLogServiceReset(self):
        """ Clear the SEL log """
        self.url = "/redfish/v1/Systems/0/LogServices/Log/Actions/LogService.ClearLog" # For 3.1.0
        self.method = "POST"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None

        response = self.rfRequest(self)
        result = response.text
        if (self.get_logVerbose() >= 0):
            self.logger.info("status=%d result=\n%s", response.status_code, result)
        if (response.status_code == 200):
            self.logger.info("headers=%s]", response.headers)

    # Get Managers/0/NetworkProtocol
    def getManagers0NetworkProtocol(self):
        if (self.lstURL3["NetworkProtocol"] != ''):
            self.url = self.lstURL3["NetworkProtocol"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            # Get the next link(s) of getManagers0NetworkProtocol
            self.url = ''
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'HTTPS':
                        self.url = i[1]["Certificates"]["@odata.id"]
                        self.logger.debug("Next link=%s", self.url)
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/NetworkProtocol/HTTPS/Certificates
    def getManagers0NetworkProtocolHTTPSCertificates(self):
        if (self.url != ''):
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            # Get the next link(s) of getManagers0NetworkProtocolHTTPSCertificates
            self.lstURL5 = []
            self.nCount5 = 0
            self.nIndex5 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount5 = i[1]
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL5.append(iii[1])
                                    self.nIndex5 = self.nIndex5 + 1
                                    self.logger.debug("Next link=%s", self.lstURL5[self.nIndex5-1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/NetworkProtocol/HTTPS/Certificates/*
    def getManagers0NetworkProtocolHTTPSCertificatesAll(self):
        for i in range(self.nCount5):
            if (self.lstURL5[i] != ''):
                self.url = self.lstURL5[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            if (i[0] in {"CertificateString"}):
                                self.logger.debug("%s:\n%s", i[0], i[1])
                            else:
                                self.logger.debug("%s: %s", i[0], i[1])


    # Get Managers/0/SerialInterfaces
    def getManagers0SerialInterfaces(self):
        if (self.lstURL3["SerialInterfaces"] != ''):
            self.url = self.lstURL3["SerialInterfaces"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            # Get the next link(s) of EthernetInterfaces
            self.lstURL4 = []
            self.nCount4 = 0
            self.nIndex4 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount4 = i[1]
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL4.append(iii[1])
                                    self.nIndex4 = self.nIndex4 + 1
                                    self.logger.debug("Next link=%s", self.lstURL4[self.nIndex4-1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/SerialInterfaces/*
    def getManagers0SerialInterfacesAll(self):
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/HostInterfaces
    def getManagers0HostInterfaces(self):
        if (self.lstURL3["HostInterfaces"] != ''):
            self.url = self.lstURL3["HostInterfaces"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            # Get the next link(s) of HostInterfaces
            self.lstURL4 = []
            self.nCount4 = 0
            self.nIndex4 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount4 = i[1]
                    elif i[0] == 'Members':
                        json_data2 = dict(enumerate(i[1]))
                        for ii in json_data2.items():
                            for iii in ii[1].items():
                                if iii[0] == '@odata.id':
                                    self.lstURL4.append(iii[1])
                                    self.nIndex4 = self.nIndex4 + 1
                                    self.logger.debug("Next link=%s", self.lstURL4[self.nIndex4-1])
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/HostInterfaces/*
    def getManagers0HostInterfacesAll(self):
        for i in range(self.nCount4):
            if (self.lstURL4[i] != ''):
                self.url = self.lstURL4[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Post Managers/0/Actions/Manager.Reset
    def postManagers0ActionsManagerReset(self, ResetType="ForceRestart"):
        self.url = "/redfish/v1/Managers/0/Actions/Manager.Reset"
        self.method = "POST"
        self.logger.info("[%s %s]", self.method, self.url)
        data = dict()
        data['ResetType'] = ResetType
        self.payload = data
        self.logger.info('BMC ForceRestart')
        response = self.rfRequest()
        result = response.text
        if (self.get_logVerbose() >= 0):
            self.logger.info("status=%d result=\n%s", response.status_code, result)

        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if (self.get_logVerbose() >= 1):
                    self.logger.debug("%s: %s", i[0], i[1])
        self.payload = None

    # Get Registries
    def getRegistries(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/Registries Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        self.url = "/redfish/v1/Registries"
        self.method = "GET"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        # Get the next link(s) of Registries
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount2 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL2.append(iii[1])
                                self.nIndex2 += 1
                                self.logger.debug("Next link=%s", self.lstURL2[self.nIndex2-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Registries/*
    def getRegistriesAll(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/Registries/* Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        for i in range(self.nCount2):
            if (self.lstURL2[i] != ''):
                self.url = self.lstURL2[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if i[0] == 'Location':
                            json_data2 = dict(enumerate(i[1]))
                            for ii in json_data2.items():
                                for iii in ii[1].items():
                                    if iii[0] == 'Uri':
                                        self.url = iii[1]
                                        self.logger.info(
                                            "Next link=%s", self.url)
                            if self.url != '':
                                self.method = "GET"
                                self.logger.info("[%s %s]", self.method, self.url)
                                self.payload = None
                                response = self.rfRequest()
                                result = response.text
                                #if (self.get_logVerbose() >= 1):
                                self.logger.info("status=%d result=\n%s", response.status_code, result)

                        else:
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", i[0], i[1])

    # Get JsonSchemas
    def getJsonSchemas(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/JsonSchemas Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        self.url = "/redfish/v1/JsonSchemas"
        self.method = "GET"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        # Get the next link(s) of JsonSchemas
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount2 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL2.append(iii[1])
                                self.nIndex2 += 1
                                self.logger.debug("Next link=%s", self.lstURL2[self.nIndex2-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get JsonSchemasAll
    def getJsonSchemasAll(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/JsonSchemas/* Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        for i in range(self.nCount2):
            if (self.lstURL2[i] != ''):
                self.url = self.lstURL2[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if i[0] == 'Location':
                            json_data2 = dict(enumerate(i[1]))
                            for ii in json_data2.items():
                                for iii in ii[1].items():
                                    if iii[0] == 'Uri':
                                        self.url = iii[1]
                                        self.logger.info(
                                            "Next link=%s", self.url)
                            if self.url != '':
                                self.method = "GET"
                                self.logger.info("[%s %s]", self.method, self.url)
                                self.payload = None
                                response = self.rfRequest()
                                result = response.text
                                self.logger.info("status=%d result=\n%s", response.status_code, result)
                        elif i[0] == 'Oem':
                            json_data2 = i[1]["Advantech"]
                            for ii in json_data2.items():
                                if ii[0] == "XmlMetadataLocation":
                                    self.url = ii[1]
                                    self.logger.info("Next link=%s", self.url)
                            if self.url != '':
                                self.method = "GET"
                                self.logger.info("[%s %s]", self.method, self.url)
                                self.payload = None
                                response = self.rfRequest()
                                result = response.text
                                if (self.get_logVerbose() >= 0):
                                    myxml = None
                                    myxml = xml.dom.minidom.parseString(result)
                                    xml_pretty_str = myxml.toprettyxml()
                                    self.logger.info(xml_pretty_str)
                        else:
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", i[0], i[1])

    # Get TaskService
    def getTaskService(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/TaskService Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        self.url = "/redfish/v1/TaskService"
        self.method = "GET"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if (i[0] == "Tasks"):
                    self.url = i[1]["@odata.id"]
                    self.logger.debug("Next Link=%s", self.url)

    # Get TaskService/Tasks
    def getTaskServiceTasks(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/TaskService/Tasks Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        if (self.url != ''):
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Members@odata.count':
                        self.nCount2 = i[1]
                    elif i[0] == 'Members':
                        json_data2 = json.loads(json.dumps(i[1]))
                        self.nIndex2 = 0
                        for ii in json_data2:
                            self.lstURL2.append(ii["@odata.id"])
                            self.logger.info(
                                "Task(%d) link=%s", self.nIndex2, self.lstURL2[self.nIndex2])
                            self.nIndex2 += 1
                    else:
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get TaskService/Tasks/* or TaskService/Tasks/[task_id]
    def getTaskServiceTasksAll(self, index=-1):
        if index == -1:
            for i in range(self.nCount2):
                if (self.lstURL2[i] != ''):
                    self.url = self.lstURL2[i]
                    self.method = "GET"
                    self.logger.info("[%s %s]", self.method, self.url)
                    self.payload = None
                    response = self.rfRequest()
                    result = response.text
                    self.logger.info("status=%d result=\n%s", response.status_code, result)
                    if (response.status_code == 200):
                        json_data = json.loads(result)
                        for i in json_data.items():
                            if (self.get_logVerbose() >= 1):
                                self.logger.debug("%s: %s", i[0], i[1])
        else:
            if (self.lstURL2[index] != ''):
                self.url = self.lstURL2[index]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)
                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get TaskService/Tasks/[task_id] until it is completed
    def getTaskServiceTasksCompletion(self, task_id=0):
        if (self.authToken and task_id >= 0 and task_id < self.nCount2):
            if (self.lstURL2[task_id] != ''):
                try:
                    while True:
                        self.url = self.lstURL2[task_id]
                        self.method = "GET"
                        self.logger.debug("[%s %s]", self.method, self.url)
                        self.payload = None
                        response = self.rfRequest()
                        result = response.text
                        self.logger.debug("status=%d result=\n%s", response.status_code, result)
                        if (response.status_code in {200, 202}):
                            json_data = json.loads(result)
                            for i in json_data.items():
                                if i[0] == "PercentComplete":
                                    self.logger.info("HTTP status=%d {%s: %s} (CTRL-C to stop)", response.status_code, i[0], i[1])
                                    cmd = "ipmitool -I lanplus -H " + bmcObject.hostname + " -U " + bmcObject.username + " -P " + bmcObject.password + " hpm check | grep -i bios"
                                    os.system(cmd)
                                elif i[0] == "Messages":
                                    json_data2 = dict(enumerate(i[1]))
                                    for ii in json_data2.items():
                                        for iii in ii[1].items():
                                            if iii[0] == 'Message':
                                                self.logger.info("Message=%s", iii[1])
                                            elif iii[0] == 'MessageArgs':
                                                self.logger.info("MessageArgs=%s", iii[1])
                                            else:
                                                self.logger.debug("%s=%s", iii[0], iii[1])
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("Press Ctrl-C to terminate while statement")
                    pass

    # Delete TaskService/Tasks/[task_id]
    def delTaskServiceTasksAll(self, task_id=0):
        if (self.authToken and task_id >= 0 and task_id < self.nCount2 and self.lstURL2[task_id] != ''):
            self.url = self.lstURL2[task_id]
            self.method = "DELETE"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)
            if response.status_code not in [200, 202, 204]:
                self.logger.info("Invalid task: %s", self.url)
            else:
                self.logger.info("Task: %s has been deleted", self.url)

    # Get UpdateService
    def getUpdateService(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/UpdateService Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        self.url = "/redfish/v1/UpdateService"
        self.method = "GET"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if (i[0] == "FirmwareInventory"):
                    self.url = i[1]["@odata.id"]
                    self.logger.debug("FirmwareInventory Link=%s", self.url)
                elif i[0] == "HttpPushUri":
                    self.urlFWUpdate = i[1]
                    self.logger.info("FWUpdate Link=%s", self.urlFWUpdate)

    # Get UpdateService/FirmwareInventory
    def getUpdateServiceFirmwareInventory(self):
        if (self.get_redfishVersion() < "2.0.0"):
            self.logger.warning(
                "/redfish/v1/UpdateService/FirmwareInventory Not Implemented in Advantech redfish version %s]", self.get_redfishVersion())
            return
        self.url = "/redfish/v1/UpdateService/FirmwareInventory"
        self.method = "GET"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        self.lstURL2 = []
        self.nCount2 = 0
        self.nIndex2 = 0
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Members@odata.count':
                    self.nCount2 = i[1]
                elif i[0] == 'Members':
                    json_data2 = dict(enumerate(i[1]))
                    for ii in json_data2.items():
                        for iii in ii[1].items():
                            if iii[0] == '@odata.id':
                                self.lstURL2.append(iii[1])
                                self.nIndex2 += 1
                                self.logger.debug("Next link=%s", self.lstURL2[self.nIndex2-1])
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get UpdateService/FirmwareInventory/*
    def getUpdateServiceFirmwareInventoryAll(self):
        self.lstURL3 = dict()
        self.nCount3 = 0
        self.nIndex3 = 0
        for i in range(self.nCount2):
            if (self.lstURL2[i] != ''):
                self.url = self.lstURL2[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if i[0] == "Name":
                            strName = i[1]
                        elif i[0] == "Version":
                            strVersion = i[1]
                            #self.logger.info("Firmware=%10s: Version=%10s", strName, strVersion)
                            self.lstURL3[strName] = strVersion
                            self.nCount3 += 1
                            self.nIndex3 += 1
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])
        for i in self.lstURL3.items():
            self.logger.info("%-12s: Version=%10s", i[0], i[1])

    # post UpdateService/FWUpdate
    def postUpdateServiceFWUpdate(self):
        try:
            while True:
                filename = input("Please enter the filename to update (CTRL-C to cancel):")
                if os.path.isfile(filename):
                    print("The file is exist")
                    strFilename = os.path.basename(filename)
                    strFullpath = os.path.abspath(filename)
                    break
                else:
                    print("The file is not exist. Please try again.")
        except KeyboardInterrupt:
            print("Press Ctrl-C to terminate while statement")
            pass

        #self.strFWPath = "/Users/ch.huang789/redfish_advantech_library/examples/SKY7223D_bios_customized_02_34.img"
        self.strFWPath = strFullpath
        strFilename = os.path.basename(self.strFWPath)
        strFullpath = os.path.abspath(strFilename)
        self.url = self.urlFWUpdate
        self.method = "POST"
        self.logger.info("[%s %s]", self.method, self.url)

        body = open(self.strFWPath, 'rb')
        mp_encoder = MultipartEncoder(
            fields={
                'file': (strFilename, body, 'application/octet-stream')
                #'file': (strFilename, body, 'application/octet-stream'),
                #'upload[active]': 'True', # new line for progress bar
                #'upload[title]': 'Title From Python - Monitored with bar' # new line for progress bar
            }
        )

        #callback = create_callback(mp_encoder) # new line for progress bar
        #payload = MultipartEncoderMonitor(mp_encoder, callback) # new line for progress bar

        headers = {
                'Accept': '*/*',
                'Expect': '100-continue',
                'X-Auth-Token': self.authToken, 
                'Content-Type': mp_encoder.content_type
        }

        self.logger.info("Upgrade '%s' in progress and take times. Please stay tuned.", strFilename)
        response = self.session.post(
           self.strProtocol + self.hostname + self.url, data=mp_encoder, headers=headers, verify=False)
        # Replace by the next 2 lines for progress bar
        #response = self.session.post(
        #   self.strProtocol + self.hostname + self.url, data=payload, headers=headers, verify=False)
        
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        if (response.status_code in {200, 201, 202}):
            json_data = json.loads(result)
            for i in json_data.items():
                if (self.get_logVerbose() >= 1):
                    self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/CertificateService
    def getManagers0CertificateService(self):
        self.url = "/redfish/v1/CertificateService"
        self.method = "GET"
        self.logger.info("[%s %s]", self.method, self.url)
        self.payload = None
        response = self.rfRequest()
        result = response.text
        self.logger.info("status=%d result=\n%s", response.status_code, result)

        # Get the next link(s) and action link(s) of CertificateService
        self.lstURL2 = dict()
        self.nCount2 = 0
        self.nIndex2 = 0
        if (response.status_code == 200):
            json_data = json.loads(result)
            for i in json_data.items():
                if i[0] == 'Actions':
                    json_data2 = i[1]
                    for ii in json_data2.items():
                        self.lstURL2["target"] = ii[1]["target"]
                        self.logger.info("Next link=%s", self.lstURL2["target"])
                        self.nCount2 += 1
                        self.nIndex2 += 1
                        self.lstURL2["@Redfish.ActionInfo"] = ii[1]["@Redfish.ActionInfo"]
                        self.logger.info("Next link=%s", self.lstURL2["@Redfish.ActionInfo"])
                        self.nCount2 += 1
                        self.nIndex2 += 1
                elif i[0] == 'CertificateLocations':
                    self.lstURL2["@odata.id"] = i[1]["@odata.id"]
                    self.logger.info("Next link=%s", self.lstURL2["@odata.id"])
                    self.nCount2 += 1
                    self.nIndex2 += 1
                else:
                    if (self.get_logVerbose() >= 1):
                        self.logger.debug("%s: %s", i[0], i[1])

    # Get Managers/0/CertificateService/CertificateLocations
    def getManagers0CertificateServiceCertificateLocations(self):
        self.url = self.lstURL2["@odata.id"]
        if self.url != "":
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

            # Get the next link(s) of CertificateService/CertificateLocations
            self.lstURL3 = []
            self.nCount3 = 0
            self.nIndex3 = 0
            if (response.status_code == 200):
                json_data = json.loads(result)
                for i in json_data.items():
                    if i[0] == 'Links':
                        json_data2 = (i[1])
                        for ii in json_data2.items():
                            if ii[0] == 'Certificates@odata.count':
                                self.nCount3 = ii[1]
                            elif ii[0] == 'Certificates':
                                if (self.get_logVerbose() >= 1):
                                    self.logger.debug("%s: %s", ii[0], ii[1])
                                json_data3 = dict(enumerate(ii[1]))
                                for iii in json_data3.items():
                                    self.lstURL3.append(iii[1]["@odata.id"])
                                    self.nIndex3 += 1
                                    self.logger.info("Next link=%s", self.lstURL3[self.nIndex3-1])

    # Get /redfish/v1/Managers/0/NetworkProtocol/HTTPS/Certificates/*
    def getManagers0CertificateServiceCertificateLocationsAll(self):
        for i in range(self.nCount3):
            if (self.lstURL3[i] != ''):
                self.url = self.lstURL3[i]
                self.method = "GET"
                self.logger.info("[%s %s]", self.method, self.url)
                self.payload = None
                response = self.rfRequest()
                result = response.text
                self.logger.info("status=%d result=\n%s", response.status_code, result)

                if (response.status_code == 200):
                    json_data = json.loads(result)
                    for i in json_data.items():
                        if (self.get_logVerbose() >= 1):
                            self.logger.debug("%s: %s", i[0], i[1])

    # Get /redfish/v1/CertificateService/CertificateService.ReplaceCertificateActionInfo
    def getManagers0CertificateServiceReplaceCertificateActionInfo(self):
        if (self.lstURL2["@Redfish.ActionInfo"] != ''):
            self.url = self.lstURL2["@Redfish.ActionInfo"]
            self.method = "GET"
            self.logger.info("[%s %s]", self.method, self.url)
            self.payload = None
            response = self.rfRequest()
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)

    def postManagers0CertificateServiceReplaceCertificate(self):
        if (self.lstURL2["target"] != ''):
            self.url = self.lstURL2["target"]
            self.method = "POST"
            data = dict()
            data['CertificateString'] = "-----BEGIN CERTIFICATE-----\nMIIGeTCCBGGgAwIBAgIRAO3mrXCSuz9y2Xo3qHueT3UwDQYJKoZIhvcNAQEMBQAw\nSzELMAkGA1UEBhMCQVQxEDAOBgNVBAoTB1plcm9TU0wxKjAoBgNVBAMTIVplcm9T\nU0wgUlNBIERvbWFpbiBTZWN1cmUgU2l0ZSBDQTAeFw0yMTA4MDcwMDAwMDBaFw0y\nMTExMDUyMzU5NTlaMCAxHjAcBgNVBAMTFXNreTcyMjMtYm1jLmNpb3Qud29yazCC\nASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANHUey70LoPgdAFNCRRZu0qQ\nTHwyrCLsMdG0HMjTFvGlSVGaICIgjHu1TfznDlTSD3UGetvlOhpY0wQA/Fhm0BKM\nkXSl+TulNqYMjSkqDomvdK4xISgEgn3TRw2+oZ24J/WfjLBpvdO0w5g9YvzLaHlj\nX2O/pcfds53gjpt2MeW36lHv1yk+oiASDM0F/XOSWaqQzETq17Yfa8wPGzzEGsfy\nAbQJQ0jrG44x/nKhEXIRKCWss+1qADCqEUEhCtQcp2gSkQq2JOccSjGLlOFJ34Ni\n7i3HI54JCn/i8MY4yRidTqEZasNjhN33zQeCkq5alGjyInc56yk0w3AVcuw9aFEC\nAwEAAaOCAoEwggJ9MB8GA1UdIwQYMBaAFMjZeGii2Rlo1T1y3l8KPty1hoamMB0G\nA1UdDgQWBBRpSncl9vJaH7gya9uDr6gtpaDUZTAOBgNVHQ8BAf8EBAMCBaAwDAYD\nVR0TAQH/BAIwADAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwSQYDVR0g\nBEIwQDA0BgsrBgEEAbIxAQICTjAlMCMGCCsGAQUFBwIBFhdodHRwczovL3NlY3Rp\nZ28uY29tL0NQUzAIBgZngQwBAgEwgYgGCCsGAQUFBwEBBHwwejBLBggrBgEFBQcw\nAoY/aHR0cDovL3plcm9zc2wuY3J0LnNlY3RpZ28uY29tL1plcm9TU0xSU0FEb21h\naW5TZWN1cmVTaXRlQ0EuY3J0MCsGCCsGAQUFBzABhh9odHRwOi8vemVyb3NzbC5v\nY3NwLnNlY3RpZ28uY29tMIIBBAYKKwYBBAHWeQIEAgSB9QSB8gDwAHYAfT7y+I//\niFVoJMLAyp5SiXkrxQ54CX8uapdomX4i8NcAAAF7IG7pHQAABAMARzBFAiEAp8xP\nvgi6xCLIew61BIuODTQTYbWZjsDK+pwLRhc6AwUCIGFLHTzK7fuomX2o10lO46zD\nZZt6sCj8sRzRVzaUixnSAHYARJRlLrDuzq/EQAfYqP4owNrmgr7YyzG1P9MzlrW2\ngagAAAF7IG7pFQAABAMARzBFAiAG22Try1pvDVLm+lFh2cCxWQ5Sc3ZTfMO0xVfW\nioHF1AIhAOoO5ff0LdumkSAvwX/Duh7b04qUo6EktNTvQqQMC2bVMCAGA1UdEQQZ\nMBeCFXNreTcyMjMtYm1jLmNpb3Qud29yazANBgkqhkiG9w0BAQwFAAOCAgEAau2g\np5yLSd/PFy+f5tiOTi28XynoVeWBwm06GEHYrOAfMTxZAg3TmqcykpNLunnsA24t\n+Is/+2wvolB2fUstORA6mS8HASB/Z+Hy4PPDmJ6wtZ8Gj7c1YEHU66s3QNoUOr29\nhkB40WRdXBeIDy3AFCCtBmcYMWjOsyUhpklSfzCfS0WYz1hpvj9fwDfoAqS91K7V\nMWw4kZ/SCWCp5eL1Vh/MZnUKJBrjp17QnJdJiCvIvW5G08qt/vjUVIF+65Kw4dLf\nS8QnUEumSoRMgUBaH+CKtejPrDA71oqURbAgiIGBQvY31zQ7MjjL34ShHkvH+JRq\nvxCjbgah0RCFo9hJarxSdEwRIJkFNBGYpwSrkzWjpSEedoymO8Ycv9SiOB2a/h0+\n4LA+jB4bZXXNoq1ZAZ10rA5KjOvpOTlhy2bZQpMNsz37I+TS2POw0+oT2RLfNqJF\nHtD+ov/roV8argSJgfFctobqhWwSd/ESDIjb/sFSqlynSFOSIzoGPYHAyU76spz0\nE9g9BA7S5gyIszQ94C/bBwEjpJr3XhEr461pXyQic7aIZT1EXSqjtsqHXmPX/XQf\n+4qj+d5YVoEYbEHOYX0w647nwfphcmleLlCkVSebBHv7Bf7xD3nrLD/BOYWLKm5F\nUvL7I4WLxVnFqd1N4zl27DRTHa5UQ4QN0xsmZBI=\n-----END CERTIFICATE-----\n-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0dR7LvQug+B0AU0JFFm7SpBMfDKsIuwx0bQcyNMW8aVJUZog\nIiCMe7VN/OcOVNIPdQZ62+U6GljTBAD8WGbQEoyRdKX5O6U2pgyNKSoOia90rjEh\nKASCfdNHDb6hnbgn9Z+MsGm907TDmD1i/MtoeWNfY7+lx92zneCOm3Yx5bfqUe/X\nKT6iIBIMzQX9c5JZqpDMROrXth9rzA8bPMQax/IBtAlDSOsbjjH+cqERchEoJayz\n7WoAMKoRQSEK1BynaBKRCrYk5xxKMYuU4Unfg2LuLccjngkKf+LwxjjJGJ1OoRlq\nw2OE3ffNB4KSrlqUaPIidznrKTTDcBVy7D1oUQIDAQABAoIBAEM55WGMwB5mWiRU\njxUjDpt8EdU00uu5ati58QLyhoZTI2Nukt78OKYl11+wk2nfhy5CLjinf28TiD/f\nJPoZro5S1QNfbbOLYi/fE5bdr5yzRxnMCchtcXVorHod2l/SsZLDVGrs5fGfF49+\nE2nUrZs+mEA4FaAsSrDJUkdCngfvyJUM9PIDT4lUO39mjrTLIFa4notyF0HuzrbV\nB6kFpzhYqi4ngIHa4pJVOtQV+KJHiVc/FpuWz6YcuDbfhzwn7COOUP2pTEfrjWii\nVsck6lRq2Nmsaokvl1SQ4tGhufFX85dhv27qwE49TT1bbiURGRsAIce9mO7TmYuE\ngx7pnQUCgYEA/eFCTLrYP44YD5gdPoRRmhIwXxMevYrDNnJ596MQ/8ChxtcrzoAM\nr6Y87dpdHDKtGSuzF/U79+B2vILDJv6jxl3zNvTGA6q2B0tGg7MfMrm+NfWXON8m\nZMJRh6KJbOIKHB9wuUKeAgmzh9yK7nCItikQ8nIgUVe+qaEDKlSiPZsCgYEA05UN\nitV+hNjQ7YUPZNRunSqP1r3j6tCD4tydjtFwSg3QMWp+ZcirQfyQhpySXpwWEcum\nzS5hnWaRmOcwfz1fUhFYzqGiBvWEFFjqkko/xh55iBDprNBkTiyQNg9UXNio3RiO\n0uCQQ9Hk3Dis6MrR4NVEmwhWqdiGvRkKeQbWxoMCgYBKfXZzhvr+ItYCdVJXToGW\n4DFbJAQH/xfp+Mq6kxjgwYd2DRooW7/dJbyI2WIqbOAHG6BPrj+rKiwMgZ166onp\nIRXEkSssVkFUgIyvBbZorsEVmfqF0Eu2kqFTV6hUzznCKKNtaBNua6RGf7ov3crv\nD7uON1guJb2mjbydBfoYcwKBgQDJA/txw5QIMtWMU7ZkXU8aEq3Fn3NCTAiBKIio\nf2LneGgsCrk7ioLqlkHZIjgNms186rb2iPJE0IXTdxIkUPKWzdRJvFZrtiZeDnwN\nsG0WlS1xkF/xx6sEemIoejf0XgNQy1wmDSQCyw9cCpx8LvVnXjdn82wiwYyBa6D/\nivfScQKBgC0kKf/Bn+ZwE4tIgOTrRZ19yU6GnFopJy5iOk0lNI8xyPNofFA+AUbV\nr6lgX+DMdusXOY7CPSQuJNY00eYdFLa2A/LGlqqbPj1R/SQcYjE/uYvXtJOfJNke\naJ3iALxzThzrLRt5IZZNN72MdZ5dbffuJNo4YzNXEucpO24IzJyH\n-----END RSA PRIVATE KEY-----\n"
            data['CertificateType'] = "PEM"
            data['CertificateUri'] = "/redfish/v1/Managers/0/NetworkProtocol/HTTPS/Certificates/0"
            self.payload = data
            self.logger.info("[%s %s]", self.method, self.url)
            response = self.rfRequest()
            self.payload = None
            result = response.text
            self.logger.info("status=%d result=\n%s", response.status_code, result)
### End of advantech_redfish ###