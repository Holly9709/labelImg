# -*- coding: utf-8 -*-
import pylab as pl
import xml.dom.minidom 
import os.path
import os

def IOU(Reframe=[],GTframe=[]):
    x1 = Reframe[0]
    y1 = Reframe[1]
    width1 = Reframe[2]-Reframe[0]
    height1 = Reframe[3]-Reframe[1]
    
    x2 = GTframe[0]
    y2 = GTframe[1]
    width2 = GTframe[2]-GTframe[0]
    height2 = GTframe[3]-GTframe[1]

    endx = max(x1+width1,x2+width2)
    startx = min(x1,x2)
    width = width1+width2-(endx-startx)

    endy = max(y1+height1,y2+height2)
    starty = min(y1,y2)
    height = height1+height2-(endy-starty)

    if width <=0 or height <= 0:
        ratio = 0 
    else:
        Area = width*height
        Area1 = width1*height1
        Area2 = width2*height2
        ratio = Area*1./(Area1+Area2-Area)
    # return IOU
    return ratio#,Reframe,GTframe

def read(root):
    Reframe=[]
    #filename=root.getElementsByTagName('filename')
    xmin=root.getElementsByTagName('xmin')
    xmax=root.getElementsByTagName('xmax')
    ymin=root.getElementsByTagName('ymin')
    ymax=root.getElementsByTagName('ymax')
    rectnum = len(xmin)
    #n0=filename[0]
    #Name = n0.firstChild.data
    #Reframe.append(Name)
    for i in range(0,rectnum):
        n1=xmin[i]
        n2=xmax[i]
        n3=ymin[i]
        n4=ymax[i]
        Xmin=Ymin=Xmax=Ymax=0
        Xmin = int(n1.firstChild.data)
        Xmax = int(n2.firstChild.data)
        Ymin = int(n3.firstChild.data)
        Ymax = int(n4.firstChild.data)
        Reframe.append([Xmin,Ymin,Xmax,Ymax])
    return Reframe
               
def Analyze_xml(standard_path,test_path):
    wrong,creat,pos=0,0,0
    ratio=0.
    list1=[]
    Reframe=GTframe=[]
    path1=standard_path
    path2=test_path
    files1 = os.listdir(path2)
    
    for xmlFile in files1:
        
        testpath_xml=os.path.join(path2,xmlFile)
        standpath_xml=testpath_xml.replace(path2,path1)
        
        if os.path.isfile(standpath_xml):
            dom_test=xml.dom.minidom.parse(testpath_xml)
            dom_stand=xml.dom.minidom.parse(standpath_xml)
            root1=dom_test.documentElement
            root2=dom_stand.documentElement
            Reframe=read(root1)
            GTframe=read(root2)
            pos+=len(GTframe)
            
            if len(GTframe)>len(Reframe):
                for i in range(len(GTframe)-len(Reframe)):
                    list1.append([0,1,0])
                    
            for i in range(len(Reframe)):
                wrong=creat=0
                for j in range(len(GTframe)):
                    ratio=IOU(Reframe[i],GTframe[j])
                    if ratio>=0.5:
                        creat=1
                        list1.append([creat,wrong,ratio])
                        break
                if creat==0:
                    wrong=1
                    list1.append([creat,wrong,ratio])
                
        else:
            creat=wrong=0
            dom_test=xml.dom.minidom.parse(testpath_xml)
            root1=dom_test.documentElement
            Reframe=read(root1)
            for i in range(len(Reframe)):
                ratio=0
                wrong=1
                list1.append([creat,wrong,ratio])
    return list1,pos
            
        

def roc(standard_path, test_path, saveDir):
    db=[]
    db,pos=Analyze_xml(standard_path,test_path)
    #db = sorted(db, key=lambda x:x[2], reverse=True)#sorted() 
  
    xy_arr = []
    tp,fp = 0., 0.			
    for i in range(len(db)):
        tp += db[i][1]#wrong
        fp += db[i][0]#creat
        xy_arr.append([tp,fp/pos])
   
    auc = 0.			
    prev_x = 0
    for x,y in xy_arr:
	    if x != prev_x:
		    auc += (x - prev_x) * y
		    prev_x = x     
          
    x = [_a[0] for _a in xy_arr]
    y = [_a[1] for _a in xy_arr]
    pl.title("ROC (AUC = %.4f)" % (auc))
    pl.xlabel("False Count")
    pl.ylabel("True Positive Rate")
    pl.plot(x, y)
    pl.show()
    result_roc = os.path.join(saveDir, 'result_roc.txt')
    result_IOU = os.path.join(saveDir, 'result_IOU.txt')
    with open(result_roc, 'w') as fp:
        for i in range(len(db)):
            fp.write("%d %f \n" % (x[i], y[i]))
    with open(result_IOU, 'w') as fp:
        for i in range(len(db)):
            fp.write("%d %d %f \n" % (db[i][0], db[i][1],db[i][2]))
    
if __name__ == '__main__':
    roc()