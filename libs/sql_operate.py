#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import os.path
import xml.dom.minidom
import MySQLdb
import sys
import random

global oneInNum
global project_name
#project_name='test0720'
project_name='test0724'
global db
global idNum
idNum = 0
global idNumSelect

def con_db():
    global project_name
    hostName = "172.23.250.51"
    userName = "root"
    passWord = "20180712"
    #dataBase = "ground_truth"
    dataBase = project_name
    charset = "utf8"
    db = MySQLdb.connect("%s"%(hostName), "%s"%(userName), "%s"%(passWord), "%s"%(dataBase), charset='utf8' )
    
    global oneInNum
    oneInNum = 20
    global idNum
    idNum = 0
    
    return db

db = con_db()
def setProjectName(projectNameNew):
    global project_name,db
    project_name_old=project_name
    #project_name = str(projectNameNew)
    #cursor = db.cursor()
    #cursor_execute("use %s"%(projectName))
    db.close()
    message = []
    try:
        project_name = str(projectNameNew)
        db=con_db()
        message.append("set project_name=%s success.project_name=%s"%(projectNameNew,project_name))
        message.append(True)
    except Exception as e:
        print e
        #message=e
        #message="set project_name=%s failed."%(projectNameNew)
        project_name=project_name_old
        message.append("set project_name=%s failed.project_name=%s"%(projectNameNew,project_name))
        message.append(False)
        db=con_db()
    print message
    return message
def insert2sql(xmlfile):
    global project_name 
    global db
    #connect xml databases to upload xml file.
    cursor = db.cursor()
    
    with open(xmlfile, "r") as f:
        xml_content = f.read()
    filename = str(xmlfile).split('\\')[-1]
    image_name = filename[:-4]
    #print "xml_content:",xml_content

    #sql = "SELECT xml_content FROM pngtry WHERE image_name = '%s'"%(image_name)
    
    sql = "SELECT xml_content FROM %sxml WHERE image_name = '%s'"%(project_name,image_name)
    is_null = cursor_execute(sql)    

    if is_null == None:
        sql = "INSERT INTO %sxml (image_name, xml_content) VALUES ('%s','%s')"%(project_name,image_name,xml_content)
    else:
        sql = "UPDATE %sxml SET xml_content = '%s' WHERE image_name = '%s'" % (project_name,xml_content, image_name)
        
    cursor_execute(sql) 
    
    # db.close()
    
    #connect image database to change "is_marking" state.
    #db = con_db()
    #cursor = db.cursor()
    
    #cursor_execute("UPDATE %simg SET is_marking = 'done' WHERE image_name = '%s'"%(project_name,image_name))
    #print "%s xml file has update in database."% image_name

    db.commit()  

def cursor_execute(sqlstr):
    global db
    cursor = db.cursor()
    content=None
    try:
        #sql = "SELECT xml_content FROM %sxml WHERE image_name = '%s'"%(project_name,image_name)
        #sql = "SELECT xml_content FROM %sxml WHERE image_name = '%s'"%(project_name,image_name)
        cursor.execute(sqlstr)
        content = cursor.fetchone()
    except Exception as e:
        print sqlstr
        print e
    return content



def xmlfromsql(xmlpath):
    global project_name
    global db
    
    cursor = db.cursor()
    
    filename = str(xmlpath).split('\\')[-1]
    image_name = filename[:-4]
    #print image_name 
    #sql = "SELECT xml_content FROM pngtry WHERE image_name = '%s'"%(image_name)
    sql = "SELECT xml_content FROM %sxml WHERE image_name = '%s'"%(project_name,image_name)
    #xml_content = cursor_execute(sql)
    xml_content=cursor_execute(sql)
    print "xml content:",xml_content
    if xml_content == None:
        return
    else:
        if not os.path.isfile(xmlpath):     
            fout = open(xmlpath,'wb')
            fout.write("")
            fout.write(xml_content[0])
            fout.close()
            print "The xml file have downloaded form database."
        else:
            return
    
    db.commit()
    #cursor.close()

def resetIdNum():
    global idNum
    idNum = 0
    print idNum

