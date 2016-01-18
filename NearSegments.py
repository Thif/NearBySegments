from flask import Flask,render_template
from polyline.codec import PolylineCodec
import base64
import sys
import stravalib.client as strava



app = Flask(__name__)

@app.route("/")
def hello():
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

    segments=client.explore_segments([minlat,minlng,maxlat,maxlng], activity_type=sys.argv[1], min_cat=None, max_cat=None)
    matched_segments=[]
    seen = []
    segments_poly=[]
    for value in segments:
     if value not in seen:
        seen.append(value)
    
    for s in seen:
     match=0
     size=0
     segment=client.get_segment(s.id)
     s_coord=PolylineCodec().decode(segment.map.polyline)
     for s in range(0,len(s_coord),1):
      size+=1
      for a in range(0,len(a_coord),1):
       if (a_coord[a][1]<=s_coord[s][1]+0.0002 and a_coord[a][1]>=s_coord[s][1]-0.0002) and (a_coord[a][0]<=s_coord[s][0]+0.0002 and a_coord[a][0]>=s_coord[s][0]-0.0002):
        match+=1
        break 
     matched_segments.append(segment.name)
     segments_poly.append(s_coord)
    return render_template('NearSegments.html',matched_segments=matched_segments,segments_poly=segments_poly,polyline=a_coord)



if __name__ == "__main__":
    app.run(debug=True)
