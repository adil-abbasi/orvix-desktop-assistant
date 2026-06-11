import os
import time
from pathlib import Path


# PowerPoint / Office constants
MSO_SHAPE_RECTANGLE = 1
MSO_TEXT_ORIENTATION_HORIZONTAL = 1
MSO_FALSE = 0
MSO_TRUE = -1


def rgb(red, green, blue):
    # Office COM uses BGR-like integer through VBA RGB format
    return red + (green * 256) + (blue * 65536)


THEME = {
    "bg": rgb(8, 12, 24),
    "surface": rgb(17, 24, 39),
    "surface_2": rgb(30, 41, 59),
    "text": rgb(248, 250, 252),
    "muted": rgb(203, 213, 225),
    "gold": rgb(212, 175, 55),
    "purple": rgb(139, 92, 246),
    "cyan": rgb(34, 211, 238),
    "green": rgb(52, 211, 153),
}


def resolve_output_folder(location: str):
    location = str(location or "desktop").lower().strip()
    home = Path.home()

    if location in ["documents", "document"]:
        return home / "Documents"

    if location in ["downloads", "download"]:
        return home / "Downloads"

    onedrive = os.environ.get("OneDrive")
    if onedrive:
        onedrive_desktop = Path(onedrive) / "Desktop"
        if onedrive_desktop.exists():
            return onedrive_desktop

    return home / "Desktop"


def clean_filename(filename: str):
    filename = str(filename or "Orvix_Presentation").strip()

    for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
        filename = filename.replace(char, "_")

    filename = filename.replace(" ", "_").strip("_")

    if not filename:
        filename = "Orvix_Presentation"

    if not filename.lower().endswith(".pptx"):
        filename += ".pptx"

    return filename


def normalize_bullets(bullets):
    if isinstance(bullets, list):
        return [str(item).strip() for item in bullets if str(item).strip()]

    if isinstance(bullets, str):
        lines = bullets.replace("•", "\n").splitlines()
        return [line.strip("-• ").strip() for line in lines if line.strip()]

    return []


def fallback_slides(topic: str, slide_count: int):
    topic = str(topic or "Artificial Intelligence").strip()

    base = [
        {
            "title": topic,
            "bullets": [
                "Prepared by Orvix AI Desktop Assistant",
                "Generated live from a natural language command"
            ]
        },
        {
            "title": "Introduction",
            "bullets": [
                f"{topic} is an important topic in today’s digital world.",
                "It connects concepts, applications, and real-world value.",
                "This presentation explains the topic in simple structured points."
            ]
        },
        {
            "title": "Key Concepts",
            "bullets": [
                "Core definitions and important ideas",
                "Main components and working principles",
                "Examples that make the topic easier to understand"
            ]
        },
        {
            "title": "Applications",
            "bullets": [
                "Used in education, business, healthcare, and technology",
                "Supports automation, productivity, and better decisions",
                "Helps solve practical real-world problems"
            ]
        },
        {
            "title": "Benefits",
            "bullets": [
                "Saves time and reduces manual work",
                "Improves accuracy and consistency",
                "Creates smarter workflows and better outcomes"
            ]
        },
        {
            "title": "Conclusion",
            "bullets": [
                f"{topic} has strong value in modern life.",
                "It creates opportunities for innovation and learning.",
                "This presentation was generated live by Orvix."
            ]
        }
    ]

    if slide_count <= len(base):
        return base[:slide_count]

    while len(base) < slide_count:
        base.insert(
            -1,
            {
                "title": f"Additional Insight {len(base)}",
                "bullets": [
                    f"This slide adds more useful information about {topic}.",
                    "The idea can be expanded with examples, data, or visuals.",
                    "It keeps the presentation complete and organized."
                ]
            }
        )

    return base[:slide_count]


def normalize_slides(raw_slides, topic: str, slide_count: int):
    slides = []

    if isinstance(raw_slides, dict):
        raw_slides = raw_slides.get("slides", [])

    if isinstance(raw_slides, list):
        for item in raw_slides:
            if not isinstance(item, dict):
                continue

            title = str(item.get("title", "")).strip()
            bullets = normalize_bullets(
                item.get("bullets")
                or item.get("points")
                or item.get("content")
                or []
            )

            if title:
                slides.append({
                    "title": title,
                    "bullets": bullets[:5]
                })

    if slides:
        return slides[:slide_count]

    return fallback_slides(topic, slide_count)


