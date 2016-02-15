from flask import Flask, render_template,request,Markup
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import json
import Geohash
import getdata
import datetime

# configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('KILLRTAXI_SETTINGS', silent=True)

GoogleMaps(app)

initlat=51
initlng=0
ErrorMessage="Problem with API calls, check console messages and API application"

init_vehicule_map = Map(
    identifier="view-side",
    lat=initlat,
    lng=-initlng,
    style="height:700px;width:700px;margin:0;",
    zoom=5
)

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

    vehicule_map=init_vehicule_map

    if request.method == 'POST':

        if request.form['lon'] and request.form['lat']:

            lon=request.form['lon']
            lat=request.form['lat']
            dist=request.form['dist']

            if dist=="":dist="10"

            app.logger.debug('Debugging dist : %s',dist)

            markers_map=getdata.getvehicules_forme(lat,lon,dist)

            if not isinstance(markers_map,list):
                app.logger.debug('Connection error : %s',markers_map)
                return render_template('getme.html',vehicule_map=vehicule_map,error=ErrorMessage)

            nbmvts=len(markers_map)

            vehicule_map = Map(
                identifier="view-side",
                lat=lat,
                lng=lon,
                style="height:700px;width:700px;margin:10;",
                zoom=12,
                markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png':markers_map,
                         'http://maps.google.com/mapfiles/ms/icons/blue-dot.png':[(lat, lon)]}
                #markers=[(54.96848201388808, 0.39963558097359564),(54.968382013888075, -0.39953558097359565)]
            )

            return render_template('getme.html', nbmvts=nbmvts,lon=lon,lat=lat,dist=dist,vehicule_map=vehicule_map)

    return render_template('getme.html',vehicule_map=vehicule_map)



@app.route("/gettile", methods=['GET', 'POST'])
def gettile():

    vehicule_map=init_vehicule_map

    tilesresult=getdata.tiles()

    if tilesresult[:8]!="<option>":
        app.logger.debug('Connection error : %s',tilesresult)
        return render_template('gettile.html',vehicule_map=vehicule_map,error=ErrorMessage)
    else:
        alltiles=Markup(tilesresult)

    if request.method == 'POST':

        if request.form['tile']:

            tile=request.form['tile']

            markers_map=getdata.getvehicules_fortile(tile)

            #app.logger.debug('Debugging KILLRTAXI : %s',markers_map)

            if not isinstance(markers_map,list):
                app.logger.debug('Connection error : %s',markers_map)
                return render_template('gettile.html',vehicule_map=vehicule_map,error=ErrorMessage)

            nbmvts=len(markers_map)

            mappos=Geohash.decode(tile)

            vehicule_map = Map(
                identifier="view-side",
                lat=str(float(mappos[0])-0.2),
                lng=str(float(mappos[1])-0.2),
                style="height:700px;width:700px;margin:10;",
                zoom=9,
                markers=markers_map
                #markers=[(54.96848201388808, 0.39963558097359564),(54.968382013888075, -0.39953558097359565)]
            )

            return render_template('gettile.html', alltiles=alltiles,nbmvts=nbmvts,tile=tile,vehicule_map=vehicule_map)

    return render_template('gettile.html',alltiles=alltiles,vehicule_map=vehicule_map)


@app.route("/getvehicle", methods=['GET', 'POST'])
def getvehicle():

    vehicule_map=init_vehicule_map

    if request.method == 'POST':

        if request.form['vehicle_id']:

            vehicle_id=request.form['vehicle_id']
            day=request.form['day']

            if day=="":
                now=datetime.datetime.now()
                day=now.strftime("%d/%m/%Y")
                apiday=now.strftime("%Y%m%d")
            else:
                apiday=day[6:10]+day[3:5]+day[0:2]

            #apiday="20160127"
            app.logger.debug('Debugging KILLRTAXI : %s',apiday)

            markers_map=getdata.getvehicules_forone(vehicle_id,apiday)

            if not isinstance(markers_map,list):
                app.logger.debug('Connection error : %s',markers_map)
                return render_template('getvehicle.html',vehicule_map=vehicule_map,error=ErrorMessage)

            nbmvts=len(markers_map)

            app.logger.debug('Debugging KILLRTAXI : %s',nbmvts)

            if nbmvts > 0:
                latmap=str(markers_map[0][0])
                lngmap=str(markers_map[0][1])
                zoom=11
            else:
                latmap=initlat
                lngmap=-initlng
                zoom=5

            vehicule_map = Map(
                identifier="view-side",
                lat=latmap,
                lng=lngmap,
                style="height:700px;width:700px;margin:10;",
                zoom=zoom,
                markers=markers_map
                #markers=[(54.96848201388808, 0.39963558097359564),(54.968382013888075, -0.39953558097359565)]
            )

            return render_template('getvehicle.html', nbmvts=nbmvts,vehicle_id=vehicle_id,vehicule_map=vehicule_map,day=day)

    return render_template('getvehicle.html',vehicule_map=vehicule_map)





@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()