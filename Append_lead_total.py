import pandas as pd
import os

file_1 = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_Lead Total_20-07-2026 _ 31-07-2026_download_20261021153718.csv'
file_2 = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_Lead Total_01-08-2026 _ 10-08-2026_download_20261021155152.csv'
file_3 = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_Lead Total_11-08-2026 _ 20-08-2026_download_20261021160903.csv'
file_4 = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_Lead Total_21-08-2026 _ 31-08-2026_download_20261021161848.csv'
file_5 = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_Lead Total_01-09-2026 _ 10-09-2026_download_20261021163441.csv'
file_6 = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_Lead Total_11-09-2026 _ 20-09-2026_download_20261021164018.csv'
file_7 = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_Lead Total_21-09-2026 _ 30-09-2026_download_20261021164552.csv'
file_8 = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_Lead Total_01-10-2026 _ 12-10-2026_download_20261021103628.csv'
file_9 = r'c:\Users\Mukesh Maurya\Downloads\Rupee on time_Lead Total_13-10-2026 _ 20-10-2026_download_20261021104023.csv'

df_1 = pd.read_csv(file_1)
df_2 = pd.read_csv(file_2)
df_3 = pd.read_csv(file_3)
df_4 = pd.read_csv(file_4)
df_5 = pd.read_csv(file_5)
df_6 = pd.read_csv(file_6)
df_7 = pd.read_csv(file_7)
df_8 = pd.read_csv(file_8)
df_9 = pd.read_csv(file_9)

df = pd.concat([df_1,df_2,df_3,df_4,df_5,df_6,df_8,df_9],ignore_index=True)

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ","_")

df = df[df['application_status']>0]

df = df.drop_duplicates(subset='lead_id')

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

output_path = os.path.join(downloads_path, "Lead_Total_Rupee On Time_20_07_2026_to_20_10_2026.csv")

df.to_csv(output_path, index=False)
print(df)