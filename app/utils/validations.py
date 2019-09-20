#! /usr/bin/env python
# coding: utf-8

from .exceptions import ValidationError


def validate_email(email, suffix_need=None, prefix_len_min=3, prefix_len_max=64, suffix_len_min=3, suffix_len_max=32):
    """Simple validate email"""
    # First, str needed
    if not isinstance(email, str):
        return False
    # Second, `@` needed
    if '@' not in email:
        return False
    prefix, suffix = email.split('@', maxsplit=1)
    # If suffix_need provide, check whether equal
    if suffix_need and suffix != suffix_need:
        return False
    # Roughly check prefix length and suffix length
    prefix_len, suffix_len = len(prefix), len(suffix)
    if any([prefix_len < prefix_len_min,
            prefix_len > prefix_len_max,
            suffix_len < suffix_len_min,
            suffix_len > suffix_len_max]):
        return False
    return True


def validate_phone(phone, fail_raise=False):
    """Simple validate phone num"""
    if str(phone).isdigit() and 9 < len(phone) < 12:
        return True
    if fail_raise:
        raise ValidationError('phone invalid.')
    return False


def validate_password(password, fail_raise=False):
    if 5 < len(password) < 64 and str(password)[0].isalpha():
        return True
    if fail_raise:
        raise ValidationError('password invalid.')
    return False
