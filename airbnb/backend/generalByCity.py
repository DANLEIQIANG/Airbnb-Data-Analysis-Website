'''
Danlei Qiang, task4:
1. read data from excel
2. data clean --- drop null
3. Use spark process data, select data from table --- roomtype/rent time/average price
4. create table in db, city, longrent  short rent, private, share, average price
5. creat get api, accept city and type as parameter, return city type data
6. plot figure --- show in web
'''
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from backend.models import GeneralByCity,Avgscore, TopAvgscoreByNeighbor
import pymysql
pymysql.install_as_MySQLdb()


def draw(city):
    result = GeneralByCity.objects.filter(city__contains=city)

    Entire_home_Or_apt = result[0].Entire_home_Or_apt
    Private_room = result[0].Private_room
    Shared_room = result[0].Shared_room
    room_type_x = ['Entire home/apt','Private room','Shared room' ]
    room_type_y = [Entire_home_Or_apt,Private_room, Shared_room]
    long_rent = result[0].long_rent
    short_rent = result[0].short_rent
    tenancy_term_x = ['Long Rent', 'Short Rent']
    tenancy_term_y = [long_rent, short_rent]

    Average_price = result[0].Average_price
    return room_type_x, room_type_y,tenancy_term_x,tenancy_term_y,Average_price



def calAvgScore(city):
    result = Avgscore.objects.filter(city__contains=city)
    neighborhood = []
    score = []
    for row in result:
        score.append(row.avg_review_score)
        neighborhood.append(row.neighbourhood)

    return score, neighborhood


def topAvgScoreByNeighborhood(city, neighborhood):
    result = TopAvgscoreByNeighbor.objects.filter(city__contains=city,neighborhood__contains =neighborhood)
    id = []
    score = []
    for row in result:
        id.append(row.id)
        score.append(row.review_scores_average)

    return id, score



