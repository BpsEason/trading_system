from decimal import Decimal

LIMITS = {'USD': Decimal('10000'), 'EUR': Decimal('8000'), 'JPY': Decimal('1200000')} # 新增 JPY 限制

def check_limits(amount: Decimal, currency: str):
    limit = LIMITS.get(currency, Decimal('0'))
    if amount <= 0:
        return False, "金額必須大於 0"
    if currency not in LIMITS:
        return False, f"不支援的貨幣類型: {currency}"
    if amount > limit:
        return False, f"{currency} 金額 {amount} 超出限額 {limit}"
    return True, "OK"
