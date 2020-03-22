# -*- coding: UTF-8 -*-
#!/usr/bin/python

from itertools import islice 
import requests
from bs4 import BeautifulSoup
from Bio import Entrez
from Bio import Medline
import Drugs

def RE_extractor(med):
	
	with open("CIS.txt",  encoding="ISO-8859-1") as f:
		cis = []
		for line in islice(f, 0, None): 
			l = line.split("\t")
			try:
				if med in l[1] and l[-2] not in cis and len(l[-2]) != 0:
					cis.append(l[-2])
			except:
				pass

	return cis

def ansm_parser(med, side_effect): 

	cis = RE_extractor(med)
	if len(cis) ==  1:
		quote_page = "http://agence-prd.ansm.sante.fr/php/ecodex/rcp/R"+ str(cis[0]) +".htm"
		page = requests.get(quote_page)
		src = page.content
		soup = BeautifulSoup(src, 'html.parser')
		tables = soup.find("table", attrs={"class": "AmmCorpsTexteTable"})
		EI = []
		
		for row in tables.find_all('tr'):
			cells = row.find('td')
			paragraph = cells.find('p')
			EI.append(str(paragraph))

		for ei in EI:
			if side_effect.title() in ei:
				return True 
		return False
	else:
		# "Le médicament n'a pas un RCP sur le site de l'agence nationale de santé"	
		return False

def ID_extractor(side_effect):
	
	with open("meddra_all_se.tsv", "r", encoding="ISO-8859-1") as f:
		res = []
		for line in islice(f, 0, None): 
			l=line.split("\t")
			if l[3] == "PT":
				if side_effect in l[-1] and l[-2] not in res :
					res.append(l[-1])
					res.append(l[-2])
	if len(res) == 1:
		return res[1]
	else:
		return str(0)
	
def sider_parser(drug, side_effect):

	with open("side_effects.tsv.ods", "r", encoding="ISO-8859-1") as f:
		for line in islice(f, 0, None): 
			l = line.split("\t")
			if side_effect == l[-1]:
				side_effect = l[0]
	ID = ID_extractor(side_effect.title())
	quote_page = "http://sideeffects.embl.de/se/"+ ID
	page = requests.get(quote_page)
	src = page.content
	soup = BeautifulSoup(src, 'html.parser')
	a = soup.find_all('a')
	drug_eng = Drugs.drugs(drug)
	ans = 0
	if len(drug_eng) == 1:
		for i in a:
			if drug_eng.lower() in i.lower():
				ans += 1	
	elif len(drug_eng) > 1:
		for i in range(len(drug_eng)):
			for j in a:
				if drug_eng[i].lower() in i.lower():
					ans += 1
	if ans > 0:
		return True
	else:
		return False

def pub_med_parser(drug, side_effect):
	
	Entrez.email = "cnpm@cnpm.org.dz"
	terms = "(("+drug+"[Title]) AND "+side_effect+"[Title/Abstract])" 
	handle= Entrez.esearch(db = "pubmed", term = terms, rettype = "medline", retmode = "text") 
	record = Entrez.read(handle)
	handle.close()
	if record["Count"] != "0":
		idlist = record["IdList"]
		handle2 = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
		records = Medline.parse(handle2)
		records = list(records)

		for record in records:
			print("title:", record.get("TI", "?"))
			print("authors:", record.get("AU", "?"))
			print("source:", record.get("SO", "?"))
		return True
	else:
		print("0 résultats trouvés")
		return False