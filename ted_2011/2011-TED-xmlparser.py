#!/usr/bin/python
# -*- coding: utf- 8 -*-

from bs4 import BeautifulSoup as bs
import glob, os, re, csv
from slugify import slugify
from datetime import datetime

startTime = datetime.now()

#PYTHON: glob module http://stackoverflow.com/questions/18262293/python-open-every-file-in-a-folder
#VIM: comment multiple lines http://unix.stackexchange.com/questions/120615/how-to-comment-multiple-lines-at-once
#VIM: comment more lines at the same time http://stackoverflow.com/questions/9549729/in-vim-how-do-i-effectively-insert-the-same-characters-across-multiple-lines

testfile = open("repairkit/tmp.xml").read()
xmlnum = 0

# oanda.com http://www.oanda.com/currency/average?amount=1&start_month=1&start_year=2011&end_month=12&end_year=2011&base=EUR&avg_type=Year&Submit=1&exchange=BGN&exchange=CHF&exchange=CYP&exchange=CZK&exchange=DKK&exchange=EEK&exchange=GBP&exchange=HUF&exchange=ISK&exchange=JPY&exchange=LTL&exchange=LVL&exchange=MKD&exchange=MTL&exchange=NOK&exchange=PLN&exchange=RON&exchange=SEK&exchange=SKK&exchange=TRY&exchange=USD&interbank=0&format=CSV

exchangefile = csv.reader(open("oneeuro.csv"))
exchangerates = {r[0] : r[1] for r in exchangefile}

def parse(xmlfile):

    global xmlnum
    # numbers in the function names represents how deep in the tree teh function needs to go
    # and if it needs to get an attribute of that tag or parse numbers

    def iferror1(tagname):

        try:
            return soup.find(tagname).text.encode('utf-8')
        except AttributeError:
            return ""

    def iferror1get(tagname,attrib):

        try:
            return soup.find(tagname).get(attrib)
        except AttributeError:
            return ""

    def iferror2alt(tagname,tagname2,alttagname,alttagname2):

        try:
            return soup.find(tagname).find(tagname2).text.encode("utf-8")
        except AttributeError:
            try:
                return soup.find(alttagname).find(alttagname2).text.encode("utf-8")
            except AttributeError:
                return ""

    def iferror2(tagname,tagname2):

        try:
            return soup.find(tagname).find(tagname2).text.encode("utf-8")
        except AttributeError:
            return ""

    def iferror3get(tagname,tagname2,tagname3,attrib):

        try:
            return soup.find(tagname).find(tagname2).find(tagname3).get(attrib)
        except AttributeError:
            return ""

    def iferror2num(tagname,tagname2):

        try:
            return float(soup.find(tagname).find(tagname2).text.replace(",",".").replace(" ",""))
        except (AttributeError, ValueError):
            return ""

    def iferror2get(tagname,tagname2,attrib):

        try:
            return soup.find(tagname).find(tagname2).get(attrib)
        except AttributeError:
            return ""

    def iferror2getalt(tagname,tagname2,attrib,tagnamealt):

        try:
            return soup.find(tagname).find(tagname2).get(attrib)
        except AttributeError:
            try:
                return soup.find(tagnamealt).find(tagname2).get(attrib)
            except AttributeError:
                return ""

    def getvat(tagname1,tagname2):
    
        vat = []

        try:
            soup.find(tagname1).find(tagname2).find("value_cost").find("excluding_vat")
            vat = "excl"
        except AttributeError:
            vat = ""

        try:
            soup.find(tagname1).find(tagname2).find("value_cost").find("including_vat")
            if vat == "excl":
                pass
            else:
                vat = "incl"
        except AttributeError:
                vat = ""

        try: 
            percentage = soup.find(tagname1).find(tagname2).find("vat_prct").get("fmtval")
        except AttributeError:
            percentage = ""

        return vat, percentage

    def getcpv():

        cpvs = []

        try:
            for cpv in soup.find("cpv").find_all("cpv_code"):
                cpvs.append(cpv.get("code"))

            return ';'.join(cpvs)
        except AttributeError:
            return ""

    def euproject():

        try:
        
            if soup.find("complementary_information_contract_award").find("relates_to_eu_project_no") != None:
                return "NO"
            elif soup.find("complementary_information_contract_award").find("relates_to_eu_project_yes") != None:
                return soup.find("complementary_information_contract_award").find("relates_to_eu_project_yes").text.encode('utf-8')

        except AttributeError:
            return ""

    def toeuro(value,currency):

        try:
            eur = float(value) / float(exchangerates[currency])
            return round(eur, 2)
        except (AttributeError, KeyError, ValueError, TypeError):
            return ""

    soup = bs(xmlfile)

    #attrs
    doc_type = iferror1get("td_document_type","code")
    url = iferror1("uri_doc")

    # NO attrs
    if doc_type != "7":
        return

