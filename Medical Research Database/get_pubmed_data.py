# -*- coding: utf-8 -*-
"""
Spyder Editor

GHI PoC v1.4 ---

This script is able to pull all the needed study data.
working on:
    - filter out certain pub types [x]
    - log data for 0 results [x]
    - Fixed CSV header issue [x]
"""

# Import packages including MeSH lists from config file
from lxml import etree #new
import requests
import os
import csv
import json
from config.terms import substance_list,coconditions_list,relatedterms_list

##### Functions #####

# Post process abstract for edge cases with odd formatting (BACKGROUND, METHODS, etc)
def process_abstract(xml_abstract):
    
    if '<AbstractText' not in xml_abstract:
       return xml_abstract.strip()
    
    abstract_texts = xml_abstract.split('<AbstractText ')
    processed_abstract = ""
    
    for abstract_text in abstract_texts[1:]:  # Skip the first element (before the first AbstractText)
        label_start = abstract_text.find('Label="') + len('Label="')
        label_end = abstract_text.find('"', label_start)
        label = abstract_text[label_start:label_end]

        text_start = abstract_text.find('>', label_end) + 1
        text_end = abstract_text.find('</AbstractText>')
        text = abstract_text[text_start:text_end].strip()

        # Append label as a subheading if available
        if label:
            processed_abstract += f"<p><b>{label}</b>:<br>{text}</p>"
        else:
            processed_abstract += f"\n\n{text}"

    return processed_abstract.strip()

# Function to format a single term as JSON for Entry Tags field
def format_single_term_json(term, tag_color="#bdccf9"): 
    term = [
        {
            "label": term,
            "value": term,
            "color": tag_color,
            "text_color": "#101517",
            "style": f"--tag-bg:{tag_color}; --tag-text-color:#101517; --tag-remove-btn-color: #101517;"
        }
    ]

    return json.dumps(term)

# Function to format a list of terms as JSON for Entry Tags field
def format_terms_as_json(term_list):
    formatted_terms = [
        {
            "label": term,
            "value": term,
            "color": "#bdccf9",
            "text_color": "#101517",
            "style": "--tag-bg:#bdccf9; --tag-text-color:#101517; --tag-remove-btn-color: #101517;"
        }
        for term in term_list if term in mesh_terms
    ]

    # Check if the result is empty
    if not formatted_terms:
        return format_single_term_json("None provided","#c8c8c8")
    else:
        return json.dumps(formatted_terms)
    
# Function to replace None or empty values
def replace_empty(value, default="None provided"):
    if value is not None and value != "":
        return value 
    else:
        return default

##### # #####

# Counter for no. of studies
counter = 0

# Define the PubMed API base URL and endpoints
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
esearch_url = base_url + "esearch.fcgi"
efetch_url = base_url + "efetch.fcgi"

# Define the search query
disease = "Irritable Bowel Syndrome"

# Define the MeSH terms to check for
related_mesh_terms = relatedterms_list
    
# Define related co-conditions in MeSH
co_conditions_mesh = coconditions_list

# A test list for testing purposes! (change when ready for full run!)
substance_list_test = ["Probiotics", "Berberine"] #substance_list

# Define the CSV file path
csv_file_path = "CSV files/test.csv"

# Check if the CSV file already exists
csv_file_exists = os.path.exists(csv_file_path)

# Initialize a set to store unique study identifiers
# unique_study_ids = set()

