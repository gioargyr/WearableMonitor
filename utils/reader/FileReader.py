'''
Created on May 19, 2020
@author: gioargyr
'''

from utils.reader import Sample


class FileReader():

    """
        Read samples/data from csv file.
        Return list of Sample(s)
    """
    def read_csv_file(self, samples_filepath, delim=",", def_val=0):

        data_from_file = []
        with open(samples_filepath, "r") as lines:
            for line in lines:
                pureline = line.strip()
                tmp = pureline.split(delim)
                timestamp = int(tmp[0].strip())
                value = tmp[1]
                if value is None:
                    value = def_val
                else:
                    value = float(tmp[1].strip())
                readable_string = ""
                # for i in range(1, len(tmp)):
                #     readable_string += tmp[i]

                data_from_file.append(Sample(timestamp, value, readable_string))

        return data_from_file


    """
        Read samples/data that have multiple values
    """
    def read_csv_multi(self, samples_filepath, delim=","):

        accX = []
        accY = []
        accZ = []
        with open(samples_filepath, "r") as lines:
            for line in lines:
                pureline = line.strip()
                tmp = pureline.split(delim)
                timestamp = int(tmp[0].strip())
                readable_string = ""
                for i in range(1, len(tmp)):
                    if i == 1:
                        accX.append(Sample.Sample(timestamp, float(tmp[i].strip()), readable_string))
                    if i == 2:
                        accY.append(Sample.Sample(timestamp, float(tmp[i].strip()), readable_string))
                    if i == 3:
                        accZ.append(Sample.Sample(timestamp, float(tmp[i].strip()), readable_string))
                        # if i == 4:
                        #     gx.append(sampler.Sample(timestamp, float(tmp[i].strip()), readable_string))
                        # if i == 5:
                        #     gy.append(sampler.Sample(timestamp, float(tmp[i].strip()), readable_string))
                        # if i == 6:
                        #     gz.append(sampler.Sample(timestamp, float(tmp[i].strip()), readable_string))
                # for i in range(1, len(tmp)):
                #     readable_string += tmp[i]

                #data_from_file.append(sampler.Sample(timestamp, multi_value, readable_string))
        #data_from_file = [ax, ay, az, gx, gy, gz]
        data_from_file = [accX, accY, accZ]

        return data_from_file
