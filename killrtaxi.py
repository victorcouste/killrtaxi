from flask import Flask, render_template,request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import requests
import json
import Geohash

# configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('KILLRTAXI_SETTINGS', silent=True)

GoogleMaps(app)

@app.route("/")
def home():
    return render_template('home.html')

# TAXI API from https://github.com/PatrickCallaghan/datastax-taxi-app
# update vehicles location mvn clean compile exec:java -Dexec.mainClass="com.datastax.taxi.Main" -DcontactPoints=localhost
# Start Web server mvn jetty:run
# all mvt for vehicle 1 for 1 day http://localhost:8080/datastax-taxi-app/rest/getmovements/1/20160112
# All vehicles in a geohash http://localhost:8080/datastax-taxi-app/rest/getvehicles/gcrf
# All vehicles around around me at 5 km distance http://localhost:8080/datastax-taxi-app/rest/search/52.53956077140064/-0.20225833920426117/5
# All tile available http://localhost:8080/datastax-taxi-app/rest/gettiles

#Geohash
#https://github.com/vinsci/geohash/
#Geohash.encode(42.6, -5.6, precision=5)
#Geohash.decode('ezs42')

@app.route("/getme", methods=['GET', 'POST'])
def getme():
    error = None
    debug=""
    vehicule_map = Map(
                identifier="view-side",
                lat=37.4419,
                lng=-122.1419,
                style="height:700px;width:700px;margin:0;",
                zoom=5
    )
    if request.method == 'POST':
        if request.form['lon'] and request.form['lat'] and request.form['dist']:
            lon=request.form['lon']
            lat=request.form['lat']
            dist=request.form['dist']
            url="http://localhost:8080/datastax-taxi-app/rest/search/"+lat+"/"+lon+"/"+dist
            response=requests.get(url)
            result=""
            if(response.ok):
                result=response.content
            else:
                return render_template('getme.html',error=error,vehicule_map=vehicule_map,debug=debug)

            #result='[{"vehicle":"2","date":1452986285175,"latLong":{"lat":54.96848201388808,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},' \
            #      '{"vehicle":"2","date":1452986259330,"latLong":{"lat":54.968382013888075,"lon":0.39953558097359565},"tile":"u1b29nd","tile2":""},{"vehicle":"2","date":1452986233158,"latLong":{"lat":54.96828201388807,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986218088,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986198654,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986180302,"latLong":{"lat":54.96858201388808,"lon":0.3999355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986173759,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986169289,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986150746,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986129093,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986116895,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""}]'
            jData = json.loads(result)
            markers_map=[]
            for d in jData:
                markers_map.append((d["latLong"]["lat"],d["latLong"]["lon"]))

            nbmvts=len(jData)
            #debug=result
            vehicule_map = Map(
                identifier="view-side",
                lat=lat,
                lng=lon,
                style="height:700px;width:700px;margin:10;",
                zoom=12,
                markers=markers_map
                #markers=[(54.96848201388808, 0.39963558097359564),(54.968382013888075, -0.39953558097359565)]
            )

            return render_template('getme.html', nbmvts=nbmvts,lon=lon,lat=lat,dist=dist,vehicule_map=vehicule_map,debug=debug)
            #else:
            #    error=response.raise_for_status().str
    #else:
    #    url="http://localhost:8080/datastax-taxi-app/rest/gettiles
    #    response=requests.get(url)
    return render_template('getme.html',error=error,vehicule_map=vehicule_map,debug=debug)


