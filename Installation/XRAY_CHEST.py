#!/usr/bin/python3
"""
Program to edit from JSON file input to add more or
edit existing data and to ultimately sign and print
a text based report from this date.
"""

#################################################################################################
#
#  Copyright (C) 2024 Kaiser Permanente
#
#  This program is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#


#################################################################################################
#
# Imports
#
import subprocess
import tkinter as tk
import json
import textwrap
import argparse

#################################################################################################
#
# Variables
#
radiologist = "Dr Roberts"
rowvar = 0

#################################################################################################
#
# Constants and shorthands
#
REPORT_DIR = "/code_dark/reports"


HI = "history"
PA = "patient_age"
PH = "patient_history"
TH = "technique"
VI = "views"
FI = "findings"
CM = "comparison"
IM = "impression"

HISTORY = "** HISTORY **"
PATIENT_AGE = "Patient Age"
PATIENT_HISTORY = "Patient History"

TECHNIQUE = "** TECHNIQUE **"
VIEWS = "Views"

FINDINGS = "** FINDINGS **"
COMPARISON = "Comparison"

IMPRESSION = "** IMPRESSION **"

"""
#################################################################################################
#
# Create default report dictionary- used only once to create the first template
#

#
# Dictionary Structure
#
# history {
#  patient_age : string,
#  patient_history : string
# }
#
# technique {
#  views : string,
#  comparison : string
# }
#
#
# report {
#  version : integer,
#  mrn : string,
#  session : string,
#  signed : boolean,
#  signer : string,
#  history : dict,
#  technique : dict,
#  findings : string,
#  impression : string
# }

REPORT_VERSION = 0

report = {
    "report_version" : REPORT_VERSION,
    "mrn" : "",
    "session" : "",
    "signed" : False,
    "signer" : "",
    "history" : {
        "patient_age" : "42Y",
        "patient_history" : PATIENT_HISTORY + ".....",
    },
    "technique" : {
        "views" : "view(s) of chest acquired",
        "comparison" : "None Available",
    },
    "findings" : "No Focal Consolidation",
    "impression" : "Normal Chest",
}
TEMPLATE_OUT = "/tmp/xray_tmplt.json"
#
# Write out initial template file per command line argument with the defaults that we have set.
#
with open(TEMPLATE_OUT, "w") as outfile:
    json.dump(report, outfile)
"""

#
# Process command line arguments and load initial json data
#
parser = argparse.ArgumentParser(description="Report on Study Entry Package for CHEST XRAY")
parser.add_argument("-m", "--mrn", help="MRN for Study", required=True)
parser.add_argument("-s", "--session", help="Session for Study", required=True)
parser.add_argument("-R", "--report_dir", help="Where we fetch/save reports", default="/code_dark/reports")

args=vars(parser.parse_args())
mrn = args['mrn']
session = args['session']
report_dir = REPORT_DIR
if args['report_dir']:
    report_dir = args['report_dir']

reportnm = "study_" + mrn + "_" + session
jsonfile = report_dir + "/" + reportnm + ".json"
reportfl = report_dir + "/" + reportnm + ".txt"


#
# Read in JSON input
#
with open(jsonfile, "r") as infile:
    json_data = json.load(infile)

#################################################################################################
#
# Window and Frame Management Code
#

#
# Root window creation
#
root=tk.Tk()
root.title("XRAY Chest Study" + " MRN: " + mrn + " SESSION: " + session)
root.geometry('1024x768')

#
# Display sections with labels and text boxes,
# using data read in as existing values.
#

# History Section
hisvar = tk.StringVar()
hisvar.set(HISTORY)
hislab = tk.Label(root, textvariable=hisvar, relief=tk.RAISED)
hislab.grid(sticky=tk.W, row=rowvar)
rowvar = rowvar + 1

age_label_text = tk.StringVar()
age_label_text.set(PATIENT_AGE + " (years)")
age_label = tk.Label(root, textvariable=age_label_text, anchor=tk.W, width=15, justify="left")
age_label.grid(sticky=tk.W, row=rowvar, column=0)

age_text = tk.StringVar()
age_text.set(json_data[HI][PA])
age_entry = tk.Entry(root, textvariable=age_text, width=4, justify="right")
age_entry.grid(sticky=tk.W, row=rowvar, column=1)

rowvar = rowvar + 1

history_label_text = tk.StringVar()
history_label_text.set(PATIENT_HISTORY)
history_label = tk.Label(root, textvariable=history_label_text, anchor=tk.W, width=20, justify="left")
history_label.grid(sticky=tk.N+tk.W, row=rowvar, column=0)

history_box = tk.Text(root, height=5, width=80)
history_box.insert(tk.END, json_data[HI][PH])
history_box.grid(sticky=tk.W, row=rowvar, column=1, pady=(0,10))
rowvar = rowvar + 5

# Technique Section
tekvar = tk.StringVar()
tekvar.set(TECHNIQUE)
teklab = tk.Label(root, textvariable=tekvar, relief=tk.RAISED)
teklab.grid(sticky=tk.W, row=rowvar)
rowvar = rowvar + 1

