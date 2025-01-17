import pygame
from config import *
from inventory import *
import math
import random


class SpriteSheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])

        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(WHITE)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.p_sprite_group, self.game.player_group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 0

        self.down_animations = [
            self.game.character_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.character_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.up_animations = [
            self.game.character_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.character_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        self.left_animations = [
            self.game.character_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE),
            self.game.character_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE)
        ]

        self.right_animations = [
            self.game.character_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE),
            self.game.character_spritesheet.get_sprite(175, 0, TILESIZE, TILESIZE)
        ]

        
        self.image = self.game.character_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.inventory = Inventory()
        self.weapon_slot = WeaponSlot()
        self.weapon_slot2 = WeaponSlot()
        self.couldron = Couldron()

        self.armed_melee = False
        self.armed_ranged = False

        self.health = 100
        self.pc_health = 100
        self.level = 1
        self.gold = 0

    def update(self):
        #   call movement and animate functions.

        self.movement()
        self.animate()

        #   move and check collisions

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_snakes('x')
        self.collide_badgers('x')
        self.collide_wells('x')
        self.collide_items('x')
        self.collide_guard_trigger_1('x')
        self.collide_monument1_trigger('x')
        self.collide_flat_top_mountain_trigger('x')
        self.collide_blacksmith_convo_trigger('x')
        
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_snakes('y')
        self.collide_badgers('y')
        self.collide_wells('y')
        self.collide_items('y')
        self.collide_guard_trigger_1('y')
        self.collide_monument1_trigger('y')
        self.collide_flat_top_mountain_trigger('y')
        self.collide_blacksmith_trigger('y')
        self.collide_farm_girl_trigger('y')
        self.collide_penny_orchard_sign_trigger('y')

        self.x_change = 0
        self.y_change = 0

        #   cap health
        self.max_health = 98 + self.level * 2

        if self.health >= self.max_health:
            self.health = self.max_health

        self.dec_health = self.health / self.max_health
        self.pc_health = self.dec_health * 100

        #   cap level
        if self.level > 99:
            self.level = 99

        #   check if armed

        for item in self.weapon_slot.inv:
            if item.name == 'Axe - Basic':
                self.armed_melee = True

        for item in self.weapon_slot2.inv:
            if item.name == 'Crossbow':
                self.armed_ranged = True

    def movement(self):
        keys = pygame.key.get_pressed()
        #   left
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.game.blacksmith == False:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED
            for sprite in self.game.blacksmith_int_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            
            self.facing = 'left'
        #   right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.game.blacksmith == False:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
            for sprite in self.game.blacksmith_int_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            
            self.facing = 'right'
        #   up
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.game.blacksmith == False:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED
            for sprite in self.game.blacksmith_int_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            
            self.facing = 'up'
        #   down
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.game.blacksmith == False:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED
            for sprite in self.game.blacksmith_int_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            
            self.facing = 'down'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    for sprite in self.game.blacksmith_int_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    for sprite in self.game.blacksmith_int_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    for sprite in self.game.blacksmith_int_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    for sprite in self.game.blacksmith_int_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_npcs(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.npcs, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.npcs, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_snakes(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.snakes, False)
            if hits:
                now = pygame.time.get_ticks()
                if now - self.game.last >= 1000:
                    self.health -= random.randint(5, 15)
                    self.game.last = now
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    
                
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.snakes, False)
            if hits:
                now = pygame.time.get_ticks()
                if now - self.game.last >= 1000:
                    self.health -= random.randint(5, 15)
                    self.game.last = now
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    
    def collide_badgers(self, direction):

        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.badgers, False)
            if hits:
                now = pygame.time.get_ticks()
                if now - self.game.last >= 1000:
                    self.health -= random.randint(10, 20)
                    self.game.last = now
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.badgers, False)
            if hits:
                now = pygame.time.get_ticks()
                if now - self.game.last >= 1000:
                    self.health -= random.randint(10, 20)
                    self.game.last = now
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    
    def collide_wells(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.wells, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.wells, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    
    def collide_items(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.items, True)
            if hits:
                if hits[0].name == 'Axe - Basic':
                    self.weapon_slot.add_item(weapon_list[0])
                if hits[0].name == 'Crossbow':
                    self.weapon_slot2.add_item(weapon_list[1])
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.items, True)
            if hits:
                if hits[0].name == 'Axe - Basic':
                    self.weapon_slot.add_item(weapon_list[0])
                if hits[0].name == 'Crossbow':
                    self.weapon_slot2.add_item(weapon_list[1])
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_guard_trigger_1(self, direction):
            if direction == 'x':
                hits = pygame.sprite.spritecollide(self, self.game.guard_trigger_1_sprite, False)
                if hits:
                    self.game.guard_1_convo_trigger = True
                else:
                    self.game.guard_1_convo_trigger = False

            if direction == 'y':
                hits = pygame.sprite.spritecollide(self, self.game.guard_trigger_1_sprite, False)
                if hits:
                    self.game.guard_1_convo_trigger = True
                else:
                    self.game.guard_1_convo_trigger = False

    def collide_monument1_trigger(self, direction):
                if direction == 'x':
                    hits = pygame.sprite.spritecollide(self, self.game.monument1_trigger_sprite, False)
                    if hits:
                        self.game.monument1_trigger = True
                    else:
                        self.game.monument1_trigger = False

                if direction == 'y':
                    hits = pygame.sprite.spritecollide(self, self.game.monument1_trigger_sprite, False)
                    if hits:
                        self.game.monument1_trigger = True
                    else:
                        self.game.monument1_trigger = False

    def collide_flat_top_mountain_trigger(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.flat_top_mountain_trigger_sprite, False)
            if hits:
                self.game.flat_top_mountain_trigger = True
            else:
                self.game.flat_top_mountain_trigger = False

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.flat_top_mountain_trigger_sprite, False)
            if hits:
                self.game.flat_top_mountain_trigger = True
            else:
                self.game.flat_top_mountain_trigger = False

    def collide_blacksmith_trigger(self, direction):

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blacksmith_trigger_sprite, False)
            if hits:
                if self.facing == 'up':
                    self.game.blacksmith_trigger = True
            else:
                self.game.blacksmith_trigger = False

    def collide_blacksmith_convo_trigger(self, direction):

        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blacksmith_convo_trigger_sprite, False)
            if hits:
                if self.facing == 'left':
                    self.game.blacksmith_convo_trigger = True
            else:
                self.game.blacksmith_convo_trigger = False

    def collide_farm_girl_trigger(self, direction):

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.farm_girl_trigger_sprite, False)
            if hits:
                if self.facing == 'up':
                    self.game.farm_girl_trigger = True
            else:
                self.game.farm_girl_trigger = False

    def collide_penny_orchard_sign_trigger(self, direction):
                    
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.penny_orchard_sign_trigger_sprite, False)
            
            if hits:
                if self.game.player.facing == 'up':
                    self.game.penny_orchard_sign = True
            else:
                self.game.penny_orchard_sign = False

    def animate(self):

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0


