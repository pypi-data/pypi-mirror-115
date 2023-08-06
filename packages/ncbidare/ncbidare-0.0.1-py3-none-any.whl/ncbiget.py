# retrives results from NCBI and writes it to a csv file (Accession ID and Definition)
# rettype genbank database nucleotide
# genbank info retrieval

import csv
from Bio import Entrez

def get_genbank(query="Klebsiella pneumoniae", count=1, filename="results.csv"):

    Entrez.email = "sera.1@iitj.ac.in" 

    handle = Entrez.esearch(db="nucleotide", term=str(query), retmax=count)
    record = Entrez.read(handle)
    gi_list = record["IdList"]

    number = 0

    fields = ['Sno','Accession ID','Description'] 
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile, dialect='excel') 
        csvwriter.writerow(fields)

        for ide in gi_list:
            handle = Entrez.efetch(db="nucleotide", id=ide, rettype="gb", retmode="text") 
            data = handle.read()
            words = data.split()
            x = int(words.index('ACCESSION'))
            y = int(words.index('VERSION'))
            acc_number = words[y+1]
            description = ' '.join(words[9:x])
            number += 1
            row = [number,acc_number,description]
            csvwriter.writerow(row)

#to get list of unique strains from the csv file

def get_strains(filename="results.csv"):

    Entrez.email = "sera.1@iitj.ac.in" 
    strains = []

    with open(filename, 'r') as file:  #input file name - refer for format, check line 22
        reader = csv.reader(file)
        itercars = iter(reader)
        next(itercars)
        for row in itercars:
            if row != []:
                new_strain = row[2].split(' ')[row[2].split(' ').index("strain")+ 1]
                write_file = open("results.txt", "a")
                write_file.write(new_strain)
                write_file.write("\n")
                if new_strain in strains:
                    None
                else:         
                    write_file = open(filename, "a")
                    write_file.write(new_strain)
                    write_file.write("\n")
                    strains.append(new_strain)

#to get fasta file of each strain

def get_fasta(filename="results.csv"):

    Entrez.email = "sera.1@iitj.ac.in" 
    no = 1

    with open(str(filename), 'r') as file:  #input file name - refer for format, check line 22
        reader = csv.reader(file)
        itercars = iter(reader)
        next(itercars)
        for row in itercars:
            if row != ['', '', '']:
                new_strain = row[2].split(' ')[row[2].split(' ').index("strain")+ 1]
                search_handle = Entrez.esearch(db="nucleotide",term=row[1], usehistory="y", idtype="acc")   #change row[index]
                search_results = Entrez.read(search_handle)
                search_handle.close()

                webenv = search_results["WebEnv"]
                query_key = search_results["QueryKey"]

                fetch_handle = Entrez.efetch(db="nucleotide",rettype="fasta",retmode="text",webenv=webenv,query_key=query_key,idtype="acc")
                data = fetch_handle.read()

                filename = "kleb_" + str(new_strain) + ".fasta"
                write_file = open(filename, "a")
                write_file.write(data)

                no+=1