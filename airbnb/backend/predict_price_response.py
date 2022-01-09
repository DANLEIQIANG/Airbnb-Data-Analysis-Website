import sys

assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
from .common import model_file

from pyspark.ml import PipelineModel

price_schema = types.StructType([
    types.StructField('accommodates', types.IntegerType()),
    types.StructField('neighbourhood_cleansed', types.StringType()),
    types.StructField('bedrooms', types.IntegerType()),
    types.StructField('room_type', types.StringType()),
    types.StructField('price', types.FloatType()),
])


def test_model(accommodates, neighbourhood_cleansed, bedrooms, room_type):
    spark = SparkSession.builder.appName('price').getOrCreate()
    assert spark.version >= '2.3'  # make sure we have Spark 2.3+
    spark.sparkContext.setLogLevel('WARN')
    # get the data
    spark_rdd = spark.sparkContext.parallelize([(accommodates, neighbourhood_cleansed, bedrooms, room_type, 0.0)])
    test_price = spark.createDataFrame(spark_rdd, price_schema)
    # load the model
    model = PipelineModel.load("./backend/" + model_file)

    # use the model to make predictions
    predictions = model.transform(test_price).collect()
    print('Predicted price:', predictions[0][8])
    return predictions[0][8]


if __name__ == '__main__':
    test_model(2, 'Little Portugal', 1, 'Private room')
