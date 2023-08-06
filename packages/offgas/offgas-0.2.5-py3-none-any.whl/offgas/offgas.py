""" Class for reading data from CO2 monitor.

    E-mail: aerk@berkeley.edu
"""
try:
    import hid
except AttributeError as e:
    if 'windll' in e.message:
        raise ImportError(('Import failed with an error "AttributeError: %s". '
                           'Possibly there''s a name conflict. Please check if '
                           'library "hid" is instlled and if so - uninstall it, '
                           'keeping only "hidapi".' % str(e)))
    else:
        raise
import datetime as dt
from datetime import datetime
import sched, time
import matplotlib.pyplot as plt
from pathlib import Path
from contextlib import contextmanager
import threading
import time
import os

plt = None  # To be imported on demand only
try:
    import pandas as pd
except ImportError:
    pd = None

_CO2MON_HID_VENDOR_ID = 0x04d9
_CO2MON_HID_PRODUCT_ID = 0xa052
_CO2MON_MAGIC_WORD = b'Htemp99e'
_CO2MON_MAGIC_TABLE = (0, 0, 0, 0, 0, 0, 0, 0)

_CODE_END_MESSAGE = 0x0D
_CODE_CO2 = 0x50
_CODE_TEMPERATURE = 0x42

_COLORS = {'r': (0.86, 0.37, 0.34),
           'g': (0.56, 0.86, 0.34),
           'b': 'b'}

CO2_HIGH = 1200
CO2_LOW = 800


#############################################################################
def now():
    return dt.datetime.now().replace(microsecond=0)


#############################################################################
def list_to_longint(x):
    return sum([val << (i * 8) for i, val in enumerate(x[::-1])])


#############################################################################
def longint_to_list(x):
    return [(x >> i) & 0xFF for i in (56, 48, 40, 32, 24, 16, 8, 0)]


#############################################################################
def convert_temperature(val):
    """ Convert temperature from Kelvin (unit of 1/16th K) to Celsius
    """
    return val * 0.0625 - 273.15

class NonUniqueNameError(RuntimeError):
   def __init__(self):
      self.message = 'ERROR! You must initialize with a unique name, ie. Indican9000'
      print(self.message)
