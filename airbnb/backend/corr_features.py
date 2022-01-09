import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import pandas as pd
from pyspark.sql import SparkSession, functions, types
import os, sys
from pyspark.sql.window import Window
from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    # main logic starts here
    listings_schema = types.StructType([
        types.StructField('id', types.IntegerType(), False),
        types.StructField('listing_url', types.StringType(), False),
        types.StructField('scrape_id', types.StringType(), False),
        types.StructField('last_scraped', types.StringType(), False),
        types.StructField('name', types.StringType(), False),
        types.StructField('description', types.StringType(), False),
        types.StructField('neighborhood_overview', types.StringType(), False),
        types.StructField('picture_url', types.StringType(), False),
        types.StructField('host_id', types.StringType(), False),
        types.StructField('host_url', types.StringType(), False),
        types.StructField('host_name', types.StringType(), False),
        types.StructField('host_since', types.StringType(), False),
        types.StructField('host_location', types.StringType(), False),
        types.StructField('host_about', types.StringType(), False),
        types.StructField('host_response_time', types.StringType(), False),
        types.StructField('host_response_rate', types.StringType(), False),
        types.StructField('host_acceptance_rate', types.StringType(), False),
        types.StructField('host_is_superhost', types.StringType(), False),
        types.StructField('host_thumbnail_url', types.StringType(), False),
        types.StructField('host_picture_url', types.StringType(), False),
        types.StructField('host_neighbourhood', types.StringType(), False),
        types.StructField('host_listings_count', types.StringType(), False),
        types.StructField('host_total_listings_count', types.StringType(), False),
        types.StructField('host_verifications', types.StringType(), False),
        types.StructField('host_has_profile_pic', types.StringType(), False),
        types.StructField('host_identity_verified', types.StringType(), False),
        types.StructField('neighbourhood', types.StringType(), False),
        types.StructField('neighbourhood_cleansed', types.StringType(), False),
        types.StructField('neighbourhood_group_cleansed', types.StringType(), False),
        types.StructField('latitude', types.DoubleType(), False),
        types.StructField('longitude', types.DoubleType(), False),
        types.StructField('property_type', types.StringType(), False),
        types.StructField('room_type', types.StringType(), False),
        types.StructField('accommodates', types.IntegerType(), False),
        types.StructField('bathrooms', types.IntegerType(), False),
        types.StructField('bathrooms_text', types.StringType(), False),
        types.StructField('bedrooms', types.IntegerType(), False),
        types.StructField('beds', types.IntegerType(), False),
        types.StructField('amenities', types.StringType(), False),
        types.StructField('price', types.StringType(), False),
        types.StructField('minimum_nights', types.IntegerType(), False),
        types.StructField('maximum_nights', types.IntegerType(), False),
        types.StructField('minimum_minimum_nights', types.IntegerType(), False),
        types.StructField('maximum_minimum_nights', types.IntegerType(), False),
        types.StructField('minimum_maximum_nights', types.IntegerType(), False),
        types.StructField('maximum_maximum_nights', types.IntegerType(), False),
        types.StructField('minimum_nights_avg_ntm', types.IntegerType(), False),
        types.StructField('maximum_nights_avg_ntm', types.IntegerType(), False),
        types.StructField('calendar_updated', types.StringType(), False),
        types.StructField('has_availability', types.StringType(), False),
        types.StructField('availability_30', types.IntegerType(), False),
        types.StructField('availability_60', types.IntegerType(), False),
        types.StructField('availability_90', types.IntegerType(), False),
        types.StructField('availability_365', types.IntegerType(), False),
        types.StructField('calendar_last_scraped', types.StringType(), False),
        types.StructField('number_of_reviews', types.IntegerType(), False),
        types.StructField('number_of_reviews_ltm', types.IntegerType(), False),
        types.StructField('number_of_reviews_l30d', types.IntegerType(), False),
        types.StructField('first_review', types.StringType(), False),
        types.StructField('last_review', types.StringType(), False),
        types.StructField('review_scores_rating', types.DoubleType(), False),
        types.StructField('review_scores_accuracy', types.DoubleType(), False),
        types.StructField('review_scores_cleanliness', types.DoubleType(), False),
        types.StructField('review_scores_checkin', types.DoubleType(), False),
        types.StructField('review_scores_communication', types.DoubleType(), False),
        types.StructField('review_scores_location', types.DoubleType(), False),
        types.StructField('review_scores_value', types.DoubleType(), False),
        types.StructField('license', types.StringType(), False),
        types.StructField('instant_bookable', types.StringType(), False),
        types.StructField('calculated_host_listings_count', types.IntegerType(), False),
        types.StructField('calculated_host_listings_count_entire_homes', types.IntegerType(), False),
        types.StructField('calculated_host_listings_count_private_rooms', types.IntegerType(), False),
        types.StructField('calculated_host_listings_count_shared_rooms', types.IntegerType(), False),
        types.StructField('reviews_per_month', types.DoubleType(), False),
    ])
    df = spark.read.csv("/Users/yizhelyu/Desktop/all/732project/airbnb/Canada/Toronto,\ Ontario,\ Canada/listings-1.csv",
                        header=True, multiLine=True, schema=listings_schema, quote='"', escape='"')
    df = df.select('neighbourhood_cleansed', 'room_type', 'accommodates', 'bedrooms',
                   functions.substring_index(df.price, '$', -1).cast('float').alias('price'), 'review_scores_rating', 'minimum_nights')\
                    .filter(~df['review_scores_rating'].isNull())
    df_neighbour = df.groupby('neighbourhood_cleansed').agg(functions.rank().over(Window.orderBy('neighbourhood_cleansed')).alias('rank'))\
                    .withColumnRenamed('neighbourhood_cleansed', 'neighbourhood_cleansed1')
    df_room_type = df.groupby('room_type').agg(functions.rank().over(Window.orderBy('room_type')).alias('rank2')).\
                    withColumnRenamed('room_type', 'room_type1')
    cond = [df['neighbourhood_cleansed'] == df_neighbour['neighbourhood_cleansed1']]
    cond2 = [df['room_type'] == df_room_type['room_type1']]
    df_with_neighbour = df.join(df_neighbour, on=cond, how='inner')
    df_with_type = df_with_neighbour.join(df_room_type, on=cond2, how='inner')
    df_data = df_with_type.select('rank', 'rank2', 'accommodates', 'bedrooms', 'price', 'review_scores_rating'
                                  , 'minimum_nights').withColumnRenamed('rank', 'neighbourhood_cleansed')\
                        .withColumnRenamed('rank2', 'room_type')
    df_data = df_data.filter(~df['accommodates'].isNull() & ~df['bedrooms'].isNull() & ~df['neighbourhood_cleansed'].isNull()
                             & ~df['room_type'].isNull() & ~df['price'].isNull() & ~df['review_scores_rating'].isNull() & ~df['minimum_nights'].isNull())
    # convert to vector column first
    pandas_df = df_data.toPandas()
    result_pandas = pandas_df.corr(method='pearson')
    vector_col = "corr_features"
    assembler = VectorAssembler(inputCols=df_data.columns, outputCol=vector_col)
    df_vector = assembler.transform(df_data).select(vector_col)
    # get correlation matrix
    matrix = Correlation.corr(df_vector, vector_col)
    result = matrix.collect()[0]["pearson({})".format(vector_col)].values.reshape(7, 7)
    plt.figure(figsize=(15, 12))
    palette = sns.diverging_palette(20, 220, n=256)
    sns.heatmap(result_pandas, annot=True, fmt=".2f", cmap=palette, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5}).set(ylim=(11, 0))
    plt.title("Correlation Matrix", size=15, weight='bold')
    plt.show()
    # Shared room, Hotel room, Entire home/apt, Private room

if __name__ == '__main__':
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()