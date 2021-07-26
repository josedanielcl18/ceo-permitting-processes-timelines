#Import libraries
import pandas as pd

# Import dfs
#from db.df_preprocessing import df1, df2
from db.df_preprocessing import getPreprocessedData

# --------------------------------------------------------------------------------------------------------------------------------------
# Pre-processing data related to Permits in Progress

def getPermitsInProgress(file_location_1, file_location_2):
    
    df1, df2 = getPreprocessedData(file_location_1, file_location_2)
    
    # All Permits In Progress (no issue date)
    df_inProgress = df1[df1['ISSUEDATE'].isnull()]
    # Exclude permits with the following outcome
    outcome = ["Cancelled", "Expired", "Refused", "Suspended", "N.B.P.R", "N.B.P.R.", "NBPR", "Completed", "Issued", 
            "Permit Prepared", "On Hold", "New"] 
    df_inProgress = df_inProgress[~df_inProgress['STATUSDESCRIPTION'].isin(outcome)]

    from datetime import date
    # Add today's date to calculate "project_duration"
    df_inProgress.loc[:, 'ISSUEDATE'] = df_inProgress.loc[:, 'ISSUEDATE'].fillna(date.today())
    # Correct data type
    df_inProgress['ISSUEDATE'] = pd.to_datetime(df_inProgress['ISSUEDATE'], infer_datetime_format=True)
    # Calculate current "project_duration"
    df_inProgress['project_duration'] = (df_inProgress['ISSUEDATE'] - df_inProgress['RECEIVEDDATE']).dt.days

    # --------------------------------------------------------------------------------------------------------------------------------------
    # Match JOBIDs in tables

    # Check JOBIDs in PROJECTS are the same as Processes
    df1 = df_inProgress.copy() 
    df1_JOBIDs = df1['JOBID'].unique()
    df2 = df2[df2['JOBID'].isin(df1_JOBIDs)]

    #Merge RECEIVEDDATE from Projects to Processes table
    df1_ = df1[['JOBID', 'RECEIVEDDATE', 'ISSUEDATE', 'pools']]
    df2 = df2.merge(df1_, how='left', on='JOBID')

    return df1, df2

# --------------------------------------------------------------------------------------------------------------------------------------
# FINAL DATASETS

from app import cache
import json

# Store Data as JSON Format
@cache.memoize(timeout=0)
def getPermitsInProgressAsJson(file_location_1, file_location_2):
    
    # Permits in progress
    df1_inProgress, df2_inProgress = getPermitsInProgress(file_location_1, file_location_2)

    datasets = {
              "df1_inProgress":df1_inProgress.to_json(orient='split', date_format='iso'),
              "df2_inProgress":df2_inProgress.to_json(orient='split', date_format='iso'),
              } 

    return json.dumps(datasets)