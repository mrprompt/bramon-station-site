#!/usr/bin/env python3
# -*- coding: utf8 -*-
import argparse
import csv
import os
import sqlite3


PATH = os.path.dirname(__file__)
PATH_OF_ANALYZERS = "{}/../_data/".format(PATH)


def import_showers_file(showers_file):
    connection_cursor = connection.cursor()
    connection_cursor.execute("""
        CREATE TABLE IF NOT EXISTS showers (
            "LP" TEXT, "IAUNo" TEXT, "AdNo" TEXT, "Code" TEXT, "shower_name" TEXT, "activity" TEXT, "s" TEXT, 
            "LaSun" TEXT, "Ra" TEXT, "De" TEXT, "dRa" TEXT, "dDe" TEXT, "Vg" TEXT, "a" TEXT, "q" TEXT, "e" TEXT, 
            "peri" TEXT, "node" TEXT, "inc" TEXT, "N" TEXT, "Group" TEXT, "CG" TEXT, "Parent" TEXT, "body" TEXT, 
            "Remarks" TEXT, "Ote" TEXT, "References" TEXT, "Submission" TEXT, "date" TEXT, "UTC" TEXT
        );
        """)

    showers = []

    with open(showers_file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='|', quotechar='"')

        for row in csv_reader:
            try:
                if row[-1].startswith(":") or len(row) < 2:
                    continue

                if len(row) == 26:
                    row.append(" ")
                    row.append(" ")
                    row.append(" ")
                    row.append(" ")

                showers.append(row)
            except IndexError:
                pass

    connection_cursor.executemany("""
        INSERT INTO showers 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, showers)

    connection.commit()


def generate_shower():
    connection_cursor = connection.cursor()
    connection_cursor.execute("""
    SELECT *
    FROM showers
    GROUP BY Code
    """)

    capture_filename = PATH_OF_ANALYZERS + "showers.yaml"
    filehandle = open(capture_filename, "w")

    for shower in connection_cursor.fetchall():
        filehandle.write("J8_{}:\n".format(shower[3].strip()))
        filehandle.write("  LP: \"{}\"\n".format(shower[0].strip()))
        filehandle.write("  IAUNo: \"{}\"\n".format(shower[1].strip()))
        filehandle.write("  AdNo: \"{}\"\n".format(shower[2].strip()))
        filehandle.write("  Code: \"{}\"\n".format(shower[3].strip()))
        filehandle.write("  shower_name: \"{}\"\n".format(shower[4].strip()))
        filehandle.write("  activity: \"{}\"\n".format(shower[5].strip()))
        filehandle.write("  s: \"{}\"\n".format(shower[6].strip()))
        filehandle.write("  LaSun: \"{}\"\n".format(shower[7].strip()))
        filehandle.write("  Ra: \"{}\"\n".format(shower[8].strip()))
        filehandle.write("  De: \"{}\"\n".format(shower[9].strip()))
        filehandle.write("  dRa: \"{}\"\n".format(shower[10].strip()))
        filehandle.write("  dDe: \"{}\"\n".format(shower[11].strip()))
        filehandle.write("  Vg: \"{}\"\n".format(shower[12].strip()))
        filehandle.write("  a: \"{}\"\n".format(shower[13].strip()))
        filehandle.write("  q: \"{}\"\n".format(shower[14].strip()))
        filehandle.write("  e: \"{}\"\n".format(shower[15].strip()))
        filehandle.write("  peri: \"{}\"\n".format(shower[16].strip()))
        filehandle.write("  node: \"{}\"\n".format(shower[17].strip()))
        filehandle.write("  inc: \"{}\"\n".format(shower[18].strip()))
        filehandle.write("  N: \"{}\"\n".format(shower[19].strip()))
        filehandle.write("  Group: \"{}\"\n".format(shower[20].strip()))
        filehandle.write("  CG: \"{}\"\n".format(shower[21].strip()))
        filehandle.write("  Parent: \"{} {}\"\n".format(shower[22].strip(), shower[23].strip()))
        filehandle.write("  Remarks: \"{}\"\n".format(shower[24].strip()))
        filehandle.write("  Ote: {}\n".format(shower[25].strip().replace('?', '')))
        filehandle.write("  References: \"{}\"\n".format(shower[26].strip()))
        filehandle.write("  Submission: \"{}\"\n".format(shower[27].strip()))
        filehandle.write("  date: \"{}\"\n".format(shower[28].strip()))
        filehandle.write("  UTC: \"{}\"\n".format(shower[29].strip()))
    filehandle.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import CSV file of showers')
    parser.add_argument('showers_file', metavar='showers', type=str, help='CSV file from showers')

    args = parser.parse_args()
    csv_file = args.showers_file

    print("- Connecting to database")
    connection = sqlite3.connect(':memory:')

    print("- Importing showers data")
    import_showers_file(csv_file)

    print("- Generating shower data to site")
    generate_shower()

    print("- Closing database connection")
    connection.close()

    print("- Done :)")
