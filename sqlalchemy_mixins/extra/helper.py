from .phone_number import PhoneNumber


def is_valid_phone(phone):
    try:
        if phone is None or phone == '':
            return None
        phone = PhoneNumber(phone)
        return phone.e164
    except:
        raise Exception("Invalid phone number type! Phone number format must be +901234567890")

