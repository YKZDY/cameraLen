from pyfbsdk import *
from pyfbsdk_additions import *
from functools import partial
import math


cameraData=[]
lensData=[]
title='cameraLen'
filePath="C:\Users\Calven\OneDrive\Documents\workCloud\MobuCoder\cameraLen"

f=open(filePath+'\cameraData.txt','r+')
data=f.readlines()
data[-1]=data[-1]+'\r\n'
for i in data:
    cameraData.append(i[:-1])
f.close()
f=open(filePath+'\lensData.txt','r+')
data=f.readlines()
data[-1]=data[-1]+'\r\n'
for i in data:
    lensData.append(i[:-1])
f.close()

def mathAngle(x,f):
    rad=2*math.atan((25.4*x)/(2*f))
    gad=(rad/6.283185306)*360
    return round(gad,2)

def mathField(x,y):
    return math.sqrt(x*x+y*y)

class cameraLen(FBTool):
    def __init__(self):
        self.title=title
        FBTool.__init__(self,self.title)
        FBAddTool(self)
        self.StartSizeX = 400
        self.StartSizeY = 520
        self.actionButtonName='apply and close'
        self.applyButtonName='apply'
        self.closeButtonName='close'
        self.cameraTabName='camera'
        self.cameraManufacturerName='camera manufacturer :'
        self.cameraModelName='camera model :'
        self.lensTabName='lens'
        self.lensManufacturerName='lens manufacturer :'
        self.lensModelName='lens model :'
        self.focalLengthName='focal length :'
        self.selectTabName='select'
        self.selectCameraName='select camera :'
        self.temp='NONE'
        self.sign=[]
        self.cameraRadioName=[]
        self.lensRadioName=[]
        self.cameraMenuList=[]
        self.lensMenuList=[]
        self.selectCameraList=[]
        self.cameraList=[]
        self.lensList=[]
        for i in cameraData:
            if i[0] is '#':
                self.cameraRadioName.append(i[1:])
                self.cameraList.append(['NONE'])
            else:
                self.cameraList[len(self.cameraRadioName)-1].append(i.split(' '))
        for i in range(len(self.cameraList)):
            del self.cameraList[i][0]
        for i in lensData:
            if i[0] is '#':
                self.lensRadioName.append(i[1:])
                self.lensList.append(['NONE'])
            else:
                self.lensList[len(self.lensRadioName)-1].append(i.split(' '))
        for i in range(len(self.lensList)):
            del self.lensList[i][0]
    def bulidLayout(self):
        x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
        y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
        w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
        h = FBAddRegionParam(0,FBAttachType.kFBAttachBottom,"")
        self.AddRegion("main","main", x, y, w, h)
        x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"main")
        y = FBAddRegionParam(10,FBAttachType.kFBAttachTop,"main")
        w = FBAddRegionParam(-10,FBAttachType.kFBAttachRight,"main")
        h = FBAddRegionParam(180,FBAttachType.kFBAttachNone,"")
        self.AddRegion("camera","camera", x, y, w, h)
        self.SetBorder("camera",FBBorderStyle.kFBEmbossSmoothEdgeBorder,True, True,2,-2,90,0)
        x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"main")
        y = FBAddRegionParam(10,FBAttachType.kFBAttachBottom,"camera")
        w = FBAddRegionParam(-10,FBAttachType.kFBAttachRight,"main")
        h = FBAddRegionParam(190,FBAttachType.kFBAttachNone,"")
        self.AddRegion("lens","lens", x, y, w, h)
        self.SetBorder("lens",FBBorderStyle.kFBEmbossSmoothEdgeBorder,True, True,2,-2,90,0)
        x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"main")
        y = FBAddRegionParam(10,FBAttachType.kFBAttachBottom,"lens")
        w = FBAddRegionParam(-10,FBAttachType.kFBAttachRight,"main")
        h = FBAddRegionParam(50,FBAttachType.kFBAttachNone,"")
        self.AddRegion("select","select", x, y, w, h)
        self.SetBorder("select",FBBorderStyle.kFBEmbossSmoothEdgeBorder,True, True,2,-2,90,0)
        x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"main")
        y = FBAddRegionParam(10,FBAttachType.kFBAttachBottom,"select")
        w = FBAddRegionParam(-10,FBAttachType.kFBAttachRight,"main")
        h = FBAddRegionParam(30,FBAttachType.kFBAttachNone,"")
        self.AddRegion("button","button", x, y, w, h)
        x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"camera")
        y = FBAddRegionParam(10,FBAttachType.kFBAttachTop,"camera")
        w = FBAddRegionParam(-10,FBAttachType.kFBAttachRight,"camera")
        h = FBAddRegionParam(-10,FBAttachType.kFBAttachBottom,"camera")
        self.AddRegion("cameraSet","cameraSet", x, y, w, h)
        x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"lens")
        y = FBAddRegionParam(10,FBAttachType.kFBAttachTop,"lens")
        w = FBAddRegionParam(-10,FBAttachType.kFBAttachRight,"lens")
        h = FBAddRegionParam(-10,FBAttachType.kFBAttachBottom,"lens")
        self.AddRegion("lensSet","lensSet", x, y, w, h)
        x = FBAddRegionParam(10,FBAttachType.kFBAttachLeft,"select")
        y = FBAddRegionParam(10,FBAttachType.kFBAttachTop,"select")
        w = FBAddRegionParam(-10,FBAttachType.kFBAttachRight,"select")
        h = FBAddRegionParam(-10,FBAttachType.kFBAttachBottom,"select")
        self.AddRegion("selectSet","selectSet", x, y, w, h)
    def angleText(self):
        self.flag=self.temp
        if (self.cameraText.Caption != 'NONE')and(self.temp != 'NONE'):
            self.HOVapply=mathAngle(self.apertureHApply,self.focalLengthApply)
            self.VOVapply=mathAngle(self.apertureVApply,self.focalLengthApply)
            self.FOVapply=mathAngle(mathField(self.apertureHApply,self.apertureVApply),self.focalLengthApply)
            self.flag=self.flag+'\n  H Angle of View : '+"{:^5.2f}".format(self.HOVapply)+' (deg)'\
                +'\n  V Angle of View : '+"{:^5.2f}".format(self.VOVapply)+' (deg)'\
                +'\n  F Angle of View : '+"{:^5.2f}".format(self.FOVapply)+' (deg)'
        if not self.temp == 'NONE':
            self.lensText.Caption=self.flag
    def changeCameraList(self,control,*args):
        self.cameraFlag=self.cameraRadioName.index(control.Caption)
        self.cameraModelList.Items.removeAll()
        for i in self.cameraList[self.cameraFlag]:
            self.cameraModelList.Items.append(i[0])
        self.cameraModelList.Selected(0,True)
        self.cameraListCallback(self.cameraModelList)
    def changeLensList(self,control,*args):
        self.lensFlag=self.lensRadioName.index(control.Caption)
        self.lensModelList.Items.removeAll()
        for i in self.lensList[self.lensFlag]:
            self.lensModelList.Items.append(i[0])
        self.lensModelList.Selected(0,True)
        self.lensListCallback(self.lensModelList)
    def cameraListCallback(self,control,*args):
        for i in self.cameraList:
            for j in i:
                if j[0] == control.Items[control.ItemIndex]:
                    self.cameraText.Caption='\n  H Film Aperture : '+str(round(float(j[1])/25.4,2))+' (in) '+j[1]+' (mm)'+\
                    '\n  V Film Aperture : '+str(round(float(j[2])/25.4,2))+' (in) '+j[2]+' (mm)'+\
                    '\n     H Resolution : '+j[3]+' (pixel)'+\
                    '\n     V Resolution : '+j[4]+' (pixel)'+\
                    '\nFilm Aspect Ratio : '+str(round(float(j[1])/float(j[2]),2))
                    self.apertureHApply=float(j[1])/25.4
                    self.apertureVApply=float(j[2])/25.4
        self.angleText()
    def lensListCallback(self,control,*args):
        for i in self.lensList:
            for j in i:
                if j[0] == control.Items[control.ItemIndex]:
                    if j[1]=='prime':
                        self.flag='\n     Focal Length : '+j[2]+' (mm)'
                        self.temp=self.flag
                        self.focalLengthApply=float(j[2])
                        self.focalLengthEdit.ReadOnly=True
                        self.focalLengthEdit.Min=float(j[2])
                        self.focalLengthEdit.Max=float(j[2])+1
                        self.focalLengthEdit.Value=float(j[2])
                    else:
                        self.flag='\n     Focal Length : '+j[2]+' (mm) - '+j[3]+' (mm)'
                        self.temp=self.flag
                        self.focalLengthApply=float(j[2])
                        self.focalLengthEdit.ReadOnly=False
                        self.focalLengthEdit.Min=float(j[2])
                        self.focalLengthEdit.Max=float(j[3])
                        self.focalLengthEdit.Value=float(j[2])
        self.angleText()
    def focalLengthCmd(self,control,*args):
        self.focalLengthApply=control.Value
        self.angleText()
    def selectRefresh(self,*args):
        self.selectList.Items.removeAll()
        for i in FBSystem().Scene.Cameras:
            if i.Name[:8] != "Producer":
                self.selectList.Items.append(i.Name)
        self.selectCmd(self.selectList)
    def selectCmd(self,control,*args):
        if len(control.Items) != 0:
            self.selectCameraApply=control.Items[control.ItemIndex]
    def configButton(self):
        self.buttonLayout=FBHBoxLayout()
        self.actionButton=FBButton()
        self.actionButton.Caption=self.actionButtonName
        self.actionButton.Justify=FBTextJustify.kFBTextJustifyCenter
        self.actionButton.OnClick.Add(self.actionButtonCmd)
        self.buttonLayout.AddRelative(self.actionButton)
        self.applyButton=FBButton()
        self.applyButton.Caption=self.applyButtonName
        self.applyButton.Justify=FBTextJustify.kFBTextJustifyCenter
        self.applyButton.OnClick.Add(self.applyButtonCmd)
        self.buttonLayout.AddRelative(self.applyButton)
        self.closeButton=FBButton()
        self.closeButton.Caption=self.closeButtonName
        self.closeButton.Justify=FBTextJustify.kFBTextJustifyCenter
        self.closeButton.OnClick.Add(self.closeButtonCmd)
        self.buttonLayout.AddRelative(self.closeButton)
        self.SetControl("button",self.buttonLayout)
    def configCamera(self):
        self.cameraLayout=FBVBoxLayout()
        self.SetControl("cameraSet",self.cameraLayout)

        self.cameraManufacturer=FBLabel()
        self.cameraManufacturerLayout=FBHBoxLayout()
        self.cameraManufacturerLayout.AddRelative(self.cameraManufacturer)    
        self.cameraManufacturer.Caption=self.cameraManufacturerName
        self.cameraLayout.Add(self.cameraManufacturerLayout,10)

        self.cameraRadioLayout=FBGridLayout()
        self.cameraRadio=[]
        self.cameraRadioGroup=FBButtonGroup()
        self.cameraRadioGroup.AddCallback(self.changeCameraList)
        for i in range(0,len(self.cameraRadioName)):
            self.cameraRadio.append(FBButton())
            self.cameraRadio[i].Style=FBButtonStyle.kFBRadioButton
            self.cameraRadio[i].Caption=self.cameraRadioName[i]
            self.cameraRadioGroup.Add(self.cameraRadio[i])
            self.cameraRadioLayout.Add(self.cameraRadio[i],i/4,i%4)
        self.cameraLayout.Add(self.cameraRadioLayout,(len(self.cameraRadioName)/4)*20+30)

        self.cameraModelLayout=FBHBoxLayout()
        self.cameraModel=FBLabel()
        self.cameraModelList=FBList()
        self.cameraModel.Caption=self.cameraModelName
        self.cameraModelList.OnChange.Add(self.cameraListCallback)
        self.cameraModelLayout.AddRelative(self.cameraModel,0.5)
        self.cameraModelLayout.AddRelative(self.cameraModelList)
        self.cameraLayout.Add(self.cameraModelLayout,20)
        
        self.cameraText=FBLabel()
        self.cameraTextLayout=FBHBoxLayout()
        self.cameraTextLayout.AddRelative(self.cameraText)
        self.cameraText.Caption=self.temp
        self.cameraText.Style=FBTextStyle.kFBTextStyleItalic
        self.cameraLayout.AddRelative(self.cameraTextLayout)
    def configLens(self):
        self.lensLayout=FBVBoxLayout()
        self.SetControl("lensSet",self.lensLayout)

        self.lensManufacturer=FBLabel()
        self.lensManufacturerLayout=FBHBoxLayout()
        self.lensManufacturerLayout.AddRelative(self.lensManufacturer)    
        self.lensManufacturer.Caption=self.lensManufacturerName
        self.lensLayout.Add(self.lensManufacturerLayout,10)

        self.lensRadioLayout=FBGridLayout()
        self.lensRadio=[]
        self.lensRadioGroup=FBButtonGroup()
        self.lensRadioGroup.AddCallback(self.changeLensList)
        for i in range(0,len(self.lensRadioName)):
            self.lensRadio.append(FBButton())
            self.lensRadio[i].Style=FBButtonStyle.kFBRadioButton
            self.lensRadio[i].Caption=self.lensRadioName[i]
            self.lensRadioGroup.Add(self.lensRadio[i])
            self.lensRadioLayout.Add(self.lensRadio[i],i/4,i%4)
        self.lensLayout.Add(self.lensRadioLayout,(len(self.lensRadioName)/4)*20+30)

        self.lensModelLayout=FBHBoxLayout()
        self.lensModel=FBLabel()
        self.lensModelList=FBList()
        self.lensModel.Caption=self.lensModelName
        self.lensModelList.OnChange.Add(self.lensListCallback)
        self.lensModelLayout.AddRelative(self.lensModel,0.5)
        self.lensModelLayout.AddRelative(self.lensModelList)
        self.lensLayout.Add(self.lensModelLayout,20)

        self.focalLengthLayout=FBHBoxLayout()
        self.focalLength=FBLabel()
        self.focalLengthEdit=FBEditNumber()
        self.focalLengthEdit.ReadOnly=True
        self.focalLengthEdit.OnChange.Add(self.focalLengthCmd)    
        self.focalLength.Caption=self.focalLengthName
        self.focalLengthLayout.AddRelative(self.focalLength,0.5)
        self.focalLengthLayout.AddRelative(self.focalLengthEdit)
        self.lensLayout.Add(self.focalLengthLayout,20)

        self.lensText=FBLabel()
        self.lensTextLayout=FBHBoxLayout()
        self.lensTextLayout.AddRelative(self.lensText)
        self.lensText.Caption=self.temp
        self.lensText.Style=FBTextStyle.kFBTextStyleItalic
        self.lensLayout.AddRelative(self.lensTextLayout)
    def configSelect(self):
        self.selectLayout=FBVBoxLayout()
        self.SetControl("selectSet",self.selectLayout)
        self.selectCameraLayout=FBHBoxLayout()
        self.selectTitle=FBLabel()
        self.selectList=FBList()
        self.selectRefreshButton=FBButton()
        self.selectList.OnChange.Add(self.selectCmd)
        self.selectRefresh()
        self.selectTitle.Caption=self.selectCameraName
        self.selectRefreshButton.Caption="RE"
        self.selectCmd(self.selectList)
        self.selectRefreshButton.OnClick.Add(self.selectRefresh)
        self.selectCameraLayout.AddRelative(self.selectTitle,0.56)
        self.selectCameraLayout.AddRelative(self.selectList)
        self.selectCameraLayout.Add(self.selectRefreshButton,20)
        self.selectLayout.AddRelative(self.selectCameraLayout)
    def applyButtonCmd(self,*args):
        for i in FBSystem().Scene.Cameras :
            if i.Name == self.selectCameraApply :
                i.FieldOfView=self.FOVapply
    def closeButtonCmd(self,*args):
        CloseTool(win)
    def actionButtonCmd(self,*args):
        self.applyButtonCmd()
        self.closeButtonCmd()
    def create(self):
        self.bulidLayout()
        self.configButton()
        self.configCamera()
        self.configLens()
        self.configSelect()
if title in FBToolList:
    FBDestroyToolByName(title)
win=cameraLen()
win.create()
ShowTool(win)