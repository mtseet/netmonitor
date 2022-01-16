#!/usr/bin/python3

import sys
import time
import sqlite3
import subprocess

root = "/home/user/github/netmonitor"
dbconn = sqlite3.connect(root+'/packets.db')

c = dbconn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS packets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ptime DATETIME,
  utime DATETIME,
  srchost VARCHAR(128),
  srcport VARCHAR(8),
  dsthost VARCHAR(128),
  dstport VARCHAR(8),
  protocol VARCHAR(8),
  ptype VARCHAR(32),
  plen INT
)''')


c.execute('CREATE INDEX IF NOT EXISTS idxsrchost ON packets (srchost);');
c.execute('CREATE INDEX IF NOT EXISTS idxdsthost ON packets (dsthost);');
c.execute('CREATE INDEX IF NOT EXISTS idxptime ON packets (ptime);');


def gethostandport(host,proto):

    if (host.find('.') != -1 and (proto == "tcp" or proto == "UDP")):
        name = host[0:host.rindex(".")]
        port = host[host.rindex(".")+1:len(host)].replace(":","")
    else:
        name = host
        port = 'none'

    name = name.replace(":","")

    return  [name,port]

start = time.time()
zlenc = 0
commitstatus = 0
commitafter = 100
ec = 0
count = 0
pmap = {}

cmd="tcpdump -q -p -i any -tttt -l tcp or udp or icmp"
stream = subprocess.Popen(cmd.split(" "),
   shell=False,
   bufsize=1024000,
   stdout=subprocess.PIPE)

for aline in stream.stdout:
    try:
        line = aline.decode("utf-8").replace("\n","")
        #print(line)

        parts = line.split(", ")

        #print(parts)
        host = parts[0].split(" ")
        #print(host)

        ptime = host[0] + " " + host[1]

        pdate = host[0]

        packetType = host[2]

        protocol = host[6]

        tmpa = gethostandport(host[3],protocol)
        srchost = tmpa[0]
        srcport = tmpa[1]
        tmpa = gethostandport(host[5],protocol)
        dsthost = tmpa[0]
        dstport = tmpa[1]

        plen = "0"
        if len(parts)>1:
           plen = parts[len(parts)-1]
        elif len(host)<8:
           plen = "0"
        else:
           plen = host[7]

        plen = plen.replace("length ","")
        plen = plen.replace("len ","")

        try:
          plen = int(plen)
        except:
          continue

        if plen==0:
           zlenc = zlenc + 1
           continue

        """
        print("Packet:")
        print(ptime)
        print(packetType)
        print(srchost)
        print(srcport)
        print(dsthost)
        print(dstport)
        print(protocol)
        print(plen)
        print("")
        """

        pkey = packetType+srchost+srcport+dsthost+dstport+protocol

        sptime = ""
        spdate = ""

        isnew = False
        if pmap.get(pkey) == None:
            pmap[pkey] = [ptime,plen]
            isnew = True
        else:
            sptime = pmap[pkey][0]
            spdate = sptime.split(" ")[0]
            if pdate != spdate:
               pmap[pkey] = [ptime,plen]

        if (not isnew) and (pdate == spdate):
            nplen = pmap[pkey][1] + plen
            pmap[pkey][1] = nplen

            c.execute( """update packets set plen=?,
            utime=? where 
            ptime=? and srchost=? and srcport=? and
            dsthost=? and dstport=? and protocol=?""",
            (nplen,ptime,sptime,srchost,srcport,
            dsthost,dstport,protocol))
        else:
            c.execute( """INSERT INTO packets 
            (ptime,utime,srchost,srcport, 
            dsthost,dstport,protocol,ptype,plen) VALUES( 
            ?,?,?,?,?,?,?,?,?)""", 
            (ptime,ptime,srchost,srcport,dsthost,dstport,
             protocol,packetType,plen))

        commitstatus = commitstatus + 1

        if commitstatus > commitafter:
           dbconn.commit()
           commitstatus = 0

        count = count + 1
    except Exception as err:
        ec = ec + 1
        print(line)
        print("Processed: "+str(count))
        print(str(ec)+"**:"+line)
        print(err)
        commitstatus = 0
        #raise


if commitstatus >0 and commitstatus <= commitafter:
   dbconn.commit()

for row in c.execute('SELECT * FROM packets LIMIT 2'):
    print(row)

dbconn.close()

print("total:"+str(count))
print("zlenc:"+str(zlenc))
print("elapsed: "+str(round(time.time()-start,3))+ " seconds")



