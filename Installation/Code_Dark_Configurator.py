#!/usr/bin/python3
# Program to configure Code Dark workstation parameters

import subprocess
import tkinter as tk
from tkinter import messagebox
import json

"""
We need to be able to configure the following items:

 Networking
  Static IP Address for connections from Modalities
  Static IP Netmask for connections from Modalities

 DICOM
  Static Orthanc Port number to receive DICOM data
  Orthanc AET (Application Entity Title)

 Physicians

  Add a physician to list of those who are authorized to sign reports
  Remove a physician to list of those who are authorized to sign reports

"""
""" Variables and Constants """
NW = "networking"
DC = "dicom"
PH = "physicians"

jsonfile = "configurator.json"
fontfamily = 'Times'
fontsize = 12
fontstring = fontfamily + ' ' + str(fontsize)
boxsize = 5

""" Data hanlders """
def save_n_exit():
    json_data[NW]["addr"] = ip_entry.get()
    json_data[NW]["mask"] = nm_entry.get()
    json_data[DC]["port"] = port_entry.get()
    json_data[DC]["aet"] = aet_entry.get()
    pboxstr = pbox.get("1.0", "end-1c")
    json_data[PH] = [x.strip() for x in pboxstr.split(",")]
    with open(jsonfile, "w") as ofile:
        json.dump(json_data, ofile, indent=2)
        print("", file=ofile)
    exit(0)

""" TK functions """

def add_section_label(str, rv):
    tlab = tk.Label(root, text=str, relief=tk.FLAT, font=(fontfamily, fontsize + 2))
    tlab.grid(sticky=tk.N+tk.W, row=rv, column=0, columnspan=2, pady=(1,3))
    return rv + 1

def add_label(str, rv, col):
    tlab = tk.Label(root, text=str, relief=tk.FLAT, font=(fontfamily, fontsize))
    tlab.grid(sticky=tk.N+tk.W, row=rv, column=col)
    return rv + 1

""" add an unlabeled box """
def add_box(insert, row):
    box = tk.Text(root, height=boxsize, width=50, font=fontstring)
    box.insert(tk.END, insert)
    box.grid(sticky=tk.EW, row=row, column=0, columnspan=2, pady=(0,10), padx=(0,9))
    return box, row + boxsize

""" Add an entry to the right of a label """
def add_label_entry(label, ivalue, rv, w):
    tlab = tk.Label(root, text=label, anchor=tk.W, justify="left", font=(fontfamily, fontsize - 1))
    tlab.grid(sticky=tk.N+tk.W, row=rv, column=0)
    tt_text = tk.StringVar()
    tt_text.set(ivalue)
    tt_entry = tk.Entry(root, textvariable=tt_text, width=w, justify="left", font=fontfamily + str(fontsize - 1))
    tt_entry.grid(sticky=tk.W, row=rv, column=1)
    return tt_text, rv + 1


""" Add an entry to the right of a button
Not currently used
def add_button_entry(label, ivalue, w, rv, cb, cbarg):
    btn = tk.Button(root, text=label, command=lambda: cb(cbarg))
    btn.grid(sticky=tk.E, row=rv, column=0)
    tt_text = tk.StringVar()
    tt_text.set(ivalue)
    tt_entry = tk.Entry(root, textvariable=tt_text, width=w, font=fontstring)
    tt_entry.grid(sticky=tk.N+tk.W, row = rv, column=1)
    return tt_entry, rv + 1
"""

""" Begin Main Code section """

#
# Read in JSON saved data
#
with open(jsonfile, "r") as infile:
    json_data = json.load(infile)

#
# Version check
#

version = json_data["version"]
if version < 1:
    print("Version of JSON too low: " + str(version))
    exit(1)

root=tk.Tk()
cdf ="Code Dark Configurator"
root.title("")
headliner = tk.Label(root, text=cdf, font=(fontfamily, fontsize + 4))
headliner.grid(sticky=tk.N, row=0, column=0, columnspan = 2)

rowvar = 2

rowvar = add_section_label("IP NETWORKING", rowvar)
ip_entry, rowvar = add_label_entry("Static IP Address", json_data[NW]["addr"], rowvar, 16)
nm_entry, rowvar = add_label_entry("Static IP Netmask", json_data[NW]["mask"], rowvar, 16)

rowvar = add_section_label("DICOM PARAMETERS", rowvar)
port_entry, rowvar = add_label_entry("Update Listening Port", json_data[DC]["port"], rowvar, 16)
aet_entry, rowvar = add_label_entry("Update AET", json_data[DC]["aet"], rowvar, 16)

rowvar = add_section_label("AUTHORIZED RADIOLOGISTS", rowvar)
rowvar = add_label("Edit List (this is a comma separated list)", rowvar, 0)
plist = json_data[PH]
pbox, rowvar = add_box(','.join(plist), rowvar)

btn = tk.Button(root, text="Save and Exit", command=save_n_exit)
btn.grid(sticky=tk.W+tk.S, row=rowvar + 3, column=0)

root.mainloop()
