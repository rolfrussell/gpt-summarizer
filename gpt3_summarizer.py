import openai
import os
import sys
from datetime import datetime
import re


def load_conversation():
    if len(sys.argv) < 2:
        print("\nError:  Input file not specified")
        print("Usage:  python " + sys.argv[0] + " [input file name]\n")
        exit()
    else:
        return open_file(sys.argv[1])


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save(chunks, summaries):
    file_name = "logs/output_%s.txt" % datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    with open(file_name, 'w', encoding='utf-8') as outfile:
        outfile.write("Chunks:\n\n")
        outfile.write("\n------------------------------------\n".join(chunks))
        outfile.write("\n\n------------------------------------------------------------------------\nSummaries:\n\n")
        outfile.write("\n------------------------------------\n".join(summaries))


def new_chunk():
    return "Please summarize the following:\n"


def chunk(conversation, max_characters_in_chunk=8000):
    chunks = list()
    chunk = new_chunk()
    paragraphs = re.split("Unknown Speaker  \d+:\d\d\n", conversation)
    for paragraph in paragraphs:
        if len(paragraph) >= max_characters_in_chunk:
            print("\n\nERROR: Paragraph " + str(len(paragraph)) + " characters!!!\n")
            print(paragraph)
            exit()
        elif len(chunk) + len(paragraph) <= max_characters_in_chunk:
            chunk = chunk + "\n" + paragraph
        else:
            chunks.append(chunk)
            chunk = new_chunk()
    return chunks


def summarize(chunks):
    summaries = list()
    print("Not calling CPT-3!!!!\n")
    return summaries
    for chunk in chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk,
            temperature=0.2,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        summary = response["choices"][0]["text"]
        summaries.append(summary)
        print(summary)
    return summaries


if __name__ == '__main__':
    openai.api_key = open_file('openaiapikey.txt')
    conversation = load_conversation()
    chunks = chunk(conversation)
    summaries = summarize(chunks)
    save(chunks, summaries)