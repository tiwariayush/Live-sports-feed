#!/usr/bin/python
# coding=utf-8
from bs4 import BeautifulSoup
from urllib import urlopen
try:
  import json
except ImportError:
  import simplejson as json

football_page=urlopen("http://www.livescores.com").read()
cricket_page=urlopen('http://static.cricinfo.com/rss/livescores.xml').read()
football_soup=BeautifulSoup(football_page)
cricket_soup=BeautifulSoup(cricket_page)

#FOOTBALL DATA SCRAPING STARTS HERE

matches=[]
new=[]
new_matches=[]
links=[]
newlist=[]

teams_important=["Arsenal","Chelsea","Liverpool","Manchester City","Manchester United","Tottenham","Napoli","Juventus","Inter","AC Milan","Barcelona","Athletico Madrid","Real Madrid","Bayern Munich","Borussia Dortmund","Bayer Leverkusen","Monaco","Paris Saint Germain","Marseille","Spain","Germany","Argentina","Colombia","Belgium","Uruguay","Switzerland","Netherlands","Italy","England","Brazil","Chile","United States","Portugal","Greece","Bosnia and Herzegovina","Ivory Coast","Croatia","Russia","Ukraine","Cote d'Ivoire"]

for data in football_soup.findAll('tr'):
  for rows in data.findAll('td'):
    for link in rows.findAll('a'):
      match = data.get_text().replace('\n','').replace('\t','').replace(' - ','-').split()
      matches.append(match)
      single_link=link['href']
      links.append(single_link)
      for item in match:
          string=" ".join(match)
      newlist.append(string)

final_matches=[]
for item in newlist:
  for team in teams_important:
    if item.lower().find(team.lower()) >= 0:
     final_matches.append(item)
     break

soccer_dict_pre=dict(zip(newlist, links))

final_links=[]
for item in links:
  for team in teams_important:
    if item.lower().find(team.lower()) >=0 :
      final_links.append(item)
      break

final_links_pre=[]
for item in final_matches:
   for key ,val in soccer_dict_pre.iteritems():
     if item == key:
       final_links_pre.append(val)
       break

final=[]
for item, link in zip(final_matches, final_links_pre):
    dict_ma={"text":item,
            "link":link}
    final.append(dict_ma)

f=open("football_data.py",'wb+')
f.write('# coding=utf-8 \n')
f.write('results=[')
for item in newlist:
  f.write( '"%s",\n' % item.encode('utf-8'))
f.write(']\n')
f.write('match_links=[')
for item in links:
  f.write( '"%s",\n' % item.encode('utf-8'))
f.write(']\n')
f.write('soccer_dict=dict(zip(results,match_links))')
f.close()

with open("foo_data.txt",'wb+') as result:
  json.dump(final, result)
result.close()


#CRICKET DATA SCRAPING STARTS HERE

important_cric_teams=["India","Australia","Pakistan","Zimbabawe","Kenya","England","South Africa","New Zealand","Kenya","Sri Lanka","West Indies","Bangladesh","Ireland","Netherlands","Afghanistan","Scotland","Chennai Super Kings","Delhi Daredevils","Kings XI Punjab","Kolkata Knight Riders","Mumbai Indians","Mumbai Indians","Pune Warriors India","Rajasthan Royals","Royal Challengers Bangalore","Sunrisers Hyderabad"]

cricket_item=cricket_soup.findAll('item')

cric_match_score=[]
for item in cricket_item:
  match=item.description.string
  cric_match_score.append(match)

cric_links=[]
for item in cricket_item:
  link=item.guid.string
  cric_links.append(link)

ini_cric_dict=dict(zip(cric_match_score, cric_links))

final_cric_score=[]
for item in cric_match_score:
  for team in important_cric_teams:
    if item.lower().find(team.lower()) >= 0:
      final_cric_score.append(item)
      break

final_cric_links=[]
for item in final_cric_score:
  for key , val in ini_cric_dict.iteritems():
    if key == item :
      final_cric_links.append(val)
      break

final_cric=[]
for item , link in zip(final_cric_score, final_cric_links):
  dict_cric={"text":item,
             "link":link}
  final_cric.append(dict_cric)

with open("cric_data.txt", 'wb+') as cric_res:
  json.dump(final_cric, cric_res)
cric_res.close()
