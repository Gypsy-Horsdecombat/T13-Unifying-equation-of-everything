#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T₁₃ Recursive Law - Batch Processing Utility
-------------------------------------------
Processes a list of inputs (numbers or text) through t13_collapse and outputs CSV.
Imports t13_collapse from t13_collapse.py.

Usage:
  python t13_batch.py -i input1 input2 ... -o output.csv
  python t13_batch.py -f input.txt -o output.csv

Author: Gypsy-Horsdecombat + G
License: ECHO License / MIT-compatible
"""

import argparse
import csv
from t13_collapse import t13_collapse

def main():
    """Parse CLI arguments and process T₁₃ inputs in batch."""
    parser = argparse.ArgumentParser(description="T₁₃ Recursive Law - Batch Processor")
    parser.add_argument("-i", "--inputs", nargs='+', help="List of inputs (numbers or text)")
    parser.add_argument("-f", "--file", type=str, help="File with one input per line")
    parser.add_argument("-o", "--output", type=str, default="t13_output.csv", help="Output CSV file")
    parser.add_argument("-D", "--dimension", type=int, default=13, help="Observer dimension D (default: 13)")
    parser.add_argument("--base", type=int, default=12, help="Modular base (default: 12)")
    parser.add_argument("--text-mode", choices=["concat", "sum"], default="concat", help="Text conversion mode")
    parser.add_argument("--t8-set", choices=["universal", "heart"], default="universal", help="T₈ truth label set")

    args = parser.parse_args()

    inputs = []
    if args.inputs:
        inputs = args.inputs
    elif args.file:
        with open(args.file, 'r') as f:
            inputs = [line.strip() for line in f if line.strip()]

    if not inputs:
        print("Error: No inputs provided.")
        return

    # Process inputs and write CSV
    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Input", "Index", "Truth"])
        for inp in inputs:
            try:
                is_numeric = inp.lstrip('-').replace('.', '', 1).isdigit()
                idx, truth = t13_collapse(
                    inp, D=args.dimension, base=args.base,
                    from_text=not is_numeric, text_mode=args.text_mode,
                    t8_set=args.t8_set, verbose=False
                )
                writer.writerow([inp, idx, truth])
            except Exception as e:
                writer.writerow([inp, 0, f"Error: {str(e)}"])

if __name__ == "__main__":
    main()
