from HTMLParser import HTMLParser
from urllib import urlopen
from datetime import *
import re,time

today=date.today()

#set this to True
friendly=True

month={
	'January':1,
	'February':2,
	'March':3,
	'April':4,
	'May':5,
	'June':6,
	'July':7,
	'August':8,
	'September':9,
	'October':10,
	'November':11,
	'December':12
}

num_days={
	1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31
}


webdata=[]
dateranges={}
provinces={}
obituaries={}
baseurl='http://www.legacy.com/obituaries/timescolonist/obituary-search.aspx?'
content=urlopen(baseurl)

def welcome():
	print 'Welcome to the Legacy software.'
	print 'This software is designed for funeral chapel and is meant to used professionally.'
	getprompt('Please press Enter to continue...')




def parsedate(dtstr):
	dtstr=dtstr.strip()
	pat='^(\d{1,2}) */ *(\d{1,2}) */ *((?:\d\d){1,2})$'
	mat=re.search(pat,dtstr)
	if mat:
		try:
			y,m,d=[int(mat.group(i)) for i in [3,1,2]]
			if y<=20:
				y+=2000
			elif y<100:
				y+=1900
		except:
			raise TypeError('Illegal date format')
	else:
		pat='^(\w+) +(\d{1,2}) *(?:,| ) *(\d{4})$'
		mat=re.search(pat,dtstr)
		if mat:
			try:
				y,d=[int(mat.group(i)) for i in [3,2]]
				m=mat.group(1).capitalize()
				m=month[m]
			except:
				raise TypeError('Illegal date format')
		else:
			pat='^(\d{1,2}) +(\w+) +(\d{4})$'
			mat=re.search(pat,dtstr)
			try:
				y,d=[int(mat.group(i)) for i in [3,1]]
				m=mat.group(2).capitalize()
				m=month[m]
			except:
				raise TypeError('Illegal date format')
	if not all([1<=m<=12,1<=d<=num_days.get(m,0)]):
		raise ValueError('Illegal date value')
	if all([m==2,d==29,
		y%4!=0 or (y%100==0 and y%400!=0) ]):#not a leap year
		raise ValueError('Illegal date value')
	return date(y,m,d)



def clearwebdata():
	while webdata:
		webdata.pop(0)

def search_tag_attr(tag,*args):
	for num,i in enumerate(webdata):
		if i[0]=='start tag' and i[1]==tag:
			atr=dict(i[2])
			for j,k in args:
				if atr.get(j,None)==k:
					return num

def getynprompt(text):
	if friendly:
		prompt=raw_input(text+' (y/n) ')
		return prompt.lower().strip()=='y'
	return False

def getprompt(text,default=''):
	if friendly:
		return raw_input(text+' ')
	return default

def urldatastr(udata):
	return '&'.join(['='.join([i,j]) for i,j in udata.items()])


def specdates(dres):
	legalfmt='''
Legal formats are:
	mm/dd/[yy]yy
	Month [d]d [,] yyyy
	[d]d Month yyyy
(formats inside [] are optional)
'''
	if dres.strip()=='specific date':
		while 1:
			prompt=getprompt('Please Enter a date:'+legalfmt)
			print
			try:
				startdate=parsedate(prompt)
				enddate=startdate
				break
			except:
				print 'Illegal input! Please try again.'
	elif dres.strip()=='date range':
		while 1:
			prompt=getprompt('Please Enter a starting date:'+legalfmt)
			print
			try:
				startdate=parsedate(prompt)
				break
			except:
				print 'Illegal input! Please try again.'
		while 1:
			prompt=getprompt('Please Enter an ending date:'+legalfmt)
			print
			try:
				enddate=parsedate(prompt)
				break
			except:
				print 'Illegal input! Please try again.'
	return startdate,enddate


welcome()

form_data={}

class htmlprocess(HTMLParser):
	def handle_starttag(self,tag,attrs):
		webdata.append(('start tag',tag,attrs))
	def handle_data(self,data):
		webdata.append(('data',data))
	def handle_endtag(self,tag):
		webdata.append(('end tag',tag))


process=htmlprocess()
process.feed(content.read())

content.close()


#prompt for the first name
prompt=getynprompt('Do you want to enter a First Name?')
if prompt:
	res=getprompt('Please Enter a First Name:','')
	if res:
		form_data['firstname']=res

#prompt for the last name
prompt=getynprompt('Do you want to enter a Last Name?')
if prompt:
	res=getprompt('Please Enter a Last Name:','')
	if res:
		form_data['lastname']=res

