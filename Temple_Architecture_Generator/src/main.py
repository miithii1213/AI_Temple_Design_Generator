import math
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# ============================================================
# AI-BASED TRADITIONAL TEMPLE ARCHITECTURE GENERATOR
# Stable version: compact GUI + always-visible navigation + multiple
# South Indian temple styles
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AI-Based Traditional Temple Architecture Generator")
app.geometry("900x600")
app.resizable(False, False)

# -------------------- THEME --------------------
BG = "#F7F1E3"
PANEL = "#FFFDF7"
MAROON = "#5A1725"
MAROON2 = "#7A2438"
GOLD = "#C58A22"
GOLD2 = "#E4B44C"
CREAM = "#F3E2B8"
BROWN = "#70442C"
STONE = "#A66A42"
DARK = "#2D2020"
GREEN = "#496B4A"
WHITE = "#FFFFFF"
MUTED = "#806E64"

current_design = {}


# ============================================================
# BASIC HELPERS
# ============================================================

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()


def header(title, subtitle=""):
    # Fixed top header + navigation.  Navigation is kept at the top
    # so it remains visible on every page regardless of content size.
    bar = ctk.CTkFrame(
        app, fg_color=MAROON, corner_radius=0, height=118
    )
    bar.pack(fill="x")
    bar.pack_propagate(False)

    ctk.CTkLabel(
        bar,
        text="✦  " + title,
        font=("Georgia", 23, "bold"),
        text_color=GOLD2
    ).pack(anchor="w", padx=24, pady=(10, 0))

    if subtitle:
        ctk.CTkLabel(
            bar,
            text=subtitle,
            font=("Segoe UI", 10),
            text_color="#F5EBD7"
        ).pack(anchor="w", padx=27, pady=(0, 5))

    nav = ctk.CTkFrame(bar, fg_color="#42101B", corner_radius=8, height=40)
    nav.pack(fill="x", padx=18, pady=(2, 8))
    nav.pack_propagate(False)

    def safe_new():
        show_input_page()

    def safe_2d():
        if current_design:
            show_floor_plan()
        else:
            show_input_page()

    def safe_3d():
        if current_design:
            show_3d_view()
        else:
            show_input_page()

    def safe_ai():
        if current_design:
            show_analysis()
        else:
            show_input_page()

    def safe_gopuram():
        if current_design:
            show_gopuram()
        else:
            show_input_page()

    def safe_back():
        if current_design:
            show_result_page()
        else:
            show_dashboard()

    nav_button(
        nav, "HOME", show_dashboard, 92, "#6B2432"
    ).pack(side="left", padx=(8, 3), pady=3)
    nav_button(
        nav, "NEW DESIGN", safe_new, 118, GOLD
    ).pack(side="left", padx=3, pady=3)
    nav_button(
        nav, "2D PLAN", safe_2d, 105, "#8B5E34"
    ).pack(side="left", padx=3, pady=3)
    nav_button(
        nav, "3D TEMPLE", safe_3d, 112, "#7A2438"
    ).pack(side="left", padx=3, pady=3)
    nav_button(
        nav, "AI ANALYSIS", safe_ai, 112, GREEN
    ).pack(side="left", padx=3, pady=3)
    nav_button(
        nav, "GOPURAM", safe_gopuram, 105, BROWN
    ).pack(side="left", padx=3, pady=3)
    nav_button(
        nav, "BACK", safe_back, 88, "#8B5E34"
    ).pack(side="right", padx=(3, 8), pady=3)


def nav_button(parent, text, command, width=105, fg=MAROON):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=32,
        corner_radius=7,
        fg_color=fg,
        hover_color=MAROON2,
        text_color=WHITE,
        font=("Segoe UI", 9, "bold")
    )


def button(parent, text, command, width=180, height=38, fg=MAROON):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=height,
        corner_radius=9,
        fg_color=fg,
        hover_color=MAROON2,
        text_color=WHITE,
        font=("Segoe UI", 12, "bold")
    )


def card(parent, width=300, height=180):
    f = ctk.CTkFrame(
        parent,
        width=width,
        height=height,
        fg_color=PANEL,
        border_color="#D8C8A8",
        border_width=1,
        corner_radius=14
    )
    f.pack_propagate(False)
    return f


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():
    clear_window()
    header(
        "AI-BASED TRADITIONAL TEMPLE ARCHITECTURE GENERATOR",
        "Generate a conceptual South Indian temple from your selected architectural design."
    )

    body = ctk.CTkFrame(app, fg_color=BG)
    body.pack(fill="both", expand=True, padx=22, pady=18)

    left = card(body, 620, 480)
    left.pack(side="left", fill="y", padx=(0, 14))

    ctk.CTkLabel(
        left,
        text="DIVINE ARCHITECTURE STUDIO",
        font=("Georgia", 25, "bold"),
        text_color=MAROON
    ).pack(pady=(45, 10))

    ctk.CTkLabel(
        left,
        text="Create different South Indian temple concepts\n"
             "from plot dimensions, floors, style and entrance.",
        font=("Segoe UI", 14),
        text_color=DARK,
        justify="center"
    ).pack(pady=8)

    info = (
        "Available architectural families\n\n"
        "• Chola / Brihadisvara-inspired\n"
        "• Madurai Nayaka-inspired\n"
        "• Pandya-style Dravidian\n"
        "• Traditional South Indian\n"
        "• Kerala–Dravidian fusion\n\n"
        "Each selected style changes the 3D massing."
    )

    ctk.CTkLabel(
        left,
        text=info,
        font=("Segoe UI", 13),
        text_color=MUTED,
        justify="left"
    ).pack(pady=22)

    button(
        left,
        "CREATE NEW TEMPLE DESIGN",
        show_input_page,
        width=310,
        fg=MAROON
    ).pack(pady=12)

    right = card(body, 340, 480)
    right.pack(side="left", fill="y")

    ctk.CTkLabel(
        right,
        text="SYSTEM MODULES",
        font=("Georgia", 19, "bold"),
        text_color=MAROON
    ).pack(pady=(35, 22))

    modules = [
        ("01", "Design Input"),
        ("02", "Architecture Engine"),
        ("03", "Style Generator"),
        ("04", "2D Floor Plan"),
        ("05", "3D Temple Model"),
        ("06", "AI Design Analysis"),
    ]

    for num, name in modules:
        row = ctk.CTkFrame(right, fg_color="#F7EED8", corner_radius=9, height=48)
        row.pack(fill="x", padx=22, pady=5)
        row.pack_propagate(False)

        ctk.CTkLabel(
            row,
            text=num,
            width=42,
            font=("Segoe UI", 12, "bold"),
            text_color=GOLD
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=name,
            font=("Segoe UI", 12, "bold"),
            text_color=DARK
        ).pack(side="left")


