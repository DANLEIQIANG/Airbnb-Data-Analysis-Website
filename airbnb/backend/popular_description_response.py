import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from backend.models import PopularDescription
import pymysql
pymysql.install_as_MySQLdb()


def build_popular_description_response(city):
    result = PopularDescription.objects.filter(city__contains=city)[:20]
    key_word_x = []
    key_word_y = []
    for i in result:
        key_word_x.append(i.word)
        key_word_y.append(i.count)
    return key_word_x, key_word_y



