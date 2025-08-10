from decimal import Decimal

LIMITS = {'USD': Decimal('10000'), 'EUR': Decimal('8000')}

def check_limits(amount: Decimal, currency: str):
    limit = LIMITS.get(currency, Decimal('0'))
    if amount > limit:
        return False, f"exceeds {limit} {currency}"
    return True, "OK"
