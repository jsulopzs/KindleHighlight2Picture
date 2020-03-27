import csv
import re
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

f = open('My Clippings.txt', 'r', encoding='utf-8')

notes = f.read()

# print(notes[0:1000])

# Amazon Kindle saves highlighted notes between \n\n and \n. We use regular expressions to find them.
note_list = re.findall(r'(?<=\n\n)(.*?)(?=\n)', notes, flags=re.M)

# Between all the notes, we'd like to choose one in order to make a picture out of it. We ask the user to introduce words of the desired note.
to_search = input('What are you looking for? ')

matched_notes = []

for note in note_list:
    if to_search in note.lower():
        matched_notes.append(note)

print('Matched notes list:')

# Showing a list of matched notes so that the user will introduce the number of the desired one.
for i, item in enumerate(matched_notes, 1):
    print(i, '. ' + item + '\n', sep='')

note_number = int(input('Please, choose the number of the note you want: '))

note_to_picture = matched_notes[note_number - 1]

# Now it's time to start with the picture

def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        # split the line by spaces to get words
        words = re.split('(?<=-)| ', text)
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                if '-' not in words[i]:
                    line = line + words[i] + " "
                    i += 1
                else:
                    line = line + words[i]
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
            # when the line gets longer than the max width do not append the word,
            # add the line to the lines array
            lines.append(line[:len(line)-1])
    return lines

# Setting the font for the body
font = ImageFont.truetype('PTSerif-Regular', size=79)

lines = text_wrap(note_to_picture, font, 2048-200)

line_height = font.getsize('Hg\"')[1]

# Starting position of the note
x = y = 100
img = Image.new(mode='RGBA', size= (2048, (line_height+20)*(len(lines)+1)+200), color=(245,240,219))
draw = ImageDraw.Draw(img)

for line in lines:
    draw.text((x,y), line[:len(line)], fill=(0,0,0), font=font)
    y +=font.getsize(line)[1] + 20

# Font to add the source
font = ImageFont.truetype('HelveticaNeue-Bold', size=50)

# Setting the source of the note
source = 'Source: The Economist'
draw.text((x,y+80), source, fill=(0,0,0), font=font)

# Creating layer for transparency ("Shared by ...")
t = Image.new(mode='RGBA', size=img.size, color=(255,255,255,0))
font = ImageFont.truetype('HelveticaNeue', size=50)
d = ImageDraw.Draw(t)
d.text((2048-720,y+80), 'Shared via @jesusloplarr', fill=(0,0,0,128), font=font)

# We finally combine the two images
combined = Image.alpha_composite(img, t)

filename = input('How would you like to name your note? ')

combined.save(filename + '.png', quality=95)

# This will show the picture if you have a Unix System (Mac or Linux)
os.system('open ' + filename + '.png')
