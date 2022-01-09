import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types
import os, sys
from pyspark.sql.window import Window

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
    df = df.select(df['neighbourhood_cleansed'], df['review_scores_accuracy'], df['review_scores_cleanliness'], df['review_scores_checkin'],
                   df['review_scores_communication'], df['review_scores_location'], df['review_scores_value'], df['id'], df['name'])
    df = df.withColumn('review_scores_average', (df['review_scores_accuracy'] + df['review_scores_cleanliness'] + df['review_scores_checkin'] +
                   df['review_scores_communication'] + df['review_scores_location'] + df['review_scores_value'])/6)
    df_with_average = df.select(df['neighbourhood_cleansed'], df['review_scores_average'], df['id'], df['name'])
    df_with_average = df_with_average.drop_duplicates()
    window = Window.partitionBy(df['neighbourhood_cleansed']).orderBy(df['review_scores_average'].desc())
    #top_average_neigh = df_with_average.select('*', functions.rank().over(window).alias('rank')).filter(functions.col('rank') <= 5).orderBy('neighbourhood_cleansed')
    top_average_neigh = df_with_average.withColumn('rank', functions.rank().over(window)).filter(
        functions.col('rank') <= 5).orderBy('neighbourhood_cleansed')
    print(top_average_neigh.collect())


if __name__ == '__main__':
    spark = SparkSession.builder.appName('example code').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()