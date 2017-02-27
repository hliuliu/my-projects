from HTMLParser import HTMLParser
from urllib import urlopen
from datetime import *
import re,time,json,os,csv

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

month_abbrev={
	'Jan':'January','Feb':'February','Mar':'March','Apr':'April',
	'Jun':'June','Jul':'July','Aug':'August','Sep':'September',
	'Oct':'October','Nov':'November','Dec':'December'
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
	print 'This software is designed for funeral chapel and is meant to be used professionally.'
	getprompt('Please press Enter to continue...')
	print 



#keep
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
			if mat:
				try:
					print dtstr
					y,d=[int(mat.group(i)) for i in [3,1]]
					m=mat.group(2).capitalize()
					print m
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
				if atr.get(j,None)!=k:
					break
			else:
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

def specdatestr(dt):
	def zfill(num):
		if num<10:
			return '0'+str(num)
		return str(num)
	return '%s%s%s'%(dt.year,zfill(dt.month),zfill(dt.day))

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

form_data['daterange']=dateranges[dateres]

if dateres in ['specific date','date range']:
	startdate,enddate=specdates(dateres)
	if dateres=='specific date':
		form_data['specificdate']=specdatestr(startdate)
	else:
		form_data['startdate']=specdatestr(startdate)
		form_data['enddate']=specdatestr(enddate)



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
		obituaries[webdata[obitselect][1]]=valat
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

form_data['affiliateid']=obituaries[obitres]

clearwebdata()

#########Scrape API#####################

apiurl='http://www.legacy.com/obituaries/timescolonist/api/obituarysearch?'

if form_data['affiliateid']=='all':
	form_data['affiliateid']='0'

print apiurl+urldatastr(form_data)
content=urlopen(apiurl+urldatastr(form_data))

obits=json.load(content)
content.close()
pagerem=obits['NumPageRemaining']
obitlist=[]

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

def unicodecut(s):
	s=list(s)
	for i,j in enumerate(s):
		if ord(j)>128:
			s[i]=' '
	return ''.join(s)


def altername(name):
	nlst=name.strip().split()
	for i,j in enumerate(list(nlst)[2:],2):
		if re.search('obituary(\:)?',j,re.I):
			nlst[i:]=[]
	nlst.insert(0,nlst.pop().upper()+',')
	while nlst[-1].lower() in ['de','van','von','der','le']:
		nlst.insert(0,nlst.pop().upper())
	return ' '.join(nlst)

totres=obits['Total']

print 'Total Numer of Results:',totres
print 'Total Numer of Pages:',pagerem+1
time.sleep(1)
for i in range(pagerem+1):
	print 'Page:',i+1,'Number of Entries:',len(obits['Entries'])
	print 
	time.sleep(0.5)
	for entry in obits['Entries']:
		name=entry['name']
		oblink=entry['obitlink']
		# pl=entry.get('printline','').replace('&nbsp;',' ')
		# for a,b in month_abbrev.items():
		# 	pl=re.sub('%s *\.'%a,b,pl)
		print 'Name:',name
		print 'Obituary Link:',oblink
		print
		#time.sleep(0.5)
		# pl=parsepubl(pl)
		# p1,p2=pl
		if re.search('\( *[Ii]n +[Mm]emoriam *\)',name):
			continue
		#name=altername(name)
		obitlist.append((name,oblink))
	form_data['page']=str(2+i)
	content=urlopen(apiurl+urldatastr(form_data))
	obits=json.load(content)
	content.close()

totfilt=len(obitlist)

curr=1
obrecords=[]
for name,url in obitlist:
	name=unicodecut(name)
	clearwebdata()
	content=urlopen(url)
	url=content.geturl()
	url=url.replace('obituary.aspx?','obituary-print.aspx?')
	content.close()
	content=urlopen(url)
	process.feed(content.read().decode('utf-8'))
	content.close()
	ind=search_tag_attr('title')
	if type(ind)==int:
		webdata.pop(ind)
		_,name=webdata[ind]
		name=unicodecut(name)
		name=altername(name)
	print 'Processing',name,': %d out of %d'%(curr,totfilt)
	curr+=1
	ind=search_tag_attr('div',('id','obitText'))
	para='unknown'
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
		para=unicodecut(para)
	ind=search_tag_attr('span',('id','FHName'))
	fhome='unknown'
	if type(ind)==int:
		fhome=''
		webdata.pop(ind)
		_,fhome=webdata[ind]
		fhome=unicodecut(fhome)
	obrecords.append((name,para,fhome))

while 1:
	prompt=getprompt('Please type a csv file to write in. (including .csv is optional)').strip()
	if not prompt.endswith('.csv'):
		prompt+='.csv'
	if os.path.exists(prompt):
		conf=getynprompt('The file %s already exists. Do you want to overwrite it?'%prompt)
		if conf:
			break
	else:
		break


with open(prompt,'w') as f:
	fieldnames=['Name','Funeral Home','Obituary']
	wr=csv.writer(f,lineterminator='\n')
	wr.writerow(fieldnames)
	for name,para,fhome in obrecords:
		wr.writerow([name,fhome,para])



