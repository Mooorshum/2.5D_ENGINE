from graphics.particles import ParticleSystem




earthen_dust = ParticleSystem()
DUST_BROWN_1 = (184, 160, 133)
DUST_BROWN_2 = (181, 153, 140)
DUST_BROWN_3 = (181, 153, 140)
DUST_BROWN_4 = (199, 186, 151)
earthen_dust.colours = (
    DUST_BROWN_1, DUST_BROWN_2, DUST_BROWN_3, DUST_BROWN_4,
)
earthen_dust.lifetime_range = (10, 100)
earthen_dust.acceleration_range = (10, 50)
earthen_dust.ay_system = -30




flame = ParticleSystem()
YELLOW = (255, 255, 0)
FLAME_ORANGE_1 = (255, 240, 0)
FLAME_ORANGE_2 = (255, 230, 0)
FLAME_ORANGE_3 = (255, 220, 0)
FLAME_ORANGE_4 = (255, 200, 0)
FLAME_ORANGE_5 = (255, 180, 0)
FLAME_ORANGE_6 = (255, 160, 0)
FLAME_ORANGE_7 = (255, 140, 0)
FLAME_ORANGE_8 = (255, 120, 0)
FLAME_ORANGE_9 = (255, 100, 0)
RED = (255, 0, 0)
flame.colours = (
    YELLOW, 
    FLAME_ORANGE_1, FLAME_ORANGE_2, FLAME_ORANGE_3,
    FLAME_ORANGE_4, FLAME_ORANGE_5, FLAME_ORANGE_6,
    FLAME_ORANGE_7, FLAME_ORANGE_8, FLAME_ORANGE_9
)
flame.max_count = 100
flame.r_range = (1, 15)
flame.lifetime_range = (10, 80)
flame.acceleration_range = (20, 100)
flame.ay_system = -150