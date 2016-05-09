import sys
import os
import maya.OpenMayaMPx as ommpx
import maya.cmds as cmds
from functools import partial
import math

kPluginCmdName='cameraLen'

cameraData=[]
lensData=[]
filePath=os.path.abspath(os.path.dirname(sys.argv[0]))

print filePath

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
class cameraLen(object):
	def __init__(self):
		self.size=(400,520)
		self.title='cameraLen'
		self.actionButtonName='apply and close'
		self.applyButtonName='apply'
		self.closeButtonName='close'
		self.cameraManufacturerName='camera manufacturer'
		self.cameraModelName='camera model'
		self.lensManufacturerName='lens manufacturer'
		self.lensModelName='lens model'
		self.focalLengthName='focal length'
		self.selectCameraName='select camera'
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
	def angleText(self):
		self.flag=self.temp
		if not ((cmds.text(self.cameraText,q=True,l=True) == 'NONE')or(self.temp == 'NONE')):
			self.flag=(self.flag+'\nH Angle of View : '+str(mathAngle(self.apertureHApply,self.focalLengthApply))+' (deg)'
				+'\nV Angle of View : '+str(mathAngle(self.apertureVApply,self.focalLengthApply))+' (deg)'
				+'\nF Angle of View : '+str(mathAngle(mathField(self.apertureHApply,self.apertureVApply),self.focalLengthApply))+' (deg)')
		if not self.temp == 'NONE':
			cmds.text(self.lensText,e=True,l=self.flag)
	def cameraCmd(self,*args):
		self.sign=cmds.optionMenu(self.cameraMode,q=True,v=True)
		for i in self.cameraList:
			for j in i:
				if j[0] == self.sign:
					if len(j) == 5:
						cmds.text(self.cameraText,e=True,
							l='    H Film Aperture : '+str(round(float(j[1])/25.4,2))+' (in) '+j[1]+' (mm)'+
							'\n    V Film Aperture : '+str(round(float(j[2])/25.4,2))+' (in) '+j[2]+' (mm)'+
							'\n        H Resolution : '+j[3]+' (pixel)'+
							'\n        V Resolution : '+j[4]+' (pixel)'+
							'\nFilm Aspect Ratio : '+str(round(float(j[1])/float(j[2]),2)))
					else:
						cmds.text(self.cameraText,e=True,
							l='    H Film Aperture : '+str(round(float(j[1])/25.4,2))+' (in) '+j[1]+' (mm)'+
							'\n    V Film Aperture : '+str(round(float(j[2])/25.4,2))+' (in) '+j[2]+' (mm)'+
							'\nFilm Aspect Ratio : '+str(round(float(j[1])/float(j[2]),2)))
					self.apertureHApply=float(j[1])/25.4
					self.apertureVApply=float(j[2])/25.4
		self.angleText()
	def focalLengthCmd(self,*args):
		self.focalLengthApply=cmds.floatSliderGrp(self.focalLength,q=True,v=True)
		self.angleText()
	def lensCmd(self,*args):
		self.sign=cmds.optionMenu(self.lensMode,q=True,v=True)
		for i in self.lensList:
			for j in i:
				if j[0] == self.sign:
					if j[1]=='prime':
						self.flag='     Focal Length : '+j[2]+' (mm)'
						self.temp=self.flag
						self.focalLengthApply=float(j[2])
						cmds.text(self.focalLengthLable,e=True,en=False)
						cmds.floatSliderGrp(self.focalLength,e=True,en=False,v=float(j[2]),min=float(j[2]),max=float(j[2])+1,)
					else:
						self.flag='     Focal Length : '+j[2]+' (mm) - '+j[3]+' (mm)'
						self.temp=self.flag
						self.focalLengthApply=float(j[2])
						cmds.text(self.focalLengthLable,e=True,en=True)
						cmds.floatSliderGrp(self.focalLength,e=True,en=True,v=float(j[2]),min=float(j[2]),max=float(j[3]),cc=self.focalLengthCmd)
		self.angleText()
	def cameraData(self,flag,*args):
		for i in self.cameraMenuList:
			cmds.deleteUI(i,menuItem=True)
			self.cameraMenuList=[]
		for i in range(0,len(self.cameraList[flag])):
			self.cameraMenuList.append('cameraMenu'+str(i))
			cmds.menuItem(self.cameraMenuList[i],l=self.cameraList[flag][i][0],p=self.cameraMode)
		cmds.text(self.cameraText,e=True,l='NONE')
		self.angleText()
	def lensData(self,flag,*args):
		for i in self.lensMenuList:
			cmds.deleteUI(i,menuItem=True)
			self.lensMenuList=[]
		for i in range(0,len(self.lensList[flag])):
			self.lensMenuList.append('lensMenu'+str(i))
			cmds.menuItem(self.lensMenuList[i],l=self.lensList[flag][i][0],p=self.lensMode)
		cmds.text(self.lensText,e=True,l='NONE')		
	def createButton(self):
		self.buttonSize=((self.size[0]-18)/3,26)
		self.actionButton=cmds.button(
			l=self.actionButtonName,
			h=self.buttonSize[1],
			c=self.actionButtonCmd)
		self.applyButton=cmds.button(
			l=self.applyButtonName,
			h=self.buttonSize[1],
			c=self.applyButtonCmd)
		self.closeButton=cmds.button(
			l=self.closeButtonName,
			h=self.buttonSize[1],
			c=self.closeButtonCmd)
	def createCameraTab(self):
		self.cameraTab=cmds.frameLayout(
			l='camera',collapsable=True,p=self.mainForm)
		self.createCameraForm=cmds.formLayout(nd=100)
		self.cameraText=cmds.text(l='NONE',fn='obliqueLabelFont',al='left')	 
		self.cameraManufacturer=cmds.text(l=self.cameraManufacturerName)
		self.cameraRadioGroup=cmds.radioCollection()
		self.cameraRadio=[]
		for i in range(0,len(self.cameraRadioName)):
			self.cameraRadio.append(cmds.radioButton(l=self.cameraRadioName[i],onCommand=partial(self.cameraData,i)))
		self.cameraMode=cmds.optionMenu(cc=self.cameraCmd)
		self.cameraModeLable=cmds.text(l=self.cameraModelName)
		cmds.formLayout(
			self.createCameraForm,e=True,
			attachForm=(
				[self.cameraManufacturer,'top',5],
				[self.cameraManufacturer,'left',5]))
		for i in range(0,len(self.cameraRadioName)):
			x=i%4+1
			y=i/4+1
			cmds.formLayout(
				self.createCameraForm,e=True,
				attachPosition=(
					[self.cameraRadio[i],'left',0,(x-1)*25+1],
					[self.cameraRadio[i],'right',0,x*25-1]))
			if y!=1:
				cmds.formLayout(
					self.createCameraForm,e=True,
				attachControl=([self.cameraRadio[i],'top',5,self.cameraRadio[i-4]]))
			else:
				cmds.formLayout(
					self.createCameraForm,e=True,
				attachControl=([self.cameraRadio[i],'top',5,self.cameraManufacturer]))
		cmds.formLayout(
			self.createCameraForm,e=True,
			attachForm=(
				[self.cameraModeLable,'left',5],
				[self.cameraMode,'right',5],
				[self.cameraText,'left',5],
				[self.cameraText,'bottom',5]),
			attachControl=(
				[self.cameraMode,'top',5,self.cameraRadio[len(self.cameraRadio)-1]],
				[self.cameraModeLable,'top',9,self.cameraRadio[len(self.cameraRadio)-1]],
				[self.cameraMode,'left',4,self.cameraModeLable],
				[self.cameraText,'top',5,self.cameraMode]))
	def createLensTab(self):
		self.lensTab=cmds.frameLayout(
			l='lens',collapsable=True,p=self.mainForm)
		self.createLensForm=cmds.formLayout(nd=100)
		self.lensText=cmds.text(l='NONE',fn='obliqueLabelFont',al='left')	   
		self.lensManufacturer=cmds.text(l=self.lensManufacturerName)
		self.lensRadioGroup=cmds.radioCollection()
		self.lensRadio=[]
		for i in range(0,len(self.lensRadioName)):
			self.lensRadio.append(cmds.radioButton(l=self.lensRadioName[i],onCommand=partial(self.lensData,i)))
		self.lensMode=cmds.optionMenu(cc=self.lensCmd)
		self.lensModeLable=cmds.text(l=self.lensModelName)
		self.focalLengthLable=cmds.text(l=self.focalLengthName,en=False)
		self.focalLength=cmds.floatSliderGrp(f=True,max=100,min=0,en=False)
		cmds.formLayout(
			self.createLensForm,e=True,
			attachForm=(
				[self.lensManufacturer,'top',5],
				[self.lensManufacturer,'left',5]))
		for i in range(0,len(self.lensRadioName)):
			x=i%4+1
			y=i/4+1
			cmds.formLayout(
				self.createLensForm,e=True,
				attachPosition=(
					[self.lensRadio[i],'left',0,(x-1)*25+1],
					[self.lensRadio[i],'right',0,x*25-1]))
			if y!=1:
				cmds.formLayout(
					self.createLensForm,e=True,
				attachControl=([self.lensRadio[i],'top',5,self.lensRadio[i-4]]))
			else:
				cmds.formLayout(
					self.createLensForm,e=True,
				attachControl=([self.lensRadio[i],'top',5,self.lensManufacturer]))
		cmds.formLayout(
			self.createLensForm,e=True,
			attachForm=(
				[self.lensModeLable,'left',5],
				[self.lensMode,'right',5],
				[self.focalLengthLable,'left',5],
				[self.focalLength,'right',5],
				[self.lensText,'left',5],
				[self.lensText,'bottom',5]),
			attachControl=(
				[self.lensMode,'top',5,self.lensRadio[len(self.lensRadio)-1]],
				[self.lensModeLable,'top',9,self.lensRadio[len(self.lensRadio)-1]],
				[self.lensMode,'left',4,self.lensModeLable],
				[self.focalLengthLable,'top',9,self.lensMode],
				[self.focalLength,'top',5,self.lensMode],
				[self.focalLength,'left',4,self.focalLengthLable],
				[self.lensText,'top',5,self.focalLength]))
	def selectCameraCmd(self,*args):
		cmds.select(cmds.optionMenu(self.selectCamera,q=True,v=True))
		self.selectCameraApply=cmds.optionMenu(self.selectCamera,q=True,v=True)
	def refreshCameraCmd(self,*args):
		for i in self.selectCameraList:
			if cmds.menuItem(i,exists=True):
				cmds.deleteUI(i,menuItem=True)
			self.selectCameraList=[]
		self.selectCameraList=cmds.ls(type='camera')
		for i in self.selectCameraList:
			if not i in [u'frontShape', u'sideShape', u'perspShape', u'topShape']:
				cmds.menuItem(i,l=i,p=self.selectCamera)
	def createSelectCameraTab(self):
		self.selectCameraTab=cmds.frameLayout(
			l='select',collapsable=True,p=self.mainForm)
		self.createSelectCameraForm=cmds.formLayout(nd=100) 
		self.selectCamera=cmds.optionMenu(l=self.selectCameraName,cc=self.selectCameraCmd)
		self.selectRefreshButton=cmds.button(l="RE",c=self.refreshCameraCmd)
		cmds.formLayout(
			self.createSelectCameraForm,e=True,
			attachForm=(
				[self.selectCamera,'top',5],
				[self.selectCamera,'left',5],
				[self.selectCamera,'bottom',5],
				[self.selectRefreshButton,'top',5],
				[self.selectRefreshButton,'bottom',5],
				[self.selectRefreshButton,'right',5]),
			attachControl=(
				[self.selectCamera,'right',5,self.selectRefreshButton]))
	def create(self):
		if cmds.window(self.title,exists=True):
			cmds.deleteUI(self.title,window=True)
		self.win=cmds.window(self.title,title=self.title,wh=self.size)
		self.mainForm=cmds.formLayout(nd=100)	   
		self.createButton()
		self.createCameraTab()
		self.createLensTab()
		self.createSelectCameraTab()
		cmds.formLayout(
			self.mainForm,e=True,
			attachForm=(
				[self.cameraTab,'top',5],
				[self.cameraTab,'left',5],
				[self.cameraTab,'right',5],
				[self.lensTab,'left',5],
				[self.lensTab,'right',5],
				[self.selectCameraTab,'left',5],
				[self.selectCameraTab,'right',5]),
			attachControl=(
				[self.lensTab,'top',5,self.cameraTab],
				[self.selectCameraTab,'top',5,self.lensTab]))
		cmds.formLayout(
			self.mainForm,
			e=True,
			attachForm=(
				[self.actionButton,'left',5],
				[self.actionButton,'bottom',5],
				[self.applyButton,'bottom',5],
				[self.closeButton,'bottom',5],
				[self.closeButton,'right',5]),
			attachPosition=(
				[self.actionButton,'right',0,33],
				[self.closeButton,'left',0,66]),
			attachControl=(
				[self.applyButton,'left',5,self.actionButton],
				[self.applyButton,'right',5,self.closeButton]))
		cmds.showWindow(self.win)
	def applyButtonCmd(self,*args):
		cmds.setAttr(self.selectCameraApply+'.focalLength',self.focalLengthApply)
		cmds.setAttr(self.selectCameraApply+'.horizontalFilmAperture',self.apertureHApply)
		cmds.setAttr(self.selectCameraApply+'.verticalFilmAperture',self.apertureVApply)
	#   cmds.imagePlane.setLookThrough(self.selectCameraApply)
	def closeButtonCmd(self,*args):
		cmds.deleteUI(self.title,window=True)
	def actionButtonCmd(self,*args):
		self.applyButtonCmd()
		self.closeButtonCmd()

class STstartup(ommpx.MPxCommand):
	def __init__(self):
		ommpx.MPxCommand.__init__(self)
	def doIt(self, args):
		win=cameraLen()
		win.create()

def creator():
	return ommpx.asMPxPtr(STstartup())
	
def initializePlugin(mObject):
	mPlugin=ommpx.MFnPlugin(mObject,'Calven Gu','1.0')
	try:
		mPlugin.registerCommand(kPluginCmdName,creator)
	except:
		sys.stderr.write('Failed load plugin : %s' %kPluginCmdName)
		raise

def uninitializePlugin(mObject):
	mPlugin=ommpx.MFnPlugin(mObject)
	try:
		mPlugin.deregisterCommand(kPluginCmdName)
	except:
		sys.stderr.write('Failed unload plugin : %s' %kPluginCmdName)
		raise