def get_slide_content(topic: str, slide_count: int, user_command: str = ""):
    try:
        from app.ppt_agent.ppt_content_generator import generate_ppt_content

        try:
            raw = generate_ppt_content(
                topic=topic,
                slide_count=slide_count,
                user_command=user_command
            )
        except TypeError:
            try:
                raw = generate_ppt_content(topic, slide_count, user_command)
            except TypeError:
                raw = generate_ppt_content(topic, slide_count)

        return normalize_slides(raw, topic, slide_count)

    except Exception as error:
        print("LIVE PPT: Content generation failed. Using fallback.")
        print("LIVE PPT ERROR:", error)
        return fallback_slides(topic, slide_count)


def add_shape(slide, shape_type, left, top, width, height, fill_color, transparency=0, line=False):
    shape = slide.Shapes.AddShape(shape_type, left, top, width, height)

    shape.Fill.Visible = MSO_TRUE
    shape.Fill.ForeColor.RGB = fill_color
    shape.Fill.Transparency = transparency

    if not line:
        shape.Line.Visible = MSO_FALSE

    return shape


def add_textbox(
    slide,
    text,
    left,
    top,
    width,
    height,
    font_size=24,
    bold=False,
    color=None,
    font_name="Segoe UI",
    align=1
):
    box = slide.Shapes.AddTextbox(
        MSO_TEXT_ORIENTATION_HORIZONTAL,
        left,
        top,
        width,
        height
    )

    text_range = box.TextFrame.TextRange
    text_range.Text = str(text or "")
    text_range.Font.Name = font_name
    text_range.Font.Size = font_size
    text_range.Font.Bold = MSO_TRUE if bold else MSO_FALSE
    text_range.Font.Color.RGB = color or THEME["text"]

    try:
        text_range.ParagraphFormat.Alignment = align
    except Exception:
        pass

    box.TextFrame.MarginLeft = 6
    box.TextFrame.MarginRight = 6
    box.TextFrame.MarginTop = 4
    box.TextFrame.MarginBottom = 4

    return box


def apply_slide_theme(slide, presentation, slide_no=None, total_slides=None):
    width = presentation.PageSetup.SlideWidth
    height = presentation.PageSetup.SlideHeight

    # Main dark background
    bg = add_shape(
        slide,
        MSO_SHAPE_RECTANGLE,
        0,
        0,
        width,
        height,
        THEME["bg"]
    )
    bg.ZOrder(1)

    # Large soft purple block
    add_shape(
        slide,
        MSO_SHAPE_RECTANGLE,
        width * 0.62,
        -20,
        width * 0.42,
        height + 40,
        THEME["purple"],
        transparency=0.76
    )

    # Gold accent top line
    add_shape(
        slide,
        MSO_SHAPE_RECTANGLE,
        42,
        34,
        width - 84,
        4,
        THEME["gold"],
        transparency=0
    )

    # Small Orvix mark
    add_shape(
        slide,
        MSO_SHAPE_RECTANGLE,
        42,
        height - 45,
        10,
        10,
        THEME["gold"]
    )

    add_textbox(
        slide,
        "ORVIX AI DESKTOP ASSISTANT",
        58,
        height - 52,
        260,
        22,
        font_size=9,
        bold=True,
        color=THEME["muted"]
    )

    if slide_no and total_slides:
        add_textbox(
            slide,
            f"{slide_no:02d} / {total_slides:02d}",
            width - 122,
            height - 54,
            80,
            24,
            font_size=11,
            bold=True,
            color=THEME["muted"],
            align=3
        )


def add_title_slide(presentation, title, subtitle, total_slides):
    # 12 = ppLayoutBlank
    slide = presentation.Slides.Add(1, 12)
    width = presentation.PageSetup.SlideWidth
    height = presentation.PageSetup.SlideHeight

    apply_slide_theme(slide, presentation, 1, total_slides)

    # Eyebrow
    add_textbox(
        slide,
        "LIVE GENERATED PRESENTATION",
        62,
        92,
        width - 124,
        30,
        font_size=13,
        bold=True,
        color=THEME["gold"]
    )

    # Main title
    add_textbox(
        slide,
        title,
        62,
        135,
        width - 145,
        155,
        font_size=44,
        bold=True,
        color=THEME["text"]
    )

    # Subtitle glass panel
    add_shape(
        slide,
        MSO_SHAPE_RECTANGLE,
        62,
        318,
        width - 124,
        86,
        THEME["surface"],
        transparency=0.08
    )

    add_textbox(
        slide,
        subtitle,
        82,
        338,
        width - 164,
        46,
        font_size=19,
        bold=False,
        color=THEME["muted"]
    )

    # Bottom badges
    badges = ["AI Assisted", "Auto Created", "Saved by Orvix"]

    left = 62
    for badge in badges:
        add_shape(
            slide,
            MSO_SHAPE_RECTANGLE,
            left,
            430,
            145,
            34,
            THEME["surface_2"],
            transparency=0.05
        )

        add_textbox(
            slide,
            badge,
            left + 10,
            438,
            125,
            18,
            font_size=10,
            bold=True,
            color=THEME["gold"]
        )

        left += 160

    return slide


