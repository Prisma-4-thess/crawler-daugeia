import urllib2
import xml.etree.cElementTree as ET
import re, urlparse
import os

def getTags(csr):    # write Fibonacci series up to n
    query = (
      "INSERT INTO tag "
      "(id,version,label)"
      "VALUES (%s,%s,%s)")

    tree = ET.ElementTree(file='tags.xml')
    root = tree.getroot() 
    child = root[0]
    for tag in child:
      try:  
        uid = tag.attrib['uid']
        label = tag[0].text
        data = (uid,1,label)
        csr.execute(query,data)
        # print ("Success. ID "+uid+" entered.")
        if int(uid)%1000 == 1:
          print("ID: "+uid)
      except Exception, e:
        print (uid+" "+str(e))
      
def getTypes(csr):
    query = (
      "INSERT INTO type "
      "(id,version,label)"
      "VALUES (%s,%s,%s)")

    query2 = (
      "INSERT INTO extra "
      "(id,version,form_name,label,name,required,type_id,validation_type)"
      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")

    tree = ET.ElementTree(file='types.xml')
    root = tree.getroot()
    child = root[0]
    for types in child:
      try:  
        typeID = types.attrib['uid']
        typelabel = types[0].text
        extras = types[1]
        data = (typeID,1,typelabel)
        csr.execute(query,data)
      except Exception, e:
        print(typeID+" "+str(e))
      for extra in extras:
          try:
            uid = extra.attrib['uid']
            name = extra[0].text
            label = extra[1].text
            formName = extra[2].text
            required = extra[3].text
            if required=='true':
              required = '1'
            else:
              required = '0'
            validationType = extra[4].text
            data = (uid,1,formName,label,name,required,typeID,validationType)
            # print ('Ready to add '+uid)
            csr.execute(query2,data)
            # print (uid+' added')
          except Exception, e:
            print(uid+" "+str(e))
        # print("Success. ID "+uid+" entered.")
      if int(typeID)%1000 == 1:
        print("ID: "+typeID)


def getSigners(csr):
    query = (
      "INSERT INTO signer "
      "(id,version,active,first_name,last_name,position,title)"
      "VALUES (%s,%s,%s,%s,%s,%s,%s)")

    tree = ET.ElementTree(file='signers.xml')
    root = tree.getroot()
    child = root[0]
    for signer in child:
      try:  
        uid = signer.attrib['uid']
        firstName = signer[0].text
        lastName = signer[1].text
        active = signer[2].text
        if active=='true':
          active = '1'
        else:
          active = '0'
        title = signer[3].text
        position = signer[4].text
        data = (uid,1,active,firstName,lastName,position,title)
        csr.execute(query,data)
        # print("Success. ID "+uid+" entered.")
        if int(uid)%1000 == 1:
          print("ID: "+uid)
      except Exception, e:
        print(uid+" "+str(e))

def getOrgs(csr):
    query = (
      "INSERT INTO organization "
      "(id,version,active,label,latin_name)"
      "VALUES (%s,%s,%s,%s,%s)")

    tree = ET.ElementTree(file='organizations.xml')
    root = tree.getroot()
    child = root[0]
    for org in child:
      try:  
        uid = org.attrib['uid']
        label = org[0].text
        latinName = org[1].text
        active = org[2].text
        if active=='true':
          active = '1'
        else:
          active = '0'
        data = (uid,1,active,label,latinName)
        csr.execute(query,data)
        # print("Success. ID "+uid+" entered.")
        if int(uid)%1000 == 1:
          print("ID: "+uid)
      except Exception, e:
        print(uid+" "+str(e))

def getUnits(csr):
    query = (
      "INSERT INTO unit "
      "(id,version,label,organization_id)"
      "VALUES (%s,%s,%s,%s)")

    tree = ET.ElementTree(file='units.xml')
    root = tree.getroot()
    child = root[0]
    for org in child:
      organization_id = org.attrib['uid']
      units = org[3]
      for unit in units:
        try:
          uid = unit.attrib['uid']
          label = unit[0].text
          data = (uid,1,label,organization_id)
          csr.execute(query,data)
          # print("Success. ID "+uid+" entered.")
        except Exception, e:
          print(organization_id +'/'+ uid+" "+str(e)) 
      # if int(uid)%1000 == 1:
        # print("ID: "+uid)
               
# def getDecisions(csr):
#     query = (
#       "INSERT INTO decision"
#       "(version,ada,date,document_url,protocol_number,signer_id,subject,type_id,unit_id,url,decision_to_correct_id)"
#       "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

#     tree = ET.ElementTree(file='decisions.xml')
#     root = tree.getroot()
#     child = root[0]
#     i=0;
#     for decision in child:
#       # i=i+1;
#       # if i==10:
#         # break
#       ada = decision[0].text
#       # dec_id = findIdDec(csr,ada)
#       # submissionTimestamp = decision[1].text
#       meta = decision[2]
#       protocolNumber = meta[0].text
#       date = meta[1].text
#       subject = meta[2].text
#       organizationId = meta[3].text
#       organizationUnitId = meta[4].text
#       # CHECK IF UNIT IS 0 AND PUT APPROPRIATE
#       if organizationUnitId=='0':
#         organizationUnitId = findZeroUnit(csr,organizationId)
#         organizationUnitId = organizationUnitId[0]
#       decisionTypeId = meta[5].text
#       signerID = meta[7].text
#       url = decision[3].text
#       documentUrl = decision[4].text
#       correcting = None
#       data = (1,ada,date,documentUrl,protocolNumber,signerID,subject,decisionTypeId,organizationUnitId,url,correcting)
#       print len(meta)
#       # print (meta[8])
#       if len(meta)==10:
#         print (meta[9])
#         try:
#           meta[9].tag.index('isCorrectionOfAda')
#           correcting = meta[9].text
#           data = (1,ada,date,documentUrl,protocolNumber,signerID,subject,decisionTypeId,organizationUnitId,url,correcting)
#           csr.execute(query,data)
#         except Exception, e:
#           print("Not correcting ada: " + str(e))
#       if len(meta)==9:
#         if 'isCorrectionOfAda' in meta[8].tag:
#           try:
#             meta[8].tag.index('isCorrectionOfAda')
#             correcting = meta[8].text
#             data = (1,ada,date,documentUrl,protocolNumber,signerID,subject,decisionTypeId,organizationUnitId,url,correcting)
#             csr.execute(query,data)
#           except Exception, e:
#             print("Not correcting ada: " + str(e))    
#       try:
#         correcting = None
#         data = (1,ada,date,documentUrl,protocolNumber,signerID,subject,decisionTypeId,organizationUnitId,url,correcting)
#         csr.execute(query,data)
#       except Exception, e:
#         print(str(e))
#         print(ada +" "+str(organizationUnitId))
#       dec_id = findIdDec(csr,ada)
#       for tag in meta[6]:
#         addTag(csr,tag,dec_id)
#       if len(meta)==9:
#         if 'extraFields' in meta[8].tag:
#           addExtra(csr,meta[8],dec_id,decisionTypeId)
#       # return b
#       i = i+1
#       if i ==109:
#         return meta

def malakesDi(csr):
  query = (
    "INSERT INTO unit "
    "(version,label,organization_id)"
    "VALUES (%s,%s,%s)")

  tree = ET.ElementTree(file='organizations.xml')
  root = tree.getroot()
  child = root[0]
  orgids =[]
  for org in child:
    uid = org.attrib['uid']
    orgids.append(uid)
  
  for myid in orgids:
    data = (1,'<NO-UNIT>',myid)
    try:
      csr.execute(query,data)
    except Exception,e:
      print(myid+' '+str(e))

def findZeroUnit(csr,organizationId):
  query = (
    """SELECT id FROM unit WHERE label =%s AND organization_id=%s""")
  label = ('<NO-UNIT>',organizationId)
  print ('ok')
  csr.execute(query,label)
  print ('ok')
  for unitID in csr:
    return unitID

def addTag(csr,tag,dec_id):

  query_tag = (
      "INSERT INTO decision_tags"
      "(decision_id,tag_id)"
      "VALUES (%s,%s)")

  tagID = tag.text
  try:
    data_tag = (dec_id,tagID)
    csr.execute(query_tag,data_tag)
  except Exception, e:
    print("ID: "+str(dec_id)+" TAG: "+tagID)
    print(str(e))

def addExtra(csr,meta,dec_id,typeID):

  query_extra = (
      "INSERT INTO decision_ext"
      "(version,decision_id,extra_id,value)"
      "VALUES (%s,%s,%s,%s)")
  decExtras = findExtras(csr,typeID)
  print(decExtras)
  for extra in meta:
    # return extra
    extraFormName = extra.attrib['name']
    extraID = decExtras['extrafield_'+extraFormName]
    value = extra[0].text
    try:
      data_extra = (1,dec_id,extraID,value)
      csr.execute(query_extra,data_extra)
    except Exception, e:
      print(str(e))

def findExtras(csr,typeID):
  query = (
    """SELECT id,form_name FROM extra WHERE type_id =%s""")
  extras = {}
  csr.execute(query,(typeID,))
  for extra in csr:
    extras[extra[1]] = extra[0]
  return extras

def findIdDec(csr,ada):
  query = (
    """SELECT id FROM decision WHERE ada =%s""")
  csr.execute(query,(ada,))
  for num in csr:
    return num[0]

def addDecisionsCorrect(csr,mfile):
  query = (
      "INSERT INTO decision"
      "(version,ada,date,document_url,protocol_number,signer_id,subject,type_id,unit_id,url,decision_to_correct_id)"
      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

  stat_url = 'http://83.212.109.124:80/Prisma/pdf/'
  tree = ET.ElementTree(file=mfile)
  root = tree.getroot()
  child = root[0]
  i=0;
  for decision in child:
    i=i+1;
    if i==111:
      break
    ada = decision[0].text
    print (ada)
    meta = decision[2]
    url = decision[3].text
    # doc_url = decision[4].text
    doc_url = stat_url+ada+'.pdf'
    # Add static meta
    protocol_number = meta[0].text
    date = meta[1].text
    subject = meta[2].text
    organization_id = meta[3].text
    organization_unit_id = meta[4].text
    if organization_unit_id=='0':
      organization_unit_id = findZeroUnit(csr,organization_id)
      organization_unit_id = organization_unit_id[0]
    type_id = meta[5].text
    tags_id = meta[6]
    signer_id = meta[7].text
    correcting = None
    print (len(meta))
    if len(meta)>8:
      for x in range(8,len(meta)):
        if 'isCorrectionOfAda' in meta[x].tag:
          correctingADA = meta[x].text
          correcting = str(findIdDec(csr,correctingADA))
          if correcting == 'None':
            print('NO ID FOR CORRECTION')
            getCorrectingADA(csr,correctingADA)
            correcting = str(findIdDec(csr,correctingADA))
            print('********HERE HERE HERE'+correcting)
          else:
            print ('ID FOR CORRECTION: '+correcting)
        elif 'isCorrectedByAda' in meta[x].tag:
          # DO NOTHING
          print("Corrected By Ada")
        elif 'relativeAda' in meta[x].tag:
          # DO NOTHING
          print("Relative Ada")
        elif 'extraFields' in meta[x].tag:
          # addExtra(csr,meta[x],dec_id,decisionTypeId)
          print("Extra Fields")
        else:
          print("NEW TYPE IN META")
    data = (1,ada,date,doc_url,protocol_number,signer_id,subject,type_id,organization_unit_id,url,correcting)
    try:
      csr.execute(query,data)
      # PDF INSERTION
      # dlPDF(ada)
    except Exception, e:
      print (ada)
      print (str(e))
    dec_id = findIdDec(csr,ada)
    for tag_id in tags_id:
      addTag(csr,tag_id,dec_id)
    # Search meta
    if len(meta)>8:
      for x in range(8,len(meta)):
        if 'extraFields' in meta[x].tag:
          addExtra(csr,meta[x],dec_id,type_id)
        elif 'relativeAda' in meta[x].tag:
          print ("***ADDING RELATIVE***")
          addRelative(csr,dec_id,meta[x].text)

def addRelative(csr,dec_id,rada):
  query = (
      "INSERT INTO relative_decision"
      "(version,final_dec_id,related_dec_id)"
      "VALUES (%s,%s,%s)")

  rel_adas = rada.split(',')
  for decision in rel_adas:
    rel_id = str(findIdDec(csr,decision))
    print (rel_id)
    if rel_id == 'None':
      getCorrectingADA(csr,decision)
      rel_id = str(findIdDec(csr,decision))
      print (rel_id)
    try:
      data = (1,dec_id,rel_id)
      csr.execute(query,data)
    except Exception, e:
      print ('error in relative ada')
      print (str(e))

def getXML(request):
  # request = request.decode('iso-8859-7')
  print (request)
  url = u'http://opendata.diavgeia.gov.gr/api/decisions?ada='+request
  url = iriToUri(url)
  print (url)
  opener = urllib2.build_opener()
  opener.addheaders = [
  ('Accept','*/*'),
  ('Connection','Keep-Alive'),
  ('Content-type','text/xml')
  ]
  page = opener.open(url.encode('utf-8')).read()
  mfile = open('export.xml','w')
  mfile.write(page)
  mfile.close()
  
def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

def getCorrectingADA(csr,ada):
  getXML(ada)
  addDecisionsCorrect(csr,'export.xml')

def dlPDF(ada):
  # ada = ada.decode('iso-8859-7')
  theurl = 'http://static.diavgeia.gov.gr/doc/'+ada
  theurl = iriToUri(theurl)
  opener = urllib2.build_opener()
  opener.addheaders = [
  ('Accept','*/*'),
  ('Connection','Keep-Alive'),
  ('Content-type','text/xml')
  ]
  
  # print("... Sending HTTP GET to %s" % theurl)
  f = opener.open(theurl.encode('utf-8'))
  data = f.read()
  f.close()
  opener.close()
  file_path = '/var/lib/tomcat6/webapps/Prisma/pdf'
  completeName = os.path.join(file_path, ada+".pdf")    
  FILE = open(completeName, "wb")
  FILE.write(data)
  FILE.close()

# def getGEO(csr):
#   query = (
#      "INSERT INTO geo"
#      "(version,address,dimos,latitude,longitude,namegrk,new_cat,new_sub_cat,phone,tk)"
#      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")  

#   tree = ET.ElementTree(file='poi_thessalonikis.gml')
#   root = tree.getroot()
#   dimos = u'\u0394\u03ae\u03bc\u03bf\u03c2 \u0398\u03b5\u03c3\u03c3\u03b1\u03bb\u03bf\u03bd\u03af\u03ba\u03b7\u03c2'
#   for member in root:
#     if 'featureMember' in member.tag:
#       # fid = member[0].attrib['fid']
#       address = point_x = point_y = namegrk = newcat = newsubcat = phone = tk = None
#       for meta in member[0]:
#         if 'geometryProperty' in meta.tag:
#           coord = meta[0][0].text
#           coord = coord.split(',')
#           point_x = coord[0]
#           point_y = coord[1]
#         if 'tk' in meta.tag:
#           tk = meta.text
#         if 'newcat' in meta.tag:
#           newcat = meta.text
#         if 'namegrk' in meta.tag:
#           namegrk = meta.text
#         if 'phone' in meta.tag:
#           phone = meta.text
#         if 'newsubcat' in meta.tag:
#           newsubcat = meta.text
#         if 'address' in meta.tag:
#           if meta.tag.endswith('address'):
#             address = meta.text
#       data = (1,address,dimos,point_x,point_y,namegrk,newcat,newsubcat,phone,tk)
#       try:
#         csr.execute(query,data)
#       except Exception, e:
#         print (str(e))

#____KML crawler_______
def getGEO(csr):
  query = (
     "INSERT INTO geo"
     "(version,address,dimos,latitude,longitude,namegrk,new_cat,new_sub_cat,phone,tk)"
     "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")  

  tree = ET.ElementTree(file='poi_thessalonikis.kml')
  root = tree.getroot()
  child = root[0]
  print child
  folder=child[0]
  for member in folder:
    if member.tag == 'Placemark':
      #Structure if each Placemark Element
      name=member[0]
      ext_data=member[1]
      schemadata=ext_data[0]
      dimos = u'\u0394\u03ae\u03bc\u03bf\u03c2 \u0398\u03b5\u03c3\u03c3\u03b1\u03bb\u03bf\u03bd\u03af\u03ba\u03b7\u03c2'
      address = point_x = point_y = namegrk = newcat = newsubcat = phone = tk = None
      for parts in schemadata:
        if parts.attrib['name'] == 'tk':
          tk=parts.text
        if parts.attrib['name'] == 'newcat':
          newcat=parts.text
        if parts.attrib['name'] == 'phone':
          phone=parts.text
          if phone is "0":
            phone = None
        if parts.attrib['name'] == 'address':
          address=parts.text
        if parts.attrib['name'] == 'newsubcat':
          newsubcat=parts.text
        if parts.attrib['name'] == 'namegrk':
          namegrk=parts.text
      point=member[2]
      coord=point[0]
      coordstr=coord.text.split(',',2)
      coordX=coordstr[1]
      coordY=coordstr[0]
      data = (1,address,dimos,coordX,coordY,namegrk,newcat,newsubcat,phone,tk)
      # for temp in data:
      #   print (temp)
      try:
        csr.execute(query,data)
      except Exception, e:
        print (str(e))
