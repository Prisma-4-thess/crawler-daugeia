import xml.etree.cElementTree as ET
import codecs
import mysql.connector
import diaugeia as di
from mysql.connector import errorcode

try:
  # cnx = mysql.connector.connect(user='*******', password='***********',
  #                             host='83.212.109.124',charset='utf8',
  #                             database='******')

  cnx = mysql.connector.connect(user='******', password='***********',
                              host='localhost',charset='utf8',
                              database='******')

  csr = cnx.cursor()
  #  print("tags")
  #  di.getTags(csr)
  # # cnx.commit()
  #  print("types")
  #  di.getTypes(csr)
  # # cnx.commit()
  #  print("signers")
  #  di.getSigners(csr)
  # # cnx.commit()
  #  print("orgs")
  #  di.getOrgs(csr)
  # # cnx.commit()
  #  print("units")
  #  e = di.findExtras(csr,20)
  #  print (e)
  #  di.getUnits(csr)
  # # cnx.commit()
  # # print("null")
  # # di.malakesDi(csr)
  # # cnx.commit()
  print("decision")
  di.addDecisionsCorrect(csr,'decisions.xml')
  # print("geo")
  # di.getGEO(csr)
  cnx.commit()
  csr.close()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exists")
  else:
    print(err)
cnx.close()