#    else:
#        print "score! "+url

    #contract attrs
    doc_number = iferror1("no_doc_ojs")
    country = iferror1get("iso_country","value")
    cpv = getcpv()
    title_contract = iferror2("title_contract","p")
    NUTS = iferror2get("location_nuts","nuts","code")
    framework = iferror1get("notice_involves_desc", "value")
    short_contract_description = iferror2("short_contract_description", "p")
    GPA = iferror1get("contract_covered_gpa","value")
    additional_info = iferror2("complementary_information_contract_award", "additional_information")
    eu_project = euproject()
    currency = iferror1get("value", "currency")

    notice_dispatch_day = iferror2("notice_dispatch_date","day")
    notice_dispatch_month = iferror2("notice_dispatch_date","month")
    notice_dispatch_year = iferror2("notice_dispatch_date","year")

    tender_value = iferror2num("values_list","value")
    tender_currency = iferror2get("values_list","value", "currency")
    tender_value_eur = toeuro(tender_value,tender_currency)
    tender_value_vat,tender_value_vat_percent = getvat("total_final_value","costs_range_and_currency_with_vat_rate")
    
    # auth attrs
    authority_name = iferror2alt("contacting_authority_information","organisation","contracting_authority_information_contract_award","officialname")
    authority_name_slug = slugify(authority_name)
    authority_address = iferror2alt("contacting_authority_information","address","contracting_authority_information_contract_award","address")
    authority_town = iferror2alt("contacting_authority_information","town","contracting_authority_information_contract_award","town")
    authority_postal_code = iferror2alt("contacting_authority_information","postal_code","contracting_authority_information_contract_award","postal_code")
    authority_country = iferror2getalt("contacting_authority_information","country","value","contracting_authority_information_contract_award")
    authority_contact_person = iferror2alt("contacting_authority_information","attention","contracting_authority_information_contract_award","attention")
    authority_www = iferror2("internet_addresses_contract_award", "url_buyer")
    authority_type = iferror1get("type_of_contracting_authority", "value")

    # notice attrs
    dispatch_date = iferror1("ds_date_dispatch")
    auth_type = iferror1get("aa_authority_type","code")
    doc_type = iferror1get("td_document_type","code")
    contract_type = iferror1get("nc_contract_nature","code")
    proc_type = iferror1get("pr_proc","code")
    regulation_type = iferror1get("rp_regulation","code")
    bid_type = iferror1get("ty_type_bid","code")
    award_criteria_type = iferror1get("ac_award_crit","code")

    row = []
    
    # company attrs - check if multiple companies if so, each of it in a separate row
    for ca in soup.find_all("award_of_contract"):
             
        contract = []    

        soup = ca

        xmlnum += 1
        contract_id = country+"%06d" % xmlnum # internal contract ID

        contract_number = iferror1("contract_number")   
        nr_bids = iferror1("offers_received_number")
        lot = iferror1("lot_number")
        contract_title = iferror2("contract_title", "p")

        contract_award_day = iferror2("contract_award_date","day")
        contract_award_month = iferror2("contract_award_date","month")
        contract_award_year = iferror2("contract_award_date","year")

        company_name = iferror2("economic_operator_name_address","organisation")
        company_name_slug = slugify(company_name)
        company_address = iferror2("economic_operator_name_address","address")
        company_town = iferror2("economic_operator_name_address","town")
        company_postal_code = iferror2("economic_operator_name_address","postal_code")
        company_country = iferror2get("economic_operator_name_address","country","value")

        initial_value = iferror2get("initial_estimated_total_value_contract","value_cost","fmtval")
        initial_value_currency = iferror1get("initial_estimated_total_value_contract","currency")
        initial_value_eur = toeuro(initial_value,initial_value_currency)
        initial_value_vat,initial_value_vat_percent = getvat("contract_value_information","initial_estimated_total_value_contract")
        
        contract_value = iferror3get("contract_value_information","costs_range_and_currency_with_vat_rate","value_cost","fmtval")
        contract_currency = iferror2get("contract_value_information","costs_range_and_currency_with_vat_rate","currency")
        contract_value_eur = toeuro(contract_value,contract_currency)
        contract_value_vat,contract_value_vat_percent = getvat("contract_value_information","costs_range_and_currency_with_vat_rate")

        contract.extend([notice_dispatch_year,notice_dispatch_month,notice_dispatch_day,doc_number,doc_type,contract_type,proc_type,regulation_type,bid_type,award_criteria_type,framework,eu_project,GPA,country,NUTS,cpv,contract_number,contract_id,title_contract,short_contract_description,additional_info,tender_value,tender_currency,tender_value_eur,tender_value_vat,tender_value_vat_percent,authority_name,authority_name_slug,authority_address,authority_town,authority_postal_code,authority_country,authority_contact_person,authority_www,authority_type,auth_type,contract_title,lot,nr_bids,contract_award_day,contract_award_month,contract_award_year,company_name,company_name_slug,company_address,company_town,company_postal_code,company_country,initial_value,initial_value_currency,initial_value_eur,initial_value_vat,initial_value_vat_percent,contract_value,contract_currency,contract_value_eur,contract_value_vat,contract_value_vat_percent,url])
        row.append(contract)
    
    if len(row) == 0:
