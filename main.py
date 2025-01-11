import pygame
import sys
from sprites import *
from config import *
from inventory import *
import math


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        

        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = SpriteSheet('img/playerspritesheet.png')
        self.snake_spritesheet = SpriteSheet('img/snakespritesheet.png')
        self.badger_spritesheet = SpriteSheet('img/badgerspritesheet.png')
        self.dogon_spritesheet = SpriteSheet('img/dogonspritesheet.png')
        self.knight_spritesheet = SpriteSheet('img/knightspritesheet.png')
        self.tree1_spritesheet = SpriteSheet('img/tree1spritesheet.png')
        self.water_spritesheet = SpriteSheet('img/waterspritesheet.png')
        self.grass_spritesheet = SpriteSheet('img/grassspritesheet.png')
        self.mushroom_spritesheet = SpriteSheet('img/mushroomspritesheet.png')
        self.melee_attack_spritesheet = SpriteSheet('img/meleeattackspritesheet.png')
        self.healthbar_spritesheet = SpriteSheet('img/healthbar_spritesheet.png')
        self.ranged_attack_spritesheet = SpriteSheet('img/rangedattackspritesheet.png')
        self.stone_floor_spritesheet = SpriteSheet('img/stonefloorspritesheet.png')
        self.ruined_pillar_spritesheet = SpriteSheet('img/ruinedpillarspritesheet.png')
        self.dogon_attack_spritesheet = SpriteSheet('img/dogonattackspritesheet.png')
        self.lighthouse_spritesheet = SpriteSheet('img/lighthouse.png')
        self.blacksmith_ext_spritesheet = SpriteSheet('img/blacksmith_ext.png')
        self.blacksmith_int_spritesheet = SpriteSheet('img/blacksmith_int_spritesheet.png')
        self.shopcounter_spritesheet = SpriteSheet('img/shopcounter_spritesheet.png')
        self.furnace_spritesheet = SpriteSheet('img/furnace_spritesheet.png')
        self.shopkeep_spritesheet = SpriteSheet('img/shopkeep_spritesheet.png')
        self.long_ranged_attack_spritesheet = SpriteSheet('img/longrangedattackspritesheet.png')
        self.apple_tree_spritesheet = SpriteSheet('img/apple_tree_spritesheet.png')

        self.font = pygame.font.Font('jennifer.ttf', 26)
        self.font_mid = pygame.font.Font('jennifer.ttf', 18)
        self.font_small = pygame.font.Font('jennifer.ttf', 14)
        self.font_smaller = pygame.font.Font('jennifer.ttf', 10)

        #   overlay setup
        self.overlay_bg = pygame.image.load('img/overlaybg.png')
        self.overlay_bg.set_colorkey(WHITE)
        
        self.overlay_title = self.font.render('The Fateful Misadventures of Flatman', True, WHITE)
        self.overlay_title_rect = self.overlay_title.get_rect(x=170, y=5)

        self.couldron_slot1 = pygame.Surface((TILESIZE, TILESIZE))
        self.couldron_slot2 = pygame.Surface((TILESIZE, TILESIZE))
        self.coudron_timer = pygame.time.get_ticks()
        self.crafting_exp = 0.05
        
        pygame.display.set_caption('The Fateful Misadventures Of Flatman')
        pygame.display.set_icon(self.character_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE))
        

        self.intro_bg = pygame.image.load('img/sign.png')

        self.convo_text = ''
        self.text_timer = pygame.time.get_ticks()


        self.guard_1_convo = [
            'Guard - There\'s a Dogon up there, I can\'t let you through...',
            'Guard - Whoah!, you\'ve got stronger, mayebe you could help...'
        ]
        self.guard_1_convo_trigger = False

        self.sign_text = [
            'Sign - San Flat-Tonio; Heroic defender of the Isles of Flerror.',
            'Sign - Flat Top Mountain; The ruined shrine of the planewalkers.',
            'Blacksmith\'s; Upgrade your gear here! - Press \'E\' to enter',
            'Press \'X\' to exit',
            'Penny Orchard - Home of the Penny Red apple!'
        ]

        self.blacksmith_convo = [
            'Welcome, Traveller.  May I hone your axe? Stiffen your bow? - \'E\'',
            'Press \'1\' to upgrade your axe.  Press \'2\' to upgrade your bow',
            'You\'d like to upgrade your axe, that will be 100 gold. - \'E\'',
            'You\'d like to upgrade your bow, that will be 100 gold. - \'E\''
        ]

        self.farm_girl_convo_text = [
            'Hi there Traveller.  You look lost, can I help you in some way? - \'E\'',
            '\'1\' - I\'m Looking for work.    \'2\' - How do I get out of here?',
            'If you chop some logs and bring me them, I\'ll pay you well - \'E\'',
            'I have some logs for you. - \'E\' to sell logs.',
            'This place is a maze, be careful of the Badgers.'
        ]

        self.monument1_trigger = False
        self.flat_top_mountain_trigger = False
        self.blacksmith_trigger = False
        self.blacksmith = False
        self.blacksmith_convo_trigger = False
        self.blacksmith_upgrade_convo1 = False
        self.blacksmith_upgrade_axe = False
        self.blacksmith_upgrade_bow = False
        self.farm_girl_trigger = False
        self.farm_girl_trigger2 = False
        self.farm_girl_work_trigger = False
        self.farm_girl_work_trigger2 = False
        self.farm_girl_directions = False
        self.penny_orchard_sign = False

    def create_ground_map(self):
        for i, row in enumerate(ground_map):
            for j, col in enumerate(row):
                if col == 'w':
                    Water(self, j, i)
                if col == 'g':
                    Grass(self, j, i)
                if col == 'S':
                    Path1(self, j, i)
                if col == 's':
                    #   sand
                    Dirt(self, j, i)
                if col == 'd':
                    Dirt(self, j, i)
                if col == '-':
                    StoneFloor(self, j, i)

    def create_l2_map(self):
        for i, row in enumerate(layer2_map):
            for j, col in enumerate(row):
                if col == 'T':
                    Tree1(self, j, i)
                if col == 'M':
                    Mushroom(self, j, i)
                if col == 'L':
                    Logs(self, j, i)
                if col == '1':
                    WellStatic1(self, j, i)
                if col == '2':
                    WellStatic2(self, j, i)
                if col == '3':
                    WellStatic3(self, j, i)
                if col == '4':
                    WellStatic4(self, j, i)
                if col == 'A':
                    AxeBasic(self, j, i)
                if col == 'X':
                    Crossbow(self, j, i)
                if col == 'k':
                    StoneFloor(self, j, i)
                if col == 'i':
                    StoneFloorTop(self, j, i)
                if col == 'u':
                    StoneWallLeft(self, j, i)
                if col == 'o':
                    StoneWallRight(self, j, i)
                if col == 'j':
                    StoneBottomWallLeft(self, j, i)
                if col == 'l':
                    StoneBottomWallRight(self, j, i)
                if col == 'm':
                    StoneBottomWall(self,j, i)
                if col == 's':
                    StoneSteps(self, j, i)
                if col == 'p':
                    StoneFloor(self, j, i)
                    RuinedPillar(self, j, i)
                if col == 'G':
                    StoneFloor(self, j, i)
                    GuardHut(self, j, i)
                if col == '<':
                    StoneFloorBottomLeft(self, j, i)
                if col == '>':
                    StoneFloorBottomRight(self, j, i)
                if col == 'h':
                    HouseOne(self, j, i)
                if col == 'H':
                    HouseTwo(self, j, i)
                if col == '9':
                    LightHouse(self, j, i)
                if col == '8':
                    Monument1(self, j, i)
                if col == 'S':
                    SignPost(self, j, i)
                if col == ',':
                    Monument1SignTrigger(self, j, i)
                if col == '-':
                    StoneFloor(self, j, i)
                    FlatTopMountainSignTrigger(self, j, i)
                if col == 'v':
                    StaticShip(self, j, i)
                if col == 'B':
                    BlackSmithExt(self, j, i)
                if col == 'b':
                    BlackSmithTrigger(self, j, i)
                if col == 'a':
                    AppleTree(self, j, i)
                if col == '7':
                    PennyOrchardSignTrigger(self, j, i)

    def create_character_map(self):
        for i, row in enumerate(character_map):
            for j, col in enumerate(row):
                if col == 'P':
                    self.player = Player(self, j, i)
                if col == 'B':
                    Badger(self, j, i)
                if col == 'S':
                    Snake(self, j, i)
                if col == 'D':
                    Dogon(self, j, i)
                if col == 'K':
                    Knight(self, j, i)
                if col == 'G':
                    GuardKnight(self, j, i)
                if col == '1':
                    GuardTriggerOne(self, j, i)
                if col == 'F':
                    FarmGirl(self, j, i)
                if col == '2':
                    FarmGirlTrigger(self, j, i)

    def create_blacksmith_map(self):
        for i, row in enumerate(blacksmith_interior_tilemap):
            for j, col in enumerate(row):
                if col == 'f':
                    BlackSmithFloor(self, j, i)
                if col == 'l':
                    BlackSmithWallLeft(self, j, i)
                if col == 'r':
                    BlackSmithWallRight(self, j, i)
                if col == 't':
                    BlackSmithWallTop(self, j, i)
                if col == 'b':
                    BlackSmithWallBottom(self, j, i)
                if col == 'd':
                    BlackSmithIntDoor(self, j, i)

    def create_blacksmith_furniture_map(self):
        for i, row in enumerate(blacksmith_furniture_tilemap):
            for j, col in enumerate(row):
                if col == 'C':
                    ShopCounter(self ,j, i)
                if col == 'B':
                    WorkBench(self, j, i)
                if col == 'F':
                    Furnace(self, j, i)
                if col == 'S':
                    ShopKeep(self, j, i)
                if col == '1':
                    BlackSmithConvoTrigger(self, j, i)

    def new(self):
        #   start a new game
        self.playing = True
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.p_sprite_group = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.snakes = pygame.sprite.LayeredUpdates()
        self.badgers = pygame.sprite.LayeredUpdates()
        self.wells = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()
        self.mushrooms = pygame.sprite.LayeredUpdates()
        self.overlay_sprites = pygame.sprite.LayeredUpdates()
        self.logs = pygame.sprite.LayeredUpdates()
        self.dogon_attacks = pygame.sprite.LayeredUpdates()
        self.player_group = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.guard_trigger_1_sprite = pygame.sprite.LayeredUpdates()
        self.monument1_trigger_sprite = pygame.sprite.LayeredUpdates()
        self.flat_top_mountain_trigger_sprite = pygame.sprite.LayeredUpdates()
        self.blacksmith_int_sprites = pygame.sprite.LayeredUpdates()
        self.blacksmith_trigger_sprite = pygame.sprite.LayeredUpdates()
        self.blacksmith_convo_trigger_sprite = pygame.sprite.LayeredUpdates()
        self.farm_girl_trigger_sprite = pygame.sprite.LayeredUpdates()
        self.apple_trees = pygame.sprite.LayeredUpdates()
        self.penny_orchard_sign_trigger_sprite = pygame.sprite.LayeredUpdates()

        self.create_ground_map()
        self.create_l2_map()
        self.create_character_map()
        self.last = pygame.time.get_ticks()

        self.healthbar_images = [
            self.healthbar_spritesheet.get_sprite(0, 0, 600, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 540, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 480, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 420, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 360, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 300, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 240, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 180, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 120, 10),
            self.healthbar_spritesheet.get_sprite(0, 0, 60, 10)
        ]

        self.health_text = self.font.render('Health:', True, WHITE)
        self.health_text_rect = self.health_text.get_rect(x= 20, y= 570)

        self.inv_slot_1_image = pygame.Surface((TILESIZE, TILESIZE))
        self.inv_slot_2_image = pygame.Surface((TILESIZE, TILESIZE))
        self.inv_slot_3_image = pygame.Surface((TILESIZE, TILESIZE))
        self.inv_slot_4_image = pygame.Surface((TILESIZE, TILESIZE))
        self.inv_slot_5_image = pygame.Surface((TILESIZE, TILESIZE))
        self.inv_slot_1_image_rect = self.inv_slot_1_image.get_rect()
        self.inv_slot_2_image_rect = self.inv_slot_2_image.get_rect()
        self.inv_slot_3_image_rect = self.inv_slot_3_image.get_rect()
        self.inv_slot_4_image_rect = self.inv_slot_4_image.get_rect()
        self.inv_slot_5_image_rect = self.inv_slot_5_image.get_rect()

        self.level_text = self.font.render(f'Level: {math.floor(self.player.level)}', True, WHITE)
        self.level_text_rect = self.level_text.get_rect(x=740, y=170)
        self.dec_lvl =self.player.level - math.floor(self.player.level)
        self.pc_lvl = int(self.dec_lvl * 100)
        self.percent_complete_text = self.font_small.render(f'{self.pc_lvl}% to lvl {math.floor(self.player.level) + 1}.', True, WHITE)
        self.percent_complete_text_rect = self.percent_complete_text.get_rect(x= 740, y= 210)

        self.healthbar = self.healthbar_images[0]
        if self.player.pc_health > 90:
            self.healthbar = self.healthbar_images[0]
        elif self.player.pc_health == 90:
            self.healthbar = self.healthbar_images[1]
        elif self.player.pc_health >= 80:
            self.healthbar = self.healthbar_images[2]
        elif self.player.pc_health >= 70:
            self.healthbar = self.healthbar_images[3]
        elif self.player.pc_health >= 60:
            self.healthbar = self.healthbar_images[4]
        elif self.player.pc_health >= 50:
            self.healthbar = self.healthbar_images[5]
        elif self.player.pc_health >= 40:
            self.healthbar = self.healthbar_images[6]
        elif self.player.pc_health >= 30:
            self.healthbar = self.healthbar_images[7]
        elif self.player.pc_health >= 20:
            self.healthbar = self.healthbar_images[8]
        elif self.player.pc_health >= 10:
            self.healthbar = self.healthbar_images[9]

        self.slots_title = self.font.render('Weapons:', True, WHITE)
        self.slots_title_rect = self.slots_title.get_rect(x= 740, y= 40)

        self.weapon_slot_1_image = pygame.Surface((TILESIZE, TILESIZE))
        self.weapon_slot_1_image_rect = self.weapon_slot_1_image.get_rect()
        self.weapon_slot_1_image.blit(self.player.weapon_slot.inv[0].image, (0, 0))
        self.weapon_slot_1_image.set_colorkey(WHITE)
        self.slot_1_text = self.font_small.render(self.player.weapon_slot.inv[0].name, True, WHITE)
        self.slot_1_text_rect = self.slot_1_text.get_rect(x= 740, y= 80)

        self.weapon_slot_2_image = pygame.Surface((TILESIZE, TILESIZE))
        self.weapon_slot_2_image_rect = self.weapon_slot_2_image.get_rect()
        self.weapon_slot_2_image.blit(self.player.weapon_slot2.inv[0].image, (0, 0))
        self.weapon_slot_2_image.set_colorkey(WHITE)
        self.slot_2_text = self.font_small.render(self.player.weapon_slot2.inv[0].name, True, WHITE)
        self.slot_2_text_rect = self.slot_1_text.get_rect(x= 820, y= 80)

        
        
        self.inv_slot_1_image.blit(self.player.inventory.inv[0].image, (0, 0))
        self.inv_slot_1_image.set_colorkey(WHITE)
        self.inv_1_text = self.font_small.render(self.player.inventory.inv[0].name, True, WHITE)
        self.inv_1_text_rect = self.inv_1_text.get_rect(x= 110, y= 530)
        self.inv1_button = Button(110, 550, 50, 20, WHITE, BLACK, 'Use', 18)
        self.inv1_drop_button = Button(161, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
        self.inv_slot_2_image.blit(self.player.inventory.inv[1].image, (0, 0))
        self.inv_slot_2_image.set_colorkey(WHITE)
        self.inv_2_text = self.font_small.render(self.player.inventory.inv[1].name, True, WHITE)
        self.inv_2_text_rect = self.inv_2_text.get_rect(x= 230, y= 530)
        self.inv2_button = Button(230, 550, 50, 20, WHITE, BLACK, 'Use', 18)
        self.inv2_drop_button = Button(281, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
        self.inv_slot_3_image.blit(self.player.inventory.inv[2].image, (0, 0))
        self.inv_slot_3_image.set_colorkey(WHITE)
        self.inv_3_text = self.font_small.render(self.player.inventory.inv[2].name, True, WHITE)
        self.inv_3_text_rect = self.inv_3_text.get_rect(x= 350, y= 530)
        self.inv3_button = Button(350, 550, 50, 20, WHITE, BLACK, 'Use', 18)
        self.inv3_drop_button = Button(401, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
        self.inv_slot_4_image.blit(self.player.inventory.inv[3].image, (0, 0))
        self.inv_slot_4_image.set_colorkey(WHITE)
        self.inv_4_text = self.font_small.render(self.player.inventory.inv[3].name, True, WHITE)
        self.inv_4_text_rect = self.inv_4_text.get_rect(x= 470, y= 530)
        self.inv4_button = Button(470, 550, 50, 20, WHITE, BLACK, 'Use', 18)
        self.inv4_drop_button = Button(521, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
        self.inv_slot_5_image.blit(self.player.inventory.inv[4].image, (0, 0))
        self.inv_slot_5_image.set_colorkey(WHITE)
        self.inv_5_text = self.font_small.render(self.player.inventory.inv[4].name, True, WHITE)
        self.inv_5_text_rect = self.inv_5_text.get_rect(x= 590, y= 530)
        self.inv5_button = Button(590, 550, 50, 20, WHITE, BLACK, 'Use', 18)
        self.inv5_drop_button = Button(641, 550, 50, 20, WHITE, BLACK, 'Drop', 18)

        self.couldron_title = self.font.render('Couldron:', True, WHITE)
        self.couldron_title_rect = self.couldron_title.get_rect(x= 740, y= 240)

        self.couldron_slot1_text = self.font_small.render(f'{self.player.couldron.inv[0].name}', True, WHITE)
        self.couldron_slot1_text_rect = self.couldron_slot1.get_rect(x= 740, y= 280)
        
        self.couldron_slot1.blit(self.player.couldron.inv[0].image, (0, 0))
        self.couldron_slot1.set_colorkey(WHITE)

        self.couldron_slot2_text = self.font_small.render(f'{self.player.couldron.inv[1].name}', True, WHITE)
        self.couldron_slot2_text_rect = self.couldron_slot2.get_rect(x= 820, y= 280)
        
        self.couldron_slot2.blit(self.player.couldron.inv[1].image, (0, 0))
        self.couldron_slot2.set_colorkey(WHITE)

        self.make_button = Button(740, 340, 50, 20, WHITE, BLACK, 'Cook', 16)
        self.clear_button = Button(820, 340, 50, 20, WHITE, BLACK, 'Clear', 16)

        self.convo_text_disp = self.font_smaller.render(self.convo_text, True, (180, 180, 180))
        self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=460)

        self.player_cash_disp = self.font.render(f'Gold: {self.player.gold}', True, (180, 180, 180))
        self.player_cash_disp_rect = self.player_cash_disp.get_rect(x=750, y=445)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.armed_melee:
                        if self.player.facing == 'up':
                            MeleeAttack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                        if self.player.facing == 'down':
                            MeleeAttack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                        if self.player.facing == 'left':
                            MeleeAttack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                        if self.player.facing == 'right':
                            MeleeAttack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
                if event.key == pygame.K_b:
                    if self.player.armed_ranged:
                        if self.player.facing == 'up':
                            if self.player.weapon_slot2.inv[0].name == 'Crossbow':
                                RangedAttackY(self, self.player.rect.x, self.player.rect.y - 75)
                            elif self.player.weapon_slot2.inv[0].name == 'Longbow':
                                LongRangedAttackY(self, self.player.rect.x, self.player.rect.y - 100)
                        if self.player.facing == 'down':
                            if self.player.weapon_slot2.inv[0].name == 'Crossbow':
                                RangedAttackY(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                            elif self.player.weapon_slot2.inv[0].name == 'Longbow':
                                LongRangedAttackY(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                        if self.player.facing == 'left':
                            if self.player.weapon_slot2.inv[0].name == 'Crossbow':
                                RangedAttackX(self, self.player.rect.x - 75, self.player.rect.y)
                            elif self.player.weapon_slot2.inv[0].name == 'Longbow':
                                LongRangedAttackX(self, self.player.rect.x - 100, self.player.rect.y)
                        if self.player.facing == 'right':
                            if self.player.weapon_slot2.inv[0].name == 'Crossbow':
                                RangedAttackX(self, self.player.rect.x + TILESIZE, self.player.rect.y)
                            elif self.player.weapon_slot2.inv[0].name == 'Longbow':
                                RangedAttackX(self, self.player.rect.x + TILESIZE, self.player.rect.y)


        if self.player.health <= 0:
            self.playing = False

        #   get click and pos events and button logic here
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.inv1_button.is_pressed(mouse_pos, mouse_pressed):
            if self.player.inventory.inv[0].name == 'Mushroom':
                self.player.couldron.add_item(item_list[0])
                self.player.inventory.inv.pop(0)
                self.player.inventory.inv.insert(0, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[0].name == 'Logs':
                self.player.couldron.add_item(item_list[1])
                self.player.inventory.inv.pop(0)
                self.player.inventory.inv.insert(0, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[0].name == 'Mushtew':
                self.player.health += 30
                self.player.inventory.inv.pop(0)
                self.player.inventory.inv.insert(0, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[0].name == 'Apple':
                self.player.health += 4
                self.player.inventory.inv.pop(0)
                self.player.inventory.inv.insert(0, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            
        if self.inv1_drop_button.is_pressed(mouse_pos, mouse_pressed):
            self.player.inventory.inv.pop(0)
            self.player.inventory.inv.insert(0, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            
        if self.inv2_button.is_pressed(mouse_pos, mouse_pressed):
            if self.player.inventory.inv[1].name == 'Mushroom':
                self.player.couldron.add_item(item_list[0])
                self.player.inventory.inv.pop(1)
                self.player.inventory.inv.insert(1, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[1].name == 'Logs':
                self.player.couldron.add_item(item_list[1])
                self.player.inventory.inv.pop(1)
                self.player.inventory.inv.insert(1, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[1].name == 'Mushtew':
                self.player.health += 30
                self.player.inventory.inv.pop(1)
                self.player.inventory.inv.insert(1, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[1].name == 'Apple':
                self.player.health += 4
                self.player.inventory.inv.pop(1)
                self.player.inventory.inv.insert(1, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            

        if self.inv2_drop_button.is_pressed(mouse_pos, mouse_pressed):
            self.player.inventory.inv.pop(1)
            self.player.inventory.inv.insert(1, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
        

        if self.inv3_button.is_pressed(mouse_pos, mouse_pressed):
            if self.player.inventory.inv[2].name == 'Mushroom':
                self.player.couldron.add_item(item_list[0])
                self.player.inventory.inv.pop(2)
                self.player.inventory.inv.insert(2, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[2].name == 'Logs':
                self.player.couldron.add_item(item_list[1])
                self.player.inventory.inv.pop(2)
                self.player.inventory.inv.insert(2, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[2].name == 'Mushtew':
                self.player.health += 30
                self.player.inventory.inv.pop(2)
                self.player.inventory.inv.insert(2, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[2].name == 'Apple':
                self.player.health += 4
                self.player.inventory.inv.pop(2)
                self.player.inventory.inv.insert(2, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            

        if self.inv3_drop_button.is_pressed(mouse_pos, mouse_pressed):
            self.player.inventory.inv.pop(2)
            self.player.inventory.inv.insert(2, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))

        if self.inv4_button.is_pressed(mouse_pos, mouse_pressed):
            if self.player.inventory.inv[3].name == 'Mushroom':
                self.player.couldron.add_item(item_list[0])
                self.player.inventory.inv.pop(3)
                self.player.inventory.inv.insert(3, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[3].name == 'Logs':
                self.player.couldron.add_item(item_list[1])
                self.player.inventory.inv.pop(3)
                self.player.inventory.inv.insert(3, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[3].name == 'Mushtew':
                self.player.health += 30
                self.player.inventory.inv.pop(3)
                self.player.inventory.inv.insert(3, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[3].name == 'Apple':
                self.player.health += 4
                self.player.inventory.inv.pop(3)
                self.player.inventory.inv.insert(3, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            
        if self.inv4_drop_button.is_pressed(mouse_pos, mouse_pressed):
            self.player.inventory.inv.pop(3)
            self.player.inventory.inv.insert(3, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))

        if self.inv5_button.is_pressed(mouse_pos, mouse_pressed):
            if self.player.inventory.inv[4].name == 'Mushroom':
                self.player.couldron.add_item(item_list[0])
                self.player.inventory.inv.pop(4)
                self.player.inventory.inv.insert(4, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[4].name == 'Logs':
                self.player.couldron.add_item(item_list[1])
                self.player.inventory.inv.pop(4)
                self.player.inventory.inv.insert(4, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[4].name == 'Mushtew':
                self.player.health += 30
                self.player.inventory.inv.pop(4)
                self.player.inventory.inv.insert(4, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            if self.player.inventory.inv[4].name == 'Apple':
                self.player.health += 4
                self.player.inventory.inv.pop(4)
                self.player.inventory.inv.insert(4, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))

        if self.inv5_drop_button.is_pressed(mouse_pos, mouse_pressed):
            self.player.inventory.inv.pop(4)
            self.player.inventory.inv.insert(4, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))

        if self.make_button.is_pressed(mouse_pos, mouse_pressed):

            #   check couldron slots

            if self.player.couldron.inv[0].name == 'Mushroom':
                self.couldron_mushroom = True
            if self.player.couldron.inv[0].name == 'Logs':
                self.couldron_logs = True


            if self.player.couldron.inv[1].name == 'Mushroom':
                self.couldron_mushroom = True
            if self.player.couldron.inv[1].name == 'Logs':
                self.couldron_logs = True

            
            #   Mushtew recipe
            now = pygame.time.get_ticks()
            if now - self.coudron_timer >= 500:

                if self.couldron_mushroom and self.couldron_logs:
                    self.player.inventory.add_item(item_list[2])
                    self.player.couldron.inv.clear()
                    self.player.couldron.inv.insert(0, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
                    self.player.couldron.inv.insert(1, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
                    if self.player.level <= 9:
                        self.crafting_exp_final = self.crafting_exp
                    elif self.player.level <= 19:
                        self.crafting_exp_final = self.crafting_exp/2
                    elif self.player.level <= 29:
                        self.crafting_exp_final = self.crafting_exp/3
                    elif self.player.level <= 39:
                        self.crafting_exp_final = self.crafting_exp/4
                    elif self.player.level <= 49:
                        self.crafting_exp_final = self.crafting_exp/5
                    elif self.player.level <= 69:
                        self.crafting_exp_final = self.crafting_exp/6
                    elif self.player.level <= 99:
                        self.crafting_exp_final = self.crafting_exp/10

                    self.player.level += self.crafting_exp_final

                #   More recipes here

            self.coudron_timer = now

            #    More recipes here

        if self.clear_button.is_pressed(mouse_pos, mouse_pressed):
            self.player.couldron.inv.clear()
            self.player.couldron.inv.insert(0, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))
            self.player.couldron.inv.insert(1, ItemStats('EMPTY', pygame.image.load('img/empty.png'), 0, 0, False, False, False, False))

    def update(self):

        self.all_sprites.update()
        self.overlay_sprites.update()
        
        #   conversation logic

        if self.guard_1_convo_trigger:
            if self.player.level < 5:
                now = pygame.time.get_ticks()
                self.convo_text_disp = self.font_mid.render(self.guard_1_convo[0], True, (BLACK))
                self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
                # make it go away after
                if now - self.text_timer >= 5000:
                    self.guard_1_convo_trigger == False
                    self.text_timer = now
        
            if self.player.level >= 5:
                now = pygame.time.get_ticks()
                self.convo_text_disp = self.font_mid.render(self.guard_1_convo[1], True, (BLACK))
                self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
                # make it go away after
                if now - self.text_timer >= 5000:
                    self.guard_1_convo_trigger == False
                    self.text_timer = now
        
        if self.monument1_trigger:
            now = pygame.time.get_ticks()
            self.convo_text_disp = self.font_mid.render(self.sign_text[0], True, (BLACK))
            self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
            # make it go away after
            if now - self.text_timer >= 5000:
                self.monument1_trigger == False
                self.text_timer = now

        if self.flat_top_mountain_trigger:
            now = pygame.time.get_ticks()
            self.convo_text_disp = self.font_mid.render(self.sign_text[1], True, (BLACK))
            self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
            # make it go away after
            if now - self.text_timer >= 5000:
                self.flat_top_mountain_trigger == False
                self.text_timer = now

        if self.blacksmith_trigger:
            now = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            self.convo_text_disp = self.font_mid.render(self.sign_text[2], True, (BLACK))
            self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
            if keys[pygame.K_e]:
                self.blacksmith_int_scene()
                self.convo_text_disp = self.font_mid.render('', True, (BLACK))
            if now - self.text_timer >= 5000:
                self.blacksmith_trigger == False
                self.text_timer = now

        if self.farm_girl_trigger:
            now = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            self.convo_text_disp = self.font_mid.render(self.farm_girl_convo_text[0], True, (BLACK))
            self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
            if keys[pygame.K_e]:
                self.farm_girl_trigger2 = True
                
            if self.farm_girl_trigger2:
                
                self.convo_text_disp = self.font_mid.render(self.farm_girl_convo_text[1], True, (BLACK))
                self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)

                if keys[pygame.K_1]:
                    self.farm_girl_work_trigger = True

                if keys[pygame.K_2]:
                    self.farm_girl_directions = True

                if self.farm_girl_work_trigger:
                    
                    self.convo_text_disp = self.font_mid.render(self.farm_girl_convo_text[2], True, (BLACK))
                    self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)

                    if keys[pygame.K_e]:
                        self.farm_girl_work_trigger2 = True

                    if self.farm_girl_work_trigger2:
                        
                        self.convo_text_disp = self.font_mid.render(self.farm_girl_convo_text[3], True, (BLACK))
                        self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
                        now = pygame.time.get_ticks()
                        if keys[pygame.K_e]:
                            if now - self.text_timer >= 300:
                                for item in self.player.inventory.inv:
                                    if item.name == 'Logs':
                                        self.player.inventory.drop_item(item)
                                        self.player.gold += 10
                                self.text_timer = now
                                

                if self.farm_girl_directions:

                    self.convo_text_disp = self.font_mid.render(self.farm_girl_convo_text[4], True, (BLACK))
                    self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
        else:
            self.farm_girl_trigger2 = False
            self.farm_girl_work_trigger = False
            self.farm_girl_work_trigger2 = False
            self.farm_girl_directions = False

        self.penny_orchard_sign == False
        if self.penny_orchard_sign:
            now = pygame.time.get_ticks()
            self.convo_text_disp = self.font_mid.render(self.sign_text[4], True, (BLACK))
            self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
            if now - self.text_timer >= 5000:
                self.penny_orchard_sign == False
                self.convo_text_disp = self.font_mid.render('', True, (BLACK))
                self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
                self.text_timer = now

        

        #   overlay items that needs to update variables
        now = pygame.time.get_ticks()
        if now - self.last >= 1000:

            self.level_text = self.font.render(f'Level: {math.floor(self.player.level)}', True, WHITE)
            self.level_text_rect = self.level_text.get_rect(x=740, y=170)
            self.dec_lvl =self.player.level - math.floor(self.player.level)
            self.pc_lvl = int(self.dec_lvl * 100)
            self.percent_complete_text = self.font_small.render(f'{self.pc_lvl}% to lvl {math.floor(self.player.level) + 1}.', True, WHITE)
            self.percent_complete_text_rect = self.percent_complete_text.get_rect(x= 740, y= 210)

            self.slots_title = self.font.render('Weapons:', True, WHITE)
            self.slots_title_rect = self.slots_title.get_rect(x= 740, y= 40)

            self.weapon_slot_1_image = pygame.Surface((TILESIZE, TILESIZE))
            self.weapon_slot_1_image_rect = self.weapon_slot_1_image.get_rect()
            self.weapon_slot_1_image.blit(self.player.weapon_slot.inv[0].image, (0, 0))
            self.weapon_slot_1_image.set_colorkey(WHITE)
            self.slot_1_text = self.font_small.render(self.player.weapon_slot.inv[0].name, True, WHITE)
            self.slot_1_text_rect = self.slot_1_text.get_rect(x= 740, y= 80)

            self.weapon_slot_2_image = pygame.Surface((TILESIZE, TILESIZE))
            self.weapon_slot_2_image_rect = self.weapon_slot_2_image.get_rect()
            self.weapon_slot_2_image.blit(self.player.weapon_slot2.inv[0].image, (0, 0))
            self.weapon_slot_2_image.set_colorkey(WHITE)
            self.slot_2_text = self.font_small.render(self.player.weapon_slot2.inv[0].name, True, WHITE)
            self.slot_2_text_rect = self.slot_1_text.get_rect(x= 820, y= 80)

            self.convo_text_disp = self.font_smaller.render(self.convo_text, True, (180, 180, 180))
            self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=460)
        
            self.inv_slot_1_image.blit(self.player.inventory.inv[0].image, (0, 0))
            self.inv_slot_1_image.set_colorkey(WHITE)
            self.inv_1_text = self.font_small.render(self.player.inventory.inv[0].name, True, WHITE)
            self.inv_1_text_rect = self.inv_1_text.get_rect(x= 110, y= 530)
            self.inv1_button = Button(110, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv1_drop_button = Button(161, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
            self.inv_slot_2_image.blit(self.player.inventory.inv[1].image, (0, 0))
            self.inv_slot_2_image.set_colorkey(WHITE)
            self.inv_2_text = self.font_small.render(self.player.inventory.inv[1].name, True, WHITE)
            self.inv_2_text_rect = self.inv_2_text.get_rect(x= 230, y= 530)
            self.inv2_button = Button(230, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv2_drop_button = Button(281, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
            self.inv_slot_3_image.blit(self.player.inventory.inv[2].image, (0, 0))
            self.inv_slot_3_image.set_colorkey(WHITE)
            self.inv_3_text = self.font_small.render(self.player.inventory.inv[2].name, True, WHITE)
            self.inv_3_text_rect = self.inv_3_text.get_rect(x= 350, y= 530)
            self.inv3_button = Button(350, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv3_drop_button = Button(401, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
            self.inv_slot_4_image.blit(self.player.inventory.inv[3].image, (0, 0))
            self.inv_slot_4_image.set_colorkey(WHITE)
            self.inv_4_text = self.font_small.render(self.player.inventory.inv[3].name, True, WHITE)
            self.inv_4_text_rect = self.inv_4_text.get_rect(x= 470, y= 530)
            self.inv4_button = Button(470, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv4_drop_button = Button(521, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
            self.inv_slot_5_image.blit(self.player.inventory.inv[4].image, (0, 0))
            self.inv_slot_5_image.set_colorkey(WHITE)
            self.inv_5_text = self.font_small.render(self.player.inventory.inv[4].name, True, WHITE)
            self.inv_5_text_rect = self.inv_5_text.get_rect(x= 590, y= 530)
            self.inv5_button = Button(590, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv5_drop_button = Button(641, 550, 50, 20, WHITE, BLACK, 'Drop', 18)

            self.couldron_slot1_text = self.font_small.render(f'{self.player.couldron.inv[0].name}', True, WHITE)
            self.couldron_slot1_text_rect = self.couldron_slot1.get_rect(x= 740, y= 280)
            self.couldron_slot1 = pygame.Surface((TILESIZE, TILESIZE))
            self.couldron_slot1.blit(self.player.couldron.inv[0].image, (0, 0))
            self.couldron_slot1.set_colorkey(WHITE)

            self.couldron_slot2_text = self.font_small.render(f'{self.player.couldron.inv[1].name}', True, WHITE)
            self.couldron_slot2_text_rect = self.couldron_slot2.get_rect(x= 820, y= 280)
            self.couldron_slot2 = pygame.Surface((TILESIZE, TILESIZE))
            self.couldron_slot2.blit(self.player.couldron.inv[1].image, (0, 0))
            self.couldron_slot2.set_colorkey(WHITE)

            self.make_button = Button(740, 340, 50, 20, WHITE, BLACK, 'Cook', 16)
            self.clear_button = Button(820, 340, 50, 20, WHITE, BLACK, 'Clear', 16)

            self.player_cash_disp = self.font.render(f'Gold: {self.player.gold}', True, (180, 180, 180))
            self.player_cash_disp_rect = self.player_cash_disp.get_rect(x=750, y=445)

            self.last = now

        self.healthbar = self.healthbar_images[0]
        if self.player.pc_health > 90:
            self.healthbar = self.healthbar_images[0]
        elif self.player.pc_health == 90:
            self.healthbar = self.healthbar_images[1]
        elif self.player.pc_health >= 80:
            self.healthbar = self.healthbar_images[2]
        elif self.player.pc_health >= 70:
            self.healthbar = self.healthbar_images[3]
        elif self.player.pc_health >= 60:
            self.healthbar = self.healthbar_images[4]
        elif self.player.pc_health >= 50:
            self.healthbar = self.healthbar_images[5]
        elif self.player.pc_health >= 40:
            self.healthbar = self.healthbar_images[6]
        elif self.player.pc_health >= 30:
            self.healthbar = self.healthbar_images[7]
        elif self.player.pc_health >= 20:
            self.healthbar = self.healthbar_images[8]
        elif self.player.pc_health >= 10:
            self.healthbar = self.healthbar_images[9]

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        

        #   draw overlay
        

        self.screen.blit(self.overlay_bg, (0, 0))
        self.screen.blit(self.overlay_title, self.overlay_title_rect)
        self.screen.blit(self.level_text, self.level_text_rect)
        self.screen.blit(self.healthbar, (100, 580))
        self.screen.blit(self.health_text, self.health_text_rect)

        self.screen.blit(self.weapon_slot_1_image, (760, 100))
        self.screen.blit(self.slot_1_text, self.slot_1_text_rect)
        self.screen.blit(self.weapon_slot_2_image, (840, 100))
        self.screen.blit(self.slot_2_text, self.slot_2_text_rect)
        self.screen.blit(self.slots_title, self.slots_title_rect)

        self.screen.blit(self.inv_slot_1_image, (120, 500))
        self.screen.blit(self.inv_1_text, self.inv_1_text_rect)
        self.screen.blit(self.inv1_button.image, self.inv1_button.rect)
        self.screen.blit(self.inv1_drop_button.image, self.inv1_drop_button.rect)

        self.screen.blit(self.inv_slot_2_image, (240, 500))
        self.screen.blit(self.inv_2_text, self.inv_2_text_rect)
        self.screen.blit(self.inv2_button.image, self.inv2_button.rect)
        self.screen.blit(self.inv2_drop_button.image, self.inv2_drop_button.rect)

        self.screen.blit(self.inv_slot_3_image, (360, 500))
        self.screen.blit(self.inv_3_text, self.inv_3_text_rect)
        self.screen.blit(self.inv3_button.image, self.inv3_button.rect)
        self.screen.blit(self.inv3_drop_button.image, self.inv3_drop_button.rect)

        self.screen.blit(self.inv_slot_4_image, (480, 500))
        self.screen.blit(self.inv_4_text, self.inv_4_text_rect)
        self.screen.blit(self.inv4_button.image, self.inv4_button.rect)
        self.screen.blit(self.inv4_drop_button.image, self.inv4_drop_button.rect)

        self.screen.blit(self.inv_slot_5_image, (600, 500))
        self.screen.blit(self.inv_5_text, self.inv_5_text_rect)
        self.screen.blit(self.inv5_button.image, self.inv5_button.rect)
        self.screen.blit(self.inv5_drop_button.image, self.inv5_drop_button.rect)

        self.screen.blit(self.percent_complete_text, self.percent_complete_text_rect)

        self.screen.blit(self.couldron_title, self.couldron_title_rect)
        self.screen.blit(self.couldron_slot1_text, self.couldron_slot1_text_rect)
        self.screen.blit(self.couldron_slot1, (760, 300))
        self.screen.blit(self.couldron_slot2_text, self.couldron_slot2_text_rect)
        self.screen.blit(self.couldron_slot2, (840, 300))
        self.screen.blit(self.make_button.image, self.make_button.rect)
        self.screen.blit(self.clear_button.image, self.clear_button.rect)

        self.screen.blit(self.convo_text_disp, self.convo_text_disp_rect)

        self.screen.blit(self.player_cash_disp, self.player_cash_disp_rect)

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        intro = True

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)
        title = self.font.render('The Fateful Misadventures of Flatman', True, WHITE)
        title_rect = title.get_rect(x=10, y=10)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_bg, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def blacksmith_int_scene(self):
        self.blacksmith = True
        

        self.create_blacksmith_map()
        self.create_blacksmith_furniture_map()

        while self.blacksmith:
            self.blacksmith_trigger = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.blacksmith = False
                    self.playing = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()

            self.convo_text_disp = self.font_mid.render('', True, (BLACK))
            self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)

            if self.player.facing == 'down':
                self.convo_text_disp = self.font_mid.render(self.sign_text[3], True, (BLACK))
                self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
            #   leave shop                

            if keys[pygame.K_x]:
                self.blacksmith = False
                for sprite in self.blacksmith_int_sprites:
                    sprite.kill()

            #   update

            self.update_blacksmith_interior()

            #   Draw


            self.draw_blacksmith_interior()

            
            self.clock.tick(FPS)
            pygame.display.update()

    def draw_blacksmith_interior(self):
        self.screen.fill(BLACK)
        self.blacksmith_int_sprites.draw(self.screen)
        self.player_group.draw(self.screen)
        

        #   draw overlay
        

        self.screen.blit(self.overlay_bg, (0, 0))
        self.screen.blit(self.overlay_title, self.overlay_title_rect)
        self.screen.blit(self.level_text, self.level_text_rect)
        self.screen.blit(self.healthbar, (100, 580))
        self.screen.blit(self.health_text, self.health_text_rect)

        self.screen.blit(self.weapon_slot_1_image, (760, 100))
        self.screen.blit(self.slot_1_text, self.slot_1_text_rect)
        self.screen.blit(self.weapon_slot_2_image, (840, 100))
        self.screen.blit(self.slot_2_text, self.slot_2_text_rect)
        self.screen.blit(self.slots_title, self.slots_title_rect)

        self.screen.blit(self.inv_slot_1_image, (120, 500))
        self.screen.blit(self.inv_1_text, self.inv_1_text_rect)
        self.screen.blit(self.inv1_button.image, self.inv1_button.rect)
        self.screen.blit(self.inv1_drop_button.image, self.inv1_drop_button.rect)

        self.screen.blit(self.inv_slot_2_image, (240, 500))
        self.screen.blit(self.inv_2_text, self.inv_2_text_rect)
        self.screen.blit(self.inv2_button.image, self.inv2_button.rect)
        self.screen.blit(self.inv2_drop_button.image, self.inv2_drop_button.rect)

        self.screen.blit(self.inv_slot_3_image, (360, 500))
        self.screen.blit(self.inv_3_text, self.inv_3_text_rect)
        self.screen.blit(self.inv3_button.image, self.inv3_button.rect)
        self.screen.blit(self.inv3_drop_button.image, self.inv3_drop_button.rect)

        self.screen.blit(self.inv_slot_4_image, (480, 500))
        self.screen.blit(self.inv_4_text, self.inv_4_text_rect)
        self.screen.blit(self.inv4_button.image, self.inv4_button.rect)
        self.screen.blit(self.inv4_drop_button.image, self.inv4_drop_button.rect)

        self.screen.blit(self.inv_slot_5_image, (600, 500))
        self.screen.blit(self.inv_5_text, self.inv_5_text_rect)
        self.screen.blit(self.inv5_button.image, self.inv5_button.rect)
        self.screen.blit(self.inv5_drop_button.image, self.inv5_drop_button.rect)

        self.screen.blit(self.percent_complete_text, self.percent_complete_text_rect)

        self.screen.blit(self.couldron_title, self.couldron_title_rect)
        self.screen.blit(self.couldron_slot1_text, self.couldron_slot1_text_rect)
        self.screen.blit(self.couldron_slot1, (760, 300))
        self.screen.blit(self.couldron_slot2_text, self.couldron_slot2_text_rect)
        self.screen.blit(self.couldron_slot2, (840, 300))
        self.screen.blit(self.make_button.image, self.make_button.rect)
        self.screen.blit(self.clear_button.image, self.clear_button.rect)

        self.screen.blit(self.convo_text_disp, self.convo_text_disp_rect)

        self.screen.blit(self.player_cash_disp, self.player_cash_disp_rect)

        self.clock.tick(FPS)
        pygame.display.update()

    def update_blacksmith_interior(self):

            
        self.overlay_sprites.update()
        self.blacksmith_int_sprites.update()
        self.player_group.update()

        #   conversation logic

        if self.blacksmith_convo_trigger:
            now = pygame.time.get_ticks()
            
            keys = pygame.key.get_pressed()
            self.convo_text_disp = self.font_mid.render(self.blacksmith_convo[0], True, (BLACK))
            self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
            if keys[pygame.K_e]:
                self.blacksmith_upgrade_convo1 = True
            if self.blacksmith_upgrade_convo1:
                self.convo_text_disp = self.font_mid.render(self.blacksmith_convo[1], True, (BLACK))
                self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
                
                if keys[pygame.K_1]:
                    self.blacksmith_upgrade_axe = True
                if keys[pygame.K_2]:
                    self.blacksmith_upgrade_bow = True

            #   Axe upgrade

            if self.blacksmith_upgrade_axe:
                self.blacksmith_upgrade_convo1 = False
                self.convo_text_disp = self.font_mid.render(self.blacksmith_convo[2], True, (BLACK))
                self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
                if keys[pygame.K_e]:
                    if self.player.gold >= 100:
                        if self.player.weapon_slot.inv[0].name == 'Axe - Basic':
                            self.player.weapon_slot.add_item(weapon_list[2])
                            self.player.gold -= 100
                            self.blacksmith_upgrade_axe = False

            #   Bow upgrade
                
            if self.blacksmith_upgrade_bow:
                self.blacksmith_upgrade_convo1 = False
                self.convo_text_disp = self.font_mid.render(self.blacksmith_convo[3], True, (BLACK))
                self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=448)
                if keys[pygame.K_e]:
                    if self.player.gold >= 100:
                        if self.player.weapon_slot2.inv[0].name == 'Crossbow':
                            self.player.weapon_slot2.add_item(weapon_list[3])
                            self.player.gold -= 100
                            self.blacksmith_upgrade_bow = False


            # make it go away after
            if now - self.text_timer >= 5000:
                self.text_timer = now
        
        else:
            self.blacksmith_upgrade_convo1 = False
            self.blacksmith_upgrade_axe = False
            self.blacksmith_upgrade_bow = False

        #   overlay items that needs to update variables
        now = pygame.time.get_ticks()
        if now - self.last >= 1000:

            self.level_text = self.font.render(f'Level: {math.floor(self.player.level)}', True, WHITE)
            self.level_text_rect = self.level_text.get_rect(x=740, y=170)
            self.dec_lvl =self.player.level - math.floor(self.player.level)
            self.pc_lvl = int(self.dec_lvl * 100)
            self.percent_complete_text = self.font_small.render(f'{self.pc_lvl}% to lvl {math.floor(self.player.level) + 1}.', True, WHITE)
            self.percent_complete_text_rect = self.percent_complete_text.get_rect(x= 740, y= 210)

            self.slots_title = self.font.render('Weapons:', True, WHITE)
            self.slots_title_rect = self.slots_title.get_rect(x= 740, y= 40)

            self.weapon_slot_1_image = pygame.Surface((TILESIZE, TILESIZE))
            self.weapon_slot_1_image_rect = self.weapon_slot_1_image.get_rect()
            self.weapon_slot_1_image.blit(self.player.weapon_slot.inv[0].image, (0, 0))
            self.weapon_slot_1_image.set_colorkey(WHITE)
            self.slot_1_text = self.font_small.render(self.player.weapon_slot.inv[0].name, True, WHITE)
            self.slot_1_text_rect = self.slot_1_text.get_rect(x= 740, y= 80)

            self.weapon_slot_2_image = pygame.Surface((TILESIZE, TILESIZE))
            self.weapon_slot_2_image_rect = self.weapon_slot_2_image.get_rect()
            self.weapon_slot_2_image.blit(self.player.weapon_slot2.inv[0].image, (0, 0))
            self.weapon_slot_2_image.set_colorkey(WHITE)
            self.slot_2_text = self.font_small.render(self.player.weapon_slot2.inv[0].name, True, WHITE)
            self.slot_2_text_rect = self.slot_1_text.get_rect(x= 820, y= 80)

            self.convo_text_disp = self.font_smaller.render(self.convo_text, True, (180, 180, 180))
            self.convo_text_disp_rect = self.convo_text_disp.get_rect(x=110, y=460)
        
            self.inv_slot_1_image.blit(self.player.inventory.inv[0].image, (0, 0))
            self.inv_slot_1_image.set_colorkey(WHITE)
            self.inv_1_text = self.font_small.render(self.player.inventory.inv[0].name, True, WHITE)
            self.inv_1_text_rect = self.inv_1_text.get_rect(x= 110, y= 530)
            self.inv1_button = Button(110, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv1_drop_button = Button(161, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
            self.inv_slot_2_image.blit(self.player.inventory.inv[1].image, (0, 0))
            self.inv_slot_2_image.set_colorkey(WHITE)
            self.inv_2_text = self.font_small.render(self.player.inventory.inv[1].name, True, WHITE)
            self.inv_2_text_rect = self.inv_2_text.get_rect(x= 230, y= 530)
            self.inv2_button = Button(230, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv2_drop_button = Button(281, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
            self.inv_slot_3_image.blit(self.player.inventory.inv[2].image, (0, 0))
            self.inv_slot_3_image.set_colorkey(WHITE)
            self.inv_3_text = self.font_small.render(self.player.inventory.inv[2].name, True, WHITE)
            self.inv_3_text_rect = self.inv_3_text.get_rect(x= 350, y= 530)
            self.inv3_button = Button(350, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv3_drop_button = Button(401, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
            self.inv_slot_4_image.blit(self.player.inventory.inv[3].image, (0, 0))
            self.inv_slot_4_image.set_colorkey(WHITE)
            self.inv_4_text = self.font_small.render(self.player.inventory.inv[3].name, True, WHITE)
            self.inv_4_text_rect = self.inv_4_text.get_rect(x= 470, y= 530)
            self.inv4_button = Button(470, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv4_drop_button = Button(521, 550, 50, 20, WHITE, BLACK, 'Drop', 18)
        
        
            self.inv_slot_5_image.blit(self.player.inventory.inv[4].image, (0, 0))
            self.inv_slot_5_image.set_colorkey(WHITE)
            self.inv_5_text = self.font_small.render(self.player.inventory.inv[4].name, True, WHITE)
            self.inv_5_text_rect = self.inv_5_text.get_rect(x= 590, y= 530)
            self.inv5_button = Button(590, 550, 50, 20, WHITE, BLACK, 'Use', 18)
            self.inv5_drop_button = Button(641, 550, 50, 20, WHITE, BLACK, 'Drop', 18)

            self.couldron_slot1_text = self.font_small.render(f'{self.player.couldron.inv[0].name}', True, WHITE)
            self.couldron_slot1_text_rect = self.couldron_slot1.get_rect(x= 740, y= 280)
            self.couldron_slot1 = pygame.Surface((TILESIZE, TILESIZE))
            self.couldron_slot1.blit(self.player.couldron.inv[0].image, (0, 0))
            self.couldron_slot1.set_colorkey(WHITE)

            self.couldron_slot2_text = self.font_small.render(f'{self.player.couldron.inv[1].name}', True, WHITE)
            self.couldron_slot2_text_rect = self.couldron_slot2.get_rect(x= 820, y= 280)
            self.couldron_slot2 = pygame.Surface((TILESIZE, TILESIZE))
            self.couldron_slot2.blit(self.player.couldron.inv[1].image, (0, 0))
            self.couldron_slot2.set_colorkey(WHITE)

            self.make_button = Button(740, 340, 50, 20, WHITE, BLACK, 'Cook', 16)
            self.clear_button = Button(820, 340, 50, 20, WHITE, BLACK, 'Clear', 16)

            self.player_cash_disp = self.font.render(f'Gold: {self.player.gold}', True, (180, 180, 180))
            self.player_cash_disp_rect = self.player_cash_disp.get_rect(x=750, y=445)

            self.last = now

        self.healthbar = self.healthbar_images[0]
        if self.player.pc_health > 90:
            self.healthbar = self.healthbar_images[0]
        elif self.player.pc_health == 90:
            self.healthbar = self.healthbar_images[1]
        elif self.player.pc_health >= 80:
            self.healthbar = self.healthbar_images[2]
        elif self.player.pc_health >= 70:
            self.healthbar = self.healthbar_images[3]
        elif self.player.pc_health >= 60:
            self.healthbar = self.healthbar_images[4]
        elif self.player.pc_health >= 50:
            self.healthbar = self.healthbar_images[5]
        elif self.player.pc_health >= 40:
            self.healthbar = self.healthbar_images[6]
        elif self.player.pc_health >= 30:
            self.healthbar = self.healthbar_images[7]
        elif self.player.pc_health >= 20:
            self.healthbar = self.healthbar_images[8]
        elif self.player.pc_health >= 10:
            self.healthbar = self.healthbar_images[9]


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    

    g.game_over()

pygame.quit()
sys.exit()