# ============================================================
# INPUT PAGE
# ============================================================

def show_input_page():
    clear_window()
    header(
        "CREATE TEMPLE DESIGN",
        "Enter your architectural requirements"
    )

    # ------------------------------------------------------------
    # FIXED ACTION BAR
    # This is deliberately OUTSIDE the scrollable area, so the
    # Generate button can never disappear below the screen.
    # ------------------------------------------------------------
    footer = ctk.CTkFrame(
        app,
        fg_color="#FFF8EA",
        height=72,
        corner_radius=0,
        border_width=1,
        border_color="#D7B66A"
    )
    footer.pack(side="bottom", fill="x")
    footer.pack_propagate(False)

    footer_inner = ctk.CTkFrame(footer, fg_color="transparent")
    footer_inner.pack(expand=True)

    # ------------------------------------------------------------
    # SCROLLABLE FORM AREA
    # ------------------------------------------------------------
    scroll = ctk.CTkScrollableFrame(
        app,
        fg_color=BG,
        scrollbar_button_color=GOLD,
        scrollbar_button_hover_color=GOLD2,
        corner_radius=0
    )
    scroll.pack(fill="both", expand=True, padx=0, pady=0)

    panel = card(scroll, 760, 500)
    panel.pack(padx=35, pady=24)

    ctk.CTkLabel(
        panel,
        text="TEMPLE DESIGN PARAMETERS",
        font=("Georgia", 22, "bold"),
        text_color=MAROON
    ).pack(pady=(25, 18))

    form = ctk.CTkFrame(panel, fg_color="transparent")
    form.pack(fill="x", padx=85)

    ctk.CTkLabel(
        form, text="Plot Length (m)",
        font=("Segoe UI", 12, "bold"),
        text_color=DARK
    ).pack(anchor="w")

    length_entry = ctk.CTkEntry(
        form, height=38, font=("Segoe UI", 13),
        border_color="#CDBB98"
    )
    length_entry.pack(fill="x", pady=(3, 12))
    length_entry.insert(0, "60")

    ctk.CTkLabel(
        form, text="Plot Width (m)",
        font=("Segoe UI", 12, "bold"),
        text_color=DARK
    ).pack(anchor="w")

    width_entry = ctk.CTkEntry(
        form, height=38, font=("Segoe UI", 13),
        border_color="#CDBB98"
    )
    width_entry.pack(fill="x", pady=(3, 12))
    width_entry.insert(0, "40")

    ctk.CTkLabel(
        form, text="Number of Floors",
        font=("Segoe UI", 12, "bold"),
        text_color=DARK
    ).pack(anchor="w")

    floors_entry = ctk.CTkEntry(
        form, height=38, font=("Segoe UI", 13),
        border_color="#CDBB98"
    )
    floors_entry.pack(fill="x", pady=(3, 12))
    floors_entry.insert(0, "2")

    ctk.CTkLabel(
        form, text="Temple Style",
        font=("Segoe UI", 12, "bold"),
        text_color=DARK
    ).pack(anchor="w")

    style_box = ctk.CTkComboBox(
        form,
        values=[
            "Chola / Brihadisvara Style",
            "Madurai Nayaka Style",
            "Pandya Dravidian Style",
            "Traditional South Indian",
            "Kerala-Dravidian Fusion"
        ],
        height=38,
        font=("Segoe UI", 12),
        button_color=MAROON,
        border_color="#CDBB98",
        dropdown_fg_color=PANEL
    )
    style_box.pack(fill="x", pady=(3, 12))
    style_box.set("Chola / Brihadisvara Style")

    ctk.CTkLabel(
        form, text="Main Entrance Direction",
        font=("Segoe UI", 12, "bold"),
        text_color=DARK
    ).pack(anchor="w")

    direction_box = ctk.CTkComboBox(
        form,
        values=["East", "West", "North", "South"],
        height=38,
        font=("Segoe UI", 12),
        button_color=MAROON,
        border_color="#CDBB98",
        dropdown_fg_color=PANEL
    )
    direction_box.pack(fill="x", pady=(3, 16))
    direction_box.set("East")

    # ------------------------------------------------------------
    # FIXED BUTTONS
    # ------------------------------------------------------------
    button(
        footer_inner,
        "GENERATE TEMPLE",
        lambda: generate_design(
            length_entry.get(),
            width_entry.get(),
            floors_entry.get(),
            style_box.get(),
            direction_box.get()
        ),
        width=230,
        height=44,
        fg=MAROON
    ).pack(side="left", padx=8)

    button(
        footer_inner,
        "BACK",
        show_dashboard,
        width=130,
        height=44,
        fg=GOLD
    ).pack(side="left", padx=8)

