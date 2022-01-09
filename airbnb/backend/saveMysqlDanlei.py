'''
when running, change mysql config: root and password, before running this file, fist run:
python manage.py makemigrations backend
python manage.py migrate
to create table
'''

#room_type: shared room
import sys

from pyspark.sql.functions import lit,avg,count

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

host = '127.0.0.1'
port = 3306
db = 'airbnb'
user = 'root'
password = '12345678'

engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s?charset=utf8") % (user, password, host, db))

listings_schema = types.StructType([
    types.StructField('id', types.IntegerType(), False),
    types.StructField('name', types.StringType(), False),
    types.StructField('host_id', types.IntegerType(), False),
    types.StructField('host_name', types.StringType(), False),
    types.StructField('neighbourhood_group', types.StringType(), False),
    types.StructField('neighbourhood', types.StringType(), False),
    types.StructField('latitude', types.DoubleType(), False),
    types.StructField('longitude', types.DoubleType(), False),
    types.StructField('room_type', types.StringType(), False),
    types.StructField('price', types.IntegerType(), False),
    types.StructField('minimum_nights', types.IntegerType(), False),
    types.StructField('number_of_reviews', types.IntegerType(), False),
    types.StructField('last_review', types.StringType(), False),
    types.StructField('reviews_per_month', types.DoubleType(), False),
    types.StructField('calculated_host_listings_count', types.IntegerType(), False),
    types.StructField('availability_365', types.IntegerType(), False),
    types.StructField('number_of_reviews_ltm', types.IntegerType(), False),
    types.StructField('license', types.StringType(), False),
])


def generalByCity():
    input_df = spark.read.csv(
        '/Users/qiangdanlei/Desktop/Archive/ottawa/listings.csv',header=True,schema=listings_schema,multiLine=True)
    input_need = input_df.where(input_df['neighbourhood_group'].isNull()).select(input_df['room_type'], input_df['price'], input_df['minimum_nights']).withColumn("city", lit("Ottawa"))
    input_drop_duplicate = input_need.where(input_df['room_type'].isNotNull()).where(input_df['price'].isNotNull()).where(input_df['minimum_nights'].isNotNull())
    input_drop_duplicate.createOrReplaceTempView('input_drop_duplicate')
    res1_df = spark.sql("""
                select count(1) as long_rent, city from input_drop_duplicate where minimum_nights >=28 group by city
        """)
    res2_df = spark.sql("""
                select count(1) as short_rent, city from input_drop_duplicate where minimum_nights < 28 group by city
         """)
    res3_df = spark.sql("""
                select count(1) as Entire_home_Or_apt, city from input_drop_duplicate where room_type = 'Entire home/apt' group by city
            """)
    res4_df = spark.sql("""
                select count(1) as Private_room, city from input_drop_duplicate where room_type = 'Private room' group by city
            """)
    res6_df = spark.sql("""
                   select count(1) as Shared_room, city from input_drop_duplicate where room_type = 'Shared room' group by city
               """)
    res5_df = spark.sql("""
                select avg(price) as Average_price, city from input_drop_duplicate group by city 
            """)
    res1_df.createOrReplaceTempView('res1_df')
    res2_df.createOrReplaceTempView('res2_df')
    res3_df.createOrReplaceTempView('res3_df')
    res4_df.createOrReplaceTempView('res4_df')
    res5_df.createOrReplaceTempView('res5_df')
    res6_df.createOrReplaceTempView('res6_df')
    res_df = spark.sql("""
                select a.city as city, long_rent, short_rent,Entire_home_Or_apt,Private_room,Shared_room, Average_price  from res1_df a join res2_df b on a.city = b.city join res3_df c on a.city = c.city join res4_df d on 
                a.city = d.city  join res5_df e on a.city = e.city join res6_df f on a.city = f.city
            """).toPandas()

    try:
        res_df.to_sql('backend_generalbycity',con=engine,if_exists='append',index=False)
    except Exception as e:
        print(e)

def topAvgScore():
    input_df = spark.read.csv(
        '/Users/qiangdanlei/Desktop/Archive/ottawa/listings-1.csv',header=True,multiLine=True, quote='"', escape='"')
    input_need = input_df.select(input_df['neighbourhood_cleansed'], input_df['review_scores_value']).withColumn("city", lit("Ottawa"))
    input_drop_duplicate = input_need.where(input_df['neighbourhood_cleansed'].isNotNull()).where(
        input_df['review_scores_value'].isNotNull())
    input_drop_duplicate.createOrReplaceTempView('input_drop_duplicate')
    res_df = spark.sql("""
                    select avg(review_scores_value) as avg_review_score, neighbourhood_cleansed as neighbourhood ,city from input_drop_duplicate group by neighbourhood,city order by avg_review_score DESC
            """).toPandas()

    try:
        res_df.to_sql('backend_avgscore',con=engine, if_exists='append',index=False)
    except Exception as e:
        print(e)









if __name__ == '__main__':
    spark = SparkSession.builder.appName('get general info by city').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    generalByCity()
    topAvgScore()
