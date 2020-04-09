import os
import pandas as pd
from pandas.io.json import json_normalize
import json
from subprocess import run, PIPE, Popen
import subprocess
import argparse
import fnmatch
import numpy as np
import time
import re
from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser()
parser.add_argument("dir", help = "Enter path of Directory")
parser.add_argument("-u", "--unix", action="store_true", dest="time", default=False, help="This to manage time")
args = parser.parse_args()

path = args.dir
print("path to search for json files ==> " , path)

files=[]
for file in listdir(path):
    if '.json' in file:
        files.append(file)
print("files detected :\n", files)

checksums = {}
duplicates = []

for filename in files:
    # Use Popen to call the md5sum utility
    with Popen(["md5sum", filename], stdout=PIPE) as proc:
        checksum, _ = proc.stdout.read().split()

        # Append duplicate to a list if the checksum is found
        if checksum in checksums:
            duplicates.append(filename)
        checksums[checksum] = filename

print(f"Found Duplicates: {duplicates}")

for file in files:
    To_Url_lst=[]
    lst = []
    Operating_System_lst = []
    From_Url_lst=[]
    lst.clear()
    Operating_System_lst.clear()
    From_Url_lst.clear()
    To_Url_lst.clear()

    records = [json.loads(line) for line in open(file)]
    df = pd.DataFrame(records)
    df = df[['a','tz','r','u','t','ll','hc','cy']]
    df['web_Browser']= df.a.str.extract(r'^([a-zA-Z]*/)')   #extract any ch end with /
    df['web_Browser']= df.a.str.extract(r'^([a-zA-Z]*)')    #then remove   / extract chs only
    df['operating_system']= df.a.str.extract(r'(\([^(]+\))', expand=True)

    for i in df['operating_system']:
        i = str(i)
        lst = i.split(" ")
        x = re.sub("\(","",lst[0])
        x = re.sub(";","",x)
        Operating_System_lst.append(x)
    df['operating_system']= Operating_System_lst
                                                     # OUTPut       //t.co/N
    df['from_url'] = df.r.str.extract(r'(//[a-zA-Z]*.[a-zA-Z]*.[a-zA-Z]*)', expand=True)   # output //www.facebook.com

    for i in df['from_url']:
        i = str(i)
        x = re.sub("//","",str(i))
        if "/" in x:
            x = x[0:x.index("/")]
            From_Url_lst.append(x)
        else:
            From_Url_lst.append(x)
    From_Url_lst
    df['from_url'] = From_Url_lst

    df['to_url'] = df.u.str.extract(r'(.*[.gov])', expand=True)
    #df['to_url'] = df.u.str.extract(r'(//[a-zA-Z]*.[a-zA-Z]*.[a-zA-Z])', expand=True) # remove the beggining http // ..
    for i in df['to_url']:
        i = str(i)
        x = re.sub("http://","",str(i))
        if "/" in x:
            x = x[0:x.index("/")]
            To_Url_lst.append(x)
        else:
            To_Url_lst.append(x)
    From_Url_lst
    df['to_url'] = To_Url_lst

    df.rename(columns = {'tz' : 'time_zone', 'cy': 'city','t': 'time_in','hc':'time_out'}, inplace = True)
    df['ll'] = df['ll'].fillna('')
    df[['longitude','latitude']] = pd.DataFrame(df['ll'].values.tolist(), index = df.index)
    df = df[['web_Browser','operating_system','from_url','to_url','city','longitude','latitude','time_zone','time_in','time_out']]
    #df.replace(r'\s+', np.nan)
    df = df.replace(to_replace = "nan" , value = np.nan)
    df = df.replace(to_replace = r'\s+' , value = np.nan)
    df = df.dropna(axis=0)

    if not args.time:
        timestamp_lst_in = []
        timestamp_lst_out = []
        for i, row in df.iterrows():
            s1 = pd.to_datetime(row['time_in'], unit = 's').tz_localize(row['time_zone']).tz_convert('UTC')
            s2 = pd.to_datetime(row['time_out'], unit = 's').tz_localize(row['time_zone']).tz_convert('UTC')
            timestamp_lst_in.append(s1)
            timestamp_lst_out.append(s2)
        df['time_in'] =timestamp_lst_in
        df['time_out'] =timestamp_lst_out

    df.to_csv(path+"/target/"+file+".csv" , header=True , index=False )
    print(" Done writting to the path file : "+file+".csv")
