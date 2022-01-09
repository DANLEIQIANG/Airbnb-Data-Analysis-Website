from pyspark.sql import SparkSession, functions, types, SQLContext
import findspark
findspark.add_packages('mysql:mysql-connector-java:8.0.20')

import os, sys
from common import url, driver, user, password, model_file
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+
spark = SparkSession.builder.appName('predict_toronto_price').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
assert spark.version >= '2.4'  # make sure we have Spark 2.4+
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, SQLTransformer
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

def main():
    ctx = SQLContext(sc)

    df = ctx.read.format('jdbc').options(
        url=url,
        driver=driver,  # the driver for MySQL
        dbtable='listings',
        user=user,
        password=password,
    ).load()
    data = df.where((df.city == 'Toronto, Ontario, Canada') & (df.country == 'Canada')).select(df['accommodates'], df['neighbourhood_cleansed'], df['price'], df['bedrooms'], df['room_type'])
    data = data.filter(~df['neighbourhood_cleansed'].isNull() & ~df['bedrooms'].isNull() & ~df['room_type'].isNull() & ~df['accommodates'].isNull() & ~df['price'].isNull())
    train, validation = data.randomSplit([0.75, 0.25])
    train = train.cache()
    validation = validation.cache()
    neighborhood_indexer = StringIndexer(inputCol="neighbourhood_cleansed", outputCol="neighbourhood_cleansed_index", handleInvalid="error",
                                 stringOrderType="frequencyDesc")
    room_type_indexer = StringIndexer(inputCol="room_type", outputCol="room_type_index",
                                         handleInvalid="error",
                                         stringOrderType="frequencyDesc")

    input_assembler = VectorAssembler(inputCols=["neighbourhood_cleansed_index", "room_type_index", "accommodates", "bedrooms"],
                                        outputCol="features")
    regressor = RandomForestRegressor(featuresCol='features', labelCol='price', numTrees=10, maxDepth=5, seed=101, maxBins=140)
    # regressor = regressor = GBTRegressor(featuresCol='features', labelCol='price', maxDepth=4, seed=60, maxIter=10, stepSize=0.1)
    pipeline = Pipeline(stages=[neighborhood_indexer, room_type_indexer, input_assembler, regressor])

    model = pipeline.fit(train)
    predictions = model.transform(validation)
    predictions.show()

    r2_evaluator = RegressionEvaluator(predictionCol='prediction', labelCol='price',
                                       metricName='r2')
    r2 = r2_evaluator.evaluate(predictions)
    rmse_evaluator = RegressionEvaluator(predictionCol='prediction', labelCol='price',
                                         metricName='rmse')
    rmse = rmse_evaluator.evaluate(predictions)

    print('r2 =', r2)
    print('rmse =', rmse)
    model.write().overwrite().save(model_file)


if __name__ == '__main__':
    spark = SparkSession.builder.appName('predict_toronto_price').getOrCreate()
    assert spark.version >= '3.0'  # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()
