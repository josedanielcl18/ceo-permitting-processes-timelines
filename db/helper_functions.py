#Preprocessing Functions

#Create Pools of Permits based on 'JOBTYPEDESCRIPTION', 'Application-Type' and 'CLASSOFPERMIT'
def CreatePools(df):

    #Create Pool for Commercial Permits: Interior/Others
    mask = df['JOBTYPEDESCRIPTION']== '1. Commercial Final Permit'
    df.loc[mask, 'pools'] = 'Commercial P.: Interior/Others'

    #Create Additional Pool for Commercial Permits: New/Addition
    mask = (df['JOBTYPEDESCRIPTION']== '1. Commercial Final Permit') & ((df['Application-Type']== '(01) New') | (df['Application-Type']== '(02) Addition'))
    df.loc[mask, 'pools'] = 'Commercial P.: New/Addition'

    #Create Pool for Residential Permits: Single Detached
    mask = df['JOBTYPEDESCRIPTION']== '6. House Building Permit'
    df.loc[mask, 'pools'] = 'Residential P.: Single Detached'

    #Create Additional Pool for Residential Permits: Semi-Detached
    mask = (df['JOBTYPEDESCRIPTION']== '6. House Building Permit') & ((df['CLASSOFPERMIT']== 'Semi-Detached House (210)') | (df['CLASSOFPERMIT']== 'Semi-Detached Condo (215)') | (df['CLASSOFPERMIT']== 'Duplex (210)') | (df['CLASSOFPERMIT']== 'Duplex Condo (215)'))
    df.loc[mask, 'pools'] = 'Residential P.: Semi-Detached'

    #Create Additional Pool for Row House Permits
    mask = (df['JOBTYPEDESCRIPTION']== '6. House Building Permit') & ((df['CLASSOFPERMIT']== 'Row House (330)') | (df['CLASSOFPERMIT']== 'Row House Condo (335)'))
    df.loc[mask, 'pools'] = 'Row House'

    #Create Pool for Residential Permits: HIP
    mask = df['JOBTYPEDESCRIPTION']== 'Home Improvement Permit'
    df.loc[mask, 'pools'] = 'Residential P.: HIP'

    #Create Pool for Major Development Permits
    mask = df['JOBTYPEDESCRIPTION']== 'Major Development Permit'
    df.loc[mask, 'pools'] = 'Major Development Permit'

    #Create Pool for Minor Development Permits
    mask = df['JOBTYPEDESCRIPTION']== 'Minor Development Permit'
    df.loc[mask, 'pools'] = 'Minor Development Permit'

    return df

