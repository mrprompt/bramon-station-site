#!/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import sqlite3
import boto3
import yaml
from typing import List


PATH = os.path.dirname(__file__)
PATH_OF_STATS = "{}/..".format(PATH)
CONFIG_FILE = "{}/../_config.yml".format(PATH)


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.load(f)


def get_matching_s3_objects(bucket, prefix="", suffix=""):
    """
    Generate objects in an S3 bucket.

    From: https://alexwlchan.net/2019/07/listing-s3-keys/

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")

    kwargs = {'Bucket': bucket}

    # We can pass the prefix directly to the S3 API.  If the user has passed
    # a tuple or list of prefixes, we go through them one by one.
    if isinstance(prefix, str):
        prefixes = (prefix,)
    else:
        prefixes = prefix

    for key_prefix in prefixes:
        kwargs["Prefix"] = key_prefix

        for page in paginator.paginate(**kwargs):
            try:
                contents = page["Contents"]
            except KeyError:
                return

            for obj in contents:
                key = obj["Key"]
                if key.endswith(suffix):
                    yield obj


def get_matching_s3_keys(bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.

    From: https://alexwlchan.net/2019/07/listing-s3-keys/

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj["Key"]


def organize_captures(stations_captures: List) -> List:
    """
    Organize captures to be inserted into database with
    correct params organized into a tuple.

    :param stations_captures: The array all captures
    :returns: List
    """
    captures_organized = []

    for capture in stations_captures:
        capture_spliced = capture.split('/')
        station = capture_spliced[0]
        capture_date = capture_spliced[2]
        post = (capture_date, station, capture)

        captures_organized.append(post)

    return captures_organized


def populate_tables(connection: object, captures_list: List) -> bool:
    """
    Insert posts into table

    :param connection: The database connection
    :param captures_list: Array of posts
    :returns: bool
    """
    connection_cursor = connection.cursor()

    connection_cursor.execute("""
    CREATE TABLE IF NOT EXISTS captures (
        id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
        capture_month VARCHAR(6) NOT NULL,
        station VARCHAR(20) NOT NULL,
        files TEXT
    );
    """)

    connection_cursor.executemany("INSERT INTO captures (capture_month, station, files) VALUES (?, ?, ?)", captures_list)

    connection.commit()

    return True


def generate_stats(connection: object) -> bool:
    """
    Generate captures collections and pages from every station captures.

    :param connection: The database connection
    :return: bool
    """
    connection_cursor = connection.cursor()
    connection_cursor.execute("""
    SELECT COUNT(files) AS captures, capture_month, station 
    FROM captures 
    GROUP BY capture_month, station
    ORDER BY station, capture_month
    """)

    captures_stats_filename = "{}/estatisticas.md".format(PATH_OF_STATS)
    filehandle = open(captures_stats_filename, "w+")
    filehandle.write("---\n")
    filehandle.write("layout: stats\n")
    filehandle.write("title: Estat&iacute;sticas de Capturas\n")
    filehandle.write("permalink: estatisticas\n")
    filehandle.write("capturas: \n")

    for data in connection_cursor.fetchall():
        captures = str(data[0])
        month_and_year = str(data[1])
        capture_year = str(month_and_year[0:4])
        capture_month = str(month_and_year[4:6])
        station = str(data[2])

        filehandle.write("  - station: {}\n"
                         "    month: {}\n"
                         "    year: {}\n"
                         "    captures: {}\n".format(station, capture_month, capture_year, captures))

    filehandle.write("---\n")
    filehandle.close()

    return True


if __name__ == '__main__':
    print("- Loading site configuration")
    config = load_config()

    print('- Reading captures from S3 bucket')
    captures = get_matching_s3_keys(config['s3_bucket'], suffix='.mp4', prefix=config['build']['prefix'])

    print("- Organizing captures")
    posts = organize_captures(captures)

    print("- Connecting to database")
    conn = sqlite3.connect(':memory:')

    print("- Creating temporary table and populating...")
    populate_tables(conn, posts)

    print("- Creating stats")
    generate_stats(conn)

    print("- Closing database connection")
    conn.close()

    print("- Done :)")