views_label_text = tk.StringVar()
views_label_text.set(VIEWS)
views_label = tk.Label(root, textvariable=views_label_text, anchor=tk.W, width=20, justify="left")
views_label.grid(sticky=tk.N+tk.W, row=rowvar, column=0)

views_box = tk.Text(root, height=5, width=80)
views_box.grid(sticky=tk.W, row=rowvar, column=1)
views_box.insert(tk.END, json_data[TH][VI])
rowvar = rowvar + 5

tek_comparison_label_text = tk.StringVar()
tek_comparison_label_text.set(COMPARISON)
tek_comparison = tk.Label(root, textvariable=tek_comparison_label_text, anchor=tk.W, width=15, justify="left")
tek_comparison.grid(sticky=tk.W, row=rowvar, column=0)

tek_comparison_text = tk.StringVar()
tek_comparison_text.set(json_data[TH][CM])

tek_comparison_entry = tk.Entry(root, textvariable=tek_comparison_text, width=20, justify="left")
tek_comparison_entry.grid(sticky=tk.W, row=rowvar, column=1, pady=(0,10))
rowvar = rowvar + 1

# Findings Section
findvar = tk.StringVar()
findvar.set(FINDINGS)
findlab = tk.Label(root, textvariable=findvar, relief=tk.RAISED)
findlab.grid(sticky=tk.N+tk.W, row=rowvar)

findings_box = tk.Text(root, height=5, width=80)
findings_box.insert(tk.END, json_data[FI])
findings_box.grid(sticky=tk.W, row=rowvar, column=1, pady=(0,10))
rowvar = rowvar + 5

# Impressions Section
impressvar = tk.StringVar()
impressvar.set(IMPRESSION)
impresslab = tk.Label(root, textvariable=impressvar, relief=tk.RAISED)
impresslab.grid(sticky=tk.N+tk.W, row=rowvar)

impress_box = tk.Text(root, height=5, width=80)
impress_box.insert(tk.END, json_data[IM])
impress_box.grid(sticky=tk.W, row=rowvar, column=1, pady=(0,10))
rowvar = rowvar + 5

#################################################################################################
#
# Data interactions with tkinter frame/boxes plus action functions
#

#
# Define a function that will save data to a datafile.
# As a side effect, it updates existing data from labels and text boxes
#
def save_data(jd):
    """ Update from tkinter box areas """
    json_data[HI][PA] = age_text.get()
    json_data[HI][PH] = history_box.get("1.0", "end-1c")
    json_data[TH][VI] = views_box.get("1.0", "end-1c")
    json_data[TH][CM] = tek_comparison_text.get()
    json_data[FI] = findings_box.get("1.0", "end-1c")
    json_data[IM] = impress_box.get("1.0", "end-1c")
    with open(jsonfile, "w") as ofile:
        json.dump(jd, ofile)

# Define a function that will save existing data to a printable report text file
def create_report(rpt):
    save_data(json_data)
    with open(rpt, "w") as ofile:
        wrapper = textwrap.TextWrapper(width=60, replace_whitespace=False)
        print("XRAY Chest Study", file=ofile)
        print("", file=ofile)
        print("MRN: " + mrn, file=ofile)
        print("Session: " + session, file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        print(HISTORY, file=ofile)
        print("", file=ofile)
        print(PATIENT_AGE + " (years):  " + json_data[HI][PA], file=ofile)
        print(PATIENT_HISTORY + ":", file=ofile)
        for line in json_data[HI][PH].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        print(TECHNIQUE, file=ofile)
        print(VIEWS + ":", file=ofile)
        for line in json_data[TH][VI].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print(COMPARISON + ": " + json_data[TH][CM], file=ofile)
        print("", file=ofile)
        print(FINDINGS, file=ofile)
        for line in json_data[FI].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        print(IMPRESSION, file=ofile)
        for line in json_data[IM].split('\n'):
            print(wrapper.fill(text=line), file=ofile)
        print("", file=ofile)
        print("", file=ofile)
        """ PRINT SIGNING RADIOLIGIST NAME """

# Define a function that will print the report after saving text output to a file
def print_report():
    save_data(json_data)
    create_report(reportfl)
    try:
        result = subprocess.run(["enscript", "-B", reportfl ], capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Subprocess Error", result.stderr)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Process Error", e.output)

# Define a function that will sign the report
def sign_report():
    json_data["signed"] = True
    json_data["signer"] = radiologist
    save_data(json_data)
    try:
        result = subprocess.run(["chmod", "-w", jsonfile ], capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Subprocess Error", result.stderr)
            exit()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Process Error", e.output)
        exit()
    rpt.signed = True

# define a function that will exit, saving data and creating on-disk report as it does so.
def exit_edit():
    save_data(json_data)
    create_report(reportfl)
    exit()

#
# Add action buttons to the end
#
sign_btn = tk.Button(root, text = 'Sign Report', command = sign_report)
sign_btn.grid(sticky=tk.W)

print_btn = tk.Button(root, text = 'Print Report', command = print_report)
print_btn.grid(sticky=tk.W)

exit_btn = tk.Button(root, text = 'Exit', command = exit_edit)
exit_btn.grid(sticky=tk.W)


#
# Enter edit tkinter loop
#
root.mainloop()
