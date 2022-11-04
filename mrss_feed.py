import csv
import sys
from datetime import datetime
from github import Github

#Get parameter file to parse
filename = sys.argv[1]


#date
time = datetime.now()
iso_date = time.isoformat()
dayofweek = time.strftime("%a")
dayofmonth = time.strftime("%w")
month = time.strftime("%b")
year = time.strftime("%Y")
currenttime = time.strftime("%H") + ":" + time.strftime("%M") + ":" + time.strftime("%S")
shortTime = time.strftime("%H") +  time.strftime("%M")
datestring = dayofweek + ", " + dayofmonth + " " + month + " " + year + " " + currenttime
filedate = month + "_" + dayofmonth + "_" + year + "_" + shortTime
outfilename = 'tlnFeed_' + filedate + ".xml"
rokufilename = 'rokuFeed_' + filedate + ".json"

#Create beginning of feed
output = '<?xml version="1.0" encoding="UTF-8"?>'
output += '<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">'
output += '<channel><title><![CDATA[ VideoElephant ]]></title><link>https://mrss.videoelephant.com/</link><description><![CDATA[ VideoElephant MRSS Feed ]]></description>'
output += '<pubDate>' + datestring + '</pubDate>'

roku = '{'
roku += '"providerName": "Dollar Design School",'
roku += '"lastUpdated": "' + iso_date + '",'
roku += '"movies":['

with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ",")
    line_count = 0
    #row_count = sum(1 for row in csv_reader)
    #print(str(row_count) + " rows.")
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
            rokuURL = URL
            URL = URL.replace('&', '&amp;')
            duration = row[6].strip()
            tags = row[7].strip()
            thumbURL = row[8].strip()
            thumbURL = thumbURL.replace('&', '&amp;')
            tag1 = row[9].strip()
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
            roku += '{'
            roku += '"id": "' + guid + '",'
            roku += '"title": "' + title + '",'
            roku += '"shortDescription": "' + description + '",'
            roku += '"thumbnail": "' + thumbURL + '",'
            roku += '"releaseDate": "' + pubDate + '",'
            roku += '"genres": ["educational", "technology"],'
            roku += '"tags": ["' + tag1 +'"],'
            roku += '"content":{'
            roku += '"dateAdded": "' + pubDate + '",'
            roku += '"duration": "' + duration + '",'
            roku += '"videos":['
            roku += '{'
            roku += '"url": "' + rokuURL + '",'
            roku += '"quality": "FHD",'
            roku += '"videoType": "MP4",'
            roku += '"bitrate": "null"'
            roku += "}]}},"
            line_count += 1
    print(f'Processed {line_count} lines.')

#End Feed
output += "</channel>"
output += "</rss>"
roku = roku[:-1]
roku += "]}"

#update Roku on Github

#Roku
#Connect to Github Expires 11/4/2023
g = Github("mlassoff", "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")
repo = g.get_user().get_repo("rokuvideos")
contents = repo.get_contents("index.json")
updateMessage = "Feed update: " + iso_date
#repo.update_file(contents.path, updateMessage, roku, contents.sha, branch="main")
repo.update_file("index.json", updateMessage, roku, contents.sha)
print("Roku Github Repository Updated at https://github.com/mlassoff/rokuvideos")

#Syndicated Feed
g = Github("mlassoff", "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")
repo = g.get_user().get_repo("syndicatedvideos")
contents = repo.get_contents("index.xml")
updateMessage = "Added " + title
#repo.update_file(contents.path, updateMessage, roku, contents.sha, branch="main")
repo.update_file("index.json", updateMessage, output, contents.sha)
print("Roku Github Repository Updated at https://github.com/mlassoff/syndicatedvideos")


#write files locally
with open(outfilename , 'a') as out:
    out.write(output)
print("Written to File: " + outfilename)

with open(rokufilename, 'a') as out:
    out.write(roku)
print("Roku File: " + rokufilename)
