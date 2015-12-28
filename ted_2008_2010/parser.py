# -*- coding: utf-8 -*-

import csv, re, sys, glob
from datetime import datetime
from bs4 import BeautifulSoup as bs
from slugify import slugify

def iferror1(html,tagname):

    try:
        return html.find(tagname).text.encode('utf-8')
    except AttributeError:
        return ''

def iferror1get(html,tagname,attr):

    try:
        return html.find(tagname).get(attr)
    except AttributeError:
        return ''

def getsectionHTML(html,sectionnum):

    try:
         return html.find("nomark", text=sectionnum).parent.txtmark
    except AttributeError:
        return ''

def getsection(html,sectionnum,tagn):

    textlists = []
    
    try:
        section = html.find("nomark", text=sectionnum).parent.txtmark
        for tag in section.findAll(tagn):
            textlists.append(tag.text.encode('utf8'))
        return ';'.join(textlists)

    except AttributeError:
        return ''

def NEXTsection(html,sectionnum,tagn):

    textlists = []
    
    try:
        section = html.findNext("nomark", text=sectionnum).parent.txtmark
        for tag in section.findAll(tagn):
            textlists.append(tag.text.encode('utf8'))
        return ';'.join(textlists)
    except AttributeError:
        return ''

def getvalue(html,sectionnum):

    value = ''
    currency = ''
    VAT = ''
    rate = ''

    try:
        section = html.find("nomark", text=sectionnum).parent.txtmark
        for p in section.findAll("p"):
            if 'Value:' in p.text:
                value = re.search('[0-9, ]+',p.text).group(0).replace(" ","").replace(",",".").strip()
                currency = re.search('[A-Z]{3}',p.text).group(0)
            elif 'VAT' in p.text:
                VAT = re.search('.*cluding',p.text).group(0).strip()
                if '%' in p.text:
                    rate = re.search('[0-9]{2}',p.text).group(0)

        return value, currency, VAT, rate

    except AttributeError:
        return value, currency, VAT, rate


def getvalue_award(html,sectionnum,typevalue,notvalue):

    value = ''
    currency = ''
    VAT = ''
    rate = ''

    i = 0

    try:
        section = html.findNext("nomark",text=sectionnum).parent.txtmark
        for nr,p in enumerate(section.findAll("p")):
            if typevalue in p.text:
                i = nr

        for p in section.findAll("p")[i:]:
            if 'Value:' in p.text:
                    value = re.search('[0-9, ]+',p.text).group(0).replace(" ","").replace(",",".").strip()
                    currency = re.search('[A-Z]{3}',p.text).group(0)
            elif 'VAT' in p.text and notvalue not in p.text:
                VAT = re.search('.{2}cluding',p.text).group(0).strip()
                if '%' in p.text:
                    rate = re.search('[0-9]{2}',p.text).group(0)
            elif notvalue in p.text:
                return value, currency, VAT, rate

        return value, currency, VAT, rate

    except AttributeError:
         return value, currency, VAT, rate

def award(firstelement,nr,html):

    try:
        if firstelement == nr:
            return iferror1(html.parent.parent.txtmark,"p")
        else:
            return NEXTsection(html,re.compile("^V\.1?\.?"+str(nr)+"\)"),"p")
    except AttributeError:
        return ''

def checkelements(html,m,firstelem, elementlist):
    
    try:
        return html.findAll("nomark", text=re.compile("^V\.1?\.?"+str(firstelem)+"\)"))[m]
    except IndexError:
        for r in elementlist:
            try:
                return html.findAll("nomark", text=re.compile("^V\.1?\.?"+str(r)+"\)"))[m]
            except IndexError:
                continue


def cpv(tender):
        
    cpvs = []
    for cpv in tender.find_all("originalcpv"):
        cpvs.append(cpv["code"])

    try:
        return ";".join(cpvs)
    except AttributeError:
        return ""

