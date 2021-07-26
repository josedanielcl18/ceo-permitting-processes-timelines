#Import libraries
import pandas as pd
#from datetime import datetime

# Import dfs
#from db.df_preprocessing import df1, df2
from db.df_preprocessing import getPreprocessedData


# --------------------------------------------------------------------------------------------------------------------------------------

def getPermitsIssued(file_location_1, file_location_2):

  # Import pre-processed data
  df1, df2 = getPreprocessedData(file_location_1, file_location_2)

  # Filter Building permits
  BP_pools = ['Commercial P.: Interior/Others', 'Commercial P.: New/Addition', 'Residential P.: Single Detached',
              'Residential P.: Semi-Detached', 'Row House', 'Residential P.: HIP']
  df1 = df1[df1['pools'].isin(BP_pools)]

  # Check JOBIDs in PROJECTS are the same as Processes
  df1_JOBIDs = df1['JOBID'].unique().tolist()
  df2 = df2[df2['JOBID'].isin(df1_JOBIDs)]

  #Merge FEATURES from Projects to Processes table
  df1_ = df1[['JOBID', 'RECEIVEDDATE', 'ISSUEDATE', 'pools']]
  df2 = df2.merge(df1_, how='left', on='JOBID')

  # --------------------------------------------------------------------------------------------------------------------------------------
  #FILTER ISSUED BP
  df1_issued = df1.dropna(subset=['ISSUEDATE'])
  df1 = df1_issued.copy()

  # Check JOBIDs in PROJECTS are the same as Processes
  df1_JOBIDs = df1['JOBID'].unique()
  df2 = df2[df2['JOBID'].isin(df1_JOBIDs)]
  #df2 = df2[df2['OBJECTDEFDESCRIPTION'].isin(key_processes)] # Only key processes
  
  return df1, df2
  
    
# --------------------------------------------------------------------------------------------------------------------------------------
  
def classifyPermitsBasedOnMIRstatus(df1, df2):
  # Classify permits based on MIR status (Complete vs. Incomplete applications)
  
  # MIR INFORMATION
  # Get information about Complete Applications at Intake Stage Vs. Incomplete Applications (MIR_Intake vs No MIR_Intake)
  JOBIDS_MIRIntake = df2[df2['OBJECTDEFDESCRIPTION'] =='More Info Requested - Intake']['JOBID'].unique().tolist()
  JOBIDS_MIRPER = df2[df2['OBJECTDEFDESCRIPTION'] =='More Info Requested - Plans Examination Review']['JOBID'].unique().tolist()
  JOBIDS_MIRGeneral = df2[df2['OBJECTDEFDESCRIPTION'] =='More Information Requested']['JOBID'].unique().tolist()

  MIR = JOBIDS_MIRIntake + JOBIDS_MIRGeneral

  df1_NoMIRAtAll = df1[~df1['JOBID'].isin(MIR)].copy()
  df1_NoMIRAtAll.loc[:, 'MIR_Status'] = 'Complete Applications'
  df1_MIRboth = df1[df1['JOBID'].isin(MIR)].copy()
  df1_MIRboth.loc[:, 'MIR_Status'] = 'Incomplete Applications'

  df1 = pd.concat([df1_NoMIRAtAll, df1_MIRboth])

  # MIR PER
  MIR_per = JOBIDS_MIRPER + JOBIDS_MIRGeneral

  df1_NoMIRAtAll = df1[~df1['JOBID'].isin(MIR_per)].copy()
  df1_NoMIRAtAll.loc[:, 'MIR_Status_PER'] = 'Complete Applications'
  df1_MIRboth = df1[df1['JOBID'].isin(MIR_per)].copy()
  df1_MIRboth.loc[:, 'MIR_Status_PER'] = 'Incomplete Applications'

  df1 = pd.concat([df1_NoMIRAtAll, df1_MIRboth])

  return df1

# --------------------------------------------------------------------------------------------------------------------------------------
#Merge FEATURES from Projects to Processes table
#df1_ = df1[['JOBID', 'MIR_Status']]
#df2 = df2.merge(df1_, how='left', on='JOBID')

# --------------------------------------------------------------------------------------------------------------------------------------

# TIME DURATIONS

