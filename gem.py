import os
from pygame import image, transform, draw
class Gem:


    source_file_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(source_file_dir)

    emerald_spr = image.load(
    os.path.join(source_file_dir , "res", "emerald.png"))
    diamond_spr = image.load(
    os.path.join(source_file_dir , "res", "diamond.png"))
    amethist_spr = image.load(
    os.path.join(source_file_dir , "res", "amethist.png"))
    void_spr = image.load(
    os.path.join(source_file_dir , "res", "void.png"))
    ruby_spr = image.load(
    os.path.join(source_file_dir , "res", "ruby.png"))
    saphire_spr = image.load(
    os.path.join(source_file_dir , "res", "saphire.png"))
    dimensions = (40, 40)
    x = 0
    y = 0
    pts = 0
    sprite = None
    clicked = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        

    def render(self, screen):
        if self.clicked:
            self.resize(self.dimensions[0]+5, self.dimensions[1]+5)
        else: self.sprite = transform.scale(self.sprite, self.dimensions)
        rect = self.sprite.get_rect()
        rect.x = self.x
        rect.y = self.y
        screen.blit(self.sprite, rect)

    def resize(self, w, h):
        self.sprite = transform.smoothscale(self.sprite.convert_alpha(), (w, h))


class Amethist(Gem):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.pts = 20
        self.sprite = Gem.amethist_spr

    def __repr__(self) -> str:
        return 'Amethist'

class Emerald(Gem):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.pts = 40
        self.sprite = Gem.emerald_spr

    def __repr__(self) -> str:
        return 'Emerald'


class Diamond(Gem):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.pts = 50
        self.sprite = Gem.diamond_spr
    
    def __repr__(self) -> str:
        return 'Diamond'

class Ruby(Gem):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.pts = 30
        self.sprite = Gem.ruby_spr
    
    def __repr__(self) -> str:
        return 'Ruby'

class Saphire(Gem):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.pts = 25
        self.sprite = Gem.saphire_spr

    def __repr__(self) -> str:
        return 'Saphire'


class Void(Gem):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.pts = 0
        self.sprite = Gem.void_spr

    def __repr__(self) -> str:
        return 'Void'
