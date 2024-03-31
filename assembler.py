import argparse
from data import *

parser = argparse.ArgumentParser(
                    prog='Hack Assembler',
                    description='Converts Hack Assembly code to binary.',
                    epilog='Nothing Here')

parser.add_argument('file', metavar='file', type=argparse.FileType('r'))

args = parser.parse_args()

next_ram_index = 16
symbol_table = initial_symbol_table


# extract only asm code (returns empty string if no valid code is present)
def extract_asm_code(line: str) -> str:
  comment_index = line.find('//')
  extracted_code = line
  # if comment, then remove it
  if not comment_index == -1:
    extracted_code = line[:comment_index]
  # Return the line after removing white space and line break
  return extracted_code.replace(' ', '').replace('\n', '')

# Translate A instruction
def translate_a_instruction(line: str) -> str:
  global next_ram_index
  binary = ''
  if line[1].isnumeric():
    decimal_value = int(line[1:])
    binary = format(decimal_value, '016b')
  else:
    symbol = line[1:]
    if symbol in symbol_table:
      address = symbol_table[symbol]
      binary = format(address, '016b')
    else:
      symbol_table[symbol] = next_ram_index
      binary = format(next_ram_index, '016b')
      next_ram_index += 1
  return binary

# returns dest bit from a c instruction
def get_dest(line: str) -> str:
  eq_index = line.find('=')
  if eq_index == -1:
    return '000' 
  else:
    dest = line[:eq_index]
    sorted_dest = ''.join(sorted(dest))
    dest_binary = dest_data[sorted_dest]
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

# Assume valid asm code is provided
# String -> Binary
def translate_line(asm_code: str):
  if asm_code[0] == '@':
    return translate_a_instruction(asm_code)
  else:
    return translate_c_instruction(asm_code)
  
# Assuming there is a label in the line
def extract_label(line: str) -> str:
  start_index = line.find('(') + 1;
  end_index = line.find(')')
  label = line[start_index:end_index]
  return label
  
# First pass of the assembler to extract labels
def first_pass(file):
  current_line = 0
  for line in file:
    asm_code = extract_asm_code(line)
    if asm_code:
      # Label code is not counted towards line
      if asm_code[0] == '(':
        label = extract_label(asm_code)
        symbol_table[label] = current_line
      else:
        current_line += 1

# Second pass of the assembler to translate the code
def second_pass(file, hack_file):
  for line in file:
    asm_code = extract_asm_code(line)
    if asm_code and asm_code[0] != '(':
      translated_line = translate_line(asm_code)
      hack_file.write(translated_line + '\n')

  
def main():
  # Create a new Hack file to store the output
  if ".asm" not in args.file.name:
    print( "Invalid File")
    exit(1)

  hack_file_name = args.file.name.replace('.asm', '.hack')
  hack_file = open(hack_file_name, "w")

  first_pass(args.file)
  args.file.seek(0)
  second_pass(args.file, hack_file)

  hack_file.close()

if __name__ == '__main__':
  main()