# ============================================================
# DESIGN LOGIC
# ============================================================

def generate_design(length, width, floors, style, direction):
    try:
        length = float(length)
        width = float(width)
        floors = int(floors)

        if length <= 0 or width <= 0 or floors <= 0:
            raise ValueError

        if floors > 8:
            messagebox.showwarning(
                "Input Limit",
                "For this academic 3D generator, use 1 to 8 floors."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter positive numeric values for length, width and floors."
        )
        return

    area = length * width

    current_design.clear()
    current_design.update({
        "length": length,
        "width": width,
        "floors": floors,
        "style": style,
        "direction": direction,
        "area": area
    })

    show_result_page()


# ============================================================
# RESULT PAGE
# ============================================================

def show_result_page():
    clear_window()
    header(
        "TEMPLE DESIGN GENERATED",
        "Your selected parameters have been converted into an architectural concept."
    )

    body = ctk.CTkFrame(app, fg_color=BG)
    body.pack(fill="both", expand=True, padx=22, pady=18)

    left = card(body, 590, 495)
    left.pack(side="left", fill="y", padx=(0, 14))

    ctk.CTkLabel(
        left,
        text="DESIGN SUMMARY",
        font=("Georgia", 21, "bold"),
        text_color=MAROON
    ).pack(pady=(28, 18))

    d = current_design

    rows = [
        ("Plot", f'{d["length"]:.1f} m × {d["width"]:.1f} m'),
        ("Area", f'{d["area"]:.1f} m²'),
        ("Floors", str(d["floors"])),
        ("Style", d["style"]),
        ("Entrance", d["direction"])
    ]

    for label, value in rows:
        r = ctk.CTkFrame(left, fg_color="#F8F0DF", corner_radius=8, height=47)
        r.pack(fill="x", padx=38, pady=5)
        r.pack_propagate(False)

        ctk.CTkLabel(
            r,
            text=label,
            width=105,
            anchor="w",
            font=("Segoe UI", 12, "bold"),
            text_color=MAROON
        ).pack(side="left", padx=12)

        ctk.CTkLabel(
            r,
            text=value,
            anchor="w",
            font=("Segoe UI", 12),
            text_color=DARK
        ).pack(side="left")

    ctk.CTkLabel(
        left,
        text="3D STYLE",
        font=("Georgia", 17, "bold"),
        text_color=MAROON
    ).pack(pady=(22, 8))

    style_note = get_style_description(d["style"])

    ctk.CTkLabel(
        left,
        text=style_note,
        font=("Segoe UI", 12),
        text_color=MUTED,
        justify="left",
        wraplength=480
    ).pack(padx=40)

    right = card(body, 370, 495)
    right.pack(side="left", fill="y")

    ctk.CTkLabel(
        right,
        text="OPEN DESIGN VIEWS",
        font=("Georgia", 20, "bold"),
        text_color=MAROON
    ).pack(pady=(30, 18))

    button(
        right,
        "REALISTIC 3D TEMPLE",
        show_3d_view,
        width=280,
        fg=MAROON
    ).pack(pady=8)

    button(
        right,
        "2D FLOOR PLAN",
        show_floor_plan,
        width=280,
        fg=GOLD
    ).pack(pady=8)

    button(
        right,
        "AI DESIGN ANALYSIS",
        show_analysis,
        width=280,
        fg=GREEN
    ).pack(pady=8)

    button(
        right,
        "DETAILED GOPURAM",
        show_gopuram,
        width=280,
        fg=BROWN
    ).pack(pady=8)

    button(
        right,
        "NEW DESIGN",
        show_input_page,
        width=280,
        fg=MAROON2
    ).pack(pady=(22, 8))


def get_style_description(style):
    descriptions = {
        "Chola / Brihadisvara Style":
            "Tall pyramidal vimana, strong stone-like base, layered cornices, "
            "central sanctum and a restrained monumental composition.",
        "Madurai Nayaka Style":
            "Prominent gateway tower, decorative tiering, mandapam emphasis, "
            "multiple shrine forms and richer ornamental massing.",
        "Pandya Dravidian Style":
            "Compact stepped vimana, strong gateway, layered base mouldings "
            "and balanced courtyard composition.",
        "Traditional South Indian":
            "Balanced gopuram, mandapam, sanctum, courtyard, side shrines "
            "and traditional temple-axis planning.",
        "Kerala-Dravidian Fusion":
            "Lower stepped massing, broader roof forms, timber-inspired layers "
            "and a South Indian courtyard arrangement."
    }
    return descriptions.get(style, descriptions["Traditional South Indian"])


# ============================================================
# 3D GEOMETRY HELPERS
# ============================================================