#prompt for keyword
prompt=getynprompt('Do you want to enter a Keyword?')
if prompt:
	res=getprompt('Please Enter a Keyword:','')
	if res:
		form_data['keyword']=res

periodid='ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_uxSearchWideControl_ddlSearchRange'

periodselect=search_tag_attr('select',('id',periodid))

while webdata[periodselect]!=('end tag','select'):
	if webdata[periodselect][:2]==('start tag','option'):
		atrs=dict(webdata[periodselect][2])
		valat=atrs['value']
		webdata.pop(periodselect)
		dateranges[webdata[periodselect][1].lower()]=valat
	webdata.pop(periodselect)

webdata[:periodselect+1]=[]

dateops=dict(enumerate(dateranges))
prompt=getprompt('''Please Select an option from the following: (default is Past 30 Days)
%s

'''%'\n'.join(['%2s. %-20s'%(i,j.capitalize()) for i,j in enumerate(dateranges)]),'')

dateres=dateops.get(int(prompt) if prompt else '','past 30 days')
print '\nYou have selected',repr(dateres.capitalize()),'\n'

if dateres=='all time':
	dateres='all records'
elif dateres in ['specific date','date range']:
	startdate,enddate=specdates(dateres)



form_data['countryid']='2' #Canada

provid='ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_uxSearchWideControl_ddlState'
provselect=search_tag_attr('select',('id',provid))

while webdata[provselect]!=('end tag','select'):
	if webdata[provselect][:2]==('start tag','option'):
		atrs=dict(webdata[provselect][2])
		valat=atrs['value']
		webdata.pop(provselect)
		provinces[webdata[provselect][1]]=valat
	webdata.pop(provselect)


provops=dict(enumerate(provinces))
prompt=getprompt('''Please Select a Province: (default is British Columbia)
%s

'''%'\n'.join(['%2s. %-20s'%(i,j) for i,j in enumerate(provinces)]),'')
provres=provops.get(int(prompt) if prompt else '','British Columbia')

print '\nYou have selected',repr(provres),'\n'

form_data['stateid']=provinces[provres]

clearwebdata()

content=urlopen(baseurl+urldatastr(form_data))
process.feed(content.read())
content.close()


obitid='ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_uxSearchWideControl_ddlNewspaper'

obitselect=search_tag_attr('select',('id',obitid))

while webdata[obitselect]!=('end tag','select'):
	if webdata[obitselect][:2]==('start tag','option'):
		atrs=dict(webdata[obitselect][2])
		valat=atrs['value']
		webdata.pop(obitselect)
		obituaries[re.sub(' +',' ',webdata[obitselect][1].strip())]=valat
	webdata.pop(obitselect)

webdata[:obitselect+1]=[]

obitdef='The Times Colonist' \
	if provres=='British Columbia' \
	else 'All%s obituaries'%(' '+provres if provres!='All Provinces' else '')

obitops=dict(enumerate(obituaries))

prompt=getprompt('''Please Select an Obituary: (default is %s)
%s

'''%(obitdef,
	'\n'.join(['%2s. %-20s'%(i,j) for i,j in enumerate(obituaries)])
	),'')

obitres=obitops.get(int(prompt) if prompt else '',obitdef)

print '\nYou have selected',repr(obitres),'\n'

clearwebdata()

'''
Results:
	Date Range: dateres
	Province: provres
	Obituary: obitres
'''
 ############################Begin Legacy Website#######################################
legacy_url='http://www.legacy.com/ns/obitfinder/obituary-search.aspx?'

def firstdayofyear(yr):
	return date(yr,1,1)


content=urlopen(legacy_url+urldatastr(form_data))
process.feed(content.read())
content.close()

dateranges={}

periodid='ctl00_ctl00_MainContent_uxSearchWideControl_ddlSearchRange'
periodselect=search_tag_attr('select',('id',periodid))

while webdata[periodselect]!=('end tag','select'):
	if webdata[periodselect][:2]==('start tag','option'):
		atrs=dict(webdata[periodselect][2])
		valat=atrs['value']
		webdata.pop(periodselect)
		dateranges[webdata[periodselect][1].lower()]=valat
	webdata.pop(periodselect)
webdata[:periodselect+1]=[]

