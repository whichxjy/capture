from PIL import Image
import numpy as np
import argparse
import math
import datetime

def calculate_theta(x, y):
    if x == 0:
        # y-axis
        if y > 0:
            return math.pi / 2
        else:
            return 3 * (math.pi / 2)
    elif y == 0:
        # x-axis
        if x > 0:
            return 0
        else:
            return math.pi
    elif x > 0 and y > 0:
        # quadrant 1
        return math.atan(y / x)
    elif x < 0 and y > 0:
        # quadrant 2
        return math.pi - math.atan(y / -x)
    elif x < 0 and y < 0:
        # quadrant 3
        return math.pi + math.atan(y / x)
    else:
        # quadrant 4
        return 2 * math.pi - math.atan(-y / x)

def main():
    now = datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=1000, help='The width of the image')
    parser.add_argument('--height', type=int, default=1000, help='The height of the image')
    args = parser.parse_args()

    width = args.width
    height = args.height

    data = np.zeros((height, width, 4), dtype=np.uint8)

    # prepare for red
    max_dist = math.sqrt((width // 2) ** 2 + (height // 2) ** 2)
    if width >= height:
        lota = math.atan(width / height)
    else:
        lota = math.atan(height / width)
    max_shift = 245
    min_shift = 255 * (1 - math.cos(lota))

    # calculate blue [second]
    blue = (255 * now.second) / 59

    # calculate alpha [days]
    begin_datetime = datetime.datetime(2020, 1, 1)
    end_datetime = datetime.datetime(9999, 1, 1)
    alpha = round(255 * (1 - min(1, (now - begin_datetime).days / (end_datetime - begin_datetime).days)))

    for x in range(-width // 2, width // 2):
        for y in range(-height // 2, height // 2):
            # calculate red [hour]
            dist = math.sqrt(x ** 2 + y ** 2)
            red = int((dist / max_dist) * 255 + max_shift - (max_shift - min_shift) * (now.hour / 24))
            if red > 255:
                red -= 255

            # calculate green [minute]
            beta = (now.minute * math.pi) / 30
            angle = (3 * math.pi / 2 - calculate_theta(x, y)) + beta
            if angle > 2 * math.pi:
                angle -= 2 * math.pi
            elif angle < 0:
                angle += 2 * math.pi
            green = int(round((angle / (2 * math.pi)) * 255))

            # set rgba
            data[y + height // 2, x + width // 2] = (red, green, blue, alpha)

    img = Image.fromarray(data, 'RGBA')
    img_name = now.strftime('%Y-%m-%d_%H:%M:%S') + '.png'
    img.save(img_name)

if __name__ == '__main__':
    main()