def add_box(ax, x, y, z, sx, sy, sz, color=STONE, alpha=1.0):
    x0, x1 = x - sx / 2, x + sx / 2
    y0, y1 = y - sy / 2, y + sy / 2
    z0, z1 = z, z + sz

    vertices = [
        (x0, y0, z0), (x1, y0, z0),
        (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1),
        (x1, y1, z1), (x0, y1, z1)
    ]

    faces = [
        [vertices[i] for i in [0, 1, 2, 3]],
        [vertices[i] for i in [4, 5, 6, 7]],
        [vertices[i] for i in [0, 1, 5, 4]],
        [vertices[i] for i in [1, 2, 6, 5]],
        [vertices[i] for i in [2, 3, 7, 6]],
        [vertices[i] for i in [3, 0, 4, 7]]
    ]

    poly = Poly3DCollection(
        faces,
        facecolors=color,
        edgecolors="#5A3928",
        linewidths=0.55,
        alpha=alpha
    )
    ax.add_collection3d(poly)


def add_pyramid(ax, x, y, z, base_x, base_y, height,
                color=STONE, top_size=0.0):
    bx0 = x - base_x / 2
    bx1 = x + base_x / 2
    by0 = y - base_y / 2
    by1 = y + base_y / 2

    tx0 = x - top_size / 2
    tx1 = x + top_size / 2
    ty0 = y - top_size / 2
    ty1 = y + top_size / 2

    bottom = [
        (bx0, by0, z),
        (bx1, by0, z),
        (bx1, by1, z),
        (bx0, by1, z)
    ]

    top = [
        (tx0, ty0, z + height),
        (tx1, ty0, z + height),
        (tx1, ty1, z + height),
        (tx0, ty1, z + height)
    ]

    faces = [
        bottom,
        top,
        [bottom[0], bottom[1], top[1], top[0]],
        [bottom[1], bottom[2], top[2], top[1]],
        [bottom[2], bottom[3], top[3], top[2]],
        [bottom[3], bottom[0], top[0], top[3]]
    ]

    poly = Poly3DCollection(
        faces,
        facecolors=color,
        edgecolors="#5A3928",
        linewidths=0.55,
        alpha=1.0
    )
    ax.add_collection3d(poly)


def add_cylinder(ax, x, y, z, radius, height, color=BROWN,
                 segments=16):
    verts = []
    bottom = []
    top = []

    for i in range(segments):
        a = 2 * math.pi * i / segments
        px = x + radius * math.cos(a)
        py = y + radius * math.sin(a)
        bottom.append((px, py, z))
        top.append((px, py, z + height))

    verts.append(bottom)
    verts.append(top)

    for i in range(segments):
        j = (i + 1) % segments
        verts.append([
            bottom[i], bottom[j], top[j], top[i]
        ])

    poly = Poly3DCollection(
        verts,
        facecolors=color,
        edgecolors="#4D3326",
        linewidths=0.45
    )
    ax.add_collection3d(poly)


def add_pillar(ax, x, y, z, h=4.0, radius=0.55):
    add_cylinder(ax, x, y, z, radius, h, BROWN, 12)
    add_box(ax, x, y, z + h, radius * 1.8, radius * 1.8, 0.35, GOLD)


def add_steps(ax, x, y, z, width, depth, count=4):
    for i in range(count):
        add_box(
            ax,
            x,
            y + i * 0.9,
            z + i * 0.28,
            width - i * 0.7,
            0.9,
            0.28,
            BROWN
        )


def add_kalasam(ax, x, y, z, scale=1.0):
    add_cylinder(ax, x, y, z, 0.35 * scale, 0.65 * scale, GOLD, 14)
    add_cylinder(ax, x, y, z + 0.65 * scale,
                 0.22 * scale, 0.38 * scale, GOLD2, 14)
    add_pyramid(
        ax, x, y, z + 1.03 * scale,
        0.65 * scale, 0.65 * scale,
        0.45 * scale,
        GOLD2,
        0.08 * scale
    )


def add_decorative_band(ax, x, y, z, sx, sy):
    add_box(ax, x, y, z, sx, sy, 0.32, GOLD)


def add_arch_niches(ax, x, y, z, width, count=4):
    gap = width / count
    for i in range(count):
        px = x - width / 2 + gap / 2 + i * gap
        add_box(
            ax, px, y, z,
            gap * 0.52, 0.35, 1.5,
            "#8B5739"
        )
        add_pyramid(
            ax, px, y, z + 1.5,
            gap * 0.55, 0.42, 0.65,
            GOLD, 0.05
        )


def add_idol(ax, x, y, z, scale=1.0):
    # Stylized conceptual sanctum idol; not an exact deity replica.
    add_cylinder(ax, x, y, z, 0.38 * scale, 0.25 * scale, GOLD, 12)
    add_cylinder(ax, x, y, z + 0.25 * scale,
                 0.22 * scale, 1.0 * scale, GOLD2, 12)

    # Head
    add_cylinder(ax, x, y, z + 1.25 * scale,
                 0.28 * scale, 0.35 * scale, GOLD2, 12)

    # Halo/back plate
    add_cylinder(ax, x, y - 0.05 * scale,
                 z + 1.0 * scale,
                 0.62 * scale, 0.12 * scale,
                 "#D39A27", 16)


# ============================================================
# 3D TEMPLE STYLE BUILDERS
# ============================================================

def build_common_courtyard(ax, L, W):
    # Ground
    add_box(ax, 0, 0, 0, L * 0.92, W * 0.92, 0.55, "#B99A73")

    # Prakara / compound wall
    wall_h = 2.6
    add_box(ax, 0, W * 0.40, 0.55, L * 0.82, 1.0, wall_h, "#8D684A")
    add_box(ax, 0, -W * 0.40, 0.55, L * 0.82, 1.0, wall_h, "#8D684A")
    add_box(ax, -L * 0.40, 0, 0.55, 1.0, W * 0.80, wall_h, "#8D684A")
    add_box(ax, L * 0.40, 0, 0.55, 1.0, W * 0.80, wall_h, "#8D684A")


