#!/usr/bin/env python3
"""Check if a list of domain names are registered or available."""

import os
import sys
import whois
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_domain(domain: str) -> tuple[str, bool, str]:
    """
    Check if a domain is registered.
    Returns (domain, is_registered, status_message).
    """
    try:
        w = whois.whois(domain)
        # A domain is registered if it has a creation date or registrar
        if w.domain_name or w.registrar or w.creation_date:
            return domain, True, f"Registered (registrar: {w.registrar or 'unknown'})"
        else:
            return domain, False, "Available"
    except whois.exceptions.WhoisDomainNotFoundError:
        return domain, False, "Available"
    except Exception as e:
        return domain, None, f"Error: {e}"


def check_domains(domains: list[str], max_workers: int = 5) -> None:
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_domain = {executor.submit(check_domain, d.strip()): d.strip() for d in domains}
        for future in as_completed(future_to_domain):
            domain, is_registered, message = future.result()
            results[domain] = (is_registered, message)

    # Print sorted results
    registered = []
    available = []
    errors = []

    for domain, (is_registered, message) in sorted(results.items()):
        if is_registered is True:
            registered.append((domain, message))
        elif is_registered is False:
            available.append((domain, message))
        else:
            errors.append((domain, message))

    print(f"\n{'='*50}")
    print(f"REGISTERED ({len(registered)})")
    print(f"{'='*50}")
    for domain, message in registered:
        print(f"  [+] {domain:<30} {message}")

    print(f"\n{'='*50}")
    print(f"AVAILABLE ({len(available)})")
    print(f"{'='*50}")
    for domain, message in available:
        print(f"  [ ] {domain:<30} {message}")

    if errors:
        print(f"\n{'='*50}")
        print(f"ERRORS ({len(errors)})")
        print(f"{'='*50}")
        for domain, message in errors:
            print(f"  [?] {domain:<30} {message}")

    print()


def load_domains_from_file(path: str) -> list[str]:
    with open(path) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isfile(arg):
            domains = load_domains_from_file(arg)
            print(f"Loaded {len(domains)} domains from '{arg}'.")
            print("Usage: python check_domains.py [file.txt | domain1.com domain2.org ...]")
        else:
            domains = sys.argv[1:]
    else:
        # Example usage — replace or extend this list
        domains = [
            "google.com",
            "github.com",
            "thisisaveryunlikelydomain123456789.com",
            "python.org",
            "notregisteredexample99999.net",
        ]
        print("No domains provided. Using example list.")
        print("Usage: python check_domains.py [file.txt | domain1.com domain2.org ...]")

    print(f"\nChecking {len(domains)} domain(s)...")
    check_domains(domains)


if __name__ == "__main__":
    main()
