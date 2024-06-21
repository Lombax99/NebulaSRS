#import psycopg2
from flask import Flask, render_template
import json
#from get_conn import get_connection_uri

def prova():
    """conn_string = get_connection_uri()

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TEST;")
    rows = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return rows"""
