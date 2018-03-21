def insert(source, target, x1, y1):
    offset_x = -x1 if x1 < 0 else 0
    offset_y = -y1 if y1 < 0 else 0
    x2 = x1 + source.width() - 1
    y2 = y1 + source.height() - 1
    width = source.width() if x2 < target.width() else target.width() - x1
    height = source.height() if y2 < target.height() else target.height() - y1

    for x in range(width - offset_x):
        for y in range(height - offset_y):
            color = source.pixelColor(x + offset_x, y + offset_y)
            target.setPixelColor(x + x1 + offset_x, y + y1 + offset_y, color)
