#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import random
from xml.sax.saxutils import escape

course_tags = '''<?xml version="1.0"?>
  <course>
  <id>acc</id>
  <title>A Custom Course</title>
  <description>No description.</description>
  <keyboardLayout></keyboardLayout>
  <lessons>
  %s
  </lessons>
  </course>
  '''
lesson_tags = '  <lesson>\n%s  </lesson>\n'
id_tags = '  <id>%s</id>\n'
title_tags = '  <title>%s</title>\n'
char_tags = '  <newCharacters>%s</newCharacters>\n'
text_tags = '  <text>%s</text>\n'

course_file = 'custom_course.ktouch.xml'
min_word_length = 1
max_word_length = 9
min_line_length = 45
lines_of_new_chars = 10
extra_weight = 6        # make "easy" characters more frequent
normalset = 'qwertyuiopsadfghjk;;zxcvbnm,./'

chargroups = [
  # mix_chargroups, chargroup
  (0, 'weiosdklxc,.' * extra_weight),
  (0, 'qrupafj;zvm/' * extra_weight),
  (0, 'qpa;z/10'),
  (0, 'woslx.29'),
  (0, 'eidkc,38'),
  (0, '47rufjvm'),
  (0, '56tyghbn'),
  (0, 'rtyufghjvbnm' * extra_weight),
  (0, '4567rtyufghjvbnm'),
  (1, 'WEIOSDKLXCQRUPAFJ:ZVM?<>'),
  (1, '\'#[]-=\\'),
  (1, '@~{}_+|'),
  (1, '0123456789'),
  (0, '0123456789'),
  (1, u'!"£$%^&*()'),
  (1, u'àèìòùé'),
  (1, u'ÀÈÌÒÙÉ'),
  ]

def generate_text(allowed_chars):
  text = ''
  for line in xrange(lines_of_new_chars):
    cur_line_len = 0
    line = ''
    while 1:
      cur_word_length = random.randint(min_word_length, max_word_length)
      for character in xrange(cur_word_length):
        line += random.choice(allowed_chars)
      cur_line_len += cur_word_length + 1
      if cur_line_len < min_line_length:
        line += ' '
      else:
        break
    text += escape(line) + '\n'
  return text[:-1]

course = ''
for index in xrange(len(chargroups)):
  mix_chargroups, chargroup = chargroups[index]

  # new characters
  lesson = id_tags % ('n' + str(index))
  lesson += title_tags % escape(''.join(set(chargroup)))
  lesson += char_tags % escape(''.join(set(chargroup)))
  if mix_chargroups:
    text = generate_text(chargroup + normalset * (index > 2))
  else:
    text = generate_text(chargroup)
  lesson += text_tags % text
  course += lesson_tags % lesson

  # review
  lesson = id_tags % ('r' + str(index))
  lesson += title_tags % ('Review: ' + escape(''.join(set(chargroup))))
  lesson += char_tags % ''
  allowed_chars = ''.join(elem[1] for elem in chargroups[:index + 1]) + normalset * index
  text = generate_text(allowed_chars)
  lesson += text_tags % text
  course += lesson_tags % lesson

course = course_tags % course.encode('utf-8')

f = open(course_file, 'w')
f.write(course)
f.close()
