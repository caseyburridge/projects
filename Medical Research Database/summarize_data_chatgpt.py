#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 13:48:42 2023

@author: caseypersonal

ChatGHI v1.0.0
"""

# Import necessary modules
import openai
import pandas as pd

# Set OpenAI API key
openai.api_key = "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"


# Function to summarize the abstract (results of study)
def summarize_abstract(abstract):
    global row_counter
    if abstract != "None provided":
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Based on the below abtract, state the main conclusion of this study in 1-2 short sentences. Abstract: {abstract}",
            max_tokens=1000,  # Adjust the token limit as needed
            temperature=0.4,  # Adjust the temperature for creativity
            n=1  # Number of completions to generate
        )
        print("Returned summarized abstract")
        return response.choices[0].text
    else:
        return "None"


# Function to write a short title
def summarize_single_sentence(passage):
    global row_counter
    response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Based on the passage below, write a short, single sentence conclusion of this study (maximum 12 words!). Abstract: {passage}",
            max_tokens=1000,  # Adjust the token limit as needed
            temperature=0.4,  # Adjust the temperature for creativity
            n=1  # Number of completions to generate
        )
    print("Returned summarized title")
    return response.choices[0].text


# Read the CSV file and process the abstract column
csv_file = "CSV files/run-2.csv"
data = pd.read_csv(csv_file, sep=";")

# Run functions
data["ChatGHI Summary"] = data["Abstract"].apply(summarize_abstract)

# If abstract doesn't exist, then send the title instead
if data["Abstract"] != "None provided":
    data["ChatGHI Title"] = data["Abstract"].apply(summarize_single_sentence)
else:
    data["ChatGHI Title"] = data["Title"].apply(summarize_single_sentence)

# Write responses to CSV file
data.to_csv(csv_file, index=False)
