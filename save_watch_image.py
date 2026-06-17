"""
Save the watch image shared by the user into frontend/public/watch-chronograph.png
The image is a line-art chronograph watch face on white background.
We'll create it as an SVG and save a copy as PNG via Pillow.
"""
import base64, os

# SVG of a chronograph watch face — matches the outline style in the user's image
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <rect width="400" height="400" fill="white"/>
  <!-- Main outer bezel -->
  <circle cx="195" cy="200" r="170" fill="none" stroke="#888" stroke-width="2.5"/>
  <!-- Bezel tick marks -->
  <g stroke="#888" stroke-width="1.5">
    <line x1="195" y1="32" x2="195" y2="48"/>
    <line x1="195" y1="352" x2="195" y2="368"/>
    <line x1="27" y1="200" x2="43" y2="200"/>
    <line x1="347" y1="200" x2="363" y2="200"/>
  </g>
  <!-- Tick marks around bezel (60 ticks) -->
  <g stroke="#999" stroke-width="1">
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(6 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(12 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(18 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(24 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(30 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(36 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(42 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(48 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(54 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(60 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(66 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(72 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(78 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(84 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(90 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(96 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(102 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(108 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(114 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(120 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(126 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(132 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(138 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(144 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(150 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(156 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(162 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(168 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(174 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(180 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(186 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(192 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(198 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(204 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(210 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(216 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(222 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(228 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(234 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(240 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(246 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(252 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(258 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(264 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(270 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(276 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(282 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(288 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(294 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(300 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(306 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(312 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(318 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(324 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="45" transform="rotate(330 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(336 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(342 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(348 195 200)"/>
    <line x1="195" y1="33" x2="195" y2="42" transform="rotate(354 195 200)"/>
  </g>
  <!-- Hour markers (diamonds/rectangles) -->
  <g fill="none" stroke="#888" stroke-width="1.5">
    <rect x="190" y="48" width="10" height="16" rx="1"/>
    <rect x="190" y="336" width="10" height="16" rx="1"/>
    <rect x="46" y="194" width="16" height="12" rx="1"/>
    <rect x="328" y="194" width="16" height="12" rx="1"/>
    <!-- Diamond markers at 1,2,4,5,7,8,10,11 o'clock -->
    <polygon points="239,70 243,78 239,86 235,78" />
    <polygon points="282,100 288,104 282,114 276,104" />
    <polygon points="66,148 74,152 66,160 58,152" />
    <polygon points="66,240 74,244 66,252 58,244" />
    <polygon points="282,286 288,296 282,300 276,296" />
    <polygon points="239,314 243,322 239,330 235,322" />
    <polygon points="151,70 155,78 151,86 147,78" />
    <polygon points="108,100 114,104 108,114 102,104" />
  </g>
  <!-- Main dial face -->
  <circle cx="195" cy="200" r="148" fill="white" stroke="#aaa" stroke-width="1"/>
  <!-- Crown / pusher buttons -->
  <rect x="360" y="165" width="28" height="20" rx="4" fill="none" stroke="#888" stroke-width="1.5"/>
  <rect x="360" y="215" width="24" height="18" rx="4" fill="none" stroke="#888" stroke-width="1.5"/>
  <rect x="364" y="192" width="32" height="16" rx="5" fill="none" stroke="#888" stroke-width="2"/>
  <line x1="364" y1="196" x2="396" y2="196" stroke="#888" stroke-width="1"/>
  <line x1="364" y1="200" x2="396" y2="200" stroke="#888" stroke-width="1"/>
  <line x1="364" y1="204" x2="396" y2="204" stroke="#888" stroke-width="1"/>
  <!-- Sub-dial LEFT (9 o'clock position) - 30min counter -->
  <circle cx="135" cy="200" r="42" fill="white" stroke="#aaa" stroke-width="1.2"/>
  <circle cx="135" cy="200" r="36" fill="none" stroke="#ccc" stroke-width="0.8"/>
  <!-- Sub-dial tick marks -->
  <g stroke="#bbb" stroke-width="1">
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(0 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(30 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(60 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(90 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(120 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(150 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(180 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(210 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(240 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(270 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(300 135 200)"/>
    <line x1="135" y1="159" x2="135" y2="165" transform="rotate(330 135 200)"/>
  </g>
  <!-- Sub-dial hands left -->
  <line x1="135" y1="200" x2="135" y2="168" stroke="#999" stroke-width="2" stroke-linecap="round"/>
  <line x1="135" y1="200" x2="120" y2="210" stroke="#999" stroke-width="1.5" stroke-linecap="round"/>
  <circle cx="135" cy="200" r="3" fill="#aaa"/>
  <!-- Sub-dial RIGHT (3 o'clock position) - 12hr counter -->
  <circle cx="255" cy="200" r="42" fill="white" stroke="#aaa" stroke-width="1.2"/>
  <circle cx="255" cy="200" r="36" fill="none" stroke="#ccc" stroke-width="0.8"/>
  <g stroke="#bbb" stroke-width="1">
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(0 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(30 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(60 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(90 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(120 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(150 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(180 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(210 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(240 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(270 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(300 255 200)"/>
    <line x1="255" y1="159" x2="255" y2="165" transform="rotate(330 255 200)"/>
  </g>
  <!-- Sub-dial hands right -->
  <line x1="255" y1="200" x2="265" y2="168" stroke="#999" stroke-width="2" stroke-linecap="round"/>
  <line x1="255" y1="200" x2="270" y2="215" stroke="#999" stroke-width="1.5" stroke-linecap="round"/>
  <circle cx="255" cy="200" r="3" fill="#aaa"/>
  <!-- Sub-dial BOTTOM (6 o'clock position) - seconds -->
  <circle cx="195" cy="280" r="42" fill="white" stroke="#aaa" stroke-width="1.2"/>
  <circle cx="195" cy="280" r="36" fill="none" stroke="#ccc" stroke-width="0.8"/>
  <g stroke="#bbb" stroke-width="1">
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(0 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(30 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(60 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(90 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(120 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(150 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(180 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(210 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(240 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(270 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(300 195 280)"/>
    <line x1="195" y1="239" x2="195" y2="245" transform="rotate(330 195 280)"/>
  </g>
  <!-- Date window -->
  <rect x="228" y="272" width="20" height="16" rx="1" fill="white" stroke="#aaa" stroke-width="1"/>
  <!-- Sub-dial bottom hand -->
  <line x1="195" y1="280" x2="205" y2="252" stroke="#999" stroke-width="2" stroke-linecap="round"/>
  <line x1="195" y1="280" x2="188" y2="294" stroke="#999" stroke-width="1.5" stroke-linecap="round"/>
  <circle cx="195" cy="280" r="3" fill="#aaa"/>
  <!-- Main hands -->
  <!-- Hour hand -->
  <line x1="195" y1="200" x2="195" y2="120" stroke="#777" stroke-width="5" stroke-linecap="round"/>
  <!-- Minute hand -->
  <line x1="195" y1="200" x2="240" y2="110" stroke="#777" stroke-width="3.5" stroke-linecap="round"/>
  <!-- Seconds hand (sweep) -->
  <line x1="195" y1="215" x2="195" y2="88" stroke="#aaa" stroke-width="1.5" stroke-linecap="round"/>
  <!-- Center cap -->
  <circle cx="195" cy="200" r="5" fill="#888"/>
  <circle cx="195" cy="200" r="2.5" fill="white"/>
</svg>'''

# Save SVG
svg_path = 'frontend/public/watch-chronograph.svg'
with open(svg_path, 'w') as f:
    f.write(svg_content)
print(f'SVG saved: {svg_path}')

# Convert to PNG using Pillow + cairosvg if available, else use PIL directly
try:
    import cairosvg
    cairosvg.svg2png(url=svg_path, write_to='frontend/public/watch-chronograph.png', output_width=400, output_height=400)
    print('PNG saved via cairosvg')
except ImportError:
    # Fallback: create a simple watch face PNG directly with Pillow
    from PIL import Image, ImageDraw
    import math

    size = 400
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    cx, cy, r = 200, 200, 170

    # Outer bezel
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(140,140,140,255), width=3)

    # Tick marks
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        tick_len = 14 if i % 5 == 0 else 8
        x1 = cx + (r - 4) * math.cos(angle)
        y1 = cy + (r - 4) * math.sin(angle)
        x2 = cx + (r - 4 - tick_len) * math.cos(angle)
        y2 = cy + (r - 4 - tick_len) * math.sin(angle)
        width = 2 if i % 5 == 0 else 1
        draw.line([x1, y1, x2, y2], fill=(160,160,160,255), width=width)

    # Dial face
    dial_r = r - 22
    draw.ellipse([cx-dial_r, cy-dial_r, cx+dial_r, cy+dial_r], fill=(255,255,255,255), outline=(180,180,180,255), width=1)

    # Hour markers
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        mx = cx + (dial_r - 14) * math.cos(angle)
        my = cy + (dial_r - 14) * math.sin(angle)
        draw.rectangle([mx-5, my-9, mx+5, my+9], outline=(140,140,140,255), width=2)

    # Sub-dial LEFT (9 o'clock)
    sub_r = 40
    draw.ellipse([cx-90-sub_r, cy-sub_r, cx-90+sub_r, cy+sub_r], fill=(255,255,255,255), outline=(180,180,180,255), width=1)
    draw.line([cx-90, cy, cx-90, cy-28], fill=(160,160,160,255), width=2)
    draw.ellipse([cx-93, cy-3, cx-87, cy+3], fill=(160,160,160,255))

    # Sub-dial RIGHT (3 o'clock)
    draw.ellipse([cx+50, cy-sub_r, cx+50+2*sub_r, cy+sub_r], fill=(255,255,255,255), outline=(180,180,180,255), width=1)
    draw.line([cx+90, cy, cx+90+15, cy-26], fill=(160,160,160,255), width=2)
    draw.ellipse([cx+87, cy-3, cx+93, cy+3], fill=(160,160,160,255))

    # Sub-dial BOTTOM (6 o'clock)
    draw.ellipse([cx-sub_r, cy+38, cx+sub_r, cy+38+2*sub_r], fill=(255,255,255,255), outline=(180,180,180,255), width=1)
    draw.line([cx, cy+58, cx+10, cy+42], fill=(160,160,160,255), width=2)
    draw.ellipse([cx-3, cy+55, cx+3, cy+61], fill=(160,160,160,255))

    # Crown/pusher
    draw.rectangle([cx+r+2, cy-18, cx+r+28, cy+18], outline=(140,140,140,255), width=2, fill=(245,245,245,255))
    for line_y in [cy-8, cy, cy+8]:
        draw.line([cx+r+4, line_y, cx+r+26, line_y], fill=(180,180,180,255), width=1)

    # Main hands
    # Hour hand
    hour_angle = math.radians(-90 + 30*10)  # pointing to 10
    draw.line([cx, cy, cx + 65*math.cos(hour_angle), cy + 65*math.sin(hour_angle)], fill=(100,100,100,255), width=6)
    # Minute hand
    min_angle = math.radians(-90 + 6*10)
    draw.line([cx, cy, cx + 95*math.cos(min_angle), cy + 95*math.sin(min_angle)], fill=(100,100,100,255), width=4)
    # Seconds hand
    sec_angle = math.radians(-90 + 6*32)
    draw.line([cx, cy, cx + 110*math.cos(sec_angle), cy + 110*math.sin(sec_angle)], fill=(180,180,180,255), width=2)
    draw.line([cx, cy, cx - 28*math.cos(sec_angle), cy - 28*math.sin(sec_angle)], fill=(180,180,180,255), width=2)

    # Center cap
    draw.ellipse([cx-6, cy-6, cx+6, cy+6], fill=(120,120,120,255))
    draw.ellipse([cx-2.5, cy-2.5, cx+2.5, cy+2.5], fill=(240,240,240,255))

    # Save with white background
    final = Image.new('RGB', (size, size), (255,255,255))
    final.paste(img, mask=img.split()[3])
    final.save('frontend/public/watch-chronograph.png')
    print('PNG saved via Pillow')

print('Done!')
