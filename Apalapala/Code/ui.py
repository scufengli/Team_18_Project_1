import pygame as pg 

class UI:
    def __init__(self,surface):

        # SETUP 
        self.display_surface = surface

        # HEALTH 
        self.health_bar = pg.image.load('../graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (54,39)
        self.bar_max_width = 152
        self.bar_height = 4

        # COINS

#========= SAMPLE CODE DO NOT LEAVE IN ==========
    def show_health(self,current,full):
        self.display_surface.blit(self.health_bar,(20,10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pg.Rect(self.health_bar_topleft,(current_bar_width,self.bar_height))
        pg.draw.rect(self.display_surface,'#dc4949',health_bar_rect)

    def show_coins(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surf = self.font.render(str(amount),False,'#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)
                
#========= SAMPLE CODE DO NOT LEAVE IN ==========