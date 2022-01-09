import sys
from pyspark import SparkConf, SparkContext

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import findspark
findspark.add_packages('mysql:mysql-connector-java:8.0.20')


from pyspark.sql import SparkSession, functions, types, SQLContext
from common import url, driver, user, password
import re
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
from nltk.corpus import stopwords
en_stops = set(stopwords.words('english'))
def words_once(x):
    city = x[0]
    country = x[1]
    line = x[2]
    cleanr = re.compile('<.*?>')
    line = re.sub(cleanr, ' ', line.lower())  # 去除html标签
    line = re.sub(r'[^A-Za-z ]+', '', line)
    for w in line.split():
        if w not in en_stops:
            yield ((country, city, w), 1)

def add(x, y):
    return x + y

def output_format(kv):
    k, v = kv
    return (k[0], k[1], k[2], v)

def main():
    # main logic starts here
    ctx = SQLContext(sc)

    df = ctx.read.format('jdbc').options(
        url=url,
        driver=driver,  # the driver for MySQL
        dbtable='listings',
        user=user,
        password=password,
    ).load()
    description = df.filter(~df['description'].isNull()).select(df['city'], df['country'], df['description'])
    d_rdd = description.rdd
    words = d_rdd.flatMap(words_once)
    wordcount = words.reduceByKey(add).map(output_format)
    schema = types.StructType([types.StructField('country', types.StringType()), types.StructField('city', types.StringType()), types.StructField('word', types.StringType()), types.StructField('count', types.IntegerType())])
    result = ctx.createDataFrame(wordcount, schema).orderBy('country', 'city', functions.col("count").desc())
    result.repartition(1).write.format('jdbc').options(
        url=url,
        driver=driver,  # the driver for MySQL
        dbtable='backend_populardescription',
        user=user,
        password=password,
    ).mode('append').save()

if __name__ == '__main__':
    sc = SparkContext(appName='finaf_g')
    sc.setLogLevel('WARN')
    assert sc.version >= '3.0'  # make sure we have Spark 3.0+
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '3.0'  # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    main()