class Knight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['up', 'down', 'left', 'right'])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(10, 32)

        self.down_animations = [
            self.game.knight_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.knight_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.up_animations = [
            self.game.knight_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.knight_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        self.left_animations = [
            self.game.knight_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE),
            self.game.knight_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE)
        ]

        self.right_animations = [
            self.game.knight_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE),
            self.game.knight_spritesheet.get_sprite(175, 0, TILESIZE, TILESIZE)
        ]

        self.image = self.game.knight_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 50

        self.exp = 0.14

    def update(self):
        self.movement()
        self.animate()

        if self.game.player.level <= 9:
            self.exp = self.exp
        elif self.game.player.level <= 19:
            self.exp = self.exp/1.5
        elif self.game.player.level <= 29:
            self.exp = self.exp/2
        elif self.game.player.level <= 39:
            self.exp = self.exp/3
        elif self.game.player.level <= 49:
            self.exp = self.exp/4.5
        elif self.game.player.level <= 69:
            self.exp = self.exp/6
        elif self.game.player.level <= 99:
            self.exp = self.exp/10

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_player('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_player('y')

        self.x_change = 0
        self.y_change = 0

        if self.health <= 0:
            self.kill()

    def movement(self):
        if self.facing == 'up':
            self.y_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'down'

        if self.facing == 'down':
            self.y_change += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'up'

        if self.facing == 'left':
            self.x_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_player(self, direction):

        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.knight_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.knight_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.knight_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.knight_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0


class GuardKnight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.npcs, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE + 10
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(10, 32)

        self.down_animations = [
            self.game.knight_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.knight_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.up_animations = [
            self.game.knight_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.knight_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        self.left_animations = [
            self.game.knight_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE),
            self.game.knight_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE)
        ]

        self.right_animations = [
            self.game.knight_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE),
            self.game.knight_spritesheet.get_sprite(175, 0, TILESIZE, TILESIZE)
        ]

        self.image = self.game.knight_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = TILESIZE*2

        self.health = 50

        self.exp = 0.14
        self.lv10 = False

    def update(self):
        self.movement()
        self.animate()

        if self.game.player.level <= 9:
            self.exp = self.exp
        elif self.game.player.level <= 19:
            self.exp = self.exp/1.5
        elif self.game.player.level <= 29:
            self.exp = self.exp/2
        elif self.game.player.level <= 39:
            self.exp = self.exp/3
        elif self.game.player.level <= 49:
            self.exp = self.exp/4.5
        elif self.game.player.level <= 69:
            self.exp = self.exp/6
        elif self.game.player.level <= 99:
            self.exp = self.exp/10

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_player('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_player('y')

        self.x_change = 0
        self.y_change = 0

        if self.game.player.level >= 5:
            self.rect.width = TILESIZE-10
            self.lv10 = True

    def movement(self):
        pass

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_player(self, direction):

        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.knight_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.knight_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.knight_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.knight_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0


class Snake(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.snakes, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['up', 'down', 'left', 'right'])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(10, 32)

        self.down_animations = [
            self.game.snake_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.snake_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.up_animations = [
            self.game.snake_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.snake_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        self.left_animations = [
            self.game.snake_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE),
            self.game.snake_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE)
        ]

        self.right_animations = [
            self.game.snake_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE),
            self.game.snake_spritesheet.get_sprite(175, 0, TILESIZE, TILESIZE)
        ]

        self.image = self.game.character_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 20
        self.exp = 0.07
        
    def update(self):
        self.movement()
        self.animate()

        if self.game.player.level <= 9:
            self.exp = self.exp
        elif self.game.player.level <= 19:
            self.exp = self.exp/2
        elif self.game.player.level <= 29:
            self.exp = self.exp/3
        elif self.game.player.level <= 39:
            self.exp = self.exp/4
        elif self.game.player.level <= 49:
            self.exp = self.exp/5
        elif self.game.player.level <= 69:
            self.exp = self.exp/6
        elif self.game.player.level <= 99:
            self.exp = self.exp/10


        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_player('x')
        self.collide_badgers('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_player('y')
        self.collide_badgers('y')

        self.x_change = 0
        self.y_change = 0

        if self.health <= 0:
            self.kill()

    def movement(self):
        if self.facing == 'up':
            self.y_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['up', 'down', 'left', 'right'])

        if self.facing == 'down':
            self.y_change += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['up', 'down', 'left', 'right'])

        if self.facing == 'left':
            self.x_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['up', 'down', 'left', 'right'])

        if self.facing == 'right':
            self.x_change += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['up', 'down', 'left', 'right'])

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_player(self, direction):
        

        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_badgers(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.badgers, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.badgers, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.snake_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.snake_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.snake_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.snake_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0


class Badger(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.badgers, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['up', 'down', 'left', 'right'])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(10, 32)

        self.down_animations = [
            self.game.badger_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.badger_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.up_animations = [
            self.game.badger_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.badger_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)
        ]

        self.left_animations = [
            self.game.badger_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE),
            self.game.badger_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE)
        ]

        self.right_animations = [
            self.game.badger_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE),
            self.game.badger_spritesheet.get_sprite(175, 0, TILESIZE, TILESIZE)
        ]

        self.image = self.game.character_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 50

        self.exp = 0.14

    def update(self):
        self.movement()
        self.animate()

        if self.game.player.level <= 9:
            self.exp = self.exp
        elif self.game.player.level <= 19:
            self.exp = self.exp/1.5
        elif self.game.player.level <= 29:
            self.exp = self.exp/2
        elif self.game.player.level <= 39:
            self.exp = self.exp/3
        elif self.game.player.level <= 49:
            self.exp = self.exp/4.5
        elif self.game.player.level <= 69:
            self.exp = self.exp/6
        elif self.game.player.level <= 99:
            self.exp = self.exp/10

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_player('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_player('y')

        self.x_change = 0
        self.y_change = 0

        if self.health <= 0:
            self.kill()

    def movement(self):
        if self.facing == 'up':
            self.y_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['up', 'down', 'left', 'right'])

        if self.facing == 'down':
            self.y_change += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['up', 'down', 'left', 'right'])

        if self.facing == 'left':
            self.x_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['up', 'down', 'left', 'right'])

        if self.facing == 'right':
            self.x_change += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['up', 'down', 'left', 'right'])

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_player(self, direction):

        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.p_sprite_group, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_snakes(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.snakes, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.snakes, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.badger_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.badger_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.badger_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.badger_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0


class Dogon(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = OVERLAY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 2
        self.height = TILESIZE * 2

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(20, 35)
        self.attack_timer = pygame.time.get_ticks()

        

        self.left_animations = [
            self.game.dogon_spritesheet.get_sprite(0, 0, TILESIZE * 2, TILESIZE * 2),
            self.game.dogon_spritesheet.get_sprite(50, 0, TILESIZE * 2, TILESIZE * 2)
        ]

        self.right_animations = [
            self.game.dogon_spritesheet.get_sprite(100, 0, TILESIZE * 2, TILESIZE * 2),
            self.game.dogon_spritesheet.get_sprite(150, 0, TILESIZE * 2, TILESIZE * 2)
        ]

        self.image = self.game.dogon_spritesheet.get_sprite(0, 0, TILESIZE * 2, TILESIZE * 2)
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = 200

        self.exp = 0.26

    def update(self):
        self.movement()
        self.animate()

        if self.game.player.level <= 9:
            self.exp = self.exp
        elif self.game.player.level <= 19:
            self.exp = self.exp/1.5
        elif self.game.player.level <= 29:
            self.exp = self.exp/2
        elif self.game.player.level <= 39:
            self.exp = self.exp/3
        elif self.game.player.level <= 49:
            self.exp = self.exp/4.5
        elif self.game.player.level <= 69:
            self.exp = self.exp/6
        elif self.game.player.level <= 99:
            self.exp = self.exp/10

        self.rect.x += self.x_change

        self.x_change = 0

        if self.health <= 0:
            self.kill()

        now = pygame.time.get_ticks()
        if now - self.attack_timer >= 700:
            DogonAttack(self.game, self.rect.x + 20, self.rect.y + 40)
            self.attack_timer = now

    def movement(self):

        if self.facing == 'left':
            self.x_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                
                self.facing = 'right'
                

        if self.facing == 'right':
            self.x_change += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                
                self.facing = 'left'

    def animate(self):

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.dogon_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.dogon_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0


class DogonAttack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.dogon_attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE * 3

        self.animation_loop = 0

        self.animations = [
            self.game.dogon_attack_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.dogon_attack_spritesheet.get_sprite(25, 0, self.width, self.height),
            self.game.dogon_attack_spritesheet.get_sprite(50, 0, self.width, self.height)
        ]

        self.image = self.game.dogon_attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits_player = pygame.sprite.spritecollide(self, self.game.player_group, False)
        
        if hits_player:
            
            now = pygame.time.get_ticks()
            if now - self.game.last >= 500:
                self.game.player.health -= 50
                
                self.game.last = now

    def animate(self):
        
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.5
        if self.animation_loop >= 3:
            self.kill()


class BadgerSpawnPoint(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.origin_x = x
        self.y = y * TILESIZE
        self.origin_y = y
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.lv10 = False

        self.spawn_timer = pygame.time.get_ticks()

    def update(self):
        hits = pygame.sprite.spritecollide(self, self.game.aoi, False)
        if hits:
            self.spawn()

    def spawn(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer >= 10000:     #   5sec
            Badger(self.game, self.origin_x + self.game.rel_x, self.origin_y + self.game.rel_y)
            self.spawn_timer = now


class SnakeSpawnPoint(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.origin_x = x
        self.y = y * TILESIZE
        self.origin_y = y
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.lv10 = False

        self.spawn_timer = pygame.time.get_ticks()

    def update(self):
        hits = pygame.sprite.spritecollide(self, self.game.aoi, False)
        if hits:
            self.spawn()

    def spawn(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer >= 10000:     #   3sec
            Snake(self.game, self.origin_x + self.game.rel_x, self.origin_y + self.game.rel_y)
            self.spawn_timer = now


class DogonSpawnPoint(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.origin_x = x
        self.y = y * TILESIZE
        self.origin_y = y
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.lv10 = False

        self.spawn_timer = pygame.time.get_ticks()

    def update(self):
        hits = pygame.sprite.spritecollide(self, self.game.aoi, False)
        if hits:
            self.spawn()

    def spawn(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer >= 60000:     #   1min
            if self.game.player.level >= 4:
                Dogon(self.game, self.origin_x + self.game.rel_x, self.origin_y + self.game.rel_y)
                self.spawn_timer = now


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/wall1.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.blocks, self.game.mushrooms
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            self.game.mushroom_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.mushroom_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.mushroom_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Logs(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks, self.game.logs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/logs1.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0, 0))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.images = [
            self.game.water_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.water_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.animate()

    def animate(self):
        self.image = self.images[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 2:
            self.animation_loop = 0


class Grass(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            self.game.grass_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.grass_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
            self.game.grass_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Dirt(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/dirt1.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class WellStatic1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/wellstatic1.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(WHITE)
        self.image.blit(image_to_load, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class WellStatic2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/wellstatic2.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(WHITE)
        self.image.blit(image_to_load, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class WellStatic3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.wells
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/wellstatic3.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(WHITE)
        self.image.blit(image_to_load, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class WellStatic4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.wells
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/wellstatic4.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(WHITE)
        self.image.blit(image_to_load, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Path1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/wall1.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Tree1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.images = [self.game.tree1_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
                       self.game.tree1_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
                       ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        
        pass


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('jennifer.ttf', fontsize)
        self.content = content
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center= (self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


class MeleeAttack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.down_animations = [
            self.game.melee_attack_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.melee_attack_spritesheet.get_sprite(0, 25, self.width, self.height),
            self.game.melee_attack_spritesheet.get_sprite(0, 50, self.width, self.height)
        ]

        self.up_animations = [
            self.game.melee_attack_spritesheet.get_sprite(25, 0, self.width, self.height),
            self.game.melee_attack_spritesheet.get_sprite(25, 25, self.width, self.height),
            self.game.melee_attack_spritesheet.get_sprite(25, 50, self.width, self.height)
        ]

        self.left_animations = [
            self.game.melee_attack_spritesheet.get_sprite(50, 0, self.width, self.height),
            self.game.melee_attack_spritesheet.get_sprite(50, 25, self.width, self.height),
            self.game.melee_attack_spritesheet.get_sprite(50, 50, self.width, self.height)
        ]

        self.right_animations = [
            self.game.melee_attack_spritesheet.get_sprite(50, 0, self.width, self.height),
            self.game.melee_attack_spritesheet.get_sprite(50, 25, self.width, self.height),
            self.game.melee_attack_spritesheet.get_sprite(50, 50, self.width, self.height)
        ]

        self.image = self.game.melee_attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        now = pygame.time.get_ticks()
        hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        hits_mushrooms = pygame.sprite.spritecollide(self, self.game.mushrooms, True)
        hits_logs = pygame.sprite.spritecollide(self, self.game.logs, True)
        hits_apple_trees = pygame.sprite.spritecollide(self, self.game.apple_trees, False)

        if hits_apple_trees:
            if now - self.game.text_timer >= 300:
                self.game.player.inventory.add_item(item_list[3])
                self.game.text_timer = now

        if hits_mushrooms:
            
            self.game.player.inventory.add_item(item_list[0])

        if hits_logs:

            self.game.player.inventory.add_item(item_list[1])
            
        if hits_enemies:
            
            now = pygame.time.get_ticks()
            if now - self.game.last >= 1000:
                self.game.player.level += hits_enemies[0].exp
                hits_enemies[0].health -= self.game.player.weapon_slot.inv[0].attack_strength
                self.game.last = now

    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()

        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()


class RangedAttackX(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE*3
        self.height = TILESIZE

        self.animation_loop = 0

        self.right_animations = [
            self.game.ranged_attack_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.ranged_attack_spritesheet.get_sprite(0, 25, self.width, self.height),
            self.game.ranged_attack_spritesheet.get_sprite(0, 50, self.width, self.height)
        ]

        self.left_animations = [
            self.game.ranged_attack_spritesheet.get_sprite(0, 75, self.width, self.height),
            self.game.ranged_attack_spritesheet.get_sprite(0, 100, self.width, self.height),
            self.game.ranged_attack_spritesheet.get_sprite(0, 125, self.width, self.height)
        ]

        self.image = self.game.ranged_attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        
        if hits_enemies:
            
            now = pygame.time.get_ticks()
            if now - self.game.last >= 1000:
                self.game.player.level += hits_enemies[0].exp
                hits_enemies[0].health -= self.game.player.weapon_slot2.inv[0].attack_strength
                self.game.last = now

    def animate(self):
        direction = self.game.player.facing

        
        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()


class RangedAttackY(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE * 3

        self.animation_loop = 0

        self.up_animations = [
            self.game.ranged_attack_spritesheet.get_sprite(0, 150, self.width, self.height),
            self.game.ranged_attack_spritesheet.get_sprite(25, 150, self.width, self.height),
            self.game.ranged_attack_spritesheet.get_sprite(50, 150, self.width, self.height)
        ]

        self.down_animations = [
            self.game.ranged_attack_spritesheet.get_sprite(0, 225, self.width, self.height),
            self.game.ranged_attack_spritesheet.get_sprite(25, 225, self.width, self.height),
            self.game.ranged_attack_spritesheet.get_sprite(50, 225, self.width, self.height)
        ]

        self.image = self.game.ranged_attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        
        if hits_enemies:
            
            now = pygame.time.get_ticks()
            if now - self.game.last >= 1000:
                self.game.player.level += hits_enemies[0].exp
                hits_enemies[0].health -= self.game.player.weapon_slot2.inv[0].attack_strength
                self.game.last = now

    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()


class LongRangedAttackX(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE*4
        self.height = TILESIZE

        self.animation_loop = 0

        self.right_animations = [
            self.game.long_ranged_attack_spritesheet.get_sprite(0, 175, self.width, self.height),
            self.game.long_ranged_attack_spritesheet.get_sprite(0, 200, self.width, self.height),
            self.game.long_ranged_attack_spritesheet.get_sprite(0, 225, self.width, self.height)
        ]

        self.left_animations = [
            self.game.long_ranged_attack_spritesheet.get_sprite(0, 100, self.width, self.height),
            self.game.long_ranged_attack_spritesheet.get_sprite(0, 125, self.width, self.height),
            self.game.long_ranged_attack_spritesheet.get_sprite(0, 150, self.width, self.height)
        ]

        self.image = self.game.long_ranged_attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        
        if hits_enemies:
            
            now = pygame.time.get_ticks()
            if now - self.game.last >= 1000:
                self.game.player.level += hits_enemies[0].exp
                hits_enemies[0].health -= self.game.player.weapon_slot2.inv[0].attack_strength
                self.game.last = now

    def animate(self):
        direction = self.game.player.facing

        
        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()


class LongRangedAttackY(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE * 4

        self.animation_loop = 0

        self.up_animations = [
            self.game.long_ranged_attack_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.long_ranged_attack_spritesheet.get_sprite(25, 0, self.width, self.height),
            self.game.long_ranged_attack_spritesheet.get_sprite(50, 0, self.width, self.height)
        ]

        self.down_animations = [
            self.game.long_ranged_attack_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.long_ranged_attack_spritesheet.get_sprite(25, 0, self.width, self.height),
            self.game.long_ranged_attack_spritesheet.get_sprite(50, 0, self.width, self.height)
        ]

        self.image = self.game.long_ranged_attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        
        if hits_enemies:
            
            now = pygame.time.get_ticks()
            if now - self.game.last >= 1000:
                self.game.player.level += hits_enemies[0].exp
                hits_enemies[0].health -= self.game.player.weapon_slot2.inv[0].attack_strength
                self.game.last = now

    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.kill()


class AxeBasic(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.name = 'Axe - Basic'

        image_to_load = pygame.image.load('img/axebasic.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(WHITE)
        self.image.blit(image_to_load, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Crossbow(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.name = 'Crossbow'

        image_to_load = pygame.image.load('img/crossbow.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(WHITE)
        self.image.blit(image_to_load, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = OVERLAY_LAYER
        self.groups = self.game.overlay_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 600
        self.height = 10

        self.images = [
            self.game.healthbar_spritesheet.get_sprite(0, 0, 600, 10),
            self.game.healthbar_spritesheet.get_sprite(0, 0, 540, 10),
            self.game.healthbar_spritesheet.get_sprite(0, 0, 480, 10),
            self.game.healthbar_spritesheet.get_sprite(0, 0, 420, 10),
            self.game.healthbar_spritesheet.get_sprite(0, 0, 360, 10),
            self.game.healthbar_spritesheet.get_sprite(0, 0, 300, 10),
            self.game.healthbar_spritesheet.get_sprite(0, 0, 240, 10),
            self.game.healthbar_spritesheet.get_sprite(0, 0, 180, 10),
            self.game.healthbar_spritesheet.get_sprite(0, 0, 120, 10),
            self.game.healthbar_spritesheet.get_sprite(0, 0, 60, 10)
        ]

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):

        if self.game.player.health > 90:
            self.image = self.images[0]

        elif self.game.player.health == 90:
            self.image = self.images[1]

        elif self.game.player.health >= 80:
            self.image = self.images[2]

        elif self.game.player.health >= 70:
            self.image = self.images[3]

        elif self.game.player.health >= 60:
            self.image = self.images[4]
        
        elif self.game.player.health >= 50:
            self.image = self.images[5]

        elif self.game.player.health >= 40:
            self.image = self.images[6]

        elif self.game.player.health >= 30:
            self.image = self.images[7]

        elif self.game.player.health >= 20:
            self.image = self.images[8]
        
        elif self.game.player.health >= 10:
            self.image = self.images[9]


class StoneFloor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            self.game.stone_floor_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.stone_floor_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StoneFloorTop(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            self.game.stone_floor_spritesheet.get_sprite(50, 0, TILESIZE, TILESIZE),
            self.game.stone_floor_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE),
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StoneFloorBottomLeft(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.stone_floor_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StoneFloorBottomRight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.stone_floor_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StoneWallLeft(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        image_to_load = pygame.image.load('img/stoneleftwall.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StoneWallRight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE


        image_to_load = pygame.image.load('img/stonerightwall.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StoneBottomWallLeft(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE * 2

        
        image_to_load = pygame.image.load('img/stonebottomleftwall.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StoneBottomWallRight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE *2

        
        image_to_load = pygame.image.load('img/stonebottomrightwall.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StoneBottomWall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE *2

        
        image_to_load = pygame.image.load('img/stonebottomwall.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StoneSteps(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 2
        self.height = TILESIZE * 2

        
        image_to_load = pygame.image.load('img/2tilestonesteps.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class RuinedPillar(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        self.images = [
            self.game.ruined_pillar_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.ruined_pillar_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE),
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class GuardHut(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/guardhut.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class HouseOne(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE *2
        self.height = TILESIZE *2

        image_to_load = pygame.image.load('img/house1.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class HouseTwo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE *3
        self.height = TILESIZE *2

        image_to_load = pygame.image.load('img/house2.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class LightHouse(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE *2

        self.animation_loop = 0

        self.images = [
            self.game.lighthouse_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE*2),
            self.game.lighthouse_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE*2)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.animate()

    def animate(self):
        self.image = self.images[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 2:
            self.animation_loop = 0


class Monument1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE * 2

        
        image_to_load = pygame.image.load('img/monument1.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class SignPost(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        
        image_to_load = pygame.image.load('img/signpost.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class GuardTriggerOne(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.guard_trigger_1_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 5

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Monument1SignTrigger(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.monument1_trigger_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 5

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FlatTopMountainSignTrigger(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.flat_top_mountain_trigger_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 5

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class StaticShip(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = OVERLAY_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 2
        self.height = TILESIZE * 2

        image_to_load = pygame.image.load('img/shipstatic.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class BlackSmithExt(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        self.animation_loop = 0

        self.images = [
            self.game.blacksmith_ext_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2),
            self.game.blacksmith_ext_spritesheet.get_sprite(50, 0, TILESIZE*2, TILESIZE*2)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.animate()

    def animate(self):
        self.image = self.images[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 2:
            self.animation_loop = 0


class BlackSmithFloor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            self.game.blacksmith_int_spritesheet.get_sprite(175, 0, TILESIZE, TILESIZE),
            self.game.blacksmith_int_spritesheet.get_sprite(200, 0, TILESIZE, TILESIZE),
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class BlackSmithWallTop(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            self.game.blacksmith_int_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.blacksmith_int_spritesheet.get_sprite(6, 0, TILESIZE, TILESIZE),
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class BlackSmithWallLeft(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

       

        self.image = self.game.blacksmith_int_spritesheet.get_sprite(75, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class BlackSmithWallRight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

       

        self.image = self.game.blacksmith_int_spritesheet.get_sprite(100, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class BlackSmithWallBottom(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

       

        self.image = self.game.blacksmith_int_spritesheet.get_sprite(125, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class BlackSmithIntDoor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

       

        self.image = self.game.blacksmith_int_spritesheet.get_sprite(150, 0, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class BlackSmithTrigger(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blacksmith_trigger_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 5

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class ShopCounter(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE *2

        self.animation_loop = 0

        self.images = [
            self.game.shopcounter_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE*2),
            self.game.shopcounter_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE*2)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.animate()

    def animate(self):
        self.image = self.images[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 2:
            self.animation_loop = 0


class WorkBench(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE *2

        image_to_load = pygame.image.load('img/workbench.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        pass

    
class Furnace(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*2
        self.height = TILESIZE*2

        self.animation_loop = 0

        self.images = [
            self.game.furnace_spritesheet.get_sprite(0, 0, TILESIZE*2, TILESIZE*2),
            self.game.furnace_spritesheet.get_sprite(50, 0, TILESIZE*2, TILESIZE*2)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.animate()

    def animate(self):
        self.image = self.images[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 2:
            self.animation_loop = 0


class ShopKeep(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE+4
        self.y = y * TILESIZE+12
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.images = [
            self.game.shopkeep_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.shopkeep_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.animate()

    def animate(self):
        self.image = self.images[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 2:
            self.animation_loop = 0


class BlackSmithConvoTrigger(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.blacksmith_int_sprites, self.game.blacksmith_convo_trigger_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 5
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FarmGirl(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE+10
        self.width = TILESIZE
        self.height = TILESIZE

        
        image_to_load = pygame.image.load('img/farmgirl.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FarmGirlTrigger(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.farm_girl_trigger_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 20

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class AppleTree(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = LAYER_2
        self.groups = self.game.all_sprites, self.game.blocks, self.game.apple_trees
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.images = [self.game.apple_tree_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
                       self.game.apple_tree_spritesheet.get_sprite(25, 0, TILESIZE, TILESIZE)
                       ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        
        pass


class PennyOrchardSignTrigger(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.penny_orchard_sign_trigger_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 5

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class ReferenceSprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.ref_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load('img/empty.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class AreaOfInfluence(pygame.sprite.Sprite):
    def __init__(self, game):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.aoi
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = self.game.player.rect.x -100
        self.y = self.game.player.rect.y -150
        self.width = TILESIZE*8
        self.height = TILESIZE*8

        image_to_load = pygame.image.load('img/area_of_influence.png')
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (0,0))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.x = self.game.player.rect.x -200
        self.y = self.game.player.rect.y -175


class CastleOne(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE*4
        self.height = TILESIZE*4

        self.animation_loop = 0

        self.images = [
            self.game.castle_1_spritesheet.get_sprite(0, 0, TILESIZE*4, TILESIZE*4),
            self.game.castle_1_spritesheet.get_sprite(100, 0, TILESIZE*4, TILESIZE*4)
        ]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.animate()

    def animate(self):
        self.image = self.images[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 2:
            self.animation_loop = 0

