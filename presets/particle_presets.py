from graphics.particles import ParticleSystem, ImageCloudParticleSystem




earthen_dust = ParticleSystem()
DUST_BROWN_1 = (184, 160, 133)
DUST_BROWN_2 = (181, 153, 140)
DUST_BROWN_3 = (181, 153, 140)
DUST_BROWN_4 = (199, 186, 151)
earthen_dust.colours = (
    DUST_BROWN_1, DUST_BROWN_2, DUST_BROWN_3, DUST_BROWN_4,
)
earthen_dust.lifetime_range = (10, 100)
earthen_dust.acceleration_range_x = (0, 0)
earthen_dust.acceleration_range_y = (0, 0)
earthen_dust.acceleration_range_z = (0, 0)
earthen_dust.y0_offset = -1337




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
flame.max_count = 30
flame.r_range = (1, 7)
flame.lifetime_range = (10, 100)
flame.acceleration_range_x = (10, 30)
flame.acceleration_range_y = (10, 30)
flame.acceleration_range_z = (1, 3)
flame.y0_offset = 20



fog_cloud = ImageCloudParticleSystem(
    cloud_size=(40, 40, 30),
    max_cloud_opacity=0.1,
    images_folder='assets/fog/cloud_images'
)
fog_cloud.max_count = 10
fog_cloud.lifetime_range = (300, 500)
fog_cloud.acceleration_range_x = (-60, 60)
fog_cloud.acceleration_range_y = (-60, 60)
fog_cloud.acceleration_range_z = (10, 30)
fog_cloud.y0_offset = 20
