import sys
import time
import sqlite3
import json

def getcols(cursor): 
  d = [] 
  for idx, col in  enumerate(cursor.description):
     d.append(col[0])
  return d

def main(args=None):

   qt = sys.argv[1]

   root="/home/user/github/netmonitor/"

   start = time.time()

   dbconn = sqlite3.connect('file:'+root+'packets.db?mode=ro', uri=True)
   c = dbconn.cursor()

   """
    (ptime,srchost,srcport,dsthost,
   dstport,protocol,ptype,plen)"""

   if qt == "sources":
      query = """select sum(plen),srchost from packets where ptime >= date('now') 
         and  (not srchost like '192.168.%') and (not dsthost like '192.168.%') 
         and srchost!='localhost' and srchost!='ip6-localhost'
      group by srchost order by 1 desc LIMIT 20"""
   elif qt == "sourcesport":
      query = "select sum(plen),srchost,srcport from packets where ptime >= date('now') group by srchost,srcport order by 1 desc LIMIT 20"
   elif qt == "dests":
      query = """select sum(plen),dsthost from packets where ptime >= date('now') 
              and  (not srchost like '192.168.%') and (not dsthost like '192.168.%') 
              and dsthost!='localhost' and dsthost!='ip6-localhost'
              group by dsthost order by 1 desc LIMIT 20"""
   elif qt == "destsport":
      query = "select sum(plen),dsthost,dstport from packets where ptime >= date('now') group by dsthost,dstport order by 1 desc LIMIT 20"
   elif qt == "destsportnl":
      query = "select sum(plen),dsthost,dstport from packets where ptime >= date('now') and dsthost!='user-hp' group by dsthost,dstport order by 1 desc LIMIT 20"
   elif qt == "sourcesportsonly":
      query = """select srcport,sum(plen) from packets where ptime >= date('now') 
      and  (not srchost like '192.168.%') and (not dsthost like '192.168.%') 
      and srchost!='localhost' and srchost!='ip6-localhost'
      group by srcport order by 2 desc limit 10"""
   elif qt == "destsportsonly":
      query = """select dstport,sum(plen) from packets where ptime >= date('now') 
      and  (not srchost like '192.168.%') and (not dsthost like '192.168.%') 
      and dsthost!='localhost' and dsthost!='ip6-localhost'
      group by dstport order by 2 desc limit 10"""
   elif qt == "localnetsources":
      query = """select sum(plen),srchost from packets where ptime >= date('now') 
         and  (srchost like '192.168.%') 
         and srchost!='localhost' and srchost!='ip6-localhost'
      group by srchost order by 1 desc LIMIT 20""" 
   elif qt == "localnetdests":
      query = """select sum(plen),dsthost from packets where ptime >= date('now') 
         and  (dsthost like '192.168.%') 
         and dsthost!='localhost' and dsthost!='ip6-localhost'
      group by dsthost order by 1 desc LIMIT 20"""
   elif qt == "todaytotal":
      query = """select sum(plen) from packets 
      where ptime >= date('now')
      and srchost!='localhost' and dsthost!='localhost'
      and srchost!='ip6-localhost' and dsthost!='ip6-localhost'
      and
      (not srchost like '192.168.%')
      and
      (not dsthost like '192.168.%')
      """
   else:
      query = """select id,ptime,utime,srchost,srcport,dsthost,
   dstport,protocol,ptype,plen
   from packets 
   where ptime >= date('now')   
   and  (not srchost like '192.168.%') and (not dsthost like '192.168.%') 
   and srchost!='localhost' and dsthost!='localhost'
   and srchost!='ip6-localhost' and dsthost!='ip6-localhost'
   order by utime desc LIMIT 10"""

   jsone = json.JSONEncoder()
   #strftime('%H:%M:%S',start_date)
   #   query = "select * from packets where strftime('%H:%M:%S',ptime)='11:15:44' order by ptime desc limit 5"
   #query = 
   """SELECT * from packets 
   where ptime >= date('now') limit 5;"""

   rows = c.execute(query)
   results = []
   results.append(getcols(rows))
   for row in rows:
       results.append(row)

   print(jsone.encode(results))
   print("results:"+str(len(results)))
   print("elapsed: "+str(round(time.time()-start,3))+ " seconds")

   dbconn.close()

if __name__ == "__main__":
    main()




