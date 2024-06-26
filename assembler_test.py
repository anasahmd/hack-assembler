import unittest

from assembler import *

class TestClass(unittest.TestCase):

   def test_extract_asm_code(self):
      self.assertEqual(extract_asm_code('@2//addressing 2'), '@2')
      self.assertEqual(extract_asm_code('@2'), '@2')
      self.assertEqual(extract_asm_code('//This is a comment line'), '')
      self.assertEqual(extract_asm_code('   @2 // Comment'), '@2')
      self.assertEqual(extract_asm_code('@2   '), '@2')
      self.assertEqual(extract_asm_code('D = 1'), 'D=1')

   def test_translate_a_instruction(self):
      self.assertEqual(translate_a_instruction('@1'), '0000000000000001')
      self.assertEqual(translate_a_instruction('@2'), '0000000000000010')
      self.assertEqual(translate_a_instruction('@10'), '0000000000001010')
      self.assertEqual(translate_a_instruction('@R5'), '0000000000000101')
      self.assertEqual(translate_a_instruction('@R5'), '0000000000000101')
      self.assertEqual(translate_a_instruction('@ARG'), '0000000000000010')

   def test_get_comp(self):
      self.assertEqual(get_comp('0;JMP'), '0101010')
      self.assertEqual(get_comp('D+1'), '0011111')
      self.assertEqual(get_comp('A=D+1'), '0011111')
      self.assertEqual(get_comp('D-M'), '1010011')
      self.assertEqual(get_comp('D=D-M'), '1010011')
      self.assertEqual(get_comp('D=D&A;JEQ'), '0000000')
     
   def test_get_dest(self):
      self.assertEqual(get_dest('D+1'), '000')
      self.assertEqual(get_dest('A=D+1'), '100')
      self.assertEqual(get_dest('D=D-M'), '010')
      self.assertEqual(get_dest('AD=D'), '110')
      self.assertEqual(get_dest('AM=!D'), '101')
      self.assertEqual(get_dest('ADM=D&A;JEQ'), '111')

   def test_get_jump(self):
      self.assertEqual(get_jump('0;JMP'), '111')
      self.assertEqual(get_jump('D+1'), '000')
      self.assertEqual(get_jump('ADM=D&A;JEQ'), '010')

   def test_translate_line(self):
      self.assertEqual(translate_line('@0'), '0000000000000000')
      self.assertEqual(translate_line('D=D+A'), '1110000010010000')

   def test_extract_label(self):
      self.assertEqual(extract_label('(LOOP)'), 'LOOP')
      self.assertEqual(extract_label('(STOP)'), 'STOP')

if __name__ == '__main__':
    unittest.main()