def build_chola(ax, L, W, floors):
    # Strong stepped platform
    add_box(ax, 0, 0, 0.55, L * 0.62, W * 0.60, 1.0, BROWN)
    add_box(ax, 0, 0, 1.55, L * 0.56, W * 0.54, 0.7, STONE)

    # Sanctum body
    body_h = 5.5 + floors * 0.65
    add_box(ax, 0, 0, 2.25, L * 0.42, W * 0.40, body_h, "#9A5F3A")
    add_decorative_band(ax, 0, 0, 2.8, L * 0.45, W * 0.43)
    add_decorative_band(ax, 0, 0, body_h + 2.0, L * 0.45, W * 0.43)

    add_arch_niches(ax, 0, -W * 0.205, 3.2, L * 0.38, 5)
    add_arch_niches(ax, 0, W * 0.205, 3.2, L * 0.38, 5)

    # Mandapam
    add_box(ax, 0, -W * 0.25, 2.25, L * 0.50, W * 0.22, 2.6, "#8E593A")
    for px in [-L * 0.19, -L * 0.065, L * 0.065, L * 0.19]:
        add_pillar(ax, px, -W * 0.25, 2.25, 2.6, 0.38)

    # Tall pyramidal vimana
    levels = 8 + min(floors, 4)
    base = min(L, W) * 0.43
    z = body_h + 2.25

    for i in range(levels):
        frac = 1 - i / (levels + 1)
        sx = base * frac + base * 0.12
        sy = base * 0.82 * frac + base * 0.10
        h = 1.15 if i < 5 else 0.9
        add_pyramid(
            ax, 0, 0, z,
            sx, sy, h,
            "#A66A42" if i % 2 == 0 else "#B8794D",
            sx * 0.72
        )
        z += h

    add_box(ax, 0, 0, z, base * 0.42, base * 0.36, 0.7, GOLD)
    add_kalasam(ax, 0, 0, z + 0.7, 1.15)

    # Front entrance
    add_steps(ax, 0, -W * 0.47, 0.55, L * 0.22, 2.8, 5)

    # Side shrines
    for sx in [-L * 0.30, L * 0.30]:
        add_box(ax, sx, 0, 1.0, L * 0.15, W * 0.20, 2.8, "#8B593D")
        add_pyramid(ax, sx, 0, 3.8, L * 0.17, W * 0.21, 2.0, STONE, 0.05)
        add_kalasam(ax, sx, 0, 5.8, 0.55)

    # Nandi / vehicle platform
    add_box(ax, 0, -W * 0.33, 0.55, L * 0.12, W * 0.12, 0.45, GOLD)
    add_box(ax, 0, -W * 0.33, 1.0, L * 0.08, W * 0.09, 0.6, BROWN)


def build_nayaka(ax, L, W, floors):
    # Large mandapam
    add_box(ax, 0, 0, 0.55, L * 0.65, W * 0.62, 0.9, BROWN)
    add_box(ax, 0, 0, 1.45, L * 0.58, W * 0.55, 0.55, STONE)

    # Pillared hall
    hall_h = 4.0 + floors * 0.5
    add_box(ax, 0, 0.05, 2.0, L * 0.56, W * 0.44, hall_h, "#9A5F3B")

    for px in [-L * 0.23, -L * 0.115, 0, L * 0.115, L * 0.23]:
        for py in [-W * 0.20, W * 0.20]:
            add_pillar(ax, px, py, 2.0, hall_h, 0.35)

    # Central shrine
    add_box(ax, 0, W * 0.10, 2.0, L * 0.30, W * 0.25, 4.0, "#875236")
    add_decorative_band(ax, 0, W * 0.10, 2.5, L * 0.33, W * 0.28)

    # Medium vimana
    z = 6.0
    for i in range(6):
        frac = 1 - i / 7
        add_pyramid(
            ax, 0, W * 0.10, z,
            L * 0.32 * frac + 1.5,
            W * 0.27 * frac + 1.0,
            0.95,
            "#A96A43" if i % 2 else "#B8784A",
            0.4
        )
        z += 0.95
    add_kalasam(ax, 0, W * 0.10, z, 0.9)

    # Tall ornate entrance gopuram
    gx, gy = 0, -W * 0.39
    add_box(ax, gx, gy, 0.55, L * 0.27, W * 0.13, 3.2, "#805039")

    gz = 3.75
    for i in range(7):
        frac = 1 - i / 8
        sx = L * 0.28 * frac + 2.0
        sy = W * 0.15 * frac + 0.7
        add_pyramid(ax, gx, gy, gz, sx, sy, 1.0, STONE, 0.2)
        gz += 1.0
    add_kalasam(ax, gx, gy, gz, 1.0)

    # Side towers
    for sx in [-L * 0.31, L * 0.31]:
        add_box(ax, sx, -W * 0.03, 0.55, L * 0.12, W * 0.16, 2.8, "#89563A")
        add_pyramid(ax, sx, -W * 0.03, 3.35, L * 0.14, W * 0.18, 1.9, STONE)
        add_kalasam(ax, sx, -W * 0.03, 5.25, 0.55)

    # Nandi
    add_box(ax, 0, -W * 0.25, 0.55, L * 0.10, W * 0.10, 0.5, GOLD)


