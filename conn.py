import mysql.connector
cnx = None
def conn_op():
    cnx = mysql.connector.connect(
        host="localhost",
        user="itm",
        passwd="1tm2024+.",
        database="rec_fac_itm",
    )
    return cnx

def conn_cl():
    cnx.close()


