WIN_WIDTH = 900
WIN_HEIGHT = 600
FPS = 60

OVERLAY_LAYER = 5
PLAYER_LAYER = 4
NPC_LAYER = 3
LAYER_2 = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3
NPC_SPEED = 2

TILESIZE = 25

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ground_map = [
    'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
    'wwggwwwssssssssswwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
    'wwggwwwsssssssssswwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
    'wwggwwssggggggggggwwwwwsssswwwgggggggggggggwwwwwwwwwwwwwww',
    'wwggwwsggggggggggggggggssssgggggggggggggggggwwwwwwwwwwwwww',
    'wwwwwsgggggggggggggggggggggggggggggggggggggggwwwwwwwwwwwww',
    'wwssssggggggggggggggggggggggggggggggggggggggSSwwwwwwwwwwww',
    'wwggggggggggggggggggggggggggggggggggggggggggSSwwwwwwwwwwww',
    'wwggggggggwwwwwgggggggggggggggggggggggggggggSSSwwwwwwwwwww',
    'wwggggggggwwwwwgggggggggggggggggggggggggggggSSSSwwwwwwwwww',
    'wwggggggggwwwwwwwwggggggggggggggggggggggggggSSSSSwwwwwwwww',
    'wwgggggggggggggwwwggggggggggggggggggggggggggSSSSSSwwwwwwww',
    'wwgggggggggggggwwwggggggggggggggggggggggggggSSSSSSSwwwwwww',
    'wwggggggggggggggggggggggggggggggggggggggggggSSSSSSSSSSSwww',
    'wwggggggggggggggggggggggggggggggggggggggggggSSSSSSSSSSSwww',
    'wwgggggggggggggggggggggggggggggggggggggggggggggggggggggwww',
    'wwgggggggggggggggggggggggggggggggggggggggggggggggggggggwww',
    'wwgggggggggggggggggggggggggggggggggggggggggggggggggggggwww',
    'wwgggggggggggggggggggggggggggggggggggggggggggggggggggggwww',
    'wwgggggggggggggggggggggggggggggggggggggggggggggggggggggwww',
    'wwgggggggggggggggggggggggggggggggggggggggggggggggggggggwww',
    'wwggSSSSSSSSdddddddddggggggggggggggggggggggggggggggggggwww',
    'wwggSSSSSSSSdddddddddggggggggggggggggggggggggggggggggggwww',
    'wwggSSSSSSSSdddddddddggggggggggggggggggggggggggggggggggwww',
    'wwggSSSSSSSSdddddddddggggggggggggggggggggggggggggggggggwww',
    'wwggSSSSSSSSdddddddddggggggggggggggggggggggggggggggggggwww',
    'wwggddddddddSSSSSddddggggggggggggggggggggggggggggggggggwww',
    'wwggddddddddSSSSSddddggggggggggggggggggSSSSSSSSSSSSSSSSwww',
    'wwggddddddddSSSSSddddggggggggggggggggggSSSSSSSSSSSSSSSSwww',
    'wwggddddddddSSSSSddddggggggggggggggggggSSSSSSSSSSSSSSSSwww',
    'wwggdd---------------ggggggggggggggggggSSSSSSSSSSSSSSSSwww',
    'wwggdd---------------ggggggggggggggggggSSSSSSSSSSSSSSSSwww',
    'wwggdddddddddddddddddggggggggggggggggggSSSSSSSSSSSSSSSSwww',
    'wwggdddddddddddddddddggggggggggggggggggSSSSSSSSSwwwwwwwwww',
    'wwggdddddddddddddddddddddddddddddddddddSSSSSSSSSwwwwwwwwww',
    'wwggddddddddddddddddddddddddddddddddddddSSSSSSSSSSSSSSSwww',
    'wwggdddddddddddddddddddddddddddddddddddddSSSSSSSSSSSSSSwww',
    'wwggddddddddddddddddddddddddddddddddddddddSSSSSSSSSSSSwwww',
    'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
    'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
]

