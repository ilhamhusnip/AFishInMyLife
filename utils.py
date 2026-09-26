import pygame

def load_and_scale_fish(file_path, scale_factor=1.5):
    try:
        img = pygame.image.load(file_path).convert_alpha()
        bounding_box = img.get_bounding_rect()
        cropped_img = img.subsurface(bounding_box)

        new_width = int(cropped_img.get_width() * scale_factor)
        new_height = int(cropped_img.get_height() * scale_factor)

        return pygame.transform.scale(cropped_img, (new_width, new_height))
    except FileNotFoundError:
        surf = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (255, 165, 0), (0, 0, 40, 20))
        return surf
    