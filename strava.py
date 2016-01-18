from polyline.codec import PolylineCodec
import base64
import sys
import stravalib.client as strava

client = strava.Client(access_token=sys.argv[3])
activity=client.get_activity(sys.argv[2])
a_coord=PolylineCodec().decode(activity.map.polyline)

minlat=1000
maxlat=0
minlng=1000
maxlng=0

for x in a_coord:
 if x[0]<minlat:
  minlat=x[0]
 elif x[0]>maxlat:
  maxlat=x[0]

 if x[1]<minlng:
  minlng=x[1]
 elif x[1]>maxlng:
  maxlng=x[1]

print round((maxlng-minlng)/5.00)

segments=client.explore_segments([minlat-0.01,minlng-0.01,maxlat+0.01,maxlng+0.01], activity_type=sys.argv[1], min_cat=None, max_cat=None)
segments+=client.explore_segments([minlat-0.01,minlng-0.01,maxlat+0.01,maxlng+0.01], activity_type=sys.argv[1], min_cat=None, max_cat=None)

seen = []
for value in segments:
 if value not in seen:
    seen.append(value)

for s in seen:
 match=0
 size=0
 segment=client.get_segment(s.id)
 s_coord=PolylineCodec().decode(segment.map.polyline)
 for s in s_coord:
  size+=1
  for a in a_coord:
   if (a[1]<=s[1]+0.0002 and a[1]>=s[1]-0.0002) and (a[0]<=s[0]+0.0002 and a[0]>=s[0]-0.0002):
    match+=1
    break 
 print segment.name,float(match)*100/size,'%'