def imagefromsql(dirpath, softwareMode = 'resume'):
    global project_name
    global db
    global idNum
    global idNumSelect

    if softwareMode == 'verify':
        global oneInNum
        #cursor_execute("SELECT image_name FROM pngtry WHERE (is_marking = 'done' and if_verify = 'no') LIMIT %d"% oneInNum)
        cursor_content = cursor_execute("SELECT count(*) FROM %simg WHERE (is_marking = 'done' and if_verify = 'no') "%(project_name))
        remainNum = cursor_content[0]
        if remainNum == 0:
            print "No more picture!"
            return
        elif remainNum > 0 and remainNum < oneInNum:
            oneInNum = remainNum
        
        
        cursor = db.cursor()
        cursor.execute("SELECT id FROM %simg WHERE (is_marking = 'done' and if_verify = 'no') ORDER BY id LIMIT 20"%(project_name))
        idTuple = tuple(cursor.fetchall())
        print"id tuple:", idTuple
        select = random.randint(0, oneInNum-1)
        #idTuple is two-dimensional tuple
        idNumSelect = idTuple[select][0]
        cursor = cursor_execute("SELECT image_name FROM %simg WHERE id = %d"%(project_name, idNumSelect))
        image_name = cursor[0]
        print "Now the id of image which you are checking is %d."% idNumSelect
        #print "imgname_list[0][0]: ", imgname_list[0][0]
        imagepath = str(dirpath)+'\\'+str(image_name)+'.png'
    
        if not os.path.isfile(imagepath):
            #cursor_execute("SELECT raw_data FROM pngtry WHERE image_name = '%s'"% image_name)
            cursor = cursor_execute("SELECT raw_data FROM %simg WHERE id = %d"%(project_name, idNumSelect))

            fout = open(imagepath,'wb')
            fout.write(cursor[0])
            print "The image whose id in table is %d have downloaded from database."% idNumSelect      
            #cursor_execute("UPDATE pngtry SET is_marking = 'yes' WHERE image_name = '%s'"% image_name)

    elif softwareMode == 'no_resume':
        
        cursor = cursor_execute("SELECT count(*) FROM %simg"%(project_name))
        allImgNum = cursor[0]
        print "The number of all image :", allImgNum
        if allImgNum < idNum:
            print "No more picture!"
            return
        
        if idNum == 0:
            idNum += 1
        cursor = cursor_execute("SELECT image_name FROM %simg WHERE id = %d ORDER BY id LIMIT 1"%(project_name, idNum))
        image_name = (cursor[0])
        #print "image_name: ",image_name
        imagepath = str(dirpath)+'\\'+str(image_name)+'.png'
    
        if not os.path.isfile(imagepath):
            #cursor_execute("SELECT raw_data FROM pngtry WHERE image_name = '%s'"% image_name)
            cursor = cursor_execute("SELECT raw_data FROM %simg WHERE id = %d "%(project_name, idNum))

            fout = open(imagepath,'wb')
            fout.write(cursor[0])
            print "The image whose id in table is %d have downloaded from database."% idNum
        
        idNum += 1   
            #cursor_execute("UPDATE pngtry SET is_marking = 'yes' WHERE image_name = '%s'"% image_name)    
        
    elif softwareMode == 'resume':
        
        cursor = cursor_execute("SELECT count(*) FROM %simg"%(project_name))
        allImgNum = cursor[0]
        cursor = cursor_execute("SELECT count(*) FROM %simg WHERE is_marking = 'no'"%(project_name))
        remainNum = cursor[0]
        markedNum = allImgNum - remainNum
        print "%d images have been marked."% markedNum
        if remainNum == 0:
            print "No more picture!"
            return
        #cursor_execute("SELECT image_name FROM pngtry WHERE is_marking ='no' LIMIT 1")
        cursor = cursor_execute("SELECT id FROM %simg WHERE is_marking ='no' ORDER BY id LIMIT 1"%(project_name))
        idNum = cursor[0]
        cursor = cursor_execute("SELECT image_name FROM %simg WHERE id = %d LIMIT 1"%(project_name, idNum))
        image_name = cursor[0]
        #print "image_name: ",image_name
        imagepath = str(dirpath)+'\\'+str(image_name)+'.png'
    
        if not os.path.isfile(imagepath):
            #cursor_execute("SELECT raw_data FROM pngtry WHERE image_name = '%s'"% image_name)
            cursor = cursor_execute("SELECT raw_data FROM %simg WHERE id = %d"%(project_name, idNum))

            fout = open(imagepath,'wb')
            fout.write(cursor[0])
            print "The image whose id in table is %d have downloaded from database."% idNum
            #cursor_execute("UPDATE pngtry SET is_marking = 'yes' WHERE image_name = '%s'"% image_name)    
            
            cursor_execute("UPDATE %simg SET is_marking = 'done' WHERE id = %d"%(project_name, idNum))
            print "The is_marking status has update to 'done' in database."
            idNum += 1
            
    db.commit()
    #cursor.close()
    return imagepath