def makedate(firstelement, contract):

    if firstelement == 1:
        date = iferror1(contract.parent.parent.txtmark,"p")
    
        try:
            ddate = re.search("^[0-9][0-9]?",date).group(0)
            mdate = re.search("\.[0-9][0-9]?\.",date).group(0).replace('.','')
            ydate = re.search("[0-9]{4}",date).group(0)

        except AttributeError:
            ddate = mdate = ydate = ''

    else:
        ddate = mdate = ydate = ''

    return ddate, mdate, ydate

def getelements(tender):
# find out which sections are present

    allelements = tender.findAll("nomark", text=re.compile("^V\.1?\.?[12345]\)"))

    elements = []
    try:
	for e in allelements:
	    elements.append(int(re.search("[0-9]",re.search("([0-9])\)$",e.text).group(0)).group(0)))
    except AttributeError:
	return ''
    
    return elements


def countcontracts(elements):
# check if all tenders have the same elements
# count how many tenders there are

    occurences = []
    if len(elements) != 0:
        for i in set(elements):
            occurences.append(elements.count(i))
            if set(occurences) == 1:
                nrOfContracts = occurences[0]
            elif set(occurences) > 1:
                nrOfContracts = sorted(occurences)[-1]

    else:
        nrOfContracts = 0
    
    return nrOfContracts

def companyinfo(firstelement,contract):

    if firstelement == 3:
#           print "first!"
        try:
            return contract.parent.parent.txtmark
        except AttributeError:
            return ''
    else:
#           print "not first!"
        try:
            return contract.findNext("nomark", text=re.compile("^V\.1?\.?3\)")).parent.txtmark.p
        except AttributeError:
            return ''

def toeuro(value,currency):

    try:
        eur = float(value) / float(exchangerates[currency])
        return round(eur, 2)
    except (AttributeError, KeyError, ValueError, TypeError):
        return ""

def slug(string):

    try:
	return slugify(string)
    except TypeError:
	return ''

def parse(xml):

    soup = bs(xml,"lxml" )

    data = []
    for tender in soup.find_all("doc"):
        if tender.natnotice["code"] == '7': #check if tender award (7)

            ID = tender.nodocojs.text.encode('utf8')
#            print ID
            criteria = tender.awardcrit.get("code")
            proc = tender.proc.get("code")
            title = getsection(tender,"II.1.1)","p")
            additionalidentifiers = getsection(tender,"II.3.1)","p")
            previousnotices = getsection(tender,"II.3.2)","txnum")
            description = getsection(tender,"II.1.4)","p")
            cpvs = cpv(tender)
            NUTS = getsection(tender,"II.1.2)","txnuts")
            framework = getsection(tender,"II.1.3)","p")
            additionalinfo = getsection(tender,"VI.2)","p")

            Tvalue,Tcurrency,Tvat,Tvatrate = getvalue(tender,"II.2.1)")
            Teur = toeuro(Tvalue, Tcurrency)

    # procuring entity
            PE = getsectionHTML(tender,"I.1)")
            PEcountry = tender.isocountry.text.encode('utf8')
            PEname = iferror1(PE,"organisation")
            PEname_slug = slug(PEname)
            PEtown = iferror1(PE,"town")
            PEaddress = iferror1(PE,"address")
            PEpostalcode = iferror1(PE,"postalcode")
            PEemail = iferror1(PE,"txemail")
            PEattention = iferror1(PE,"attention")
            PEurl = iferror1(PE,"txurl")
            PEtel = iferror1(PE,"tel")
            PEactivity = getsection(tender,"I.2)","p")        
    #awards
            contractElements = getelements(tender)
            nrOfContracts = countcontracts(contractElements)

    # parse them!
            for n in xrange(nrOfContracts):
