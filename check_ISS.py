import ssl

ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

import os
os.chdir("D:/M2CAD - source/iss")
import datetime

def check_stand(stand, lnk):
    with urllib.request.urlopen(lnk) as f:
        page = f.read()
        page_soup = BeautifulSoup(page, "html.parser")

        for stat in page_soup.select_one(
            "body > div > div > div.grid-x.grid-margin-x.margin-top-2 > div:nth-child(1) > div > div.card-section > p:nth-child(1) > span.label.warning"
        ) or page_soup.select_one(
            "body > div > div > div.grid-x.grid-margin-x.margin-top-2 > div:nth-child(1) > div > div.card-section > p:nth-child(1) > span.label.success"
        ):
            # print(stand, stat.text)
            return stat.text


# read iss list
df = pd.read_csv("iss_list.txt", dtype=str)
df.fillna(value="<start_tracking>", inplace=True)
status = [check_stand(stand, lnk) for stand, lnk in zip(df["standard"], df["lnk"])]
# print(status)

# make diff of status
stat_old = df.loc[:, "stat"]
stat_cur = pd.Series(status)
diff = stat_old.compare(stat_cur)
idx = diff.index

if idx.empty is True:
    print(f"There is no update from last check: {datetime.datetime.fromtimestamp(os.path.getmtime('iss_list.txt'))}")
else:
    df.loc[idx, ["standard","stat"]].to_csv("iss_prev_stats.txt", index=False)
    print("Generated report as iss_prev_stats.txt; updates are:")
    print(df.loc[idx, ["standard","stat"]])
    df["stat"] = stat_cur
    df.to_csv("iss_list.txt", index=False)
    print("Finished!")