def veriResult(imgName, result):
    global project_name
    global db
    global idNumSelect
    global idNum
    global oneInNum
    
    cursor = db.cursor()
    #cursor_execute("UPDATE pngtry SET if_verify = '%s' WHERE image_name = '%s'"%(result, imgName))
    cursor.execute("SELECT id FROM %simg WHERE (is_marking = 'done' and if_verify = 'no') ORDER BY id LIMIT 20"%(project_name))
    idNumListTuple = list(tuple(cursor.fetchall()))
    idNumList = []
    for i in range(0,oneInNum):
        idNumList.append(idNumListTuple[i][0])
    print"id list:", idNumList 
    cursor_execute("UPDATE %simg SET if_verify = '%s' WHERE id = %d"%(project_name,result, idNumSelect))

    #cursor_execute("SELECT image_name FROM pngtry WHERE (is_marking = 'done' and if_verify = 'no') LIMIT %d"% (oneInNum-1))
    print "idNumSelect: ", idNumSelect
    idNumList.remove(idNumSelect)
    #print "set jump tuple lenfgth:", len(idNumList)
    print "id list2:", idNumList
    for i in idNumList:
        #cursor_execute("UPDATE pngtry SET if_verify = 'jump' WHERE image_name = '%s'"% imgname_list[i][0])
        cursor_execute("UPDATE %simg SET if_verify = 'jump' WHERE id = %d"%(project_name,i))
    db.commit()
    #cursor.close()

def veriCount():
    global project_name
    global db
    #list :rightNum, wrongNum, rate,veriNum,tabelVeriNum, allImgNum, veriRate
    cursor = db.cursor()
    resultList = ()
    cursor = cursor_execute("SELECT count(*) FROM %simg WHERE if_verify = '%s'"%(project_name, 'is_verified_right'))
    rightNum = cursor[0]
    #resultList.append(rightNum)
    cursor = cursor_execute("SELECT count(*) FROM %simg WHERE if_verify = '%s'"%(project_name, 'is_verified_wrong'))
    wrongNum = cursor[0]
    #resultList.append(wrongNum)
    veriNum = rightNum + wrongNum
    rate = float(rightNum) / float(veriNum)
    rate = '%.3f'% rate
    #resultList.append(rate)
    #resultList.append(veriNum)
    cursor = cursor_execute("SELECT count(*) FROM %simg WHERE if_verify != 'no'"%(project_name))
    tabelVeriNum = cursor[0]
    #resultList.append(tabelVeriNum)
    cursor = cursor_execute("SELECT count(*) FROM %simg WHERE is_marking = 'done'"%(project_name))
    allImgNum = cursor[0]
    #resultList.append(allImgNum)
    veriRate = float(tabelVeriNum) / float(allImgNum)
    veriRate = '%.2f'% veriRate
    #resultList.append(veriRate)
    resultList = (rightNum, wrongNum, rate,veriNum,tabelVeriNum, allImgNum, veriRate)
    
    db.commit()
    #cursor.close()
    return resultList

def markCount():
    
    global project_name
    global db
    #list :markNum, allNum, markRate
    cursor = db.cursor()
    resultList = ()
    cursor = cursor_execute("SELECT count(*) FROM %simg WHERE is_marking = 'done'"%(project_name))
    markNum = cursor[0]
    cursor = cursor_execute("SELECT count(*) FROM %simg "%(project_name))
    allNum = cursor[0]
    markRate = float(markNum) / float(allNum)
    markRate = '%.2f'% markRate
    resultList = (markNum, allNum, markRate)
    return resultList
    
def delfile():
    global db
    db.close()

    delList = []
    delDir = "C:\markimage"
    if os.path.isdir(delDir):
        delList = os.listdir(delDir)

        for f in delList:
            filePath = os.path.join( delDir, f )
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath,True)
        os.rmdir(delDir)
        print "Directory: " + delDir +" was removed!"
                
    delList = []
    delDir = "C:\markxml"
    if os.path.isdir(delDir):
        delList = os.listdir(delDir)

        for f in delList:
            filePath = os.path.join( delDir, f )
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath,True)
        os.rmdir(delDir)
        print "Directory: " + delDir +" was removed!"

#imagefromsql(r'D:\file\try\trydown_png', True)
