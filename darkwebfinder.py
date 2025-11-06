"""
Dark web monitoring helper for sanctioned cybersecurity research.
Use only under proper legal authority and with organizational approvals.
"""
from __future__ import annotations

import argparse
import random
import re
import textwrap
from pathlib import Path
from typing import Iterable

import requests

SEARCH_ENGINES = {
    "ahmia": "https://ahmia.fi/search/?q={query}",
    "onionland": "https://onionlandsearchengine.com/search?q={query}",
}
ONION_REGEX = r"https?://[a-z2-7]{16,56}\.onion"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

DISCLAIMER = textwrap.dedent(
    """
    WARNING: This tool is for authorized cyber-threat intelligence collection only.
    Accessing hidden services can be illegal in many jurisdictions.
    Confirm you have legal clearance, route traffic through TOR, and follow your
    organization's governance policies before continuing.
    """
).strip()

ASCII_NINJA = r"""
           _____                 _
          / ____|               | |
         | |     ___  _ __   ___| |__   ___ _ __
         | |    / _ \| '_ \ / __| '_ \ / _ \ '__|
         | |___| (_) | | | | (__| | | |  __/ |
          \_____\___/|_| |_|\___|_| |_|\___|_|

                 /\            /\            /\
                //\\          //\\          //\\
               ///\\\        ///\\\        ///\\\
              ////\\\\      ////\\\\      ////\\\\
                 ||            ||            ||
"""

SOCIAL_TAGS = [
    "IG: @code_ronin",
    "TikTok: @code.ronin",
]


def fetch_onion_links(search_query: str, engine: str) -> list[str]:
    """Query the selected engine and extract .onion URLs from results."""
    normalized = "+".join(search_query.split())
    url_template = SEARCH_ENGINES[engine]
    response = requests.get(
        url_template.format(query=normalized),
        timeout=25,
        headers=DEFAULT_HEADERS,
    )
    if response.status_code == 403:
        raise requests.HTTPError(
            "403 Forbidden: engine blocked the request. "
            "Send traffic through TOR/VPN or adjust network policy.",
            response=response,
        )
    response.raise_for_status()
    matches = re.findall(ONION_REGEX, response.text, flags=re.IGNORECASE)
    return sorted(set(matches))


def save_results_txt(links: Iterable[str], directory: Path) -> Path:
    """Persist extracted links to a timestamped txt file inside directory."""
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / f"sites_{random.randint(1, 9999):04d}.txt"
    with file_path.open("w", encoding="utf-8") as handle:
        for link in links:
            handle.write(f"{link}\n")
    return file_path


def save_results_xml(links: Iterable[str], directory: Path) -> Path:
    """Persist extracted links to a simple XML file for downstream parsing."""
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / f"sites_{random.randint(1, 9999):04d}.xml"
    with file_path.open("w", encoding="utf-8") as handle:
        handle.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        handle.write("<results>\n")
        for link in links:
            handle.write(f"  <link>{link}</link>\n")
        handle.write("</results>\n")
    return file_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="darkwebfinder.py",
        description=(
            "Dark web monitoring helper for sanctioned cybersecurity research.\n"
            "Example usage:\n"
            "  python3 darkwebfinder.py -f \"credit cards\" --format txt\n"
            "  python3 darkwebfinder.py -f ransomware --format xml --limit 30 --engine onionland\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--find",
        required=True,
        help="Search phrase to look up in Ahmia results (e.g. 'leaked credentials').",
    )
    parser.add_argument(
        "--format",
        choices=("txt", "xml"),
        default="txt",
        help="Output format for saved file (default: txt).",
    )
    parser.add_argument(
        "--out-dir",
        default="darkweb_results",
        help="Directory to store extracted links (default: darkweb_results).",
    )
    parser.add_argument(
        "--engine",
        choices=tuple(SEARCH_ENGINES.keys()),
        default="ahmia",
        help="Select the hidden-service search engine (default: ahmia).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Limit the number of links saved to file (default: 50).",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Also echo discovered links to the terminal.",
    )
    parser.add_argument(
        "--skip-confirm",
        action="store_true",
        help="Skip the interactive legal-use confirmation (useful for automation).",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.skip_confirm:
        print(DISCLAIMER)
        proceed = input("Type 'YES' to confirm authorized use: ").strip()
        if proceed.upper() != "YES":
            print("Aborting: lawful use not confirmed.")
            return 1

    print(ASCII_NINJA)
    print("Coderonin Dark Finder")
    for tag in SOCIAL_TAGS:
        print(tag)
    print()

    print(f"[+] Querying {args.engine.title()} for: {args.find}")
    try:
        links = fetch_onion_links(args.find, args.engine)
    except requests.RequestException as exc:
        print(f"Request error: {exc}")
        return 1

    if not links:
        print("[-] No .onion links detected in response.")
        return 0

    limited_links = links[: args.limit] if args.limit > 0 else links
    if args.print:
        print("\n".join(limited_links))

    if args.format == "xml":
        output_path = save_results_xml(limited_links, Path(args.out_dir))
    else:
        output_path = save_results_txt(limited_links, Path(args.out_dir))

    print(f"[+] Saved {len(limited_links)} links to {output_path}")
    print("[!] Route follow-up requests through TOR or a controlled relay before visiting any link.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