# Function to Assign STATUS OF APPLICATIONS based on last process completed and OUTCOME. 
def GetStatus(df):
  # "0. New"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'New'), 'Status'] = "0. New"
  # "1.Queue for Intake Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Info Received - Intake') & (df['OUTCOME'] == 'Information Received'), 'Status'] = "1.Intake Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Enter Application') & (df['OUTCOME'] == 'Application Accepted'), 'Status'] = "1.Intake Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'Intake Review'), 'Status'] = "1.Intake Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'Intake - Payment and More Info Requested'), 'Status'] = "1.Intake Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'Intake - More Info Requested'), 'Status'] = "1.Intake Review"
  # "2.On hold with customer at Intake"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Building Intake Review') & (df['OUTCOME'] == 'Payment and More Info Required'), 'Status'] = "2.Intake - Payment and/or More Info Requested"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Building Intake Review') & (df['OUTCOME'] == 'Payment Required'), 'Status'] = "2.Intake - Payment and/or More Info Requested"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Building Intake Review') & (df['OUTCOME'] == 'More Info Required'), 'Status'] = "2.Intake - Payment and/or More Info Requested"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Building Intake Review') & (df['OUTCOME'] == 'More Information Required'), 'Status'] = "2.Intake - Payment and/or More Info Requested"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'Intake - Payment Required'), 'Status'] = "2.Intake - Payment and/or More Info Requested"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Intake') & (df['OUTCOME'] == 'From Applicant'), 'Status'] = "2.Intake - Payment and/or More Info Requested"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Intake') & (df['OUTCOME'] == 'From Applicant Via Email'), 'Status'] = "2.Intake - Payment and/or More Info Requested"
  # "3.With DO or Pending Planning and Zoning Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Restamp/Zoning Signoff Completed') & (df['OUTCOME'] == 'DP Approval Outstanding/pending'), 'Status'] = "3.With DO or Pending Planning and Zoning Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Restamp/Zoning Signoff Completed') & (df['OUTCOME'] == 'Reassigned'), 'Status'] = "3.With DO or Pending Planning and Zoning Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Restamp/Zoning Signoff Requested') & (df['OUTCOME'] == 'Assigned re-stamp'), 'Status'] = "3.With DO or Pending Planning and Zoning Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Building Intake Review') & (df['OUTCOME'] == 'Application Complete'), 'Status'] = "3.With DO or Pending Planning and Zoning Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'With Development Officer'), 'Status'] = "3.With DO or Pending Planning and Zoning Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Plans Examination Review') & (df['OUTCOME'] == 'Restamp Required'), 'Status'] = "3.With DO or Pending Planning and Zoning Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Assign Plans Examination') & (df['OUTCOME'] == 'Restamp'), 'Status'] = "3.With DO or Pending Planning and Zoning Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'Pending Planning and Zoning Review'), 'Status'] = "3.With DO or Pending Planning and Zoning Review"
  # "4. Queue for Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Restamp/Zoning Signoff Requested') & (df['OUTCOME'] == 'Not Required'), 'Status'] = "4.To Be Assigned"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Restamp/Zoning Signoff Completed') & (df['OUTCOME'] == 'Restamp/Zoning Signoff completed'), 'Status'] = "4.To Be Assigned"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Restamp/Zoning Signoff Completed') & (df['OUTCOME'] == 'No DP required'), 'Status'] = "4.To Be Assigned"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'To Be Assigned'), 'Status'] = "4.To Be Assigned"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'System Process - Commercial Building Permit') & (df['OUTCOME'] == 'To Be Assigned'), 'Status'] = "4.To Be Assigned"
  # "5. In Plans Examination"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Restamp/Zoning Signoff Completed') & (df['OUTCOME'] == 'Restamp/Zoning Signoff Completed'), 'Status'] = "5.In Plans Examination"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Assign Plans Examination') & (df['OUTCOME'] == 'With P.E.'), 'Status'] = "5.In Plans Examination"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Assign Plans Examination') & (df['OUTCOME'] == 'With Team Leader'), 'Status'] = "5.In Plans Examination"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'Remove ISSUED date send to PE'), 'Status'] = "5.In Plans Examination"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'In Plans Examination'), 'Status'] = "5.In Plans Examination"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Info Received - Plans Examination Review') & (df['OUTCOME'] == 'Received'), 'Status'] = "5.In Plans Examination"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Information Received') & (df['OUTCOME'] == 'Information Received'), 'Status'] = "5.In Plans Examination"
  #df.loc[(df['OBJECTDEFDESCRIPTION'] == 'System Process - Initiate Plans Assignment') & (df['OUTCOME'] == 'Complete'), 'Status'] = "5.In Plans Examination"
  # "6. On hold with customer at PER"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Plans Examination Review') & (df['OUTCOME'] == 'More Info Required'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Plans Examination Review') & (df['OUTCOME'] == 'Requesting More Information'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Plans Examination Review') & (df['OUTCOME'] == 'Payment and More Info Required'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Plans Examination Review') & (df['OUTCOME'] == 'Payment Required'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Plans Examination Notification') & (df['OUTCOME'] == '2nd Notification'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Plans Examination Notification') & (df['OUTCOME'] == '3rd Notification'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Plans Examination Notification') & (df['OUTCOME'] == 'Expiry Notification'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Plans Examination Notification') & (df['OUTCOME'] == 'Final Notification'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'Plans Exam Review - More Info Requested'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'Plans Exam Review - Payment and More Inf'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'Plans Exam Review - Payment Required'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Job Status Correction') & (df['OUTCOME'] == 'More Information Required/Requested'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Plans Examination Notification') & (df['OUTCOME'] == 'Review Final Notification'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Plans Examination Review') & (df['OUTCOME'] == 'From applicant'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Plans Examination Review') & (df['OUTCOME'] == 'From Applicant'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Plans Examination Review') & (df['OUTCOME'] == 'From applicant via Email'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Info Requested - Plans Examination Review') & (df['OUTCOME'] == 'From Applicant Via Email'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'More Information Requested') & (df['OUTCOME'] == 'Information Required'), 'Status'] = "6.More Info Requested - Plans Examination Review"
  # "8.Plans Revision Intake Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Request Plans Revision') & (df['OUTCOME'] == 'Received'), 'Status'] = "8.Plans Revision Intake Review"
  df.loc[(df['OBJECTDEFDESCRIPTION'] == 'Assign Revision Review') & (df['OUTCOME'] == 'Assign to PE'), 'Status'] = "8.Plans Revision Intake Review"
  return df