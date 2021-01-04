from PIL import Image, ImageDraw, ImageFont
import math


class ImageModifier():
    def __init__(self, im, img_name: str, out_path):
        self.im = im
        self.img_name: str = img_name
        self.out_path = out_path
        self.draw: ImageDraw = ImageDraw.Draw(im)

    # xy: [(0,0), (100, 100)] [left_top, right_bottom]
    # xy 박스를 전부 흰색으로 칠하고, 전체 텍스트의 길이를 박스 너비로 나눈 값이 몇줄이 나오는 것이다.
    # 이 몇줄로 글자수를 나누면 한줄에 최대 몇줄이 들어갈지가 나오고, 이를 내림하면 적어도 몇글자씩 넣을지가
    # 나온다.
    def apply_multiline_text(self, xy, text: str, font_size):
        [left_top, right_bottom] = xy
        box_width = right_bottom[0]-left_top[0]

        font = ImageFont.truetype(
            "./misc/yangjin.ttf", font_size)
        width, height = font.getsize(text)
        line_count = width/box_width
        min_char_per_line = math.floor(len(text)/line_count)
        print('min_char_per_line', min_char_per_line)
        lines = [text[i:i+min_char_per_line]
                 for i in range(0, len(text), min_char_per_line)]
        print(lines)

        linebreaked_text = '\n'.join(lines)

        # 전체 사각형 체움
        self.draw.rectangle(xy, fill=(255, 255, 255))

        self.draw.multiline_text(left_top,
                                 text=linebreaked_text,
                                 font=font,
                                 fill=(0, 0, 0))

    def save(self):
        modified = self.img_name+'_modified.png'
        self.im.save(self.out_path+'/'+modified)


if __name__ == '__main__':
    with Image.open("./misc/manga.png") as im:
        modifier = ImageModifier(im, "manga", './out')
        modifier.apply_multiline_text(
            [(100, 100), (260, 340)], 'Hello World This is Funking Hard...', 40)
        modifier.save()