#############################################################################
# Class to operate with CO2 monitor
#############################################################################
class CO2monitor:

    def __init__(self, run_name):
        """ Initialize the CO2monitor object and retrieve basic HID info.
        """
        # set up directory structure
        self.name = run_name
        self.data_dir = Path('downloads\\offgas_data')
        self.this_runs_dir = Path.joinpath(self.data_dir, self.name)
        self.setup_directories()

        self._info = {'vendor_id': _CO2MON_HID_VENDOR_ID,
                      'product_id': _CO2MON_HID_PRODUCT_ID}
        self._h = hid.device()

        # Number of requests to open connection
        self._status = 0

        self._magic_word = [((w << 4) & 0xFF) | (w >> 4)
                            for w in bytearray(_CO2MON_MAGIC_WORD)]
        self._magic_table = _CO2MON_MAGIC_TABLE
        self._magic_table_int = list_to_longint(_CO2MON_MAGIC_TABLE)

        # Initialisation of continuous monitoring
        self._data = pd.DataFrame()
        self.final_data = pd.DataFrame()

        self._keep_monitoring = False
        self._interval = 10

        # Device info
        with self.co2hid():
            self._info['manufacturer'] = self._h.get_manufacturer_string()
            self._info['product_name'] = self._h.get_product_string()
            self._info['serial_no'] = self._h.get_serial_number_string()

        print(self.name + " is initialized")
    #########################################################################
    def hid_open(self, send_magic_table=True):
        """ Open connection to HID device. If connection is already open,
            then only the counter of requests is incremented (so hid_close()
            knows how many sub-processes keep the HID handle)

            Parameters
            ----------
            send_magic_table : bool
                If True then the internal "magic table" will be sent to
                the device (it is used for decryption)
        """
        if self._status == 0:
            # If connection was not opened before
            self._h.open(self._info['vendor_id'], self._info['product_id'])
            if send_magic_table:
                self._h.send_feature_report(self._magic_table)
        self._status += 1

    def hid_close(self, force=False):
        """ Close connection to HID device. If there were several hid_open()
            attempts then the connection will be closed only after respective
            number of calls to hid_close() method

            Parameters
            ----------
            force : bool
                Force-close of connection irrespectively of the counter of
                open requests
        """
        if force:
            self._status = 0
        elif self._status > 0:
            self._status -= 1
        if self._status == 0:
            self._h.close()

    def hid_read(self):
        """ Read 8-byte string from HID device """
        return self._h.read(8)

    @contextmanager
    def co2hid(self, send_magic_table=True):
        self.hid_open(send_magic_table=send_magic_table)
        try:
            yield
        finally:
            self.hid_close()

    #########################################################################
    @property
    def info(self):
        """ Device info """
        return self._info

    @property
    def is_alive(self):
        """ If the device is still connected """
        try:
            with self.co2hid(send_magic_table=True):
                return True
        except:
            return False

    #########################################################################
    def _decrypt(self, message):
        """ Decode message received from CO2 monitor.
        """
        # Rearrange message and convert to long int
        msg = list_to_longint([message[i] for i in [2, 4, 0, 7, 1, 6, 5, 3]])
        # XOR with magic_table
        res = msg ^ self._magic_table_int
        # Cyclic shift by 3 to the right
        res = (res >> 3) | ((res << 61) & 0xFFFFFFFFFFFFFFFF)
        # Convert to list
        res = longint_to_list(res)
        # Subtract and convert to uint8
        res = [(r - mw) & 0xFF for r, mw in zip(res, self._magic_word)]
        return res

    @staticmethod
    def decode_message(msg):
        """ Decode value from the decrypted message

            Parameters
            ----------
            msg : list
                Decrypted message retrieved with hid_read() method

            Returns
            -------
            CntR : int
                CO2 concentration in ppm
            Tamb : float
                Temperature in Celsius
        """
        # Expected 3 zeros at the end
        bad_msg = (msg[5] != 0) or (msg[6] != 0) or (msg[7] != 0)
        # End of message should be 0x0D
        bad_msg |= msg[4] != _CODE_END_MESSAGE
        # Check sum: LSB of sum of first 3 bytes
        bad_msg |= (sum(msg[:3]) & 0xFF) != msg[3]
        if bad_msg:
            return None, None

        value = (msg[1] << 8) | msg[2]

        if msg[0] == _CODE_CO2:  # CO2 concentration in ppm
            return int(value), None
        elif msg[0] == _CODE_TEMPERATURE:  # Temperature in Celsius
            return None, convert_temperature(value)
        else:  # Other codes - so far not decoded
            return None, None

    def _read_co2_temp(self, max_requests=50):
        """ Read one pair of values from the device.
            HID device should be open before
        """
        co2, temp = None, None
        for ii in range(max_requests):
            _co2, _temp = self.decode_message(self.hid_read())
            if _co2 is not None:
                co2 = _co2
            if _temp is not None:
                temp = _temp
            if (co2 is not None) and (temp is not None):
                break
        return now(), co2, temp

    #########################################################################
    def read_data_raw(self, max_requests=50):
        with self.co2hid(send_magic_table=True):
            vals = self._read_co2_temp(max_requests=max_requests)
            self._last_data = vals
            return vals

    def read_data(self, max_requests=50):
        """ Listen to values from device and retrieve temperature and CO2.

            Parameters
            ----------
            max_requests : int
                Effective timeout: number of attempts after which None is returned

            Returns
            -------
            tuple (timestamp, co2, temperature)
            or
            pandas.DataFrame indexed with timestamp
                Results of measurements
        """
        if self._keep_monitoring:
                return self._data.iloc[[-1]]
        else:
            vals = self.read_data_raw(max_requests=max_requests)
            # If pandas is available - return pandas.DataFrame
            if pd is not None:
                vals = pd.DataFrame({'co2': vals[1], 'temp': vals[2]},
                                    index=[vals[0]])
            return vals

    #########################################################################
    def _monitoring(self):
        """ Private function for continuous monitoring.
        """
        with self.co2hid(send_magic_table=True):
            while self._keep_monitoring:
                vals = self._read_co2_temp(max_requests=1000)
                if pd is None:
                    self._data.append(vals)
                else:
                    vals = pd.DataFrame({'co2': vals[1], 'temp': vals[2]},
                                        index=[vals[0]])
                    self._data = self._data.append(vals)
                time.sleep(self._interval)

    def start_monitoring(self, interval=5):
        """ Start continuous monitoring of the values and collecting them
            in the list / pandas.DataFrame.
            The monitoring is started in a separate thread, so the current
            interpreter session is not blocked.

            Parameters
            ----------
            interval : float
                Interval in seconds between consecutive data reads
        """
        print("Monitoring has begun, my friend")
        self._interval = interval
        if self._keep_monitoring:
            # If already started then we should not start a new thread
            return
        self._keep_monitoring = True
        t = threading.Thread(target=self._monitoring)
        t.start()

    """working on this one
    self.s = sched.scheduler(time.time, time.sleep)
    def continuous_plot(self, interval=10):
        print("Doing stuff...")
        s.enter(60, 1, do_something, (sc,))
        """

    def stop_monitoring(self):
        """ Stop continuous monitoring
            Log the data into a new dataframe called final_data
             with formatting set up for csv format
        """
        self._keep_monitoring = False
        self.final_data = self._data.reset_index()
        self.final_data = self.final_data.rename(columns = {'index':'timestamp'})
        self.final_data.timestamp = self.final_data.apply(lambda row: row['timestamp'].strftime("%m/%d/%Y, %H:%M:%S"), axis = 1)

    def begin_collecting_data(self):
        self.start_monitoring()

    def finish_collecting_data(self):
        self.stop_monitoring()
        self.log_data()
    #########################################################################
    @property
    def data(self):
        """ All data retrieved with continuous monitoring
        """
        return self._data
    def setup_directories(self):
        try:
            self.data_dir.mkdir()
        except FileExistsError:
            pass
        finally:
            try:
                self.this_runs_dir.mkdir()
            except FileExistsError:
                raise NonUniqueNameError

    def log_data(self):
        """
        Log data retrieved with continuous monitoring to CSV file.
        Logs the plot as a .png
        """
        fig = self.data.plot(secondary_y='temp').get_figure()
        fig.savefig(Path.joinpath(self.this_runs_dir, 'plot.png'))
        self.final_data.to_csv(Path.joinpath(self.this_runs_dir, 'data.csv'))
