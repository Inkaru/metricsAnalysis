import os
import pandas as pd
import matplotlib.pyplot as plt

path = './csv/CK/'

versions = ["3-4", "3-5", "3-6", "3-7", "3-8", "4-0", "4-1", "4-2", "4-3", "5-0"]
modules = ["architecture", "cli", "gui", "logic", "migrations", "model", "pdfimport", "preferences", "styletester",
           "shared", "collab", "event", "external", "bst", "exporter", "importer", "specialfields", "sql", "util"]
metrics = ["CBO", "DIT", "LCOM", "NOC", "RFC", "WMC"]

collection = {}

for v in versions:
    data = pd.read_csv(path + v + "CK.csv", skiprows=1)
    #     print("Version " + v + " :")
    for mod in modules:
        rows = data[data["Class"].str.contains("jabref." + mod)]
        if (not (rows.empty)):
            #             print("Module " + mod + " : ")
            #             display(rows.describe())
            collection[mod + v] = rows.describe()
            collection[mod + v]["Module"] = mod
            collection[mod + v]["Version"] = v

data = pd.concat(collection)
data.reset_index(level=0, drop=True, inplace=True)
data.index.set_names(["Measure"], inplace=True)


# metric : one of the following -> CBO DIT LCOM NOC RFC WMC
# measure : one of the following -> count mean std min 25% 50% 75% max
#   (count is the number of classes, and 50% the median)
# modules : list of the modules to plot, among the following ->
#   "architecture","cli","gui","logic","migrations","model","pdfimport",
#   "preferences","styletester","shared","collab","event","external","bst",
#   "exporter","importer","specialfields","sql","util"

def version_evol(metric, measure, mods, ymin=None, ymax=None):
    d = data.loc[measure].pivot(index="Version", columns="Module", values=metric)
    for mod in mods:
        plt.plot(versions, d[mod], label=mod)
    plt.title("Modules " + measure + " " + metric + " evolution")
    plt.legend()
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    bottom, top = plt.ylim()
    if ymin is not None:
        bottom = ymin
    if ymax is not None:
        top = ymax
    plt.ylim((bottom, top))
    plt.show()
    return


# Use example
version_evol("RFC", "mean", ["gui", "model", "logic"], 0)
