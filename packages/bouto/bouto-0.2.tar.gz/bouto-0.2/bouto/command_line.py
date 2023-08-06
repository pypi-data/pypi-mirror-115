import argparse
import tempfile

from .utils import copy_template, download, unzip


def main():
    f = tempfile.TemporaryDirectory()
    valid_templates = [
        "actix",
        "aleph",
        "django",
        "nest",
        "next",
        "nuxt",
        "react",
        "vue",
        "yew",
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="the name of the project")
    parser.add_argument(
        "template_name",
        type=str,
        help=(
            "the name of the template you want to use" ".\n must be one of {}"
        ).format(",".join(valid_templates)),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )
    args = parser.parse_args()
    if args.template_name not in valid_templates:
        raise ValueError(
            (
                "the name of the template you want to use"
                ".\n must be one of {}"
            ).format(",".join(valid_templates))
        )
    download(
        "https://github.com/Bournix/bouto/archive/refs/heads/main.zip",
        f.name,
        verbose=args.verbose,
    )
    unzip(f.name, verbose=args.verbose)
    copy_template(args.name, args.template_name, f.name, verbose=args.verbose)
    f.cleanup()
