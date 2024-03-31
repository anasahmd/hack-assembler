# Hack Assembler

This is an assembler for Hack Assembly Language written in Python. This assembler is a part of [Nand To Tetris](https://www.nand2tetris.org/) course.

## Usage

To utilize this tool, follow these steps:

1. Ensure you have Python 3 installed on your system.
2. Download or clone this repository to your local machine.
3. Navigate to the directory containing the assembler.py file using your command line interface.
4. Execute the script by running the following command:

```bash
python3 assembler.py <filename.asm> [-o output_file.hack]
```

Replace **<filename.asm>** with the name of the assembly file you wish to process.

Optionally, you can specify an output file using the -o or --output flag followed by the desired output filename. Otherwise the script will generate a new **'.hack'** file with the same name as the input assembly file (**'filename.asm'**) in the same directory. This **.hack** file will contain the processed code outputted by the assembler.

## Testing

This project includes a test file **'assembler_test.py'** script that tests the functionality of **'assembler.py'**.
To run the tests, execute one of the following commands in your terminal:

```bash
python3 -m unittest assembler_test.py
```

## Example

Consider a simple hack assembly language program named **'Add.asm'**:

```
@2
D=A
@3
D=D+A
@0
M=D
```

This program adds the values stored in memory locations 2 and 3 and stores the result in memory location 0.

When you run the **'assembler.py'** on this **'Add.asm'**, it will generate the following output in a **'.hack'** file:

```
0000000000010000
1110110000010000
0000000000010000
1110000010010000
0000000000010000
1110001100001000
```
