import pyfiglet
from pyfiglet import Figlet


def main():
    f = Figlet()

    # Fonts whose names commonly indicate block/banner styles
    keywords = (
        "block",
        "banner",
        "big",
        "doom",
        "standard",
        "small",
        "heavy",
        "bold",
        "slant",
        "shadow",
        "univers",
    )

    fonts = [
        font for font in f.getFonts()
        if any(keyword in font.lower() for keyword in keywords)
    ]

    print(f"Found {len(fonts)} candidate fonts.\n")

    for font in fonts:
        print("=" * 80)
        print(f"FONT: {font}")
        print("=" * 80)

        try:
            print(pyfiglet.figlet_format("Village Brawl", font=font))
        except Exception:
            pass

        input("Press ENTER for next font...")


if __name__ == "__main__":
    main()
