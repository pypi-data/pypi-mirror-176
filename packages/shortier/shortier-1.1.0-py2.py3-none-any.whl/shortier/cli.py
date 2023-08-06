import argparse
from .shortier import shortier

def main():
    parser = argparse.ArgumentParser(
        description="A Link shortener with support for various providers."
    )
    parser.add_argument(
        "linkURL", type=str,
        help="The resource URL to be shortened."
    )

    parser.add_argument(
        "--type", type=str,
        help=("Service used to shorten the URL "
                "if not set, will use tinyurl. "
                "Options include : chilpit, clckru, dagd, isgd, osdb, tinyurl")
    )

    args = parser.parse_args()
    shortenedURL = shortier(args.linkURL, args.type)
    print("Your link is : " + shortenedURL)

if __name__ == "__main__":
    main()