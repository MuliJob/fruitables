"""Normalize phone numbers for M-Pesa transactions"""
def normalize_phone(phone):
    """Convert 07XXXXXXXX or 01XXXXXXXX to 2547XXXXXXXX format"""
    if phone.startswith('07') or phone.startswith('01'):
        return '254' + phone[1:]
    elif phone.startswith('+254'):
        return phone[1:]
    elif phone.startswith('254') and len(phone) == 12:
        return phone
    else:
        raise ValueError("Invalid phone number format")
