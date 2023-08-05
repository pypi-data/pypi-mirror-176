"""
Created on Mon Jul 18 08:28:36 2022

@author: gorosti
"""

from Time_Machine.GUI_AgeDating import Dating_GUI
import os

# Specify the absolut path to the folder containing the data files:

cwd = os.path.dirname(os.path.realpath(__file__))
Data_path = os.path.join(cwd, 'Data')


# Specify the name of the file for each signal:
    # CALIBRATION SAMPLE

#                      No edit column   :    Insert the file name in this column 
var_to_abbrev_cal = { "Ln_880"          :   'LN_Calibration_880_20s.tif',  
                      "Ln_955"          :   'LN_Calibration_955_20s.tif',
                      "Ln_I"            :   'LN_Calibration_IRSL_10s_20_frames.tif',
                      "Ln_optical"      :   'LN_Calibration_optical_0,01s.tif',
                      "Ln_880_after"    :   "LN_Calibration_880_20s_after_IRSL.tif",
                      "Ln_955_after"    :   "LN_Calibration_955_20s_after_IRSL.tif",
                      "Lx_880"          :   'TN_Calibration_880_20s.tif',
                      "Lx_955"          :   'TN_Calibration_955_20s.tif',
                      "Lx_I"            :   'TN_Calibration_IRSL_10s_20_frames.tif',
                      "Lx_optical"      :   'TN_Calibration_optical_0,01s.tif'}


# Specify the name of the file for each signal:
    # ANALYSIS SAMPLE

#                      No edit column   :    Insert the file name in this column 
var_to_abbrev_ana = { "Ln_880"          :   'LN_Dating_880_20s.tif',  
                      "Ln_955"          :   'LN_Dating_955_20s.tif',
                      "Ln_I"            :   'LN_Dating_IRSL_3s_67_frames.tif',
                      "Ln_optical"      :   'LN_Dating_optical_0,01s.tif',
                      "Ln_880_after"    :   "LN_Dating_880_20s_after_IRSL.tif",
                      "Ln_955_after"    :   "LN_Dating_955_20s_after_IRSL.tif",
                      "Lx_880"          :   'TN_Dating_880_20s.tif',
                      "Lx_955"          :   'TN_Dating_955_20s.tif',
                      "Lx_I"            :   'TN_Dating_IRSL_3s_67_frames.tif',
                      "Lx_optical"      :   'TN_Dating_optical_0,01s.tif'}


# Run GUI

Interface = Dating_GUI(Data_path, var_to_abbrev_cal, var_to_abbrev_ana)
Interface.mainloop()

