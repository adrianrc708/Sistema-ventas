import pymysql

miConexion = pymysql.connect(
    host="b0nn3dwlore9g8ifoaeh-mysql.services.clever-cloud.com",
    user="uxlkst3md0khkpki",
    passwd="8x21AHof1FmuTomCtbRg",
    db="b0nn3dwlore9g8ifoaeh"
)
cur = miConexion.cursor()