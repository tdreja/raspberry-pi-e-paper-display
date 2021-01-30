def draw_text_centered(draw, xy, text, font, color=0, size=(0, 0)):
    text = text.strip()
    text_size = draw.textsize(text, font=font)
    offset_x = (size[0] - text_size[0]) / 2
    offset_y = (size[1] - text_size[1]) / 2
    draw.text((xy[0] + offset_x, xy[1] + offset_y), text, font=font, fill=color)


def generate_drawable_lines(draw, font, prefix='', joiner=', ', text_parts=None, width=0):
    if text_parts is None or not text_parts:
        return []

    calculated_lines = []
    first_in_line = True
    calc_line = prefix
    for part in text_parts:
        tmp = calc_line
        if not first_in_line:
            tmp += joiner

        first_in_line = False
        tmp += part
        text_size = draw.textsize(tmp, font=font)

        if text_size[0] <= width:
            calc_line = tmp

        else:
            calculated_lines.append(calc_line)
            calc_line = part
            first_in_line = True

    if calc_line not in calculated_lines:
        calculated_lines.append(calc_line)

    return calculated_lines


def draw_lines_centered(draw, font, lines=None, start_xy=(0, 0), end_xy=(0, 0), color=0, line_size=(0, 0)):
    if lines is None or not lines:
        return

    count = max(1, int((end_xy[1] - start_xy[1]) / max(1, line_size[1])))
    usable_lines = lines[:count]

    height = max(1, line_size[1]) * len(usable_lines)
    overall_offset_y = (end_xy[1] - start_xy[1] - height) / 2
    xy = (start_xy[0], start_xy[1] + overall_offset_y)

    for line in usable_lines:
        line = line.strip()
        text_size = draw.textsize(line, font=font)
        offset_x = (line_size[0] - text_size[0]) / 2
        offset_y = (line_size[1] - text_size[1]) / 2
        draw.text((xy[0] + offset_x, xy[1] + offset_y), line, font=font, fill=color)
        xy = (xy[0], xy[1] + line_size[1])
