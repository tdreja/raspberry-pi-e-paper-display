def draw_text_centered(draw, xy, text, font, color=0, size=(0, 0)):
    text = text.strip()
    text_size = draw.textsize(text, font=font)
    offset_x = (size[0] - text_size[0]) / 2
    offset_y = (size[1] - text_size[1]) / 2
    draw.text((xy[0] + offset_x, xy[1] + offset_y), text, font=font, fill=color)
