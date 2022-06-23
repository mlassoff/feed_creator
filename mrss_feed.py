import csv
import sys
from datetime import datetime

filename = sys.argv[1]

#date
time = datetime.now()
dayofweek = time.strftime("%a")
dayofmonth = time.strftime("%w")
month = time.strftime("%b")
year = time.strftime("%Y")
currenttime = time.strftime("%H") + ":" + time.strftime("%M") + ":" + time.strftime("%S")
shortTime = time.strftime("%H") +  time.strftime("%M") 
datestring = dayofweek + ", " + dayofmonth + " " + month + " " + year + " " + currenttime
filedate = month + "_" + dayofmonth + "_" + year + "_" + shortTime
outfilename = 'tlnFeed_' + filedate + ".xml"

#Create beginning of feed
output = '<?xml version="1.0" encoding="UTF-8"?>'
output += '<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">'
output += '<channel><title><![CDATA[ VideoElephant ]]></title><link>https://mrss.videoelephant.com/</link><description><![CDATA[ VideoElephant MRSS Feed ]]></description>'
output += '<pubDate>' + datestring + '</pubDate>'


with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ",")
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            guid = row[0].strip()
            title = row[1].strip()
            description = row[2].strip()
            pubDate = row[3].strip()
            category = row[4].strip()
            URL= row[5].strip()
            URL = URL.replace('&', '&amp;')
            duration = row[6].strip()
            tags = row[7].strip()
            thumbURL = row[8].strip()
            thumbURL = thumbURL.replace('&', '&amp;')
            output += '<item>'
            output += '<guid isPermaLink="false">' + guid + '</guid>' 
            output += '<title><![CDATA[' + title + ']]></title>'
            output += '<description><![CDATA[' + description + ']]></description>'
            output += '<pubDate>' + pubDate + '</pubDate>'
            output += '<enclosure url="' + URL + '" length="' + duration + '" type="video/mp4"/>'
            output += '<media:content type="video/mp4" url="' + URL + '" duration="' + duration + '" lang="en">'
            output += '<media:tags><![CDATA[' + tags + ']]></media:tags>'
            output += '<media:thumbnail url="' + thumbURL + '"/>'
            output += '<media:credit role="producer" scheme="urn:ebu"><![CDATA[ Tech Learning Network ]]></media:credit>'
            output += '</media:content>'
            output += '</item>'
            line_count += 1
    print(f'Processed {line_count} lines.')

#End Feed
output += "</channel>"
output += "</rss>"

with open(outfilename , 'a') as out:
    out.write(output)
print("Written to File: " + output)