def add_content_slide(presentation, index, title, bullets, total_slides, delay=0.35):
    # 12 = ppLayoutBlank
    slide = presentation.Slides.Add(index, 12)
    width = presentation.PageSetup.SlideWidth

    apply_slide_theme(slide, presentation, index, total_slides)

    add_textbox(
        slide,
        f"SLIDE {index:02d}",
        62,
        70,
        160,
        24,
        font_size=11,
        bold=True,
        color=THEME["gold"]
    )

    add_textbox(
        slide,
        title,
        62,
        102,
        width - 124,
        70,
        font_size=34,
        bold=True,
        color=THEME["text"]
    )

    # Accent line under heading
    add_shape(
        slide,
        MSO_SHAPE_RECTANGLE,
        62,
        182,
        140,
        5,
        THEME["gold"]
    )

    bullets = normalize_bullets(bullets)[:5]

    top = 218

    for bullet_index, bullet in enumerate(bullets, start=1):
        # Glass card
        add_shape(
            slide,
            MSO_SHAPE_RECTANGLE,
            72,
            top,
            width - 144,
            54,
            THEME["surface"],
            transparency=0.08
        )

        # Number block
        add_shape(
            slide,
            MSO_SHAPE_RECTANGLE,
            88,
            top + 12,
            34,
            30,
            THEME["gold"],
            transparency=0
        )

        add_textbox(
            slide,
            str(bullet_index),
            94,
            top + 17,
            22,
            18,
            font_size=12,
            bold=True,
            color=rgb(3, 7, 18),
            align=2
        )

        # Bullet text appears one by one
        add_textbox(
            slide,
            bullet,
            140,
            top + 12,
            width - 235,
            34,
            font_size=18,
            bold=False,
            color=THEME["muted"]
        )

        time.sleep(delay)
        top += 68

    return slide


def create_live_presentation(
    topic: str,
    filename: str = "Orvix_Presentation",
    slide_count: int = 6,
    location: str = "desktop",
    user_command: str = ""
):
    try:
        import win32com.client
    except Exception as error:
        return {
            "success": False,
            "message": (
                "Live PowerPoint generation needs pywin32. "
                "Run: pip install pywin32. "
                f"Error: {error}"
            )
        }

    try:
        output_folder = resolve_output_folder(location)
        output_folder.mkdir(parents=True, exist_ok=True)

        filename = clean_filename(filename)
        output_path = output_folder / filename

        slides = get_slide_content(topic, slide_count, user_command)

        print("LIVE PPT: Opening PowerPoint...")

        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = True

        presentation = powerpoint.Presentations.Add()
        presentation.PageSetup.SlideWidth = 960
        presentation.PageSetup.SlideHeight = 540

        time.sleep(0.7)

        title_slide = slides[0] if slides else {
            "title": topic,
            "bullets": ["Generated by Orvix"]
        }

        add_title_slide(
            presentation,
            title_slide.get("title", topic),
            "Generated live by Orvix with premium slide design",
            len(slides)
        )

        time.sleep(0.7)

        slide_index = 2

        for slide_data in slides[1:]:
            title = slide_data.get("title", "Untitled Slide")
            bullets = slide_data.get("bullets", [])

            print(f"LIVE PPT: Creating slide {slide_index}: {title}")

            add_content_slide(
                presentation,
                slide_index,
                title,
                bullets,
                len(slides),
                delay=0.28
            )

            slide_index += 1
            time.sleep(0.45)

        presentation.SaveAs(str(output_path))

        try:
            from app.session_memory import set_last_created_path
            set_last_created_path(str(output_path))
        except Exception:
            pass

        print("LIVE PPT: Saved:", output_path)

        return {
            "success": True,
            "message": f"Live premium PowerPoint created and saved: {output_path}",
            "path": str(output_path)
        }

    except Exception as error:
        print("LIVE PPT: Failed.")
        print("LIVE PPT ERROR:", error)

        return {
            "success": False,
            "message": f"Live PowerPoint generation failed: {error}"
        }