#Import libraries
import pandas as pd
#from datetime import datetime

# Import dfs
from db.df_preprocessing import df1, df2

# --------------------------------------------------------------------------------------------------------------------------------------
from app import cache
import json

#TIMEOUT=180
@cache.memoize(timeout=0)
def query_issued_data(df1, df2):

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
  # STATUS OF APPLICATIONS. # df2_fil: Dataset SHOULD include all permits (issued and in progress). 
  #df2_fil = df2.copy() 
  #print(df2_fil['Status'].unique())

  # --------------------------------------------------------------------------------------------------------------------------------------
  #FILTER ISSUED BP
  df1_issued = df1.dropna(subset=['ISSUEDATE'])
  df1 = df1_issued.copy()

  # Check JOBIDs in PROJECTS are the same as Processes
  df1_JOBIDs = df1['JOBID'].unique()
  df2 = df2[df2['JOBID'].isin(df1_JOBIDs)]
  #df2 = df2[df2['OBJECTDEFDESCRIPTION'].isin(key_processes)] # Only key processes
  # --------------------------------------------------------------------------------------------------------------------------------------

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

  # --------------------------------------------------------------------------------------------------------------------------------------
  #Merge FEATURES from Projects to Processes table
  #df1_ = df1[['JOBID', 'MIR_Status']]
  #df2 = df2.merge(df1_, how='left', on='JOBID')

  # --------------------------------------------------------------------------------------------------------------------------------------

  # TIME DURATIONS

  # Calculate time duration of Projects between "Process Start" and "Process End"
    #Sort and group processes
  df2_ = df2[['JOBID', 'OBJECTDEFDESCRIPTION', 'DATECOMPLETEDHOUR']]                  #Select relevant features
  df2_ = df2_.sort_values(by=['JOBID', 'DATECOMPLETEDHOUR'])                          #Sort values by JOBID and DATECOMPLETEDHOUR
    # Define Process Start and Process End
  process_start = 'Enter Application'
  process_end = 'Plans Examination Review'
    # Make sure the JOBID contains both processes.
  JOBIDs_ps = df2[df2['OBJECTDEFDESCRIPTION']==process_start]['JOBID'].unique().tolist()
  JOBIDs_pe = df2[df2['OBJECTDEFDESCRIPTION']==process_end]['JOBID'].unique().tolist()
  JOBIDs_intake = df2[df2['OBJECTDEFDESCRIPTION']=="Building Intake Review"]['JOBID'].unique().tolist()
  JOBIDs = list(set(JOBIDs_ps).intersection(JOBIDs_pe).intersection(JOBIDs_intake))
  df2_ = df2_[df2_['JOBID'].isin(JOBIDs)]
  df2g = df2_.groupby(['JOBID'])                                                      # Group Processes by "JOBID"

  def GetDates(name, df, process_start, process_end):
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

  #Create df that contains time durations of applications
  l1, l2, l3, l4, l5 = zip(*[GetDates(name, df2_fil, process_start, process_end) for name, df2_fil in df2g])
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

  datasets = {
              #"df1":df1.to_json(orient='split', date_format='iso'),
              #"df2":df2.to_json(orient='split', date_format='iso'),
              "df_duration":df_duration.to_json(orient='split', date_format='iso'),
              } 
              
  # return df_duration
  return json.dumps(datasets)

#datasets = query_issued_data(df1, df2)


# --------------------------------------------------------------------------------------------------------------------------------------

