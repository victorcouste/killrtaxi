import requests,json

def tiles():
    url="http://localhost:8080/datastax-taxi-app/rest/gettiles"
    response=requests.get(url)
    stroptions=''
    if(response.ok):
        jData = json.loads(response.content)
        for t in jData:
            stroptions=stroptions+'<option>'+t+'</option>'
    return stroptions


def getvehicules_forme(lat,lon,dist):

    markers_map=[]
    url="http://localhost:8080/datastax-taxi-app/rest/search/"+str(lat)+"/"+str(lon)+"/"+str(dist)
    response=requests.get(url)
    if(response.ok):
        result=response.content
    else:
        return markers_map

    #result='[{"vehicle":"2","date":1452986285175,"latLong":{"lat":54.96848201388808,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},' \
    #      '{"vehicle":"2","date":1452986259330,"latLong":{"lat":54.968382013888075,"lon":0.39953558097359565},"tile":"u1b29nd","tile2":""},{"vehicle":"2","date":1452986233158,"latLong":{"lat":54.96828201388807,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986218088,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986198654,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986180302,"latLong":{"lat":54.96858201388808,"lon":0.3999355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986173759,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986169289,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986150746,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986129093,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986116895,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""}]'
    jData = json.loads(result)
    for d in jData:
        markers_map.append((d["latLong"]["lat"],d["latLong"]["lon"]))

    return markers_map


def getvehicules_fortile(tile):

    markers_map=[]
    url="http://localhost:8080/datastax-taxi-app/rest/getvehicles/"+tile
    response=requests.get(url)
    if(response.ok):
        result=response.content
    else:
        return markers_map

    #result='[{"vehicle":"2","date":1452986285175,"latLong":{"lat":54.96848201388808,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},' \
    #      '{"vehicle":"2","date":1452986259330,"latLong":{"lat":54.968382013888075,"lon":0.39953558097359565},"tile":"u1b29nd","tile2":""},{"vehicle":"2","date":1452986233158,"latLong":{"lat":54.96828201388807,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986218088,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986198654,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986180302,"latLong":{"lat":54.96858201388808,"lon":0.3999355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986173759,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986169289,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986150746,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986129093,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986116895,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""}]'
    jData = json.loads(result)
    for d in jData:
        markers_map.append((d["latLong"]["lat"],d["latLong"]["lon"]))

    return markers_map


def getvehicules_forone(vehicle_id,apiday):

    markers_map=[]
    url="http://localhost:8080/datastax-taxi-app/rest/getmovements/"+vehicle_id+"/"+apiday
    response=requests.get(url)
    if(response.ok):
        result=response.content
    else:
        return markers_map

    #result='[{"vehicle":"2","date":1452986285175,"latLong":{"lat":54.96848201388808,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},' \
    #      '{"vehicle":"2","date":1452986259330,"latLong":{"lat":54.968382013888075,"lon":0.39953558097359565},"tile":"u1b29nd","tile2":""},{"vehicle":"2","date":1452986233158,"latLong":{"lat":54.96828201388807,"lon":0.39963558097359564},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986218088,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986198654,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986180302,"latLong":{"lat":54.96858201388808,"lon":0.3999355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986173759,"latLong":{"lat":54.96848201388808,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986169289,"latLong":{"lat":54.968382013888075,"lon":0.39973558097359563},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986150746,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986129093,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""},{"vehicle":"2","date":1452986116895,"latLong":{"lat":54.96828201388807,"lon":0.3998355809735956},"tile":"u1b29ne","tile2":""}]'
    jData = json.loads(result)
    for d in jData:
        markers_map.append((d["latLong"]["lat"],d["latLong"]["lon"]))

    return markers_map