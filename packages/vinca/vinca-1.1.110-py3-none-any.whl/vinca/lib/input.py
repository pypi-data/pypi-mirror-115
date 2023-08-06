from vinca.lib import ansi
from vinca.lib.terminal import COLUMNS
from vinca.lib import readchar
from vinca.lib.readchar import ESC, BACK
import string

def input(prompt = '', default_text = '', completions = None):
	if not completions:
		completions = []
	text = default_text
	pos = len(text)
	ansi.hide_cursor()
	while True:
		display_text = text[:pos] + ansi.codes['reverse'] + (text[pos] if pos<len(text) else ' ') + ansi.codes['reset'] + text[pos+1:] + ' '*10
		print('\r' + prompt + display_text, end = '', flush = True)

		c = readchar.readkey()
		if c in ('\n','\r', ESC):
			break
		elif c in ('\b',BACK):
			text = text[:pos - 1] + text[pos:]
			pos -= 1
		elif c in ('\t'):
			pass
		elif c in []:
			if c == LEFT:
				pos -= 1
			if c == RIGHT:
				pos += 1
				pos = pos if pos<len(text) else len(text)
		else:
			print('char is: ', ord(c))
			assert c in string.printable
			text = text[:pos] + c + text[pos:]
			pos += 1
			
				
				
	return text
		
	
input(default_text = 'test', prompt = 'editor: ')
