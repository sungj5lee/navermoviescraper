import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

df=pd.DataFrame()
url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code='
page='&page='
list=[174835, 50176, 81888, 15555, 86722, 151728]

for i in list:
  page_num=0
  while(True):
    page_num=page_num+1
    html = requests.get(url+str(i)+page+str(page_num))
    soup = BeautifulSoup(html.content, 'html.parser')
    tmp_tag=soup.find("div", {"class": "score_result"})
    if tmp_tag is not None:
      list_tag=tmp_tag.ul.find_all(recursive=False)
      for li_tag in list_tag:
        tmp_row={}
        tmp_row['movie_id']=i
        tmp_row['score']=li_tag.find(class_="star_score").em.string
        viewer_tag=li_tag.find(class_="score_reple").find(class_="ico_viewer")
        if viewer_tag==None:
          tmp_row['viewerTag']=None
        else:
          tmp_row['viewerTag']=viewer_tag.string
        spoiler_tag=li_tag.find(class_="score_reple").find(id=re.compile(r'^_text_spo'))
        if spoiler_tag==None:
          tmp_row['IsSpoiler']=False
        else:
          tmp_row['IsSpoiler']=True
        # print(i, page_num)
        tmp_row['comment']=li_tag.find(class_="score_reple").find(id=re.compile(r'^_filtered_ment')).get_text(strip=True)
        dt_tag=li_tag.find(class_="score_reple").find("dt").find_all("em")
        tmp_row['username']=dt_tag[0].find("span").string
        tmp_row['date']=dt_tag[1].string
        a_tag_text=dt_tag[0].find("a")['onclick']
        tmp_row['comment_id']=a_tag_text.partition("Nid(")[2].partition(",")[0]
        tmp_row['LikeDislike']=[tag.string for tag in li_tag.find(class_="btn_area").find_all("strong")]
        #print(tmp_row)
        df=df.append(tmp_row, ignore_index=True)
        #print(df.head())
    if soup.find(class_="pg_next")==None:
      break
    time.sleep(0.5)

df=df.applymap(str)
df.to_csv("movie.csv")
