# Tamanho da tela
WIDTH = 800
HEIGHT = 600

# Tamanho do tile (para ajustar posições de sprites e balas)
TILE_SIZE = 64
ROWS = 15
COLS = 10

# Cor de fundo e cores gerais
BACKGROUND_COLOR = (0, 0, 0)  # Cor de fundo preta
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Título e opções do menu
TITLE = "Alone Space"
SCREEN_MENU = "menu"
SCREEN_GAME = "game"
SCREEN_INSTRUCTIONS = "instructions"
MENU_OPTIONS = ["start", "instructions", "audio", "exit"]

# Constantes de energia, vida, escudo e velocidade
MAX_ENERGY = 100
MAX_HEALTH = 100
MAX_SHIELD = 100
ENERGY_COST_BULLET = 10
ENERGY_COST_BIG_BULLET = 50
ENERGY_COST_ACCELERATION = 1
DAMAGE_BULLET = 15
DAMAGE_BULLET_BIG = 65
SPEED_INCREMENT = 0.05
MIN_SPEED = 1
MAX_SPEED = 5
ROTATION_SPEED = 5

# Taxa de regeneração de energia, vida e escudo
ENERGY_REGENERATION_RATE = 0.75
HEART_REGENERATION_RATE = 1
SHIELD_REGENERATION_RATE = 0.5
ENERGY_COST_SHIELD = 1

# Configuração de disparo
SHOOT_INTERVAL = 10
CHARGE_DURATION = 60

# Configurações de animação
ANIMATION_INTERVAL_PLAYER_ENGINE = 20
BULLET_ANIMATION_FRAMES = 4

# Outras constantes úteis
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
