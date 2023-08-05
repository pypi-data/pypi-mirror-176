from uvraspy.database.DataPoint import DataPoint
from uvraspy.database.Alert import Alert
from datetime import datetime
import threading
import multiprocessing


def binsearchf(f, value, record_size, bound=None):
    """
    Binary search for a value in a file
    :param f: the file handle
    """
    f.seek(0, 2)
    end = f.tell() // record_size
    f.seek(0, 0)
    start = 0
    while end - start > 1:
        mid = (start + end) // 2
        f.seek(mid * record_size)
        line = f.read(record_size)

        # decode the line
        dp = DataPoint.fromEncoded(line)
        if dp.timestamp == value:
            # return when the timestamp is found
            return mid + 1 if bound == "upper" else mid
        if dp.timestamp < value:
            start = mid + 1
        else:
            end = mid

    return end if bound == 'upper' else start if bound == 'lower' else -1


def decrypt_chunk(data):
    return [DataPoint.fromEncoded(i) for i in data]


class DBManager:

    """
    This class is responsible for managing the database.
    It should be able to add data points,
    retrieve data points,
    add alerts,
    retrieve alerts,
    get preferences,
    and set preferences."""

    def __init__(self, db_path, alert_path):
        # open our database file
        # if it doesn't exist, create it

        # get the length of the file
        self.db = open(db_path, "a+b")
        self.db.seek(0, 2)
        self.db_length = self.db.tell() // DataPoint.RECORD_SIZE_FULL
        self.db.seek(0, 0)

        # create another file for the warning history
        # if it doesn't exist, create it
        self.alert = open(alert_path, "a+b")
        self.alert.seek(0, 2)
        self.alert_length = self.alert.tell() // DataPoint.RECORD_SIZE_FULL
        self.alert.seek(0, 0)

        # define lock for the database
        self.dblock = threading.Lock()
        self.alertlock = threading.Lock()

    def addDataPoint(self, data):
        # add a data point to the database
        # data is a DataPoint object
        self.dblock.acquire()
        self.db.write(data.toEncoded())
        self.db_length += 1
        self.dblock.release()

    def retrieveData(self, b=None, e=None, limit=None, accurracy=None, spacing=None):
        self.dblock.acquire()
        begin = 0
        end = self.db_length
        if b is not None:
            # find the index of begin
            # we can do this by doing a binary search
            # on the timestamp
            begin = binsearchf(self.db, b, DataPoint.RECORD_SIZE_FULL, 'lower')
        if e is not None:
            # find the index of end
            end = binsearchf(self.db, e, DataPoint.RECORD_SIZE_FULL, 'upper')

        if limit is None and accurracy is not None:
            limit = accurracy
        if ((limit is not None and accurracy is None) or
                (limit is not None and accurracy is not None and limit < accurracy)):
            accurracy = limit

        # now we can read the data
        self.db.seek(begin * DataPoint.RECORD_SIZE_FULL)
        data = self.db.read((end - begin) * DataPoint.RECORD_SIZE_FULL)
        self.dblock.release()

        # split the data into chunks
        data_ls = [data[i:i + DataPoint.RECORD_SIZE_FULL] for i in range(0, len(data), DataPoint.RECORD_SIZE_FULL)]

        # check if we need to limit the number of data points
        if accurracy is not None:
            # we need to limit the number of data points
            # so we need to calculate the interval
            interval = (end - begin) // accurracy
            if interval == 0:
                interval = 1
            data_ls = data_ls[::interval]

        full_data = []
        if len(data_ls) <= 150:
            # we don't need to do any multi-threading
            full_data = [DataPoint.fromEncoded(i) for i in data_ls]
        else:
            # we need to do multi-processing
            # we need to split the data into chunks
            # and then process them in parallel
            # we will use 4 processes

            # first we need to calculate the interval
            interval = len(data_ls) // 4

            # now we can split the data
            data_chunks = [data_ls[i:i + interval] for i in range(0, len(data_ls), interval)]

            # now we can create the processes
            with multiprocessing.Pool(4) as p:
                data = p.map(decrypt_chunk, data_chunks)
                full_data = data[0] + data[1] + data[2] + data[3]

        full_data_ = []
        if spacing is not None and len(full_data) > 0:
            # average every data point that falls within the same spacing
            # calculated from the first data point or begin, if defined

            space_begin = full_data[0].timestamp if b is None else b
            last_space = space_begin

            space_collection = []
            for i in full_data:
                if i.timestamp - last_space >= spacing:
                    # we need to average the space collection
                    # and add it to the full data
                    if len(space_collection) > 0:
                        # calculate the average
                        avg = DataPoint.average(space_collection)
                        full_data_.append(avg)
                    last_space = i.timestamp
                    space_collection = [i]
                else:
                    space_collection.append(i)

            # add the last space collection
            avg = DataPoint.average(space_collection)
            full_data_.append(avg)
        else:
            full_data_ = full_data

        if limit != accurracy:
            # we need to limit the number of data points
            # so we need to calculate the interval
            interval = len(full_data_) // limit
            if interval == 0:
                interval = 1
            full_data_ = full_data_[::interval]

        return full_data_

    def addAlertEntry(self, alert):
        # add an alert entry to the database
        # alert is a Alert object
        self.alertlock.acquire()
        self.alert.write(alert.toEncoded())
        self.alert_length += 1
        self.alertlock.release()

    def retrieveAlerts(self, b=None, e=None, limit=None):
        self.alertlock.acquire()
        begin = 0
        end = self.alert_length
        if b is not None:
            # find the index of begin
            # we can do this by doing a binary search
            # on the timestamp
            begin = binsearchf(self.alert, b, Alert.ALERT_RECORD_SIZE_FULL, 'lower')
        if e is not None:
            # find the index of end
            end = binsearchf(self.alert, e, Alert.ALERT_RECORD_SIZE_FULL, 'upper')

        # now we can read the data
        self.alert.seek(begin * Alert.ALERT_RECORD_SIZE_FULL)
        data = self.alert.read((end - begin) * Alert.ALERT_RECORD_SIZE_FULL)
        self.alertlock.release()
        data_ls = [data[i:i + Alert.ALERT_RECORD_SIZE_FULL] for i in range(0, len(data), Alert.ALERT_RECORD_SIZE_FULL)]
        return [Alert.fromEncoded(i) for i in data_ls]

    def normalize(self):
        # this function will normalize the database
        # it will squash the data points after the last 2 months

        # the amount that will be squashed is:
        # last 2 months: keep all data points
        # last 6 months: keep 1 data point per minute
        # last 24 months: keep 1 data point per hour
        # later: keep 1 data point per day

        # this will be done by averaging the data points
        # the timestamp of the new data point will be the average of the
        # first and last data point

        # now we need to find the first data point that is more than 2 months old
        # we can do this by doing a binary search
        self.dblock.acquire()
        m2 = int(round(datetime.timestamp(datetime.now()))) - 60 * 60 * 24 * 30 * 2
        idxm2 = binsearchf(self.db, m2, DataPoint.RECORD_SIZE_FULL, 'upper')

        # first, we need to store the initial data points
        self.db.seek(m2 * DataPoint.RECORD_SIZE_FULL)
        untouchable_data = self.db.read((self.db_length - idxm2) * DataPoint.RECORD_SIZE_FULL)

        # now we need to find the first data point that is more than 6 months old
        m6 = int(round(datetime.timestamp(datetime.now()))) - 60 * 60 * 24 * 30 * 6
        idxm6 = binsearchf(self.db, m6, DataPoint.RECORD_SIZE_FULL, 'upper')

        # get all data points in between
        self.db.seek(idxm2 * DataPoint.RECORD_SIZE_FULL)
        data = self.db.read((idxm2 - idxm6) * DataPoint.RECORD_SIZE_FULL)
        data_ls = [data[i:i + DataPoint.RECORD_SIZE_FULL] for i in range(0, len(data), DataPoint.RECORD_SIZE_FULL)]
        data_ls_6 = [DataPoint.fromEncoded(i) for i in data_ls]

        # now we need to find the first data point that is more than 24 months old
        m24 = int(round(datetime.timestamp(datetime.now()))) - 60 * 60 * 24 * 30 * 24
        idxm24 = binsearchf(self.db, m24, DataPoint.RECORD_SIZE_FULL, 'upper')

        # get all data points in between
        self.db.seek(idxm6 * DataPoint.RECORD_SIZE_FULL)
        data = self.db.read((idxm6 - idxm24) * DataPoint.RECORD_SIZE_FULL)
        data_ls = [data[i:i + DataPoint.RECORD_SIZE_FULL] for i in range(0, len(data), DataPoint.RECORD_SIZE_FULL)]
        data_ls_24 = [DataPoint.fromEncoded(i) for i in data_ls]

        # get all data points after
        self.db.seek(idxm24 * DataPoint.RECORD_SIZE_FULL)
        data = self.db.read((self.db_length - idxm24) * DataPoint.RECORD_SIZE_FULL)
        data_ls = [data[i:i + DataPoint.RECORD_SIZE_FULL] for i in range(0, len(data), DataPoint.RECORD_SIZE_FULL)]
        data_ls_24p = [DataPoint.fromEncoded(i) for i in data_ls]

        # now we need to average the data points
        # we will do this by creating a new list
        # and then adding the data points to the list
        def makeList(data_ls, interval):
            ret = []
            for i in data_ls:
                if len(ret) == 0:
                    ret.append([i])
                else:
                    if i.timestamp // interval == ret[-1][0].timestamp // interval:
                        ret[-1].append(i)
                    else:
                        ret.append([i])
            return ret

        # first, we will do the 6 month data points. from every second to every minute
        # create a list of datapoint collections that have matching minutes
        data_ls_6m = makeList(data_ls_6, 60)

        # now we can average the data points
        data_ls_6m_avg = [DataPoint.average(i) for i in data_ls_6m]

        # now we will do the 24 month data points. from every minute to every hour
        # create a list of datapoint collections that have matching hours
        data_ls_24m = makeList(data_ls_24, 60 * 60)
        data_ls_24m_avg = [DataPoint.average(i) for i in data_ls_24m]

        # now we will do the 24+ month data points. from every hour to every day
        # create a list of datapoint collections that have matching days
        data_ls_24mp = makeList(data_ls_24p, 60 * 60 * 24)
        data_ls_24mp_avg = [DataPoint.average(i) for i in data_ls_24mp]

        # now we can write the data points to the database
        # first, we need to truncate the database
        self.db.truncate(0)
        # and rewrite the whole database
        self.db.seek(0)
        # now we can write the data points
        for i in data_ls_24mp_avg:
            self.db.write(i.toEncoded())
        for i in data_ls_24m_avg:
            self.db.write(i.toEncoded())
        for i in data_ls_6m_avg:
            self.db.write(i.toEncoded())
        self.db.write(untouchable_data)

        # now we need to update the database length
        self.db.seek(0, 2)
        self.db_length = self.db.tell() // DataPoint.RECORD_SIZE_FULL
        self.db.seek(0)

        self.dblock.release()


dbm = DBManager("DB", "ALERT")