character_map = [
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '.................B........................................',
    '..........................................................',
    '................S.......B...........B.....................',
    '......B...................................................',
    '..........................................................',
    '..........................................................',
    '..................P................B......................',
    '...........................F..........B...................',
    '...........................2..............................',
    '..........................................................',
    '.....B........B...........................................',
    '.....................................S....................',
    '..........................................................',
    '....................................S.....................',
    '...........B.........................B....................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........D...................B....S......................',
    '..........................S....B.B........................',
    '...........S............S.................................',
    '..........................................................',
    '..........S...............................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........G...............................................',
    '..........1...............................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................'
]

lv10_char_map = [
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........D...............................................',
    '.......S....S.............................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................'
]

layer2_map = [
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................T...............',
    '..........................................TT..............',
    '..........................................TTh.............',
    '..........................................TT..............',
    '..........................................TT..............',
    '.................12LL....aaaa.............TT..............',
    '.......MLM.......43TTTTTTTTTTTTTTTT.......TT..............',
    '..TT...TTM...............AH.....LTT.......TT..............',
    '..TT...TT................L......LMT.......TT..............',
    '..TT...TTTTTTT...................TM.......TT..............',
    '..TT..TTTTTTTT.TTTTTa............TT.......TT..............',
    '..TT..TTTTT.......LTL.....MTTM...TT.......TT..............',
    '...T....LTTTTT..TTTTT.....TTLT...LT.......TT..............',
    '..TT....aTTT..LTTTTTT...........MLT.......TT..............',
    '..TT.....MT..TT..T......TTTTTTTTTTT.......TT..............',
    '..TT..TTTTL......T..TT....................TT..............',
    '..TT................TX...TTTTTTTTT12......TT..............',
    '..TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT43.....aTT..............',
    '..TTkuiuiiiiiioiokkkk....................aTT..............',
    '..TTkukukkkkkkokokkkk.......aa...........aTT..............',
    '..TTkukupkkkkpokokkkk.......aa.........LLTT...............',
    '..TTkukjmms.mmlkokkkk.................LTT.................',
    '..TTkuk........kokkkkMTTTTTTTTTTTTTTTTTT..................',
    '..TTkukkkkkkkkkkokkkkTTTTTTTTTTTTTTTTTTh.B....H..h........',
    '..TTkupkkkkkkkkpokkkkTT.......h.S.........................',
    '..TTkjmmmms.mmmmlkkkkTT..a..a...7.a..a...b..........H.....',
    '..TTk............kkkkTT..a..a.....a..a.......8............',
    '..TTpkkkGpkkpGkkkSpkkMT..a..a.....a..a.H....S.............',
    '..TTkkkkkkkkkkkkk-kkkTT..a..a.....a..a......,.............',
    '..TT....<kkkkkkkkkkkkTT............................v......',
    '..TT.....<kkkkkkkkkkkkkkkkkkkkkkkkkkkkk..........v........',
    '..TT......<kkkkkkkkkkkkkkkkkkkkkkkkkkkk...............9...',
    '..TT......................................................',
    '..TT......................................................',
    '..TT......................................................',
    '..........................................................',
    '..........................................................'
]

blacksmith_interior_tilemap = [
    '...............................',
    '...............................',
    '...............................',
    '...............................',
    '...............................',
    '...............................',
    '..............lttttttr.........',
    '..............lffffffr.........',
    '..............lffffffr.........',
    '..............lffffffr.........',
    '..............lffffffr.........',
    '..............bbbbdbbb.........',
    '...............................',
    '...............................'
]

blacksmith_furniture_tilemap = [
    '...............................',
    '...............................',
    '...............................',
    '...............................',
    '...............................',
    '...............................',
    '..............lttFtttt.........',
    '..............lffffffr.........',
    '..............lffffffr.........',
    '..............lSC1fBfr.........',
    '..............lfff2ffr.........',
    '..............bbbbdbbb.........',
    '...............................',
    '...............................'
]