#               print n
                firstElement = contractElements[0]
                for elem in checkelements(tender,n,firstElement,set(contractElements)):

                    contract = []

                    ddate, mdate, ydate = makedate(firstElement, elem)

                    if ydate == '':
                        ydate = re.search("[0-9]{4}$",ID).group(0)


                    offers = award(firstElement,2,elem).strip('.')
                    eo = companyinfo(firstElement,elem)

                    EOname = iferror1(eo,"organisation")
                    EOname_slug = slug(EOname)
                    EOcountry = iferror1get(eo,"country","cy")
                    EOtown = iferror1(eo,"town")
                    EOaddress = iferror1(eo,"address")
                    EOpostalcode = iferror1(eo,"postalcode")
                    EOemail = iferror1(eo,"txemail")
                    EOattention = iferror1(eo,"attention")
                    EOurl = iferror1(eo,"txurl")
                    EOtel = iferror1(eo,"tel")


                    Ivalue,Icurrency,Ivat,Ivatrate = getvalue_award(elem,re.compile("^V\.1?\.?4\)"),"Initial", "final")
                    Ieur = toeuro(Ivalue,Icurrency)
                    Fvalue,Fcurrency,Fvat,Fvatrate = getvalue_award(elem,re.compile("^V\.1?\.?4\)"),"final","Initial")
                    Feur = toeuro(Fvalue,Fcurrency)
    #                print Fvalue,Fcurrency,Fvat,Fvatrate            

                    subcontract = award(firstElement,5,elem)

                    contract.extend([ID,additionalidentifiers,ydate,mdate,ddate,Tvalue,Tcurrency,Teur,Tvat,Tvatrate,title,description,criteria,proc,cpvs,framework,subcontract,NUTS,PEname,PEname_slug,PEactivity,PEcountry,PEtown,PEaddress,PEpostalcode,PEemail,PEtel,PEurl,PEattention,Ivalue,Icurrency,Ieur,Ivat,Ivatrate,Fvalue,Fcurrency,Feur,Fvat,Fvatrate,offers,EOname,EOname_slug,EOcountry,EOtown,EOaddress,EOpostalcode,EOemail,EOtel,EOurl,additionalinfo])
                    data.append(contract)
 
    return data

startTime = datetime.now()

#testfile = open(sys.argv[1])
#print(str(sys.argv[1])),
#parse(testfile)

### change this according to the data you have
thisyear = 2010
filenames = "*.xml"
###

exchangefile = csv.reader(open("oneeuro"+str(thisyear)+".csv"))
exchangerates = {r[0] : r[1] for r in exchangefile}

for f in glob.glob(filenames):

    header = ["id","additionalIdentifiers","award.date/x_year","award.date/x_month","award.date/x_day","tender.value/amount:number","tender.value/currency","tender.value/amount/x_amountEur:number","tender.value/x_vatbool","tender.value/x_vat:number","award.title","award.description","awardCriteria","procurementMethod","x_CPV","x_framework","x_subcontracted","x_NUTS","procuringEntity/name","procuringEntity/x_slug","procuringEntity/x_type","procuringEntity/address/countryName","procuringEntity/address/locality","procuringEntity/address/streetAddress","procuringEntity/address/postalCode","procuringEntity/address/email","procuringEntity/address/telephone","procuringEntity/address/x_url","procuringEntity/contactPoint/name","award.initialValue/amount:number","award.initialValue/currency","award.x_initialValue/x_amountEur:number","award.x_initialValue/x_vatbool","award.initialValue/x_vat:number","award.value/amount:number","award.value/currency","award.value/x_amountEur:number","award.value/x_vatbool","award.value/x_vat:number","numberOfTenderers","suppliers/name","suppliers/x_slug","suppliers/address/countryName","suppliers/address/locality","suppliers/address/streetAddress","suppliers/address/postalCode","suppliers/address/email","suppliers/address/telephone","suppliers/address/x_url","x_additionalInformation"]

    print f
    xmlfile = open(f)
#    print parse(xmlfile)

    with open(f+"-output.csv","w") as csvoutput:
        lapseTime = datetime.now()
        
        xmlfile = open(f)
        rows = parse(xmlfile)
#        print rows

        writer = csv.writer(csvoutput)
        writer.writerow(header)
        writer.writerows(rows)
    #    print header
        
	print datetime.now() - lapseTime,' / ',datetime.now() - startTime

print datetime.now() - startTime
