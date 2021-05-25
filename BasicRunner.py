'''
Created on May 19, 2020
@author: gioargyr
'''

import sys, os
from utils import *
import numpy as np
from matplotlib import pyplot as plt
import scipy as sp
from scipy import stats as st

class Main:

    """
        Initialization of Main class
    """
    def __init__(self, resources_dir):

        # Objects to be used by the algorithms
        self.properties_reader = PropertiesReader(resources_dir)
        self.dataset_filepath = os.path.join(resources_dir, self.properties_reader.dataset_name)
        self.multi_samples = FileReader().read_csv_multi(self.dataset_filepath)

        # Lists to be filed by the algorithms
        # self.datapoints = []

        accX_windowed = self.windowing(self.multi_samples[0])
        stat_feats = self.run_analytics(accX_windowed)
        #self.run_analytics(self.multi_samples[2])

        self.check_relation(stat_feats)


    """
    It gets the univariate time-series and returns lists within a list.
    Each included list has only the values of one window!
    Window's width and overlap's level are defined in the .properties file.
    """
    def windowing(self, univ_ts):

        window = int(self.properties_reader.window)
        overlap = float(self.properties_reader.overlap)

        ts_windowed = []
        i = 0
        while i < len(univ_ts) - 1:
            start = i
            end = start + window
            #print(str(start) + "\t" + str(end))
            group = []
            if end < len(univ_ts):
                for i in range(start, end):
                    group.append(univ_ts[i].get_value())
            else:
                end = len(univ_ts)
                #print(str(start) + "\t" + str(end) + "\telse")
                for i in range(start, end):
                    group.append(univ_ts[i].get_value())
                ts_windowed.append(group)
                break
            ts_windowed.append(group)
            #print(str(start) + "\t" + str(end))
            i = round(end - window * overlap)

        return ts_windowed


    """
    It calculates analytics on windowed time series.
    It returns one list which has each statistical feature in one list.
    """
    def run_analytics(self, ts_windowed):

        means = []
        stds = []
        quart1 = []
        quart3 = []
        for win in ts_windowed:
            means.append(np.mean(win))
            stds.append(np.std(win))
            quart1.append((np.quantile(win, 0.25)))
            quart3.append((np.quantile(win, 0.75)))

        self.vis_grouped_analytics(means, "mean")
        self.vis_grouped_analytics(stds, "std")
        self.vis_grouped_analytics(quart1, "q1")
        self.vis_grouped_analytics(quart3, "q3")

        return [means, stds, quart1, quart3]



    """

    """
    def check_relation(self, stat_feats):

        for i in range(1):
            stat_feat = stat_feats[i]

            ttest_results = []
            j = 0
            while j < len(stat_feat) - 1:
                start = j
                end = start + 5
                group = []
                if end < len(stat_feat):
                    print("\n" + str(start) + "\t" + str(end))
                    for k in range(start, end):
                        group.append(stat_feat[k])
                    ttest_res = st.ttest_1samp(group, stat_feat[end])
                    ttest_results.append(ttest_res.pvalue)
                    print(group)
                    print(stat_feat[end])
                    print(ttest_res.pvalue)
                else:
                    print("Stat feat length = \t" + str(len(stat_feat)))
                    for l in range(start, len(stat_feat)):
                        print(stat_feat[l])
                    break

                j = start + 1

        print("\nttest_results length = \t" + str(len(ttest_results)))
        # for item in ttest_results:
        #     print(item)

        # self.vis_grouped_analytics(stat_feat, "mean")
        # self.vis_grouped_analytics(ttest_results, "ttest")





        # t_results = []
        # i = 0
        # while i < len(univ_ts) - 1:
        #     #print(i)
        #     start = i
        #     end = start + window
        #     #print(str(start) + "\t" + str(end))
        #     group = []
        #     if end < len(univ_ts):
        #         for i in range(start, end):
        #             group.append(univ_ts[i].get_value())
        #         print(str(start) + "\t" + str(end))
        #         ttest_res = st.ttest_1samp(group, univ_ts[end].get_value())
        #         t_results.append(ttest_res.pvalue)
        #     # else:
        #     #     end = len(univ_ts)
        #     #     #print(str(start) + "\t" + str(end) + "\telse")
        #     #     for i in range(start, end):
        #     #         group.append(univ_ts[i].get_value())
        #     #     grouped_values.append(group)
        #     #     break
        #     #grouped_values.append(group)
        #     #print(str(start) + "\t" + str(end))
        #     i = start + 1
        #
        # for item in t_results:
        #     print(item)




    """

    """
    def vis_grouped_analytics(self, stat_feat, name):

        # Lists for plotting original samples
        x_orig = []
        y_orig = stat_feat
        for i in range(len(stat_feat)):
            x_orig.append(i)

        fig, ax = plt.subplots(figsize=(18, 6))
        color1 = 'tab:blue'
        color2 = 'tab:red'
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Sample Value")
        ax.plot(x_orig, y_orig, color=color1, label="Original")

        filename, file_extension = os.path.splitext(self.dataset_filepath)

        # if not self.isFiltering:
        #     plt.title("AdaM @ " + os.path.basename(filename) + ", " + str(len(self.samples)) +
        #               " samples        g=" + self.properties_reader.g + ", [Tmin, Tmax]=[" + self.properties_reader.Tmin +
        #               ", " + self.properties_reader.Tmax + "]        COMP=" + str(round(self.comp_sampler, 3)) +
        #               "%, ERR=" + str(round(self.err_sampler, 4)) + "%")
        # else:
        #     plt.title("AdaM @ " + os.path.basename(filename) + ", " + str(len(self.samples)) +
        #               " samples        g=" + self.properties_reader.g + ", [Tmin, Tmax]=[" + self.properties_reader.Tmin +
        #               ", " + self.properties_reader.Tmax + "], [Rmin, Rmax]=[" + self.properties_reader.Rmin + ", " +
        #               self.properties_reader.Rmax + "]        COMP=" + str(round(self.comp_filter, 3)) +
        #               "%, ERR=" + str(round(self.err_filter, 4)) + "%")
        plt.legend()
        ov = self.properties_reader.overlap.replace(".", "")
        vis_filepath = filename + "_" + name + "_w" + self.properties_reader.window + "_ov" + ov
        plt.savefig(vis_filepath)


    """
    We visualize values of original samples VS values of transmitted samples.

    """
    def vis_orig_transm_limits(self, low, upper):

        # Lists for plotting original samples
        x_orig = []
        y_orig = []
        for s in self.samples:
            if low <= s.get_timestamp() <= upper:
                x_orig.append(s.get_timestamp())
                y_orig.append(s.get_value())

        # Lists for plotting transmitted values
        x_trans = []
        y_trans = []
        if not self.isFiltering:
            for s in self.sampler_transm:
                if low <= s.get_timestamp() <= upper:
                    x_trans.append(s.get_timestamp())
                    y_trans.append(s.get_value())
        else:
            for s in self.filter_transm:
                x_trans.append(s.get_timestamp())
                y_trans.append(s.get_value())

        fig, ax = plt.subplots(figsize=(18, 6))
        color1 = 'tab:blue'
        color2 = 'tab:red'
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Sample Value")
        ax.plot(x_orig, y_orig, color=color1, label="Original")
        ax.plot(x_trans, y_trans, color=color2, label="Transmitted")

        filename, file_extension = os.path.splitext(self.dataset_filepath)

        if not self.isFiltering:
            plt.title("AdaM @ " + os.path.basename(filename) + ", " + str(len(self.samples)) +
                      " samples        g=" + self.properties_reader.g + ", [Tmin, Tmax]=[" + self.properties_reader.Tmin +
                      ", " + self.properties_reader.Tmax + "]        COMP=" + str(round(self.comp_sampler, 3)) +
                      "%, ERR=" + str(round(self.err_sampler, 4)) + "%")
        else:
            plt.title("AdaM @ " + os.path.basename(filename) + ", " + str(len(self.samples)) +
                      " samples        g=" + self.properties_reader.g + ", [Tmin, Tmax]=[" + self.properties_reader.Tmin +
                      ", " + self.properties_reader.Tmax + "], [Rmin, Rmax]=[" + self.properties_reader.Rmin + ", " +
                      self.properties_reader.Rmax + "]        COMP=" + str(round(self.comp_filter, 3)) +
                      "%, ERR=" + str(round(self.err_filter, 4)) + "%")
        plt.legend()

        g = self.properties_reader.g.replace(".", "")
        if not self.isFiltering:
            vis_filepath = filename + "-" + "g" + g + "Tmax" + self.properties_reader.Tmax + "limits"
        else:
            vis_filepath = filename + "-" + "g" + g + "Tmax" + self.properties_reader.Tmax + "Rmax" + self.properties_reader.Rmax
        plt.savefig(vis_filepath)


    """
    Print data for visualization in a proper .tsv file that can be opened as a spreadsheet and do visualization.
    Such file was used before employing matplotlib for visualization.
    Kept here as a reference.
    """
    def print_vis_data(self):

        filename, file_extension = os.path.splitext(self.dataset_filepath)
        dtvis_out_filepath = filename + "_DT-VIS-OUT.tsv"
        with open(dtvis_out_filepath, "a") as dtvis_out:
            if self.isFiltering:
                dtvis_out.write("TIMESTAMP\tORIG-VALUE\tSAMPLE-OUT-VALUE\tFILTER-OUT-VALUE\n")
                for dp in self.datapoints:
                    if dp.get_tag() == "SMPLD":
                        dtvis_out.write(str(dp.get_timestamp()) + "\t" + str(dp.get_orig_val()) + "\t\t\t\t\n")
                    else:
                        if dp.get_isFiltered():
                            dtvis_out.write(str(dp.get_timestamp()) + "\t" + str(dp.get_orig_val()) + "\t" + str(dp.get_forec_val()) + "\t\t\n")
                        else:
                            dtvis_out.write(str(dp.get_timestamp()) + "\t" + str(dp.get_orig_val()) + "\t" + str(dp.get_forec_val()) + "\t" + str(dp.get_forec_val()) + "\n")
            else:
                dtvis_out.write("TIMESTAMP\tORIG-VALUE\tSAMPLE-OUT-VALUE\n")
                for dp in self.datapoints:
                    if dp.get_isFiltered():
                        dtvis_out.write(str(dp.get_timestamp()) + "\t" + str(dp.get_orig_val()) + "\t\t\n")
                    else:
                        dtvis_out.write(str(dp.get_timestamp()) + "\t" + str(dp.get_orig_val()) + "\t" + str(dp.get_forec_val()) + "\n")


    """
    Naive sampling
    """
    def naive_sampling(self, sampling_per):

        for s in self.samples:
            if s.get_timestamp() % sampling_per == 0:
                self.sampler_transm.append(s)

        self.evaluate_AdaM()
        self.vis_orig_transm()
        self.vis_orig_transm_limits(500, 1500)



### End of class

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("\nWM.properties and dataset file for WM should be in directory: " + sys.argv[1])
        runAdaM = Main(sys.argv[1]);
    else:
        print("WM should run with 1 argument defining the directory that holds the necessary files.")
        sys.exit(2)
