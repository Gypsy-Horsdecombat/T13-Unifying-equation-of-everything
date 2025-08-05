#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T₁₃ Recursive Law - Single-file implementation
---------------------------------------------
Implements the core T₁₃ collapse:
  T₁₃(n) = ( Σ[f_i(n) mod base] ⊕ H_D ) ⇒ T₈^D | O₁₃
Where:
  - f₁: Kaprekar-like divergence (desc(n) - asc(n))
  - f₂: Mirror collapse (|n - reverse(n)|)
  - f₃: Weighted digit resonance (Σ d_i * (i + start_index))
  - H_D = 13 * (D - 8)
  - Maps to one of 8 T₈ truths (universal or heart labels)
  - O₁₃: Implicit observer via input validation and output

Supports:
  - Numeric and text inputs (A=1..Z=26, accent-safe)
  - Configurable base (default: 12)
  - Trace output as dictionary
  - CLI via argparse
  - Unit tests for known outputs

Author: Gypsy-Horsdecombat + G
License: ECHO License / MIT-compatible
"""

from __future__ import annotations
import argparse
import re
import unicodedata
from typing import Dict, Union, Tuple
import unittest

ALPHA_MAP = {chr(ord('A') + i): str(i + 1) for i in range(26)}

def text_to_number(text: str, mode: str = "concat") -> int:
    if len(text) > 100 and mode == "concat":
        raise ValueError("Text input too long for concat mode (max 100 chars).")
    cleaned = ''.join(c for c in unicodedata.normalize('NFKD', text)
                      if not unicodedata.combining(c)).upper()
    cleaned = re.sub(r'[^A-Za-z]', '', cleaned)
    if not cleaned:
        raise ValueError("No alphabetic characters found in text input.")
    if mode == "concat":
        digits = ''.join(ALPHA_MAP[ch] for ch in cleaned)
        return int(digits)
    elif mode == "sum":
        return sum(int(ALPHA_MAP[ch]) for ch in cleaned)
    else:
        raise ValueError("Mode must be 'concat' or 'sum'.")

def digits_of(n: int) -> str:
    return str(abs(int(n)))

def reverse_int(n: int) -> int:
    return int(digits_of(n)[::-1])

def sort_digits(n: int, reverse: bool) -> int:
    return int(''.join(sorted(digits_of(n), reverse=reverse)))

def f1_kaprekar(n: int) -> int:
    desc = sort_digits(n, True)
    asc = sort_digits(n, False)
    return abs(desc - asc)

def f2_mirror(n: int) -> int:
    return abs(n - reverse_int(n))

def f3_weighted(n: int, start_index: int = 1) -> int:
    s = digits_of(n)
    return sum(int(d) * (i + start_index) for i, d in enumerate(s))

def harmonic_constant(D: int) -> int:
    if D < 1:
        raise ValueError("Dimension D must be positive.")
    return 13 * (D - 8)

T8_UNIVERSAL = {
    0: "All motion spirals",
    1: "Energy is memory",
    2: "The center watches",
    3: "Polarity balances",
    4: "Patterns are laws",
    5: "Collapse is recursion",
    6: "Function precedes name",
    7: "That which repeats is real",
}

T8_HEART = {
    0: "Presence",
    1: "Signal",
    2: "Intention",
    3: "Phase",
    4: "Joy",
    5: "Awe",
    6: "Collapse",
    7: "Truth",
}

def map_to_t8(value: int, set_name: str = "universal") -> str:
    m = T8_UNIVERSAL if set_name.lower() == "universal" else T8_HEART
    return m[value % 8]

def sentinel_lock(n: int, D: int) -> bool:
    try:
        _ = int(n)
        _ = int(D)
    except Exception:
        return True
    return n < 0 or D < 1

def t13_collapse(
    x: Union[int, str],
    D: int = 13,
    base: int = 12,
    from_text: bool = False,
    text_mode: str = "concat",
    start_index: int = 1,
    t8_set: str = "universal",
    verbose: bool = False
) -> Tuple[int, str]:
    n = text_to_number(str(x), mode=text_mode) if from_text else int(x)

    if sentinel_lock(n, D) or base < 2:
        if verbose:
            print(f"ψ(0): Sentinel lock triggered (invalid n, D, or base={base}).")
        return 0, "Sentinel Lock: recursion terminated (ψ(0))."

    f1 = f1_kaprekar(n)
    f2 = f2_mirror(n)
    f3 = f3_weighted(n, start_index=start_index)

    collapsed = (f1 + f2 + f3) % base
    H_D = harmonic_constant(D)
    fused = collapsed ^ H_D
    idx = fused % 8
    truth = map_to_t8(idx, set_name=t8_set)

    if verbose:
        print(f"Input n          : {n}")
        print(f"Dimension D      : {D}")
        print(f"Base             : {base}")
        print(f"f₁ (Kaprekar)    : {f1}")
        print(f"f₂ (Mirror)      : {f2}")
        print(f"f₃ (Weighted)    : {f3}")
        print(f"Σ f_i mod {base} : {collapsed}")
        print(f"H_D              : {H_D}")
        print(f"XOR fusion       : {fused}")
        print(f"Index (mod 8)    : {idx}")
        print(f"T₈[{idx}]        : {truth}")

    return idx, truth

def t13_trace(
    x: Union[int, str],
    D: int = 13,
    base: int = 12,
    from_text: bool = False,
    text_mode: str = "concat",
    start_index: int = 1,
    t8_set: str = "universal"
) -> Dict[str, Union[int, str]]:
    n = text_to_number(str(x), mode=text_mode) if from_text else int(x)
    if sentinel_lock(n, D) or base < 2:
        return {"n": n, "D": D, "base": base, "f1": 0, "f2": 0, "f3": 0,
                "collapsed": 0, "H_D": 0, "fused": 0, "idx": 0,
                "truth": "Sentinel Lock: recursion terminated (ψ(0))."}

    f1 = f1_kaprekar(n)
    f2 = f2_mirror(n)
    f3 = f3_weighted(n, start_index=start_index)
    collapsed = (f1 + f2 + f3) % base
    H_D = harmonic_constant(D)
    fused = collapsed ^ H_D
    idx = fused % 8
    truth = map_to_t8(idx, set_name=t8_set)

    return {
        "n": n,
        "D": D,
        "base": base,
        "f1": f1,
        "f2": f2,
        "f3": f3,
        "collapsed": collapsed,
        "H_D": H_D,
        "fused": fused,
        "idx": idx,
        "truth": truth
    }

class TestT13Collapse(unittest.TestCase):
    def test_known_outputs_universal(self):
        tests = [
            (72, 13, 12, "Patterns are laws"),
            (13, 13, 12, "Function precedes name"),
            (144, 13, 12, "The center watches"),
        ]
        for n, D, base, expected in tests:
            with self.subTest(n=n, D=D, base=base):
                _, truth = t13_collapse(n, D=D, base=base, from_text=False, t8_set="universal")
                self.assertEqual(truth, expected, f"Expected {expected}, got {truth}")

    def test_known_outputs_heart(self):
        tests = [
            (72, 13, 12, "Joy"),
            (13, 13, 12, "Collapse"),
            (144, 13, 12, "Intention"),
        ]
        for n, D, base, expected in tests:
            with self.subTest(n=n, D=D, base=base):
                _, truth = t13_collapse(n, D=D, base=base, from_text=False, t8_set="heart")
                self.assertEqual(truth, expected, f"Expected {expected}, got {truth}")

def main():
    parser = argparse.ArgumentParser(description="T₁₃ Recursive Law - Collapse Engine")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--number", type=int, help="Numeric input n")
    group.add_argument("-t", "--text", type=str, help="Text input (A=1..Z=26)")
    parser.add_argument("-D", "--dimension", type=int, default=13, help="Observer dimension D (default: 13)")
    parser.add_argument("--base", type=int, default=12, help="Modular base (default: 12)")
    parser.add_argument("--text-mode", choices=["concat", "sum"], default="concat", help="Text conversion mode")
    parser.add_argument("--start-index", type=int, default=1, help="Start index for f₃ weighting (default: 1)")
    parser.add_argument("--t8-set", choices=["universal", "heart"], default="universal", help="T₈ truth label set")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print step-by-step trace")

    args = parser.parse_args()

    if args.number is not None:
        idx, truth = t13_collapse(args.number, D=args.dimension, base=args.base, from_text=False,
                                 text_mode=args.text_mode, start_index=args.start_index, t8_set=args.t8_set,
                                 verbose=args.verbose)
    else:
        idx, truth = t13_collapse(args.text, D=args.dimension, base=args.base, from_text=True,
                                 text_mode=args.text_mode, start_index=args.start_index, t8_set=args.t8_set,
                                 verbose=args.verbose)

    print(truth)

if __name__ == "__main__":
    main()
    import sys
    if len(sys.argv) == 1:
        unittest.main(argv=[''])
