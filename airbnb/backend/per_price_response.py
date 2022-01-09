import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from backend.models import AvgPerPrice, MedianPerPrice
import pymysql
pymysql.install_as_MySQLdb()


def build_per_price_response(city):
    result = AvgPerPrice.objects.filter(city__contains=city)
    avg_per_price_x = []
    avg_per_price_y = []
    for i in result:
        avg_per_price_x.append(i.neighbourhood_cleansed)
        avg_per_price_y.append(i.avg_val)
    result2 = MedianPerPrice.objects.filter(city__contains=city)
    median_per_price_x = []
    median_per_price_y = []
    for i in result2:
        median_per_price_x.append(i.neighbourhood_cleansed)
        median_per_price_y.append(i.med_val)
    return avg_per_price_x, avg_per_price_y, median_per_price_x, median_per_price_y