def build_pandya(ax, L, W, floors):
    # Broad stepped base
    for i, mult in enumerate([0.68, 0.60, 0.53]):
        add_box(
            ax, 0, 0, 0.5 + i * 0.65,
            L * mult, W * mult, 0.65,
            BROWN if i == 0 else STONE
        )

    # Compact sanctum
    body_h = 5.0 + floors * 0.45
    add_box(ax, 0, 0, 2.45, L * 0.40, W * 0.38, body_h, "#965C3A")

    for side in [-1, 1]:
        add_arch_niches(
            ax, 0, side * W * 0.195,
            3.0, L * 0.34, 4
        )

    # Stepped vimana
    z = body_h + 2.45
    levels = 7
    for i in range(levels):
        frac = 1 - i / 8
        add_box(
            ax, 0, 0, z,
            L * 0.44 * frac,
            W * 0.40 * frac,
            0.85,
            "#A36A43" if i % 2 == 0 else "#B8784B"
        )
        add_pyramid(
            ax, 0, 0, z + 0.85,
            L * 0.44 * frac,
            W * 0.40 * frac,
            0.55,
            GOLD,
            0.12
        )
        z += 1.4

    add_kalasam(ax, 0, 0, z, 0.9)

    # Gateway
    gy = -W * 0.40
    add_box(ax, 0, gy, 0.55, L * 0.25, W * 0.14, 2.8, "#805138")

    for i in range(5):
        frac = 1 - i / 6
        add_pyramid(
            ax, 0, gy, 3.4 + i * 0.95,
            L * (0.27 * frac + 0.04),
            W * (0.15 * frac + 0.03),
            0.9,
            STONE,
            0.1
        )
    add_kalasam(ax, 0, gy, 8.15, 0.75)

    # Side sanctums
    for sx in [-L * 0.29, L * 0.29]:
        add_box(ax, sx, 0, 0.55, L * 0.13, W * 0.18, 2.4, "#8B593D")
        add_pyramid(ax, sx, 0, 2.95, L * 0.15, W * 0.19, 1.8, STONE)
        add_kalasam(ax, sx, 0, 4.75, 0.5)


def build_traditional(ax, L, W, floors):
    # Balanced central composition
    add_box(ax, 0, 0, 0.55, L * 0.64, W * 0.58, 0.9, BROWN)
    add_box(ax, 0, 0, 1.45, L * 0.55, W * 0.49, 0.6, STONE)

    # Mandapam
    add_box(ax, 0, -W * 0.18, 2.05, L * 0.47, W * 0.25, 3.1, "#925B3B")
    for px in [-L * 0.17, 0, L * 0.17]:
        add_pillar(ax, px, -W * 0.28, 2.05, 3.1, 0.38)

    # Sanctum
    add_box(ax, 0, W * 0.09, 2.05, L * 0.34, W * 0.30, 4.1, "#9D623D")

    # Vimana
    z = 6.15
    for i in range(7 + min(floors, 3)):
        frac = 1 - i / 9
        add_pyramid(
            ax, 0, W * 0.09, z,
            L * 0.38 * frac + 1.0,
            W * 0.34 * frac + 0.8,
            0.9,
            "#A56B43",
            0.25
        )
        z += 0.9

    add_kalasam(ax, 0, W * 0.09, z, 0.85)

    # Front gopuram
    gy = -W * 0.40
    add_box(ax, 0, gy, 0.55, L * 0.24, W * 0.14, 2.8, "#815139")

    for i in range(6):
        frac = 1 - i / 7
        add_pyramid(
            ax, 0, gy, 3.35 + i * 0.9,
            L * (0.27 * frac + 0.04),
            W * (0.15 * frac + 0.03),
            0.8,
            STONE,
            0.1
        )

    add_kalasam(ax, 0, gy, 8.75, 0.8)

    # Corner shrines
    for sx in [-L * 0.30, L * 0.30]:
        add_box(ax, sx, W * 0.20, 0.55, L * 0.12, W * 0.13, 2.4, "#8D593C")
        add_pyramid(ax, sx, W * 0.20, 2.95, L * 0.14, W * 0.15, 1.6, STONE)
        add_kalasam(ax, sx, W * 0.20, 4.55, 0.45)


def build_kerala(ax, L, W, floors):
    # Lower, broader architecture
    add_box(ax, 0, 0, 0.55, L * 0.67, W * 0.61, 0.9, BROWN)
    add_box(ax, 0, 0, 1.45, L * 0.57, W * 0.52, 0.55, STONE)

    # Main timber-inspired body
    add_box(ax, 0, 0.04, 2.0, L * 0.45, W * 0.42, 3.5 + floors * 0.35, "#815338")

    # Broad layered roof
    z = 5.7 + floors * 0.35
    for i in range(4):
        mult = 1 - i * 0.18
        add_pyramid(
            ax, 0, 0.04, z,
            L * 0.53 * mult,
            W * 0.48 * mult,
            0.85,
            "#7D4B33" if i % 2 == 0 else "#9A6141",
            L * 0.34 * mult
        )
        z += 0.85

    add_kalasam(ax, 0, 0.04, z, 0.65)

    # Courtyard hall
    add_box(ax, 0, -W * 0.27, 2.0, L * 0.48, W * 0.16, 2.5, "#8D593C")
    for px in [-L * 0.18, -L * 0.06, L * 0.06, L * 0.18]:
        add_pillar(ax, px, -W * 0.27, 2.0, 2.5, 0.32)

    # Compact entrance tower
    gy = -W * 0.41
    add_box(ax, 0, gy, 0.55, L * 0.20, W * 0.13, 2.6, "#805037")
    for i in range(4):
        mult = 1 - i * 0.20
        add_pyramid(
            ax, 0, gy, 3.1 + i * 0.75,
            L * 0.23 * mult,
            W * 0.15 * mult,
            0.7,
            STONE,
            0.1
        )
    add_kalasam(ax, 0, gy, 6.2, 0.55)


