# killrtaxi

This is a Web demo application using Patrick Callaghan DataStax/Cassandra demo API found here https://github.com/PatrickCallaghan/datastax-taxi-app

As Patrick says "This demo traces moving vehicles as they pass through geohash tiles. It also keeps track of a vehicle movements on a day to day basis. Similar to a vessel tracking or taxi application."

This Web application use Python Flask Web framework and Flask-GoogleMap extension.

## Installation

* Install the Python Flask framework

  All instructions here http://flask.pocoo.org/docs/0.10/installation/#installation
  
* Install Flask-GoogleMap extension

  All details here https://github.com/rochacbruno/Flask-GoogleMaps but simple to install it run
  
      pip install flask-googlemaps
  
* Install DataStax Enterprise with Apache Solr activated

  Free download here https://academy.datastax.com/downloads
  
  Installation documentation here http://docs.datastax.com/en/datastax_enterprise/4.8/datastax_enterprise/install/installTOC.html

* Install and setup Patrick API

  Get source code and instructions from my fork https://github.com/victorcouste/datastax-taxi-app
  
  Create CQL schemas and Solr core as explained.

* Install the killrtaxi Web app

  Clone this repo

      git clone https://github.com/victorcouste/killrtaxi.git


## Running

1/ Start DataStax Enterprise with Search activated

Documentation here http://docs.datastax.com/en/datastax_enterprise/4.8/datastax_enterprise/srch/srchInstall.html

2/ Start datastax-taxi-app API

To continuously update the locations of the vehicles run 
	
	mvn clean compile exec:java -Dexec.mainClass="com.datastax.taxi.Main" -DcontactPoints=localhost
	
To start the API web server, in another terminal run 

	mvn jetty:run
	
To test your installation and run,for example find all movements of a vehicle use http://localhost:8080/datastax-taxi-app/rest/getmovements/{vehicle}/{date} e.g.

	http://localhost:8080/datastax-taxi-app/rest/getmovements/1/20160112

Or

	select * from vehicle where vehicle = '1' and day='20160112';

3/ Start the Flask Web app

  In the killrtaxi directory run
  
    python killrtaxi.py
  
  Now you must be able to go to http://127.0.0.1:5000/ and play with the application
