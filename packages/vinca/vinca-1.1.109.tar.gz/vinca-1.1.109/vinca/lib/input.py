from vinca.lib import ansi
from vinca.lib.terminal import COLUMNS
from vinca.lib import readchar
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
		elif c in ('\b', BACKSPACE):
			text = text[:pos - 1] + text[pos:]
			pos -= 1
		elif c == DEL:
			text = text[:pos] + text[pos + 1:]
		elif c in ('\t'):
			pass
		elif c in (UP, DOWN, LEFT, RIGHT):
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
