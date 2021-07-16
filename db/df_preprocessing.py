#Import libraries
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
#from datetime import datetime

# Import dataframes
#from .googleData import PROJECTS_ID, PROCESSES_ID1, PROCESSES_ID2, getData
#df1 = getData(PROJECTS_ID)  # Projects 2018-2021
#df21 = getData(PROCESSES_ID1) # Processes 2020-2021
#df22 = getData(PROCESSES_ID2) # Processes 2018-2019

# Concatenate all processes
#df2 = pd.concat([df21, df22])

# ----------------------------------------------------------------------------------------------------------
# Open Pickle, load as dict and convert to dataframe.
import pickle

# Projects table
projects_pickle = open("./db/projects_commercial_2019.pkl", "rb") # rb: read binary
projects_dict = pickle.load(projects_pickle) # projects as python dict
df1 = pd.DataFrame.from_dict(projects_dict) # projects as df
# Processes table
processes_pickle = open("./db/processes_commercial_2019.pkl", "rb") # rb: read binary
processes_dict = pickle.load(processes_pickle) # processes as python dict
df2 = pd.DataFrame.from_dict(processes_dict) # processes as df

# --------------------------------------------------------------------------------------------------------------------------------------
# PRE-PROCESSING DATA

 # Projects table

# Rename columns to ensure consistency and correct data types
df1['JOBID'] = df1['JOBID'].astype('int32')
df1.rename(columns={"MAJORDEVAPPLICATIONFEE2001":'Application-Type'}, inplace=True)
#df1['RECEIVEDDATE'] = pd.to_datetime(df1['RECEIVEDDATE'], infer_datetime_format=True)
#df1['ISSUEDATE'] = pd.to_datetime(df1['ISSUEDATE'], infer_datetime_format=True)

  # Processes table

# Rename columns to ensure consistency
df2['JOBID'] = df2['JOBID'].astype('int32')
df2.rename(columns={"TO_CHAR(B.DATECOMPLETED,'YYYY-MM-DDHH24:MI:SS')":"DATECOMPLETEDHOUR"}, inplace=True)
df2['DATECOMPLETEDHOUR'] = df2['DATECOMPLETEDHOUR'].str[:10] + ' ' + df2['DATECOMPLETEDHOUR'].str[-8:]
df2['DATECOMPLETEDHOUR'] = pd.to_datetime(df2['DATECOMPLETEDHOUR'], infer_datetime_format=True)

# --------------------------------------------------------------------------------------------------------------------------------------
# FILTER DATA

# Exclude permits with the following outcome
outcome = ["Cancelled", "Expired", "Refused", "Suspended", "On Hold"] 
df1 = df1[~df1['STATUSDESCRIPTION'].isin(outcome)]
# Match JOBIDs in Projects and Processes tables
df1_JOBIDs = df1['JOBID'].unique()
df2 = df2[df2['JOBID'].isin(df1_JOBIDs)]

# ------------------------------------------------------------------------------------------------------------
# Create Pools of Permits based on 'JOBTYPEDESCRIPTION', 'Application-Type' and 'CLASSOFPERMIT'.
from db.helper_functions import CreatePools
df1 = CreatePools(df1)

# --------------------------------------------------------------------------------------------------------------------------------------
# key processes
key_processes = ['Enter Application',
                 'Building Intake Review',
                 'More Info Requested - Intake',
                 'Info Received - Intake',
                 'Restamp/Zoning Signoff Requested',
                 'Restamp/Zoning Signoff Completed',
                 'System Process - Commercial Building Permit',
                 #'System Process - Initiate Plans Assignment', # OUTCOME: "Complete". DISCUSS WITH NADYA
                 'Assign Plans Examination',
                 'Plans Examination Review',
                 'More Info Requested - Plans Examination Review',
                 'More Info Requested - Plans Examination Notification',
                 'Info Received - Plans Examination Review',
                 'More Information Requested',
                 'Information Received',
                 'Job Status Correction',
                 'Request Plans Revision',
                 'Assign Revision Review']

# Filter df2 by key processes.
df2 = df2[df2['OBJECTDEFDESCRIPTION'].isin(key_processes)]

# --------------------------------------------------------------------------------------------------------------------------------------
# Get STATUS OF APPLICATIONS based on last process completed and OUTCOME.
from db.helper_functions import GetStatus
df2 = GetStatus(df2)