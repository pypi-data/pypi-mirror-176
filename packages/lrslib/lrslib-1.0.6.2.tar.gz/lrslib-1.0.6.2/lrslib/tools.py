'''
lrslib
~~~~~~
:author lrs:
'''
import time
import typing
import pygame
import PIL


NUMBER = typing.Union[int, float]


class ImageError(ValueError):
    '''Image Not Found Error'''
    pass


def pront(msg: str, time: NUMBER=0.5, end: str='\n') -> None:
    '''高级输出'''
    new_time = float(time)
    for i in msg:
        print(i, end='')
        time.sleep(new_time)
    print(end, end='')


def show_image(image: str) -> None:
    '''This function help you show image to user.'''
    pygame.init()
    pygame.display.set_caption("图片查看器 - 按ESC键退出")
    Img = image
    try:
        myImg = pygame.image.load(Img)
        img = PIL.Image.open(Img)
        x = img.width
        y = img.height
    except:
        pygame.quit()
        raise ImageError('您选择了错误的文件，无法显示！')
    running = True
    while running:
        screen = pygame.display.set_mode((x, y))
        screen.fill((255, 255, 255))
        screen.blit(myImg, (0, 0))
        pygame.display.update()
        pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    pygame.quit()
