from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import os

# --- INISIALISASI ENGINE ---
app = Ursina()

# --- PENGATURAN GRAFIK & JENDELA ---
window.title = "RPG Adventure By Rivaldo - Ultimate Edition"
window.borderless = False
window.fullscreen = False  # Ubah ke True untuk mode Fullscreen FHD
window.exit_button.visible = False
window.fps_counter.enabled = True
window.cog_button.visible = False

# --- DATA GAME & SISTEM SAVE ---
SAVE_FILE = 'rivaldo_adventure_save.txt'
player_data = {'hp': 100, 'xp': 0, 'lvl': 1, 'xp_next': 50, 'inv': []}

def save_game():
    with open(SAVE_FILE, 'w') as f:
        f.write(f"{player_data['lvl']}\n{player_data['xp']}\n{','.join(player_data['inv'])}")

def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                lines = f.read().splitlines()
                player_data['lvl'] = int(lines[0])
                player_data['xp'] = float(lines[1])
                if len(lines) > 2: player_data['inv'] = lines[2].split(',')
        except: print("Memulai petualangan baru!")

load_game()

# --- SISTEM CUACA & WAKTU (DRAMATIS) ---
sky = Sky()
sun = DirectionalLight(y=2, z=3, rotation=(45,45,45))
sun.shadows = True

rain_particles = []
def toggle_weather(mode='clear'):
    # Hapus hujan lama jika ada
    for r in rain_particles: destroy(r)
    rain_particles.clear()

    if mode == 'rain':
        sky.color = color.dark_gray
        for i in range(100):
            p = Entity(model='line', color=color.cyan, scale=.05, 
                       position=(random.uniform(-20,20), random.uniform(10,20), random.uniform(-20,20)))
            p.animate_y(-5, duration=random.uniform(0.5, 1), loop=True)
            rain_particles.append(p)
    elif mode == 'night':
        sky.color = color.black
        sun.color = color.dark_gray
    else:
        sky.color = color.white
        sun.color = color.white

# --- SCENE MANAGER ---
world = Entity()
dungeon = Entity(enabled=False)

# --- PLAYER & KAMERA (THIRD PERSON) ---
player = Entity(model='cube', color=color.orange, scale=(1, 2, 1), y=1, collider='box', parent=scene)
camera.parent = player
camera.position = (0, 7, -15)
camera.rotation_x = 25
mouse.locked = True

sword = Entity(parent=player, model='cube', color=color.gold, scale=(0.2, 1.8, 0.2), 
               position=(0.7, 0.5, 0.5), rotation=(0,0,-15))

# --- UI (USER INTERFACE) ---
lvl_txt = Text(text=f"LEVEL: {player_data['lvl']}", position=(-0.85, 0.45), scale=1.5, color=color.yellow)
xp_bar = Entity(parent=camera.ui, model='quad', color=color.azure, scale=((player_data['xp']/player_data['xp_next'])*0.4, 0.02), 
                position=(-0.65, 0.40), origin_x=-0.5)
quest_txt = Text(text="Misi: Temukan NPC Paimon", position=(0, 0.45), origin=(0,0), scale=1.2)

# --- MUSUH & NPC ---
npc = Entity(parent=world, model='cube', color=color.azure, scale=(1,2,1), position=(10,1,10), collider='box')
Text(text="PAIMON (F)", parent=npc, y=1.2, scale=10, billboard=True)

class Slime(Entity):
    def __init__(self, parent_scene, x, z):
        super().__init__(parent=parent_scene, model='sphere', color=color.red, scale=1.5, x=x, z=z, y=0.75, collider='box')
        self.hp = 3
    def update(self):
        if self.enabled and distance(self.position, player.position) = player_data['xp_next']:
                    player_data['lvl'] += 1
                    player_data['xp'] = 0
                    lvl_txt.text = f"LEVEL: {player_data['lvl']}"
                xp_bar.scale_x = (player_data['xp']/player_data['xp_next'])*0.4
                destroy(hit.entity)
                save_game()

app.run()
