"""

"""
import typing
import sys

import aiohttp
import datetime
from bs4 import BeautifulSoup


from . import base


class AddUPIError(base.BusError):
    pass


class Sensor(base.Sensor):
    """
    A sensor connected to an ADCON network. Any object of the class "DEVICE"
    can be used as a sensor
    """

    def __init__(self, id, name=None, values=None, **kwargs):
        """
        Creates the sensor
        :param id: Id of the DEVICE
        :param name:
        """
        self.id = id
        self.name = name
        if values:
            self.valuefactories = [base.ValueFactory(**v) for v in values]
        else:
            self.valuefactories = []

        self.extradata = kwargs

    def __str__(self):
        return '{} (id={}) ({} values)'.format(self.name, self.id, len(self.valuefactories))
     
    def __repr__(self):
        return 'addupi.Sensor(id={}, name={})'.format(self.id, self.name)

    def __asdict__(self)->dict:
        res = self.extradata.copy()
        res.update(dict(id=self.id, name=self.name, values=[]))
        for vf in self.valuefactories:
            res['values'].append(vf.__asdict__())
        return res


class Bus(base.Bus):
    def __init__(self, url, user=None, password=None, sensors=None, **kwargs):
        self.url = url
        self.session = None
        self.user = user
        self.password = password
        self.extradata = kwargs
        if sensors:
            self.sensors = [Sensor(**s) for s in sensors]
        else:
            self.sensors = []

    def __asdict__(self):
        res = self.extradata.copy()
        res.update(dict(url=self.url, user=self.user, password=self.password))
        res['module'] = __name__
        res['sensors'] = []
        for s in self.sensors:
            res['sensors'].append(s.__asdict__())
        return res

    def __str__(self):
        return 'ADCONhost on {} with {} sensors'.format(self.url, len(self.sensors))

    async def __aenter__(self):
        await self.login()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.logout()

    def makesensor(self, id: str, name=None, values=None, **kwargs):
        """
        Create a sensor on this bus
        :param id: id of the DEVICE node (str)
        :param name: Name of the DEVICE node
        :param values: List of dict, describing valuefactories
        :param kwargs: Extra data to describe the sensor
        :return: The created AddUPISensor
        """
        s = Sensor(self, id, name)
        if values:
            errors = []
            for v in values:
                try:
                    s.valuefactories[v['id']] = base.ValueFactory(**v)
                except Exception as e:
                    errors.append(e)
                else:
                    errors.append(None)
            # TODO: Do something about the errors
        self.sensors.append(s)
        return s

    async def read(self, **params) ->(BeautifulSoup, str):
        """
        Reads from self.url using the params and returns the souped response
        :param params: A dictionary of parameters
        :return: a BeautifulSoup of the response
        """
        if self.session and 'session-id' not in params:
            params['session-id'] = self.session
        async with aiohttp.ClientSession() as session:
            # GET response to function
            async with session.get(self.url, params=params) as r:
                # check response

                # status check
                if r.status // 100 > 2:
                    raise AddUPIError('AddUPI connection failed, got status {} from {}'.format(r.status, r.url))
                # get text
                text = await r.text()
                # parse text
                try:
                    soup = BeautifulSoup(text, 'xml')
                except Exception as e:
                    raise AddUPIError('AddUPI connection failed, could not parse response from {}\nResponse:\n{}'
                                      .format(r.url, text)) from e
                # check for response
                if not soup.response:
                    raise AddUPIError('AddUPI connection failed, no response tag from {}, got instead:\n{}'
                                      .format(r.url, soup.prettify()))
                # check for error
                if error := soup.response.find('error', recursive=False):
                    raise AddUPIError('AddUPI connection failed got Error code {code}: {msg} on {url}'
                                      .format(url=r.url, **error.attrs))
                return soup, r.url

    async def login(self, timeout=None):
        """
        Does a login to the ADCON server using the configured username and password
        :param timeout: A timeout for the session in seconds
        :return: A new session id
        """
        params = dict(function='login', user=self.user, passwd=self.password)
        if timeout:
            params['timeout'] = timeout
        soup, url = await self.read(**params)
        self.session = str(soup.response.result.text.strip())
        if not self.session or self.session=='None':
            raise AddUPIError('Tried to login but got not a session id from {} Response:\n{}'.format(url, soup))
        return self.session

    async def logout(self):
        """
        Finishes the current session
        """
        if not self.session:
            raise AddUPIError("AddUPI is not connected, can't logout")
        params = {'function': 'logout', 'session-id': self.session}
        await self.read(**params)
        self.session = None

    async def configsensor(self, sensorid) -> Sensor:
        """
        Gets the configuration of a sensor from the getconfig function of the AddUPI protocol
        :param sensorid: Id of the sensor
        :return: The configured sensor
        """
        if not self.session:
            raise AddUPIError('addupi.Bus.configsensor: No log in session available')
        soup, url = await self.read(function='getconfig', id=sensorid, depth=1)
        sensor = soup.response.node
        if not sensor or sensor['id'] != str(sensorid):
            raise AddUPIError('AddUPI asked for sensor #{id} with {url} but got:\n{text}'
                              .format(id=sensorid, url=url, text=soup.prettify()))
        if sensor['class'] != 'DEVICE':
            raise AddUPIError('{} has not the class DEVICE'.format(sensor))

        asensor = Sensor(sensorid, sensor['name'])
        for n in sensor.nodes.find_all('node'):
            if n['class'] == 'TAG':
                asensor.valuefactories.append(base.ValueFactory(**n.attrs))
        self.sensors.append(asensor)
        return asensor

    async def read_all(self) -> typing.List[base.Value]:
        if not self.session:
            raise AddUPIError('addupi.Bus.read_all: No log in session available')
        values = []
        for sensor in self.sensors:
            s_values = await self.readsensor(sensor)
            values.extend(s_values)
        return values

    async def readsensor(self, sensor: Sensor, fromdate=None, slots=None) -> typing.List[base.Value]:
        """
        Reads a sensor
        :param sensor: AddUPISensor to read
        :return: list of values (Value)
        """
        if not self.session:
            raise AddUPIError('addupi.Bus.read_all: No log in session available')

        params = {'function': 'getdata',
                  'id': sensor.id}
        if fromdate:
            params['date'] = fromdate.strftime('%Y%m%dT%H:%M:%S')
            params['slots'] = slots or 1000

        soup, url = await self.read(**params)
        # Check returned node_id
        nodes = soup.response.find_all('node')
        # Make an empty value list
        values = []
        # Make a dict to relate id's with valuefactory numbers
        vfdict = dict((str(vf.id), i) for i, vf in enumerate(sensor.valuefactories))
        for node in nodes:
            # Get first value with absolute date
            node_id = node['id']
            if node_id in vfdict:
                if error := node.find('error', recursive=False):
                    code = error.attrs.get('code')
                    msg = error.attrs.get('msg')
                    print(f'{datetime.datetime.now()}: Addupi warning at node {node_id}: #{code}: {msg} ({url})')
                else:
                    for v_elem in node('v', recursive=False):
                        t_str = v_elem['t']
                        try:
                            t = datetime.datetime.strptime(t_str, '%Y%m%dT%H:%M:%S')
                        except ValueError:
                            if v_elem['t'].startswith('+'):
                                t += datetime.timedelta(seconds=int(v_elem['t']))
                            else:
                                raise
                        v = float(v_elem.string)
                        # Check for relative time
                        i = vfdict[node_id]
                        values.append(sensor.valuefactories[i](v, t))


        return values