@app.route("/gettile", methods=['GET', 'POST'])
def gettile():
    #form = {"vehicle_id": vehicle_id}
    #request.form['username']
    error = None
    debug=""
    vehicule_map = Map(
                identifier="view-side",
                lat=37.4419,
                lng=-122.1419,
                style="height:700px;width:700px;margin:0;",
                zoom=5
    )
    if request.method == 'POST':
        if request.form['tile']:
            tile=request.form['tile']
            url="http://localhost:8080/datastax-taxi-app/rest/getvehicles/"+tile
            response=requests.get(url)
            result=""
            if(response.ok):
                result=response.content

            #result='[{"vehicle":"2","date":1452986285175,"latLong":{"lat":54.96848201388808,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},' \
            #      '{"vehicle":"2","date":1452986259330,"latLong":{"lat":54.968382013888075,"lon":0.39953558097359565},"tile":"u1b29nd","tile2":""},{"vehicle":"2","date":1452986233158,"latLong":{"lat":54.96828201388807,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986218088,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986198654,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986180302,"latLong":{"lat":54.96858201388808,"lon":0.3999355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986173759,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986169289,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986150746,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986129093,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986116895,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""}]'
            jData = json.loads(result)
            mappos=Geohash.decode(tile)
            markers_map=[]
            for d in jData:
                markers_map.append((d["latLong"]["lat"],d["latLong"]["lon"]))

            nbmvts=len(jData)
            #debug=result
            vehicule_map = Map(
                identifier="view-side",
                lat=str(mappos[0]),
                lng=str(mappos[1]),
                style="height:700px;width:700px;margin:10;",
                zoom=9,
                markers=markers_map
                #markers=[(54.96848201388808, 0.39963558097359564),(54.968382013888075, -0.39953558097359565)]
            )

            return render_template('gettile.html', nbmvts=nbmvts,debug=debug,tile=tile,vehicule_map=vehicule_map)
            #else:
            #    error=response.raise_for_status().str
    return render_template('gettile.html',error=error,vehicule_map=vehicule_map)


@app.route("/getvehicle", methods=['GET', 'POST'])
def getvehicle():
    #form = {"vehicle_id": vehicle_id}
    #request.form['username']
    error = None
    debug=""
    vehicule_map = Map(
                identifier="view-side",
                lat=37.4419,
                lng=-122.1419,
                style="height:700px;width:700px;margin:0;",
                zoom=5
    )
    if request.method == 'POST':
        if request.form['vehicle_id']:
            vehicle_id=request.form['vehicle_id']
            day=request.form['day']
            apiday=day[6:10]+day[3:5]+day[0:2]
            apiday="20160117"
            url="http://localhost:8080/datastax-taxi-app/rest/getmovements/"+vehicle_id+"/"+apiday
            response=requests.get(url)
            result=""
            if(response.ok):
                result=response.content

            #result='[{"vehicle":"2","date":1452986285175,"latLong":{"lat":54.96848201388808,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},' \
            #      '{"vehicle":"2","date":1452986259330,"latLong":{"lat":54.968382013888075,"lon":0.39953558097359565},"tile":"u1b29nd","tile2":""},{"vehicle":"2","date":1452986233158,"latLong":{"lat":54.96828201388807,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986218088,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986198654,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986180302,"latLong":{"lat":54.96858201388808,"lon":0.3999355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986173759,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986169289,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986150746,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986129093,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986116895,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""}]'
            jData = json.loads(result)
            mappos=Geohash.decode(jData[0]["tile"])
            markers_map=[]
            for d in jData:
                markers_map.append((d["latLong"]["lat"],d["latLong"]["lon"]))

            nbmvts=len(jData)
            #debug="["+vehicle_mvt[:-1]+"]"
            vehicule_map = Map(
                identifier="view-side",
                lat=str(mappos[0]),
                lng=str(mappos[1]),
                style="height:700px;width:700px;margin:10;",
                zoom=11,
                markers=markers_map
                #markers=[(54.96848201388808, 0.39963558097359564),(54.968382013888075, -0.39953558097359565)]
            )

            return render_template('getvehicle.html', nbmvts=nbmvts,debug=debug,vehicle_id=vehicle_id,vehicule_map=vehicule_map,day=apiday)
            #else:
            #    error=response.raise_for_status().str
    return render_template('getvehicle.html',error=error,vehicule_map=vehicule_map,debug=debug)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run()