import requests
import pandas as pd
pd.set_option('display.max_columns', None)
github_api_url = "https://api.github.com/repos/squareshift/stock_analysis/contents/"
response = requests.get(github_api_url)
#print(response)
#print(response.status_code)
# a = response.json()
a = response.text
#print(a)
b = response.json()
#print(b)
csv_files = [file['download_url'] for file in b if file['name'].endswith('.csv')]
#print("files_count", len(csv_files))
#print(csv_files)
a=csv_files[0]
csv_file = csv_files.pop()
#print(csv_file)
#print(type(csv_file))
d = pd.read_csv(csv_file)
#print(d)
dataframes=[]
file_names=[]
for url in csv_files:
    file_name = url.split("/")[-1].replace(".csv", "")
    df = pd.read_csv(url)
    df['Symbol'] = file_name
    dataframes.append(df)
    file_names.append(file_name)

# print(file_names)
# print(dataframes)
combined_df = pd.concat(dataframes, ignore_index=True)
# print(combined_df)
o_df = pd.merge(combined_df,d,on='Symbol',how='left')
result = o_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
print(result)






