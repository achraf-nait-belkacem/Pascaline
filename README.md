# Pascaline - Calculator

A command-line calculator that evaluates mathematical expressions without using `eval()` or the `math` module.

## Features

- Complex expressions with parentheses
- Basic operations: `+`, `-`, `*`, `/`, `**` (exponentiation)
- Pi constant (`pi` = 3.14159265359)
- History tracking
- Input validation

## Installation

No dependencies required. Just run:

```bash
python main.py
```

## Usage

Enter mathematical expressions directly:

```
>> 2 + 3
5

>> (2 + 3) * 4
20

>> 2 ** 3
8

>> pi * 2
6.28318530718
```

**Commands:**
- `h` - Show help
- `q` or `quit` - Exit
- `Ctrl+C` - Exit

## Operator Precedence

1. `**` (Exponentiation - right-associative)
2. `*`, `/` (Multiplication, Division)
3. `+`, `-` (Addition, Subtraction)

## Project Structure

- `main.py` - Entry point
- `cli.py` - Command-line interface
- `complex_calc.py` - Core calculator logic
- `utils.py` - Utility functions
- `text.py` - Text constants
- `sig_handlers.py` - Signal handlers

## Algorithm

Uses the **Shunting Yard Algorithm** to parse and evaluate expressions with proper operator precedence.