datecheck=dateres not in dateranges
if datecheck:
	if dateres=='today':
		form_data['daterange']=dateranges['past 24 hours']
	elif dateres=='past 7 days':
		form_data['daterange']=dateranges['past 2 weeks']
	elif dateres in ['specific date','date range']:
		start2010=firstdayofyear(2010)
		end2015=firstdayofyear(2016)-timedelta(1)
		if all([start2010<=i<=end2015 for i in (startdate,enddate)]):
			form_data['daterange']=dateranges['2010-2015']
		else:
			start2000=firstdayofyear(2000)
			end2009=firstdayofyear(2010)-timedelta(1)
			if all([start2000<=i<=end2009 for i in (startdate,enddate)]):
				form_data['daterange']=daterange['2000-2009']
			else:
				form_data['dateres']=daterange['all records']
else: 
	form_data['daterange']=dateranges[dateres]

provinces={}


provid='ctl00_ctl00_MainContent_uxSearchWideControl_ddlState'
provselect=search_tag_attr('select',('id',provid))

while webdata[provselect]!=('end tag','select'):
	if webdata[provselect][:2]==('start tag','option'):
		atrs=dict(webdata[provselect][2])
		valat=atrs['value']
		webdata.pop(provselect)
		provinces[webdata[provselect][1]]=valat
	webdata.pop(provselect)

webdata[:provselect+1]=[]
form_data['stateid']=provinces[provres]

obituaries={}

obitid='ctl00_ctl00_MainContent_uxSearchWideControl_ddlNewspaper'
obitselect=search_tag_attr('select',('id',obitid))

while webdata[obitselect]!=('end tag','select'):
	if webdata[obitselect][:2]==('start tag','option'):
		atrs=dict(webdata[obitselect][2])
		valat=atrs['value']
		webdata.pop(obitselect)
		obituaries[re.sub(' +',' ',webdata[obitselect][1].strip())]=valat
	webdata.pop(obitselect)

webdata[:obitselect+1]=[]

obitcheck=obitres not in obituaries

if obitcheck:
	obitreg='All *%s *obituaries'%provres
	for i in obituaries:
		if re.search(obitreg,i):
			form_data['affiliateid']=obituaries[i]
			break
else:
	form_data['affiliateid']=obituaries[obitres]

clearwebdata()

###################Gather Individuals###########################

form_data['entriesperpage']='50'


def parsepubl(publstr):
	publstr=publstr.strip()
	pat='^[Pp]ublished +(.+)$'
	m=re.search(pat,publstr)
	if not m:
		return (None,None)
	obdt=m.group(1)
	pat='^(.+) +courtesy of'
	m=re.search(pat,obdt)
	if m:
		obdt=m.group(1).strip()
	pat='^in +(.+)$'
	m=re.search(pat,obdt)
	if m:
		obdt=m.group(1).strip()
	pat='^(.+) +on +(.+)$'
	m=re.search(pat,obdt)
	if m:
		return m.group(1),parsedate(m.group(2))
	pat='^(.+) +from +(.+) +to +(.+)$'
	m=re.search(pat,obdt)
	if m:
		d1=m.group(2)
		d2=m.group(3).strip()
		m1=re.search('(\d{4})$',d2)
		if m1:
			if not re.search(', +(.+)$',d1):
				d1+=' , '+m1.group(1)
			return m.group(1),tuple([parsedate(i) for i in (d1,d2)])
	return None,None



def gatherindivs(oblist):
	clearwebdata()
	content=urlopen(legacy_url+urldatastr(form_data))
	process.feed(content.read())
	content.close()
	listings=search_tag_attr('div',('id','Listings'))
	nest=0
	entry=False
	while webdata[listings]!=('end tag','div') or nest>1:
		if entry:
			if webdata[listings][:2]==('start tag','a'):
				href=dict(webdata[listings][2])['href']
				href=str(href)
				webdata.pop(listings)
				_,title=webdata[listings]
				webdata.pop(listings)
				oblist.append((title,href))
				entry=False
		if webdata[listings][:2]==('start tag','div'):
			nest+=1
			divatr=dict(webdata[listings][2])
			if divatr.get('class',None)=='obitName':
				entry=True
			elif divatr.get('class',None)=='obitPublished':
				webdata.pop(listings)
				#print webdata[listings:listings+3]
				_,publ=webdata[listings]
				while webdata[listings+1][0]=='data':
					webdata.pop(listings)
					_,p=webdata[listings]
					publ+=' '+p
				oblist[-1]=oblist[-1]+parsepubl(publ)
		elif webdata[listings]==('end tag','div'):
			nest-=1
		webdata.pop(listings)
	for i,j in enumerate(oblist):
		oblist[i]+=(None,)*(4-len(oblist[i]))

