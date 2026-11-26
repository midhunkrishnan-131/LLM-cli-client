import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from assistant import CalculatorArgs, calculate, regex_invoice

def test_calculator():
    assert calculate(CalculatorArgs(operation="divide",a=184.5,b=3)) == 61.5
    assert calculate(CalculatorArgs(operation="add",a=61.5,b=27)) == 88.5

def test_divide_zero():
    try: calculate(CalculatorArgs(operation="divide",a=1,b=0))
    except ValueError: return
    assert False

def test_regex_total_skips_subtotal():
    assert regex_invoice("SUBTOTAL: USD 10.00\nTOTAL: USD 12.50\n")["total"] == 12.5
    assert regex_invoice("Subtotal: AED 480.00\nGrand Total: AED 504.00\n")["total"] == 504.0
    assert regex_invoice("subtotal: 3.00\n")["total"] is None

def test_regex_currency_symbol():
    dollar=regex_invoice("Total: $12.50\n")
    assert dollar["currency"] == "$"
    assert dollar["total"] == 12.5
    rupee=regex_invoice("Grand Total: ₹1,234.56\n")
    assert rupee["currency"] == "₹"
    assert rupee["total"] == 1234.56
    assert regex_invoice("Total: AED 504.00\n")["currency"] == "AED"
    assert regex_invoice("Total: 10.00\n")["currency"] is None

def test_regex_fixture():
    from pathlib import Path
    data=(Path(__file__).parents[1]/"data"/"invoice_ocr.txt").read_text()
    result=regex_invoice(data)
    assert result["invoice_number"] == "INV-2026-1042"
    assert result["total"] == 504.0
