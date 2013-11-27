import MySQLdb
import json, csv, time

def main():
    db = MySQLdb.connect(host="mbdb.aniv.info", user="tweets", passwd="stuartdiamond", db="lgsttweets")
    c = db.cursor()
    c.execute("SELECT tweets FROM tweets")
    result = c.fetchall()
    data = []
    for row in result:
        # print row[0].replace('\n','')
        j = json.loads(row[0].replace('\n',''))
        data.append(j)

    w = csv.writer(open('tweets.csv', 'wb'))
    for d in data:
        try:
            date_str = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(int(d.get('date',0))/1000))
            w.writerow([d.get('index',0), date_str, d.get('username',0), d.get('retweets_and_replies',0), d.get('tweet',0).encode('utf8', 'ignore')])
        except KeyError as e:
            print d
            continue

    db.close()


if __name__ == "__main__":
    main()
    