def build_temple(ax, style, L, W, floors):
    build_common_courtyard(ax, L, W)

    if style == "Chola / Brihadisvara Style":
        build_chola(ax, L, W, floors)
    elif style == "Madurai Nayaka Style":
        build_nayaka(ax, L, W, floors)
    elif style == "Pandya Dravidian Style":
        build_pandya(ax, L, W, floors)
    elif style == "Kerala-Dravidian Fusion":
        build_kerala(ax, L, W, floors)
    else:
        build_traditional(ax, L, W, floors)

    # Flagstaff and Balipeetham in front courtyard
    add_box(ax, 0, -W * 0.30, 0.55, L * 0.06, W * 0.06, 0.45, GOLD)
    add_cylinder(ax, 0, -W * 0.30, 1.0, 0.13, 4.2, GOLD2, 12)

    # Flag
    add_box(
        ax,
        0.7,
        -W * 0.30,
        4.5,
        1.3,
        0.05,
        0.7,
        MAROON
    )

    # Conceptual idol visible inside front-open sanctum area
    add_idol(ax, 0, W * 0.25, 2.5, 1.1)


# ============================================================
# 3D VIEW PAGE
# ============================================================

def show_3d_view():
    """Stable 3D page with a guaranteed visible footer navigation bar."""
    clear_window()

    header(
        "REALISTIC 3D TEMPLE",
        "Interactive conceptual South Indian temple generated from your selected style"
    )

    # --------------------------------------------------------
    # IMPORTANT: Create the footer BEFORE the expandable body.
    # This reserves its height, so buttons can never be pushed
    # below the window by the 3D canvas.
    # --------------------------------------------------------
    # --------------------------------------------------------
    # Body. Because footer already reserved its space, this
    # expandable frame always stays inside the visible window.
    # --------------------------------------------------------
    body = ctk.CTkFrame(app, fg_color=BG, corner_radius=0)
    body.pack(fill="both", expand=True, padx=12, pady=(10, 8))

    model_card = ctk.CTkFrame(
        body,
        fg_color=PANEL,
        border_color="#D8C8A8",
        border_width=1,
        corner_radius=14
    )
    model_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

    info_card = ctk.CTkFrame(
        body,
        fg_color=PANEL,
        border_color="#D8C8A8",
        border_width=1,
        corner_radius=14,
        width=275
    )
    info_card.pack(side="right", fill="y")
    info_card.pack_propagate(False)

    # --------------------------------------------------------
    # 3D MODEL
    # --------------------------------------------------------
    fig = plt.Figure(figsize=(6.8, 5.0), dpi=100)
    ax = fig.add_subplot(111, projection="3d")

    d = current_design
    L = max(40.0, float(d["length"]))
    W = max(30.0, float(d["width"]))

    build_temple(ax, d["style"], L, W, int(d["floors"]))

    # Tighter camera framing so the temple is large and clearly visible.
    horizontal = max(L, W) * 0.43
    ax.set_xlim(-horizontal, horizontal)
    ax.set_ylim(-horizontal, horizontal)

    if "Chola" in d["style"]:
        max_z = 30
    elif "Madurai" in d["style"]:
        max_z = 24
    elif "Pandya" in d["style"]:
        max_z = 22
    elif "Kerala" in d["style"]:
        max_z = 18
    else:
        max_z = 23

    ax.set_zlim(0, max_z)
    ax.set_box_aspect((1.15, 1.0, 0.82))
    ax.view_init(elev=22, azim=-55)
    ax.set_axis_off()
    ax.set_facecolor("#FFFDF7")
    fig.patch.set_facecolor("#FFFDF7")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)

    canvas = FigureCanvasTkAgg(fig, master=model_card)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    # Click the model to rotate a little.
    def rotate(event):
        if event.inaxes == ax:
            ax.view_init(elev=ax.elev, azim=ax.azim + 10)
            canvas.draw_idle()

    canvas.mpl_connect("button_press_event", rotate)

    # --------------------------------------------------------
    # INFORMATION CARD
    # --------------------------------------------------------
    ctk.CTkLabel(
        info_card,
        text="TEMPLE MODEL",
        font=("Georgia", 18, "bold"),
        text_color=MAROON
    ).pack(pady=(18, 10))

    details = [
        ("STYLE", d["style"]),
        ("PLOT", f'{d["length"]:.0f} × {d["width"]:.0f} m'),
        ("FLOORS", str(d["floors"])),
        ("ENTRANCE", d["direction"]),
        ("AREA", f'{d["area"]:.0f} m²')
    ]

    for label, value in details:
        ctk.CTkLabel(
            info_card,
            text=label,
            font=("Segoe UI", 9, "bold"),
            text_color=GOLD
        ).pack(anchor="w", padx=16, pady=(3, 0))
        ctk.CTkLabel(
            info_card,
            text=value,
            font=("Segoe UI", 10),
            text_color=DARK,
            wraplength=240,
            justify="left"
        ).pack(anchor="w", padx=16, pady=(0, 3))

    ctk.CTkLabel(
        info_card,
        text="3D COMPONENTS",
        font=("Georgia", 14, "bold"),
        text_color=MAROON
    ).pack(anchor="w", padx=16, pady=(8, 3))

    ctk.CTkLabel(
        info_card,
        text="• Gopuram\n"
             "• Vimana / Shikhara\n"
             "• Mandapam\n"
             "• Pillars\n"
             "• Prakara walls\n"
             "• Nandi / Balipeetham\n"
             "• Flagstaff\n"
             "• Conceptual sanctum idol",
        font=("Segoe UI", 9),
        text_color=MUTED,
        justify="left"
    ).pack(anchor="w", padx=16)

    ctk.CTkLabel(
        info_card,
        text="Click the 3D model to rotate the view.",
        font=("Segoe UI", 9),
        text_color=MUTED,
        wraplength=235,
        justify="left"
    ).pack(anchor="w", padx=16, pady=(8, 0))

