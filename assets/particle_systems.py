from objects.particles import ParticleSystem, ImageCloudParticleSystem


vehicle_exhaust = ParticleSystem()
GREY_BROWN_1 = (184, 160, 133)
GREY_BROWN_2 = (181, 153, 140)
GREY_BROWN_3 = (181, 153, 140)
GREY_BROWN_4 = (199, 186, 151)
vehicle_exhaust.colours = (
    GREY_BROWN_1, GREY_BROWN_2, GREY_BROWN_3, GREY_BROWN_4,
)
vehicle_exhaust.lifetime_range = (10, 100)
vehicle_exhaust.acceleration_range_x = (0, 0)
vehicle_exhaust.acceleration_range_y = (0, 0)
vehicle_exhaust.acceleration_range_z = (0, 0)
vehicle_exhaust.y0_offset = -1337


fireball = ParticleSystem()
YELLOW = (255, 255, 0)
FLAME_ORANGE_3 = (255, 220, 0)
FLAME_ORANGE_6 = (255, 160, 0)
FLAME_ORANGE_9 = (255, 100, 0)
RED = (255, 0, 0)
fireball.colours = (
    YELLOW, 
    FLAME_ORANGE_3,
    FLAME_ORANGE_6,
    FLAME_ORANGE_9
)
fireball.max_count = 10
fireball.r_range = (1, 7)
fireball.lifetime_range = (10, 100)
fireball.acceleration_range_x = (10, 30)
fireball.acceleration_range_y = (10, 30)
fireball.acceleration_range_z = (1, 3)
fireball.y0_offset = 100

flame_front = ParticleSystem()
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
flame_front.colours = (
    YELLOW, 
    FLAME_ORANGE_1, FLAME_ORANGE_2, FLAME_ORANGE_3,
    FLAME_ORANGE_4, FLAME_ORANGE_5, FLAME_ORANGE_6,
    FLAME_ORANGE_7, FLAME_ORANGE_8, FLAME_ORANGE_9
)
flame_front.max_count = 30
flame_front.r_range = (1, 7)
flame_front.lifetime_range = (10, 100)
flame_front.acceleration_range_x = (10, 30)
flame_front.acceleration_range_y = (10, 30)
flame_front.acceleration_range_z = (1, 3)
flame_front.y0_offset = 100


flame_fireplace = ParticleSystem()
YELLOW = (255, 255, 0)
FLAME_ORANGE_1 = (255, 240, 0)
FLAME_ORANGE_2 = (255, 220, 0)
FLAME_ORANGE_3 = (255, 200, 0)
FLAME_ORANGE_4 = (255, 150, 0)
FLAME_ORANGE_5 = (255, 100, 0)
FLAME_ORANGE_6 = (255, 80, 0)
FLAME_ORANGE_7 = (255, 70, 0)
FLAME_ORANGE_8 = (255, 60, 0)
FLAME_ORANGE_9 = (255, 50, 0)
RED = (255, 0, 0)
flame_fireplace.colours = (
    YELLOW, 
    FLAME_ORANGE_1, FLAME_ORANGE_2, FLAME_ORANGE_3,
    FLAME_ORANGE_4, FLAME_ORANGE_5, FLAME_ORANGE_6,
    FLAME_ORANGE_7, FLAME_ORANGE_8, FLAME_ORANGE_9
)
flame_fireplace.max_count = 15
flame_fireplace.r_range = (1, 7)
flame_fireplace.lifetime_range = (10, 80)
flame_fireplace.acceleration_range_x = (10, 30)
flame_fireplace.acceleration_range_y = (10, 30)
flame_fireplace.acceleration_range_z = (0, 1)
flame_fireplace.y0_offset = 0


water_splash = ParticleSystem()
BLUE_1 = (50, 50, 255)
BLUE_2 = (75, 75, 255)
BLUE_3 = (100, 100, 255)
BLUE_4 = (125, 125, 255)
BLUE_5 = (150, 150, 255)
water_splash.colours = (
    BLUE_1,
    BLUE_2,
    BLUE_3,
    BLUE_4,
    BLUE_5
)
water_splash.max_count = 10
water_splash.r_range = (1, 5)
water_splash.lifetime_range = (10, 50)
water_splash.acceleration_range_x = (10, 50)
water_splash.acceleration_range_y = (10, 50)
water_splash.acceleration_range_z = (0, 1)
water_splash.y0_offset = 0


fog_cloud = ImageCloudParticleSystem(
    cloud_size=(50, 50, 30),
    max_cloud_opacity=0.5,
    images_folder='asset_files/fog/cloud_images'
)
fog_cloud.max_count = 3
fog_cloud.lifetime_range = (100, 200)
fog_cloud.acceleration_range_x = (-60, 60)
fog_cloud.acceleration_range_y = (-60, 60)
fog_cloud.acceleration_range_z = (500, 600)
fog_cloud.y0_offset = 20
