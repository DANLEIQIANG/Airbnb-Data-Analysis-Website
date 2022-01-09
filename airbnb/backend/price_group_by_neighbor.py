import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

import findspark
findspark.add_packages('mysql:mysql-connector-java:8.0.20')
from pyspark.sql import SparkSession, functions, types, SQLContext
import os, sys
from common import url, driver, user, password

def main():
    # main logic starts here
    ctx = SQLContext(spark)

    df = ctx.read.format('jdbc').options(
        url=url,
        driver=driver,  # the driver for MySQL
        dbtable='listings',
        user=user,
        password=password,
    ).load()
    per_price = df.filter(~df['neighbourhood_cleansed'].isNull()).select((df['price']/df['accommodates']).alias('price'), df['neighbourhood_cleansed'], df['city'], df['country'])
    avg_per_price = per_price.groupBy(per_price['neighbourhood_cleansed'], per_price['city'], per_price['country']).agg(functions.avg('price').alias('avg_val')).orderBy('city', 'country', functions.desc("avg_val"))
    median_per_price = per_price.groupBy(per_price['neighbourhood_cleansed'], per_price['city'], per_price['country']).agg(functions.percentile_approx('price', 0.5).alias('med_val')).orderBy('city', 'country', functions.col("med_val").desc())
    avg_per_price.repartition(1).write.format('jdbc').options(
        url=url,
        driver=driver,  # the driver for MySQL
        dbtable='backend_avgperprice',
        user=user,
        password=password,
    ).mode('append').save()
    median_per_price.repartition(1).write.format('jdbc').options(
        url=url,
        driver=driver,  # the driver for MySQL
        dbtable='backend_medianperprice',
        user=user,
        password=password,
    ).mode('append').save()

if __name__ == '__main__':
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()