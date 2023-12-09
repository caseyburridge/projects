#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 12:44:13 2023

v1.0.0

This file consists of predefined lists of MeSH terms

"""
keywords_list = [
"Therapy",
"Complications",
"Diagnosis",
"Enzymology",
"Ethnology",
"Etiology",
"Nursing",
"Rehabilitation",
"Transmission",
"Parasitology"
]


relatedterms_list = [
"Brain-Gut Axis",
"Gastrointestinal Microbiome",
"Dietary Supplements",
"Mental health",
"Intestinal Mucosa",
"Lacticaseibacillus rhamnosus",
"Lactobacillus acidophilus",
"Acute Disease",
"Chronic Disease",
"Infant"''
"Recurrence",
"Early Detection of Cancer",
"Nutritional Status",
"Risk Factors",
"Exercise",
"Toxins, Biological",
"Microbiota",
"Fasting",
"Colon",
"Defecation",
"Enteric Nervous System",
"Gastrointestinal Motility",
"Digestion",
"Gastrointestinal Tract",
"Quality of Life"
]


coconditions_list = [
"Depression",
"Anxiety",
"Abdominal Pain",
"Anxiety Disorders",
"Dysbiosis",
"Diarrhea",
"Constipation",
"Stress, Psychological",
"Dehydration",
"Fever",
"Inflammation",
"Obesity"   
]


substance_list = [
"Dietary fibre",
"Drugs, Chinese Herbal",
"Plant Extracts ",
"Plant Leaves",
"Herbal Medicine",
"Phytotherapy",
"Psyllium",
"Flower Essences",
"Curare",
"Grape Seed Extract",
"Ipecac" ,
"Lecithins",
"Opium",
"Pectins",
"Rhamnogalacturonans",
"Picrotoxin",
"Podophyllin",
"Senna Extract",
"Sennosides",
"Tea",
"Kombucha Tea",
"Teas, Herbal",
"Coffee",
"Vitamin D",
"Cholecalciferol",
"Ergocalciferols",
"Dietary Fiber",
"Prebiotics",
"Resistant Starch",
"Dietary Supplements",
"Nutrients",
"Curcumin",
"Carotenoids",
"Abscisic Acid",
"beta Carotene",
"Lycopene",
"Norisoprenoids",
"Retinoids",
"Acitretin",
"Etretinate",
"Fenretinide",
"Isotretinoin",
"Retinaldehyde",
"Retinyl Esters",
"Vitamin A",
"Tretinoin",
"Alitretinoin",
"Xanthophylls",
"Canthaxanthin",
"Cryptoxanthins",
"Beta-Cryptoxanthin",
"Lutein",
"Zeaxanthins",
"zeta Carotene",
"Inositol",
"Frankincense",
"Charcoal",
"Bentonite",
"Zeolites",
"Selenium",
"Vitamin B 6",
"Pyridoxamine",
"Pyridoxine",
"Pyridoxal",
"Polyphenols",
"Resveratrol",
"Berberine",
"Eugenol",
"Safrole",
"Flavonoids",
"Vitamins",
"Phenols",
"Hallucinogens",
"Micronutrients",
"Trace Elements",
"Provitamins",
"Vitamin B Complex",
"Cannabinoids",
"Cannabidiol",
"Cannabinol",
"Dronabinol",
"Ascorbic Acid",
"Biological Products"]

q_substances = '"{}"[majr] AND "{}/Therapeutic Use"[mh]'


"""
Save for later :-)

# Define dictionaries for different query types
query_type_mappings = {
    tuple(t_substances): q_substances,
    tuple(t_actions): '"Shared query type for actions"',
    tuple(t_oils): '"Shared query type for oils"',
    tuple(t_diets): '"Shared query type for diets"',
}

"""



