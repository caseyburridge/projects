# Medical research database (WIP)

View a proof of concept here: https://testing.guthealthintel.com/view/datatables/ 

As someone who has struggled with IBS and other gut-related disorders, I decided to build a gut health research database focused on natural treatments.

I wrote a Python script that queries the Pubmed API and pulls data for to relevant studies. The script formats the data and saves is to a CSV file.

There is a separate script that loops through each row in the CSV file and sends a prompt to ChatGPT asking for a 1-2 sentence summary of the findings of the study.

I then import all of this data to a WordPress website and constructed a searchable database as a proof of concept.

This project is still a work in progress, but I intend for it to be the most comprehensive natural health research database for gut disorders.
