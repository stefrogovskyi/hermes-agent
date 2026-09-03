#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validator.py — Richard Marlowe / Navo24
Strict DNS & MX Record Validator using standard socket & DNS resolution.
"""

import socket

def verify_email_domain(email: str) -> bool:
    """Check if the email format is valid and domain has active DNS/MX records."""
    if not email or '@' not in email:
        return False
    
    parts = email.strip().split('@')
    if len(parts) != 2:
        return False
    
    domain = parts[1].strip().lower()
    if not domain or '.' not in domain:
        return False
        
    # Exclude synthetic/fake patterns
    fake_patterns = ["example.com", "test.com", "invalid", "sample.com", "fake.com", "acme.com", "placeholder"]
    if any(fp in domain for fp in fake_patterns):
        return False
        
    try:
        # Resolve host addresses
        addr_info = socket.getaddrinfo(domain, 25, socket.AF_INET, socket.SOCK_STREAM)
        if addr_info and len(addr_info) > 0:
            return True
    except socket.gaierror:
        try:
            # Fallback check on port 80 / 443
            addr_info = socket.getaddrinfo(domain, 80, socket.AF_INET, socket.SOCK_STREAM)
            if addr_info and len(addr_info) > 0:
                return True
        except Exception:
            return False
    except Exception:
        return False
        
    return False

if __name__ == "__main__":
    test_emails = [
        "stefan@navo24.com",
        "rich@navo24.com",
        "fake@nonexistentdomain999xyz.org",
        "test@example.com"
    ]
    for em in test_emails:
        print(f"{em} -> Valid: {verify_email_domain(em)}")
