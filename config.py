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
    '..........................................................',
    '..........................................................',
    '................S.......B...........B.....................',
    '......B...................................................',
    '.......S............................S.....................',
    '..........................................................',
    '..................P................B......................',
    '......................................B...................',
    '..........................................................',
    '..........................................................',
    '.....B....................................................',
    '.....................................S....................',
    '..........................................................',
    '....................................S.....................',
    '...............S.....................B....................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........D...................B....S......................',
    '..........................S....B.B........................',
    '........................S.................................',
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
    '.................12.......................TT..............',
    '.................43TTTTTTTTTTTTTTTT.......TT..............',
    '..TT...TTM...............AH.....LTT.......TT..............',
    '..TT...TT.......................LMT.......TT..............',
    '..TT...TTTTTTT...................TM.......TT..............',
    '..TT..TTTTTTTT.TTTTT.............TT.......TT..............',
    '..TT..TTTTT.......LT.............TT.......TT..............',
    '...T.....TTTTT..TTTTT............LT.......TT..............',
    '..TT.....TTT..LTTTTTT...........MLT.......TT..............',
    '..TT.....MT..TT..T......TTTTTTTTTTT.......TT..............',
    '..TT..TTTTM......T..TT...........MT.......TT..............',
    '..TT................TX...TTTTTTTTT12......TT..............',
    '..TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT43......TT..............',
    '..TTkuiuiiiiiioiokkkk.....................TT..............',
    '..TTkukukkkkkkokokkkk.....................TT..............',
    '..TTkukupkkkkpokokkkk...................LTT...............',
    '..TTkukjmms.mmlkokkkk.................LTT.................',
    '..TTkuk........kokkkkMTTTTTTTTTTTTTTTTTT..................',
    '..TTkukkkkkkkkkkokkkkTTTTTTTTTTTTTTTTTTh.B....H..h........',
    '..TTkupkkkkkkkkpokkkkTT...................................',
    '..TTkjmmmms.mmmmlkkkkTT..................b..........H.....',
    '..TTk............kkkkTT......................8............',
    '..TTpkkkGpkkpGkkkSpkkMT................H....S.............',
    '..TTkkkkkkkkkkkkk-kkkTT.....................,.............',
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