# ============================================================
# DETAILED GOPURAM
# ============================================================

def show_gopuram():
    clear_window()

    header(
        "DETAILED GOPURAM",
        "Five-to-seven tier South Indian gateway tower concept"
    )

    container = ctk.CTkFrame(app, fg_color=BG)
    container.pack(fill="both", expand=True, padx=14, pady=12)

    visual = ctk.CTkFrame(
        container,
        fg_color=PANEL,
        border_color="#D8C8A8",
        border_width=1,
        corner_radius=14,
        width=700,
        height=510
    )
    visual.pack(side="left", fill="both", expand=True, padx=(0, 10))
    visual.pack_propagate(False)

    fig = plt.Figure(figsize=(7.0, 4.8), dpi=100)
    ax = fig.add_subplot(111, projection="3d")

    d = current_design
    L = max(40, d["length"])
    W = max(30, d["width"])

    gx = 0
    gy = 0

    add_box(ax, gx, gy, 0, L * 0.35, W * 0.26, 1.2, BROWN)

    # Gateway opening frame
    add_box(ax, gx - L * 0.10, gy, 1.2, L * 0.05, W * 0.30, 3.6, "#75472F")
    add_box(ax, gx + L * 0.10, gy, 1.2, L * 0.05, W * 0.30, 3.6, "#75472F")
    add_box(ax, gx, gy, 4.8, L * 0.27, W * 0.30, 0.45, GOLD)

    tiers = 6 if "Madurai" in d["style"] else 5

    z = 5.2
    for i in range(tiers):
        frac = 1 - i / (tiers + 1)
        sx = L * (0.31 * frac + 0.035)
        sy = W * (0.25 * frac + 0.025)

        add_box(
            ax,
            gx,
            gy,
            z,
            sx,
            sy,
            0.55,
            GOLD if i % 2 == 0 else STONE
        )

        add_pyramid(
            ax,
            gx,
            gy,
            z + 0.55,
            sx,
            sy,
            1.15 if i < 4 else 0.9,
            "#9B623F" if i % 2 == 0 else "#B7794D",
            sx * 0.62
        )

        # miniature corner shrine forms
        for sx_pos in [-sx * 0.36, sx * 0.36]:
            add_box(
                ax,
                sx_pos,
                gy,
                z + 0.55,
                max(1.0, sx * 0.08),
                max(0.9, sy * 0.22),
                0.9,
                "#875437"
            )
            add_pyramid(
                ax,
                sx_pos,
                gy,
                z + 1.45,
                max(1.2, sx * 0.10),
                max(1.0, sy * 0.24),
                0.65,
                GOLD
            )

        z += 1.75

    add_box(ax, gx, gy, z, L * 0.18, W * 0.16, 0.65, GOLD)
    add_kalasam(ax, gx, gy, z + 0.65, 1.1)

    ax.set_xlim(-L * 0.32, L * 0.32)
    ax.set_ylim(-W * 0.32, W * 0.32)
    ax.set_zlim(0, z + 3)
    ax.set_box_aspect((1, 0.8, 1.3))
    ax.view_init(elev=20, azim=-55)
    ax.set_axis_off()

    fig.patch.set_facecolor("#FFFDF7")
    ax.set_facecolor("#FFFDF7")
    fig.tight_layout(pad=0.4)

    canvas = FigureCanvasTkAgg(fig, master=visual)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    info = ctk.CTkFrame(
        container,
        fg_color=PANEL,
        border_color="#D8C8A8",
        border_width=1,
        corner_radius=14,
        width=285,
        height=510
    )
    info.pack(side="right", fill="y")
    info.pack_propagate(False)

    ctk.CTkLabel(
        info,
        text="GOPURAM DETAILS",
        font=("Georgia", 19, "bold"),
        text_color=MAROON
    ).pack(pady=(25, 15))

    details = (
        "Gateway Type\n"
        "South Indian Dravidian\n\n"
        "Tiers\n"
        f"{tiers} stepped levels\n\n"
        "Features\n"
        "• Tiered cornices\n"
        "• Miniature shrine forms\n"
        "• Gateway pillars\n"
        "• Crown pavilion\n"
        "• Kalasam"
    )

    ctk.CTkLabel(
        info,
        text=details,
        font=("Segoe UI", 11),
        text_color=DARK,
        justify="left"
    ).pack(anchor="w", padx=22)


# ============================================================
# START
# ============================================================

show_dashboard()
app.mainloop()