#        print row
        row.append(url)
    
    return row

#print parse(testfile)

######## get ready.. write!
######## use for end xml files in directory alltar

missing = open("TED-contracts-2011/missing_tenders.csv", "w")

for nr in xrange(1,253):

    filenr = str(nr).zfill(3)
    print filenr
    lapseTime = datetime.now()
   
#    initiate csv file and add header
    outputfile = open("TED-contracts-2011/contracts"+filenr+".csv", "w")
    writer = csv.writer(outputfile)

    missingWriter = csv.writer(missing)

    header = ["notice_dispatch_year","notice_dispatch_month","notice_dispatch_day","doc_number","doc_type","contract_type","proc_type","regulation_type","bid_type","award_criteria_type","framework","eu_project","GPA","country","NUTS","cpv","contract_number","contract_id","title_contract","short_contract_description","additional_info","tender_value","tender_currency","tender_value_eur","tender_value_vat","tender_value_vat_percent","authority_name","authority_name_slug","authority_address","authority_town","authority_postal_code","authority_country","authority_contact_person","authority_www","authority_type","auth_type","contract_title","lot","nr_bids","contract_award_day","contract_award_month","contract_award_year","company_name","company_name_slug","company_address","company_town","company_postal_code","company_country","initial_value","initial_value_currency","initial_value_eur","initial_value_vat","initial_value_vat_percent","contract_value","contract_currency","contract_value_eur","contract_value_vat","contract_value_vat_percent","url"]

    writer.writerow(header)

    for f in glob.glob('alltar/*_'+filenr+'/*.xml'):
        filename = open(f).read()
        row = parse(filename)
        
        if row == None:
            continue
        elif 'http' in row[0]:
            print row
            missingWriter.writerow([row, f])
        else:
            writer.writerows(row)

    print datetime.now() - lapseTime,' / ',datetime.now() - startTime

print datetime.now() - startTime