def getProccessingTimesForTargetSegments(df1, df2):
  # df1 must have columns "MIR_Status" and "MIR_Status_PER"
  df1 = classifyPermitsBasedOnMIRstatus(df1, df2)
  # Calculate time duration of Projects between "Process Start" and "Process End"
    #Sort and group processes
  df2_ = df2[['JOBID', 'OBJECTDEFDESCRIPTION', 'DATECOMPLETEDHOUR']]      #Select relevant features
  df2_ = df2_.sort_values(by=['JOBID', 'DATECOMPLETEDHOUR'])              #Sort values by JOBID and DATECOMPLETEDHOUR
    # Define Process Start and Process End
  process_start = 'Enter Application'
  process_end = 'Plans Examination Review'
    # Make sure the JOBID contains both processes.
  JOBIDs_ps = df2[df2['OBJECTDEFDESCRIPTION']==process_start]['JOBID'].unique().tolist()
  JOBIDs_pe = df2[df2['OBJECTDEFDESCRIPTION']==process_end]['JOBID'].unique().tolist()
  JOBIDs_intake = df2[df2['OBJECTDEFDESCRIPTION']=="Building Intake Review"]['JOBID'].unique().tolist()
  JOBIDs = list(set(JOBIDs_ps).intersection(JOBIDs_pe).intersection(JOBIDs_intake))
  df2_ = df2_[df2_['JOBID'].isin(JOBIDs)]
  df2g = df2_.groupby(['JOBID'])          # Group Processes by "JOBID"

  #Create df that contains time durations of applications
  # Use "getDates" function to get dates associated with each process in each target segment
  l1, l2, l3, l4, l5 = zip(*[getDates(name, df2_fil, process_start, process_end) for name, df2_fil in df2g])
  df_duration = pd.DataFrame(list(zip(l1, l2, l3, l4, l5)), columns=['JOBID', 'DATECOMPLETED_PS_fi', 'DATECOMPLETED_PE_fi', 
                                                                    'DATECOMPLETED_intake_fi', 'DATECOMPLETED_intake_li'])

  # In the Projects table, select relevant features to merge the information
  df1_ = df1[['JOBID', 'RECEIVEDDATE', 'ISSUEDATE','Application-Type', 'pools', 'MIR_Status', 'MIR_Status_PER']]
  df_duration = df_duration.merge(df1_, on='JOBID', how='left')
  df_duration = df_duration.sort_values('RECEIVEDDATE')

  df_duration['project_duration'] = (df_duration['ISSUEDATE'] - df_duration['DATECOMPLETED_PS_fi']).dt.days
  df_duration['project_duration_Enter_to_PER_fi'] = (df_duration['DATECOMPLETED_PE_fi'] - df_duration['DATECOMPLETED_PS_fi']).dt.days
  df_duration['project_duration_Enter_to_Intake_fi'] = (df_duration['DATECOMPLETED_intake_fi'] - df_duration['DATECOMPLETED_PS_fi']).dt.days
  df_duration['project_duration_Intake_li_to_PER_fi'] = (df_duration['DATECOMPLETED_PE_fi'] - df_duration['DATECOMPLETED_intake_li']).dt.days

  #df is the same df_duration but with RECEIVEDDATE as index
  #df = df_duration.set_index('RECEIVEDDATE')

  return df_duration


# --------------------------------------------------------------------------------------------------------------------------------------

# Helper Function to get dates associated with each process in each target segment
def getDates(name, df, process_start, process_end):
    index_ps_fi = df[(df['OBJECTDEFDESCRIPTION'] == process_start)].index.tolist()[0]                   #Enter Application - first instance
    index_intake_fi = df[(df['OBJECTDEFDESCRIPTION'] == "Building Intake Review")].index.tolist()[0]    #Intake - first instance
    index_intake_li = df[(df['OBJECTDEFDESCRIPTION'] == "Building Intake Review")].index.tolist()[-1]   #Intake - last instance
    index_pe_fi = df[(df['OBJECTDEFDESCRIPTION'] == process_end)].index.tolist()[0]                     #PER - first instance
    DATECOMPLETED_PS_fi = df.loc[index_ps_fi, 'DATECOMPLETEDHOUR']          # Date Enter Application first instance
    DATECOMPLETED_intake_fi = df.loc[index_intake_fi, 'DATECOMPLETEDHOUR']  # Date Intake first instance
    DATECOMPLETED_intake_li = df.loc[index_intake_li, 'DATECOMPLETEDHOUR']  # Date Intake last instance
    DATECOMPLETED_PE_fi = df.loc[index_pe_fi, 'DATECOMPLETEDHOUR']          # Date PER - first instance
    #DATECOMPLETED_PE_li = df.loc[index_pe_li, 'DATECOMPLETEDHOUR']
    return name, DATECOMPLETED_PS_fi, DATECOMPLETED_PE_fi, DATECOMPLETED_intake_fi, DATECOMPLETED_intake_li


# --------------------------------------------------------------------------------------------------------------------------------------
# FINAL DATASETS

from app import cache
import json

# Store Data as JSON Format
@cache.memoize(timeout=0)
def getPermitsIssuedAsJson(file_location_1, file_location_2):
    
    # Permits Issued
    df1_issued, df2_issued = getPermitsIssued(file_location_1, file_location_2)
    df_duration_issued = getProccessingTimesForTargetSegments(df1_issued, df2_issued)

    datasets = {
              "df1_issued":df1_issued.to_json(orient='split', date_format='iso'),
              "df2_issued":df2_issued.to_json(orient='split', date_format='iso'),
              "df_duration_issued":df_duration_issued.to_json(orient='split', date_format='iso'),
              } 

    return json.dumps(datasets)