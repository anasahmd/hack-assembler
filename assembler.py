import argparse
from data import *

parser = argparse.ArgumentParser(
                    prog='Hack Assembler',
                    description='Converts Hack Assembly code to binary.',
                    epilog='Nothing Here')

parser.add_argument('filename', metavar='filename', type=argparse.FileType('r'))

args = parser.parse_args()

# Create a new Hack file to store the output
hack_file_name = args.filename.name.replace('asm', 'hack')
hack_file = open(hack_file_name, "w")

# removes comment from a line
def remove_comments(line: str) -> str:
  comment_index = line.find('//')
  if not comment_index == -1:
    remove_comment = line[:comment_index]
    return remove_comment
  else:
    return line

# removes white space from a line
def remove_whitespace(line: str) -> str:
  return line.replace(' ', '').replace('\n', '')

# Translate A instruction
def translate_a_instruction(line: str) -> str:
  decimal_value = int(line[1:])
  binary = format(decimal_value, '016b')
  return binary

# returns dest bit from a c instruction
def get_dest(line: str) -> str:
  eq_index = line.find('=')
  if eq_index == -1:
    return '000' 
  else:
    dest = line[:eq_index]
    dest_binary = dest_data[dest]
    return dest_binary

# returns comp bit from a c instruction
def get_comp(line: str) -> str:
  eq_index = line.find('=')
  eq_index = None if eq_index == -1 else eq_index + 1
  sc_index = line.find(';')
  sc_index = None if sc_index == -1 else sc_index
  
  comp = line[eq_index:sc_index];
  comp_binary = comp_data[comp];
  return comp_binary

# returns jump bit from a c instruction
def get_jump(line: str) -> str:
  sc_index = line.find(';')
  if sc_index == -1:
    return '000'
  else:
    jump = line[sc_index + 1:]
    jump_binary = jump_data[jump]
    return jump_binary


# Translate C instruction
def translate_c_instruction(line: str) -> str:
  dest = get_dest(line)
  comp = get_comp(line)
  jump = get_jump(line)

  return '111' + comp + dest + jump


# Remove lines
# String -> Binary
def translate_line(line: str):
  removed_comment = remove_comments(line)
  removed_whitespace = remove_whitespace(removed_comment)

  if removed_whitespace:
    if removed_whitespace[0] == '@':
      return translate_a_instruction(removed_whitespace)
    else:
      return translate_c_instruction(removed_whitespace)
  

for line in args.filename:
  translated_line = translate_line(line)
  if translated_line :
    hack_file.write(translated_line + '\n')

hack_file.close()


