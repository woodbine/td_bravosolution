import urllib2
from cookielib import CookieJar
from bs4 import BeautifulSoup
import scraperwiki


def NumberPage(htmltext):
	try:
		navbar = htmltext.find('div', {'id':'allButtons_nav3'})
		buttons = navbar.findAll('a')
		l = []
		for el in buttons:
			l.append(el.text)
		if len(l) > 0:
			return int(l[-3])
		else:
			return 1
	except:
		return 1
	

def getTendsID(htmltext):
	ids = []
	trends = htmltext.findAll('tr', {'class':'table_cnt_body_a'})
	for el in trends:
		try:
			js = el.find('a', {'class':'detailLink'}).get('onclick')
			l = js.split("'")
			ID = l[1]
			ids.append(ID)
		except:
			pass
	trends = htmltext.findAll('tr', {'class':'table_cnt_body_b'})
	for el in trends:
		try:
			js = el.find('a', {'class':'detailLink'}).get('onclick')
			l = js.split("'")
			ID = l[1]
			ids.append(ID)
		except:
			pass	
	return ids


def getTendlink(ID, link):
	link = link + "esop/toolkit/opportunity/opportunityDetail.do?opportunityId=" + str(ID)
	return link


def formattext(text):
	soup = BeautifulSoup(str(text.encode('utf8')))
	d = soup.text
	d.strip(' ')
	return d


def replacetext(text):
	text = text.replace("\t", "")
	text = text.replace("\n", "")
	text = text.replace("\u", " ")
	return text


def dateclean(date):
	date = date.replace("/", "-")
	return date
	

def getextradetails(htmltext):
	published = []
	elem = []
	l = htmltext.findAll('tr', {'class':'table_cnt_body_a'})
	for column in l:
		tds = htmltext.findAll('td')
		for td in tds:
			text = td.text
			text = replacetext(text)
			elem.append(text)
		published.append(elem)
		elem = []
	l = htmltext.findAll('tr', {'class':'table_cnt_body_b'})
	for column in l:
		tds = htmltext.findAll('td')
		for td in tds:
			text = td.text
			text = replacetext(text)
			elem.append(text)
		published.append(elem)
		elem = []
	return published



def getDetails(ID, link, opener):
	Tend_Link =  getTendlink(ID, link)
	response = opener.open(Tend_Link)
	htmltext = BeautifulSoup(response, "html.parser")
	Columns = htmltext.findAll('div', {'class':'form_question'})
	Data = htmltext.findAll('div',{'class':'form_answer'})
	Project_Code = Data[0].text
	Project_Title = Data[1].text
	Description = formattext(Data[2].text)
	Notes = formattext(Data[3].text)
	Work_Category = Data[4].text
	Procurement_Route = Data[5].text
	Listing_Deadline = Data[6].text
	Listing_Deadline_clean = dateclean(Listing_Deadline)
	Organisation = Data[7].text
	Buyer = Data[8].text
	Buyer_Email = Data[9].text
	#extra details:
	try:
		extra_details = getextradetails(htmltext)
	except:
		extra_details = []

	data = {"ID" : unicode(ID) ,\
	"Link": unicode(Tend_Link), \
	"Project_Code" : unicode(Project_Code), \
	"Project_Title" : unicode(Project_Title), \
	"Description" : unicode(Description), \
	"Notes" : unicode(Notes), \
	"Work_Category" : unicode(Work_Category), \
	"Procurement_Route" : unicode(Procurement_Route), \
	"Listing_Deadline" : unicode(Listing_Deadline), \
	"Listing_Deadline_clean" : unicode(Listing_Deadline_clean), \
	"Organisation" : unicode(Organisation), \
	"Buyer" : unicode(Buyer), \
	"Buyer_Email" : unicode(Buyer_Email), \
	"Extra_details" : unicode(extra_details)}

	scraperwiki.sqlite.save(unique_keys=['ID'], data = data )

def Navigation(link):
	try:
		url = link + "esop/guest/go/public/opportunity/current"
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		response = opener.open(url)
	
		url = link + "esop/toolkit/opportunity/opportunityList.do?"
		L = ["GLOBAL","CURRENT","PAST"]
		for oppList in L:
			link1 = url + "oppList=" + oppList
			link2 = link1 + "&listManager.pagerComponent.page=1"
			try:
				response = opener.open(link2)
				htmltext = BeautifulSoup(response, "html.parser")
				nb_page = NumberPage(htmltext)
				for i in range(nb_page):
					link2 = link1 + "&listManager.pagerComponent.page=" + str(i+1)
					try:
						response = opener.open(link2)
						htmltext = BeautifulSoup(response, "html.parser")	
						ids = getTendsID(htmltext)
						for ID in ids:
							getDetails(ID, link, opener)
					except:
						pass
			except:
				pass
	except:
		pass
			
def main():
	urls = ["https://anchor.bravosolution.co.uk/", \
	"https://bbc.bravosolution.co.uk/", \
	"https://bl.bravosolution.co.uk/", \
	"https://candlpcts.bravosolution.co.uk/", \
	"https://centro.bravosolution.co.uk/", \
	"https://coal.bravosolution.co.uk/", \
	"https://commercialsolutions.bravosolution.co.uk/", \
	"https://crossrail.bravosolution.co.uk/", \
	"https://crowncommercialservice.bravosolution.co.uk/", \
	"https://cuh.bravosolution.co.uk/", \
	"https://eoecph.bravosolution.co.uk/", \
	"https://etenderwales.bravosolution.co.uk/", \
	"https://fco.bravosolution.co.uk/", \
	"https://hampshirepolice.bravosolution.co.uk/", \
	"https://heartofengland.bravosolution.co.uk/", \
	"https://iewm.bravosolution.co.uk/", \
	"https://lbbd.bravosolution.co.uk/", \
	"https://londonambulance.bravosolution.co.uk/", \
	"https://lse.bravosolution.co.uk/", \
	"https://lupc.bravosolution.co.uk/", \
	"https://nhsbsa.bravosolution.co.uk/", \
	"https://nhspropertyservices.bravosolution.co.uk/", \
	"https://noecpc.bravosolution.co.uk/", \
	"https://nwcph.bravosolution.co.uk/", \
	"https://ofcom.bravosolution.co.uk/", \
	"https://ontariotenders.bravosolution.com/", \
	"https://pro-cure.bravosolution.co.uk/", \
	"https://resource.bravosolution.co.uk/", \
	"https://skillsfundingagency.bravosolution.co.uk/", \
	"https://whs.bravosolution.co.uk/", \
	"https://www.capitalesourcing.com/"]

	for link in urls:
		Navigation(link)




if __name__ == '__main__':
	main()			
		