for therapeutic_sub in substance_list_test:

    query = '"{}"[majr] AND "{}/Therapeutic Use"[mh]'.format(disease, therapeutic_sub)
    
    # Step 1: Perform the initial search to get study IDs
    params = {
            "db": "pubmed",
            "term": query,
            "retmax": 3, # adjust this for proper run
            "retmode": "json",
    }
    
    response = requests.get(esearch_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        study_ids = data["esearchresult"]["idlist"]
        print("Studies found: " + str(len(study_ids)))
    else:
        print("Error in ESearch request")
        study_ids = []
    
    # Step 2: Fetch data for each study and save to CSV
    if study_ids:
        with open(csv_file_path, "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header row only if the CSV file is created initially
            if not csv_file_exists:
                csv_writer.writerow([
                "PMID",
                "Disease",
                "Title",
                "Abstract",
                "MeSH Terms",
                "Related Terms",
                "Co Conditions",
                "Therapeutic Intervention",
                "Publication Date",
                "Authors",
                "Journal Name",
                "Pub Year",
                "Pub type",
                ])
                csv_file_exists = True  # Set the flag to True after writing the header
    
            for pmid in study_ids:
                
                # Check if the study ID is already in the set
                # if pmid not in unique_study_ids: (Optional!)
                
                    # Fetch data for the study
                    params = {
                        "db": "pubmed",
                        "id": pmid,
                        "retmode": "xml",
                    }
                    response = requests.get(efetch_url, params=params)
        
                    if response.status_code == 200:
                        xml_response = response.text
                        # Parse XML using lxml
                        root = etree.fromstring(xml_response)
                        
                        # Extract publication type
                        publication_types = root.findall(".//PublicationTypeList/PublicationType")
                        publication_type_list = [pub_type.text for pub_type in publication_types]
        
                        # Join the Publication Types into a comma-separated list
                        publication_types_str = ", ".join(publication_type_list)
                        
                        # Skip study if pub type is "Interview"
                        if publication_types_str == "Interview":
                            print("Study Type: Interview; Ignored")
                        else:
                            # Extract title
                            title_path = root.xpath(".//ArticleTitle")
                            title_html = etree.tostring(title_path[0], encoding="unicode")
                            title = title_html.replace("<ArticleTitle>", "").replace("</ArticleTitle>", "")
                            
                            # Extract the raw HTML content of the abstract
                            abstract_elements = root.xpath(".//AbstractText[not(ancestor::OtherAbstract)]")
                            abstract_html = "\n".join([etree.tostring(abstract_element, encoding="unicode") for abstract_element in abstract_elements])
                            # Post-process the abstract to remove <AbstractText> tags
                            abstract_html = abstract_html.replace("<AbstractText>", "").replace("</AbstractText>", "")
                            # Continue post processing the abstract for egde cases
                            abstract = process_abstract(abstract_html)
                            
                            # Extract MeSH terms
                            mesh_terms = [mesh.text for mesh in root.findall(".//MeshHeading/DescriptorName")]
                            
                            # Format related terms and co-conditions as JSON
                            related_terms = format_terms_as_json(related_mesh_terms)
                            co_conditions = format_terms_as_json(co_conditions_mesh)
                            
                            # Extract publish date
                            pub_date_element = root.find(".//PubDate")
                            if pub_date_element is not None:
                                pub_date_year = pub_date_element.find("Year").text if pub_date_element.find("Year") is not None else ""
                                pub_date_month = pub_date_element.find("Month").text if pub_date_element.find("Month") is not None else ""
                                pub_date_day = pub_date_element.find("Day").text if pub_date_element.find("Day") is not None else ""
                                
                                # Check if all date components are present
                                if pub_date_year and pub_date_month and pub_date_day:
                                    pub_date = f"{pub_date_year}-{pub_date_month}-{pub_date_day}"
                                else:
                                    pub_date = ""
                            else:
                                pub_date = ""
                            
                            # Extract authors
                            authors = root.findall(".//Author")
                            author_list = []
                            
                            for author in authors:
                                last_name = author.find(".//LastName").text if author.find(".//LastName") is not None else ""
                                fore_name = author.find(".//ForeName").text if author.find(".//ForeName") is not None else ""
                                # Combine last name & forename, into a single string
                                author_str = f"{fore_name} {last_name} ".strip()
                                if author_str:
                                    author_list.append(author_str)
                            
                            # Extract journal name
                            journal_name_element = root.find(".//Journal")
                            journal_name = journal_name_element.find("Title").text
                            
                            # Store all the information in a dictionary for this study
                            study_info = {
                                "PMID": replace_empty(pmid),
                                "Disease": format_single_term_json(disease),
                                "Title": replace_empty(title),
                                "Abstract":  replace_empty(abstract),
                                "MeSH Terms": ", ".join(mesh_terms),
                                "Related Terms": related_terms,
                                "Co Conditions": co_conditions,
                                "Therapeutic Intervention": format_single_term_json(therapeutic_sub),
                                "Publication Date": replace_empty(pub_date),
                                "Authors": replace_empty(", ".join(author_list)),
                                "Journal Name": replace_empty(journal_name),
                                "Pub Year": replace_empty(pub_date_year),
                                "Pub type": replace_empty(publication_types_str),
                            }
                            
                            # Write study data to CSV
                            csv_writer.writerow([
                            study_info["PMID"], 
                            study_info["Disease"], 
                            study_info["Title"],
                            study_info["Abstract"], 
                            study_info["MeSH Terms"], 
                            study_info["Related Terms"],
                            study_info["Co Conditions"],
                            study_info["Therapeutic Intervention"], 
                            study_info["Publication Date"],
                            study_info["Authors"], 
                            study_info["Journal Name"],
                            study_info["Pub Year"],
                            study_info["Pub type"],
                            ])
                            
                            # Update the set with the new study ID
                            # unique_study_ids.add(study_info["PMID"])
                            # Update study counter
                            counter = counter + 1
                            print("Studies added:" + " " + str(counter))
                    else:
                        print(f"Error in EFetch request for PMID {pmid}")
    
        print(str(counter) + " studies saved to CSV file")
    else:
        print("########")
        print("No study IDs found: "+str(disease)+" | "+str(therapeutic_sub))
        print("Query: "+str(query))
        print("########")