def obitfilter():
	if not obitcheck:
		return
	for i,j,k,l in list(oblist):
		if k!=obitres:
			oblist.remove((i,j,k,l))


def datefilter():
	if not datecheck:
		return
	for dat in list(oblist):
		try:
			i,j,k,l=dat
		except:
			print dat
			exit()
		if type(l)==date:
			if dateres=='today' and l!=today:
				oblist.remove((i,j,k,l))
			elif dateres=='past 7 days' and not (today-timedelta(7)<=l<=today):
				oblist.remove((i,j,k,l))
			elif dateres in ['specific date','date range']:
				if not (startdate<=l<=enddate):
					oblist.remove((i,j,k,l))
		elif l:
			l1,l2=l
			if dateres=='today' and not (l1<=today<=l2):
				oblist.remove((i,j,k,l))
			elif dateres=='past 7 days' and not any([today-timedelta(7)<=d<=today for d in (l1,l2)]):
				oblist.remove((i,j,k,l))
			elif dateres in ['specific date','date range']:
				if not any([startdate<=d<=enddate for d in (l1,l2)]):
					oblist.remove((i,j,k,l))
		else:
			oblist.remove((i,j,k,l))

def numresults():
	clearwebdata()
	content=urlopen(legacy_url+urldatastr(form_data))
	process.feed(content.read())
	content.close()
	resid='ctl00_ctl00_MainContent_ResultsHeader'
	n=search_tag_attr('div',('id',resid))
	webdata[:n+1]=[]
	while tuple([i.strip() for i in webdata[0][:2]])!=('data','of'):
		webdata.pop(0)
	webdata.pop(0)
	_,nres=webdata[1]
	return int(nres)



print 'Gathering Data...'

form_data['Page']='1'
oblist=[]

nres=numresults()
print 'Number of Results:',nres
npages=nres/int(form_data['entriesperpage'])
if nres%int(form_data['entriesperpage']):
	npages+=1

print 'Number of Pages:',npages


curlen,prevlen=0,0
for i in range(1,npages+1):
	form_data['Page']=str(i)
	prevlen=curlen
	gatherindivs(oblist)
	curlen=len(oblist)
	print 'Completed Page',form_data['Page'],': Number of Entries:',curlen-prevlen


print 'Filtering Data...'
obitfilter()

datefilter()
time.sleep(1)
print 'Total Filtered number of entries:',len(oblist)
time.sleep(1)




obrecords=[]
for name,url,paper,dts in oblist:
	print 'Processing',name
	clearwebdata()
	content=urlopen(url)
	url=content.geturl()
	url=url.replace('obituary.aspx?','obituary-print.aspx?')
	content.close()
	print 'URL:',url
	content=urlopen(url)
	process.feed(content.read().decode('utf-8'))
	content.close()
	ind=search_tag_attr('div',('id','obitText'))
	para='(no obituary text)'
	if type(ind)==int:
		webdata.pop(ind)
		para=''
		while webdata[ind]!=('end tag','div'):
			if webdata[ind][0]=='data':
				para+=webdata[ind][1]
			elif webdata[ind][:2]==('start tag','br'):
				para+='\n'
			webdata.pop(ind)
		para=para.strip()
		webdata[:ind+1]=[]
		para=para.encode('utf-8')
	ind=search_tag_attr('table',('class','FHInfo'))
	fhome='(no funeral home data)'
	if type(ind)==int:
		fhome=''
		while webdata[ind]!=('end tag','div'):
			if webdata[ind][0]=='data':
				fhome+=webdata[ind][1]
			elif webdata[ind][:2] in [('start tag','br'),('end tag','h3')]:
				fhome+='\n'
			elif webdata[ind]== ('end tag','span'):
				fhome+=' '
			webdata.pop(ind)
	fhome='\n'.join([i.strip() for i in fhome.split('\n') if i.strip()])
	obrecords.append((name,para,fhome))

prompt=getprompt('Please type a text file to write in. (include .txt)').strip()

with open(prompt,'w') as f:
	for name,para,fhome in obrecords:
		f.write('\n')
		f.write(name+'\n')
		f.write('--------------------------------'+'\n')
		f.write(para+'\n')
		f.write('|||||||||||||||||||||||||||||||||'+'\n')
		f.write(fhome+'\n')

