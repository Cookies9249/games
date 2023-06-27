from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

sky_texture = load_texture('skybox.png')
arm_texture = load_texture('arm_texture.png')
punch_sound = Audio('assets/punch_sound.wav', loop = False, autoplay = False)

# Textures
grass_texture = load_texture('grass_block.png')
dirt_texture = load_texture('dirt_block.png')
brick_texture = load_texture('brick_block.png')
stone_texture = load_texture('stone_block.png')

blocks = [
    {'id': 0, 'name':'grass', 'texture':grass_texture},
    {'id': 1, 'name':'dirt', 'texture':dirt_texture},
    {'id': 2, 'name':'brick', 'texture':brick_texture},
    {'id': 3, 'name':'stone', 'texture':stone_texture}]

# blocks = [
#     {'id': 0, 'name':'grass'},
#     {'id': 1, 'name':'dirt'},
#     {'id': 2, 'name':'brick'},
#     {'id': 3, 'name':'stone'}]

# Inventory
inventory = [[{'block_id':None, 'count':0} for _ in range(9)] for _ in range(4)]

for block in blocks:
    id = block['id']
    # inventory[row][column][key]
    inventory[0][id]['block_id'] = id
current_slot = 0

window.fps_counter.enabled = False
window.exit_button.visible = False

def update():
    global current_slot

    # Change Blocks with Keys
    if held_keys['1']: current_slot = 0
    if held_keys['2']: current_slot = 1
    if held_keys['3']: current_slot = 2
    if held_keys['4']: current_slot = 3
    if held_keys['5']: current_slot = 4
    if held_keys['6']: current_slot = 5
    if held_keys['7']: current_slot = 6
    if held_keys['8']: current_slot = 7
    if held_keys['9']: current_slot = 8

    # Change Hand Texture (1)
    if not held_keys['left mouse'] and not held_keys['right mouse']:
        hand.passive()

class Voxel(Button):
    def __init__(self, position = (0,0,0), block_id = 0):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block.obj',
            origin_y = 0.5,
            texture = blocks[block_id]['texture'],
            color = color.color(0,0,random.uniform(0.85,1)),
            scale = 0.5)
        self.block_id = block_id
    
    def input(self, key):
        global current_slot
        pos = self.position - player.position
        in_sphere = pos[0]**2 + (pos[1]-1.75)**2 + pos[2]**2 < 36

        if self.hovered and in_sphere:
            # Place and Break Blocks
            if key == 'right mouse down':
                punch_sound.play()
                block_id = inventory[0][current_slot]['block_id']
                if not block_id == None:
                    voxel = Voxel(position = self.position + mouse.normal, block_id = block_id)
            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)
            if key == 'm':
                inventory[0][current_slot] = self.block_id
            
            # Change Hand Texture (2)
            if held_keys['left mouse'] or held_keys['right mouse']:
                hand.active()


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 150,
            double_sided = True)

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm.obj',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(155,-10,0),
            position = Vec2(0.7,-0.6))
    
    def active(self):
        self.position = Vec2(0.6,-0.5)

    def passive(self):
        self.position = Vec2(0.7,-0.6)
    
    def input(self, key):
        global current_slot

        # Scroll to Change Block
        if key == 'scroll down':
            current_slot -= 1
        if key == 'scroll up':
            current_slot += 1
        
        if current_slot > len(inventory[0])-1:
            current_slot = 0
        elif current_slot < 0:
            current_slot = len(inventory[0])-1

for z in range(16):
    for x in range(16):
        voxel = Voxel(position = (x,0,z))

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
