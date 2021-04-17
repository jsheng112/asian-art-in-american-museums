#-----------------------------------------------------------------------
# database.py
#-----------------------------------------------------------------------

import sys
from psycopg2 import connect, Error as dbError
import os
import random
import string

class Database:

    def __init__(self):
        self._connection = None


    def connect(self):
            #        DATABASE_NAME = "PTE"
            #        if not path.isfile(DATABASE_NAME):
            #            raise Exception("reg: database PTE not found")
        DATABASE_URL = os.environ['DATABASE_URL']
        self._connection = connect(DATABASE_URL, sslmode='require')
        # self._connection = connect(host = "localhost", database = "museum", user = "postgres", password = "postgres")


    def disconnect(self):
        self._connection.close()
    
    def getArtAll(self):
        try:
            cursor = self._connection.cursor()

            s = "SELECT * FROM merged LIMIT 1000;"
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                return [False, False]
            else:
                listArtworks = list(artworks)
                return [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            return [False, False]
            sys.exit(1)

        except Exception as e:
            print(str(e), file = sys.stderr)
            return [False, False]
            sys.exit(1)

    def getArt(self, info):
        try:
            cursor = self._connection.cursor()

            s = "SELECT * FROM merged"
            keys = list(info.keys())
            first = True
            for i in range(len(keys)):
                if len(info[keys[i]]) > 0:
                    if first:
                        s = s + " WHERE"
                        first = False
                    else:
                        s = s + " AND"
                    s  = s + " LOWER(" + keys[i]+ ") LIKE \'%" + info[keys[i]].strip().lower() + "%\'"
                    
            s = s + " LIMIT 1000;"
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                return [False, list()]
            else:
                listArtworks = list(artworks)
                return [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            return [False, False]
            sys.exit(1)

        except Exception as e:
            print(str(e), file = sys.stderr)
            return [False, False]
            sys.exit(1)

    def getSpecificArt(self, objectid, repository):
        try:
            cursor = self._connection.cursor()

            s = "SELECT * FROM merged WHERE objectid = \'%s\' AND repository = \'%s\' LIMIT 1000;" % (objectid, repository)
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                return [False, False]
            else:
                listArtworks = list(artworks)
                return [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            return [False, False]
            sys.exit(1)

        except Exception as e:
            print(str(e), file = sys.stderr)
            return [False, False]
            sys.exit(1)

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            return [False, False]
            sys.exit(1)

        except Exception as e:
            print(str(e), file = sys.stderr)
            return [False, False]
            sys.exit(1)

    def getArtAllPlots(self):
        culture = []
        accessionyear = []
        artist = []
        classification = []
        try:
            cursor = self._connection.cursor()

            s = "SELECT culture, COUNT(culture) FROM merged WHERE culture is not NULL GROUP BY culture order by COUNT(culture) desc limit 20;"
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                culture= [False, []]
            else:
                listArtworks = list(artworks)
                culture= [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            culture = [False, False]
            sys.exit(1)

        try:
            cursor = self._connection.cursor()

            s = "SELECT accessionyear, COUNT(accessionyear) FROM merged WHERE accessionyear is not NULL GROUP BY accessionyear order by accessionyear desc limit 50;"
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                accessionyear= [False, []]
            else:
                listArtworks = list(artworks)
                accessionyear= [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            accessionyear = [False, False]
            sys.exit(1)

        try:
            cursor = self._connection.cursor()

            s = "SELECT artistdisplayname, COUNT(artistdisplayname) FROM merged WHERE artistdisplayname is not NULL GROUP BY artistdisplayname order by COUNT(artistdisplayname) desc limit 20;"
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                artist= [False, []]
            else:
                listArtworks = list(artworks)
                artist= [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            artist = [False, False]
            sys.exit(1)

        try:
            cursor = self._connection.cursor()

            s = "SELECT classification, COUNT(classification) FROM merged WHERE classification is not NULL GROUP BY classification order by COUNT(classification) desc limit 10;"
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                classification= [False, []]
            else:
                listArtworks = list(artworks)
                classification= [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            classification = [False, False]
            sys.exit(1)

        return culture, accessionyear, artist, classification
    
    def getArtPlots(self, info):
        culture = []
        accessionyear = []
        artist = []
        classification = []
        try:
            cursor = self._connection.cursor()
            s = "SELECT culture, COUNT(culture) FROM merged"
            keys = list(info.keys())
            first = True
            for i in range(len(keys)):
                if len(info[keys[i]]) > 0:
                    if first:
                        s = s + " WHERE"
                        first = False
                    else:
                        s = s + " AND"
                    s  = s + " LOWER(" + keys[i]+ ") LIKE \'%" + info[keys[i]].strip().lower() + "%\'"
            if first:
                s = s + " WHERE culture is not NULL GROUP BY culture order by COUNT(culture) desc limit 20;"
            else:    
                s = s + " AND culture is not NULL GROUP BY culture order by COUNT(culture) desc limit 20;"
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                culture= [False, []]
            else:
                listArtworks = list(artworks)
                culture= [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            culture = [False, False]
            sys.exit(1)

        try:
            cursor = self._connection.cursor()

            s = "SELECT accessionyear, COUNT(accessionyear) FROM merged"
            keys = list(info.keys())
            first = True
            for i in range(len(keys)):
                if len(info[keys[i]]) > 0:
                    if first:
                        s = s + " WHERE"
                        first = False
                    else:
                        s = s + " AND"
                    s  = s + " LOWER(" + keys[i]+ ") LIKE \'%" + info[keys[i]].strip().lower() + "%\'"
            if first:
                s = s + " WHERE accessionyear is not NULL GROUP BY accessionyear order by accessionyear desc limit 50;"
            else:
                s = s + " AND accessionyear is not NULL GROUP BY accessionyear order by accessionyear desc limit 50;"
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                accessionyear= [False, []]
            else:
                listArtworks = list(artworks)
                accessionyear= [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            accessionyear = [False, False]
            sys.exit(1)

        try:
            cursor = self._connection.cursor()

            s = "SELECT artistdisplayname, COUNT(artistdisplayname) FROM merged"
            keys = list(info.keys())
            first = True
            for i in range(len(keys)):
                if len(info[keys[i]]) > 0:
                    if first:
                        s = s + " WHERE"
                        first = False
                    else:
                        s = s + " AND"
                    s  = s + " LOWER(" + keys[i]+ ") LIKE \'%" + info[keys[i]].strip().lower() + "%\'"
            if first:
                s = s + " WHERE artistdisplayname is not NULL GROUP BY artistdisplayname order by COUNT(artistdisplayname) desc limit 20;"
            else:
                s = s + " AND artistdisplayname is not NULL GROUP BY artistdisplayname order by COUNT(artistdisplayname) desc limit 20;"
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                artist= [False, []]
            else:
                listArtworks = list(artworks)
                artist= [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            artist = [False, False]
            sys.exit(1)

        try:
            cursor = self._connection.cursor()

            s = "SELECT classification, COUNT(classification) FROM merged"
            keys = list(info.keys())
            first = True
            for i in range(len(keys)):
                if len(info[keys[i]]) > 0:
                    if first:
                        s = s + " WHERE"
                        first = False
                    else:
                        s = s + " AND"
                    s  = s + " LOWER(" + keys[i]+ ") LIKE \'%" + info[keys[i]].strip().lower() + "%\'"
            if first:
                s = s + " WHERE classification is not NULL GROUP BY classification order by COUNT(classification) desc limit 10;"

            else:
                s = s + " AND classification is not NULL GROUP BY classification order by COUNT(classification) desc limit 10;"

            
            cursor.execute(s)
            artworks = cursor.fetchall()
            if len(artworks) == 0:
                classification= [False, []]
            else:
                listArtworks = list(artworks)
                classification= [True, listArtworks]

        except dbError as e:
            print("museum: " + str(e), file = sys.stderr)
            classification = [False, False]
            sys.exit(1)

        return culture, accessionyear, artist, classification

    
def main():
    database = Database()
    database.connect()
    info = {'index': '', 'objectid': '', 'objectnumber': '', 'title': '', 'artworkdescription': '', 'culture': '', 'city': '', 'country': '', 'timeperiod': '', 'artworkdate': '', 'datebegin': '', 'dateend': '', 'department': '', 'accessionyear': '', 'accessiondate': '', 'accessionnumber': '', 'medium': '', 'classification': '', 'dimensions': '', 'repository': '', 'tags': '', 'imageurl': '', 'inscription': '', 'markings': '', 'artistdisplayname': '', 'artistid': '', 'artistnationality': '', 'artistprefix': '', 'artistsuffix': '', 'nationality': '', 'artistbegindate': '', 'artistenddate': '', 'artistgender': '', 'artistrole': '', 'artistbio': '', 'artistulanurl': '', 'artistwikidataurl': '', 'objectwikidataurl': '', 'tagsaaturl': '', 'creditline': '', 'tagswikidataurl': '', 'artworkurl': '', 'rightsandreproduction': '', 'gallery': '', 'artistbirthplace': '', 'artistdeathplace': '', 'continent': ''}
    classification_data = database.getArtAllPlots()[3]
    classification = [x[0] for x in classification_data[1]]
    classification_counts = [x[1] for x in classification_data[1]]
    print(classification_counts)
    database.disconnect()

if __name__ == '__main__':
    main()
