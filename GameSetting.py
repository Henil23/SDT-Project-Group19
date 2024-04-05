import math

# Game settings
SCREEN_RES = SCREEN_WIDTH, SCREEN_HEIGHT = 1800, 1000  # Screen resolution
HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
FPS = 0

PLAYER_POSITION = 1.5, 5  # Initial player position on the minimap
PLAYER_ANGLE = 0  # Initial player angle
PLAYER_SPEED = 0.004  # Player movement speed
PLAYER_ROTATION_SPEED = 0.002  # Player rotation speed
PLAYER_SIZE_SCALE = 60  # Player size scale
PLAYER_MAX_HEALTH = 100  # Maximum player health

MOUSE_SENSITIVITY = 0.0003  # Mouse sensitivity
MOUSE_MAX_RELATIVE_MOVEMENT = 40  # Maximum relative movement of the mouse
MOUSE_BORDER_LEFT = 100  # Left border for mouse movement
MOUSE_BORDER_RIGHT = SCREEN_WIDTH - MOUSE_BORDER_LEFT  # Right border for mouse movement

FLOOR_COLOR = (30, 30, 30)  # Color of the floor

FIELD_OF_VIEW = math.pi / 3  # Field of view (in radians)
HALF_FIELD_OF_VIEW = FIELD_OF_VIEW / 2  # Half of the field of view
NUMBER_OF_RAYS = SCREEN_WIDTH // 2  # Number of rays for raycasting
HALF_NUMBER_OF_RAYS = NUMBER_OF_RAYS // 2  # Half of the number of rays
DELTA_ANGLE = FIELD_OF_VIEW / NUMBER_OF_RAYS  # Angle between rays
MAX_RENDER_DISTANCE = 20  # Maximum rendering distance

SCREEN_DISTANCE = HALF_SCREEN_WIDTH / math.tan(HALF_FIELD_OF_VIEW)  # Distance from the screen to the player
RAYCASTING_SCALE = SCREEN_WIDTH // NUMBER_OF_RAYS  # Scale for raycasting

TEXTURE_SIZE = 256  # Size of textures
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2  # Half of the texture size
