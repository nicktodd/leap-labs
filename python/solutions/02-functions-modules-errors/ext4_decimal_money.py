"""Extension 4: money as decimal.Decimal instead of float."""

from decimal import ROUND_HALF_UP, Decimal

from payment_utils import UnsupportedCurrencyError, card_fee, parse_amount

# Rates as Decimal, built from strings. Decimal(0.85) would copy the float's binary error.
DECIMAL_RATES = {"GBP": Decimal("1.00"), "EUR": Decimal("0.85"), "USD": Decimal("0.79")}
PENNY = Decimal("0.01")

# Why it matters: floats are binary fractions, and most decimal amounts have no exact
# binary form, so tiny errors appear and accumulate.
print(f"0.1 + 0.2 == 0.3 -> {0.1 + 0.2 == 0.3} (0.1 + 0.2 is {0.1 + 0.2!r})")
print(f"Decimal('0.1') + Decimal('0.2') == Decimal('0.3') -> "
      f"{Decimal('0.1') + Decimal('0.2') == Decimal('0.3')}")

float_total = 0.0
for _ in range(1000):
    float_total += 0.10
print(f"1,000 x 0.10 as float: {float_total!r}")
print(f"1,000 x 0.10 as Decimal: {sum(Decimal('0.10') for _ in range(1000))}")


def to_gbp_decimal(amount_text: str, currency: str) -> Decimal:
    """Convert amount text to GBP as a Decimal, rounded half-up to the penny."""
    # Validate with the float parser, then rebuild from the cleaned text so the Decimal
    # never passes through a float.
    parse_amount(amount_text)
    cleaned = amount_text.strip().lstrip("£€$").replace(",", "")
    if currency not in DECIMAL_RATES:
        raise UnsupportedCurrencyError(f"no FX rate for {currency}")
    return (Decimal(cleaned) * DECIMAL_RATES[currency]).quantize(PENNY, rounding=ROUND_HALF_UP)


print()
print(f"EUR 143.92 -> float {143.92 * 0.85!r}, Decimal {to_gbp_decimal('€143.92', 'EUR')}")
print(f"USD 1,594.61 -> float {1594.61 * 0.79!r}, "
      f"Decimal {to_gbp_decimal('$1,594.61', 'USD')}")

# Half-pennies: 1.5% of GBP 1,249.00 is exactly 18.735. round() on a float gives 18.73,
# because the float stored for 18.735 is slightly below it. ROUND_HALF_UP on a Decimal
# gives 18.74, which is what a finance team expects to see.
fee_float = card_fee(1249.00)
fee_decimal = (Decimal("1249.00") * Decimal("0.015")).quantize(PENNY, rounding=ROUND_HALF_UP)
print(f"Fee on GBP 1,249.00: float {fee_float}, Decimal {fee_decimal}")
