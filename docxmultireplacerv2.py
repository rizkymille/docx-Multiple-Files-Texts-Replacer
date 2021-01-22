# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 23:38:24 2021

@author: Rizky Millennianno
references: adejones, https://stackoverflow.com/questions/56374018/how-to-search-and-replace-a-word-text-in-word-document-using-python-docx
"""
import docx
import os

files = []
docs_path = input("Please enter documents absolute filepath: ")
for file in os.listdir(docs_path):
    if file.endswith(".docx"):
        files.append(file)

words_to_replace = []
words_to_replace_input = ''

while words_to_replace_input != "stop":
    words_to_replace_input = input("Please enter text you want to replace, type 'stop' if there's no more text to replace: ")
    if words_to_replace_input != 'stop':
        words_to_replace.append(words_to_replace_input)
    
words_replacement = []
for words_to_replace_input in words_to_replace:
    words_replacement_input = input("Please enter the replacement text: ")
    words_replacement.append(words_replacement_input)

def docx_find_replace_text(doc, search_text, replace_text):
    paragraphs = list(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraphs.append(paragraph)
    for p in paragraphs:
        if search_text in p.text:
            inline = p.runs
            # Replace strings and retain the same style.
            # The text to be replaced can be split over several runs so
            # search through, identify which runs need to have text replaced
            # then replace the text in those identified
            started = False
            search_index = 0
            # found_runs is a list of (inline index, index of match, length of match)
            found_runs = list()
            found_all = False
            replace_done = False
            for i in range(len(inline)):

                # case 1: found in single run so short circuit the replace
                if search_text in inline[i].text and not started:
                    found_runs.append((i, inline[i].text.find(search_text), len(search_text)))
                    text = inline[i].text.replace(search_text, str(replace_text))
                    inline[i].text = text
                    replace_done = True
                    found_all = True
                    break

                if search_text[search_index] not in inline[i].text and not started:
                    # keep looking ...
                    continue

                # case 2: search for partial text, find first run
                if search_text[search_index] in inline[i].text and inline[i].text[-1] in search_text and not started:
                    # check sequence
                    start_index = inline[i].text.find(search_text[search_index])
                    check_length = len(inline[i].text)
                    for text_index in range(start_index, check_length):
                        if inline[i].text[text_index] != search_text[search_index]:
                            # no match so must be false positive
                            break
                    if search_index == 0:
                        started = True
                    chars_found = check_length - start_index
                    search_index += chars_found
                    found_runs.append((i, start_index, chars_found))
                    if search_index != len(search_text):
                        continue
                    else:
                        # found all chars in search_text
                        found_all = True
                        break

                # case 2: search for partial text, find subsequent run
                if search_text[search_index] in inline[i].text and started and not found_all:
                    # check sequence
                    chars_found = 0
                    check_length = len(inline[i].text)
                    for text_index in range(0, check_length):
                        if inline[i].text[text_index] == search_text[search_index]:
                            search_index += 1
                            chars_found += 1
                        else:
                            break
                    # no match so must be end
                    found_runs.append((i, 0, chars_found))
                    if search_index == len(search_text):
                        found_all = True
                        break

            if found_all and not replace_done:
                for i, item in enumerate(found_runs):
                    index, start, length = [t for t in item]
                    if i == 0:
                        text = inline[index].text.replace(inline[index].text[start:start + length], str(replace_text))
                        inline[index].text = text
                    else:
                        text = inline[index].text.replace(inline[index].text[start:start + length], '')
                        inline[index].text = text
            # print(p.text)

for file in files:
    for i in range(0, len(words_to_replace)):
        for i in range(0, len(words_replacement)):
            doc = docx.Document(file)
            docx_find_replace_text(doc, words_to_replace[i], words_replacement[i])
            doc.save(file)
    print(f"\nReplacement {file} Completed")

input("Press Enter to exit... ")