from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import geocoder
import urllib
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


#p=Place()
#places=p.query("1600 Ampitheater Parkway Mountain View CA")

class Place(object):
    def meters_to_walking_time(self, meters):
        #80 meters in one minute walking time
        return int(meters*1000/80)

    def wiki_path(self, slug):
        return urllib.parse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

    def address_to_latlang(self, address):
        g = geocoder.yandex(address)
        return(g.lat, g.lng)

    def query(self, address):
        lat, lon = self.address_to_latlang(address)
        print(lat, lon)

        query_url = f'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}%7C{lon}&gsradius=5000&gslimit=20&format=json'
        g = urllib.request.urlopen(query_url)
        results = g.read()
        g.close()

        #parsing data as json
        data = json.loads(results)
        print(data,'\n ** \n')
        print(data['query'])

        places = []
        a=data['query']
        b=a['geosearch']
        for place in b:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lon = place['lon']

            wiki_url = self.wiki_path(name)
            waking_time = self.meters_to_walking_time(meters)

            d = {
                'name': name,
                'url': wiki_url,
                'time': waking_time,
                'lat': lat,
                'lon': lon
            }
            places.append(d)
        return places
