# MIT License

# Copyright (c) 2022 Beksultan Artykbaev

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from typing import Dict

def bricks(sentence: str, _reverse: bool = False) -> str:
	'''Returns bricked version of string
	- bricks("Hello world!") -> "HeLlO WoRlD!"
	- bricks("Hello world!", _reverse=True) -> "hElLo wOrLd!"
	'''
	if _reverse:
		new_sentence = ''.join(x + y for x, y in zip(sentence[0::2].lower(), sentence[1::2].upper()))
		if len(sentence) % 2:
			new_sentence += sentence[-1].lower()
		return new_sentence
	else:
		new_sentence = ''.join(x + y for x, y in zip(sentence[0::2].upper(), sentence[1::2].lower()))

		if len(sentence) % 2:
			new_sentence += sentence[-1].upper()
		return new_sentence

def replaceall(sentence: str, __old__new: Dict, ignore_case=False) -> str:
	'''Replaces text from given sentence and dictionary:
		dictionary should be formatted like this {old_string: new_string}
	- replaceall("123456", {"123":"456", "456":"789"}) -> "456789"
	- replaceall("Hello world!", {"Hello": "Sup", "world": "earth"}) -> "Sup earth!"
	'''
	if not __old__new:
		# Edge case that'd produce a funny regex and cause a KeyError
		return sentence

	# If case insensitive, we need to normalize the old string so that later a replacement
	# can be found. For instance with {"HEY": "lol"} we should match and find a replacement for "hey",
	# "HEY", "hEy", etc.
	if ignore_case:
		def normalize_old(s):
			return s.lower()

		re_mode = re.IGNORECASE

	else:
		def normalize_old(s):
			return s

		re_mode = 0

	__old__new = {normalize_old(key): val for key, val in __old__new.items()}

	# Place longer ones first to keep shorter substrings from matching where the longer ones should take place
	# For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
	# 'hey ABC' and not 'hey ABc'
	rep_sorted = sorted(__old__new, key=len, reverse=True)
	rep_escaped = map(re.escape, rep_sorted)

	# Create a big OR regex that matches any of the substrings to replace
	pattern = re.compile("|".join(rep_escaped), re_mode)

	# For each match, look up the new string in the __old__new, being the key the normalized old string
	return pattern.sub(lambda match: __old__new[normalize_old(match.group(0))], sentence)

def numerate_text(text: str, splitter: str = " ") -> str:
	'''Numerate each line of text.
	- numerate_text("Hello world\\nHow are you doing?") -> "1 Hello World\\n2 How are you doing?"
	- numerate_text("First line.\\nThe second line\\nThe third line") -> "1 First line.\\n2 The second line\\n3 The third line"
	'''
	numerated_lines = []
	lines = text.split("\n")
	for line_num in range(len(lines)):
		numerated_lines.append(f"{line_num+1}{splitter}{lines[line_num]}")
	return "\n".join(numerated_lines)

def remove_trailing_whitespaces(sentence: str) -> str:
	'''Remove all trailing whitespaces from sentence.
	- remove_trailing_whitespaces("text   ") -> "text"
	- remove_trailing_whitespaces("Look at this. ") -> "Look at this."
	'''
	return re.sub(r"(?<=\S)\s+$", '', sentence)

def remove_leading_whitespaces(sentence: str) -> str:
	'''Remove all leading whitespaces from sentence.
	- remove_leading_whitespaces("   text") -> "text"
	- remove_leading_whitespaces(" Look at this.") -> "Look at this."
	'''
	return re.sub(r"^\s+", '', sentence)

def text_to_binary(sentence: str) -> str:
	'''Convert string to a binary (A binary number is a number expressed in the base-2 numeral system or binary numeral system,
	a method of mathematical expression which uses only two symbols: 0 and 1)
	- text_to_binary("Hello") -> 0100100001100101011011000110110001101111
	- text_to_binary("A") -> 01000001
	'''
	# 08 means width 8, 0 padded, and the b functions as a sign to output the resulting number in base 2 (binary).
	return "".join(f"{ord(char):08b}" for char in sentence)

def binary_to_text(binary: str) -> str:
	'''Convert binary to text (A binary number is a number expressed in the base-2 numeral system or binary numeral system,
	a method of mathematical expression which uses only two symbols: 0 and 1)
	- binary_to_text("0100100001100101011011000110110001101111") -> "Hello"
	- binary_to_text("01000001") -> "A"
	'''
	return ''.join(chr(int(binary[i*8:i*8+8],2)) for i in range(len(binary)//8))

def str_to_bool(val: str) -> bool:
	'''Converts a string representation of truth to bool
		False values are: "false", "f", "no", "n", "off", "0"
		True values are: "true", "t", "yes", "y", "on", "1"
	- str_to_bool("True") -> True
	- str_to_bool("False") -> False
	'''
	val = val.lower()
	if val in ["false", "f", "no", "n", "off", "0"]:
		return False
	elif val in ["true", "t", "yes", "y", "on", "1"]:
		return True
	else:
		raise ValueError(f"Invalid truth value: {val!r}")