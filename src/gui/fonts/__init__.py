FONT_FAMILY = "Helvetica"  # default

FONTS = {
    "header": (FONT_FAMILY, 20, "bold"),
    "subheader": (FONT_FAMILY, 18, "bold"),
    "text": (FONT_FAMILY, 14),
    "button": (FONT_FAMILY, 14),
    "mono": ("Courier New", 12),
    "label": (FONT_FAMILY, 14, "bold"),
}


def update_fonts():
    global FONT_FAMILY, FONTS
    try:
        import tkinter.font as tkfont

        available_fonts = tkfont.families()
        FONT_FAMILY = (
            "SF Pro Display" if "SF Pro Display" in available_fonts else "Helvetica"
        )
    except RuntimeError:
        pass  # keep default
    FONTS = {
        "header": (FONT_FAMILY, 20, "bold"),
        "subheader": (FONT_FAMILY, 18, "bold"),
        "text": (FONT_FAMILY, 14),
        "button": (FONT_FAMILY, 14),
        "mono": ("Courier New", 12),
        "label": (FONT_FAMILY, 14, "bold"),
    }
