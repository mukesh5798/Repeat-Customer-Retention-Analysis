import numpy as np
import pandas as pd
from datetime import time, timedelta
from sqlalchemy import create_engine
import os

new_file = r'c:\Users\Mukesh Maurya\Downloads\Lead_Total_Rupee On Time_20_07_2026_to_20_10_2026.csv'
df = pd.read_csv(new_file)

nld = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_New Loan Disbursed-Lite Version_2025-09-01 _ 2026-10-21_download_20261021052543.csv'
nld_df = pd.read_csv(nld)

nld_df.columns = nld_df.columns.str.lower()
nld_df.columns = nld_df.columns.str.replace(" ","_")


df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ","_")


df['application_date'] = pd.to_datetime(df['application_date'], errors='coerce')
df['screener_recommended_datetime'] = pd.to_datetime(df['screener_recommended_datetime'], errors='coerce')
df['screener_assign_datetime'] = pd.to_datetime(df['screener_assign_datetime'], errors='coerce')
df['initiated_datetime'] = pd.to_datetime(df['initiated_datetime'], errors='coerce')


df['application_date'] = df['application_date'].combine_first(df['screener_recommended_datetime']).combine_first(df['screener_assign_datetime']).combine_first(df['initiated_datetime'])


df['application_date'] = pd.to_datetime(df['application_date'], errors='coerce')

df['time_only'] = df['application_date'].dt.time

df['date_only'] = df['application_date'].dt.date


df['adjusted_date'] = np.where(
    df['time_only'] > time(18, 30),
    df['date_only'] + timedelta(days=1),
    df['date_only']
)

df['adjusted_date'] = pd.to_datetime(df['adjusted_date'])

df['reject'] = np.where(df['status'].str.lower() == 'reject',1,0)


new_file = pd.merge(df,nld_df,on='lead_id',how='left')


new_file['disbursal_count'] = np.where(new_file['loan_amount'] > 0,1,0)

new_file['final_disbursed_datetime'] = pd.to_datetime(new_file['final_disbursed_datetime'], errors='coerce')

new_file['final_disbursed_datetime_time_only'] = new_file['final_disbursed_datetime'].dt.time

new_file['final_disbursed_datetime_date_only'] = new_file['final_disbursed_datetime'].dt.date

new_file['disbursement_date'] = pd.to_datetime(new_file['disbursement_date'], errors='coerce')


new_file['final_disbursed_datetime_date_only_adjusted_date'] = np.where(
    new_file['final_disbursed_datetime_time_only'] > time(18, 30),
    new_file['disbursement_date'] + pd.Timedelta(days=1),
    new_file['disbursement_date']
)

new_file['final_disbursed_datetime_date_only_adjusted_date'] = pd.to_datetime(new_file['final_disbursed_datetime_date_only_adjusted_date'])

new_file['new_final_date'] = np.where(
    pd.isna(new_file['final_disbursed_datetime_date_only_adjusted_date']),
    new_file['adjusted_date'],
    np.where(
        new_file['final_disbursed_datetime_date_only_adjusted_date'] > new_file['adjusted_date'],
        new_file['final_disbursed_datetime_date_only_adjusted_date'],
        new_file['adjusted_date']
    )
)

new_file['new_final_date'] = pd.to_datetime(new_file['new_final_date'])

new_file['Day'] = pd.to_datetime(new_file['new_final_date'],errors='coerce').dt.day

new_file['Month'] = pd.to_datetime(new_file['new_final_date'],errors='coerce').dt.month_name()


new_file = new_file[new_file['user_type'].isin(['REPEAT'])]

new_file.to_csv("Repeat_Application.csv",index=False)


new_file = new_file[new_file['Month'].isin(['October','September'])]


pivot_data = pd.pivot_table(
    new_file,
    index='Day',
    columns='Month',
    values=['application_status','disbursal_count','loan_amount','reject'],
    aggfunc={
        'application_status':'sum',
        'disbursal_count':'sum',
        'loan_amount':'sum',
        'reject':'sum'
    },
    fill_value=0
)

pivot_data.columns = [f'{val}_{col}' for val, col in pivot_data.columns]
pivot = pivot_data.reset_index()


print(pivot)

pivot.to_csv("Repeat.csv",index=False)