#Import libraries
import pandas as pd
#from datetime import datetime

# Import dfs
from db.df_preprocessing import df1, df2

# --------------------------------------------------------------------------------------------------------------------------------------
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
df2_fil = df2.copy() 
#print(df2_fil['Status'].unique())

# --------------------------------------------------------------------------------------------------------------------------------------
