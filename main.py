import pygame
import random
import sys

# 1. Inisialisasi Pygame
pygame.init()

# Layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cozy Fishing Game - Variasi Ikan")

# Warna
SKY_BLUE = (173, 216, 230)
OCEAN_BLUE = (0, 105, 148)
BOAT_BROWN = (139, 69, 19)
HOOK_GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# 2. Muat Gambar (Ganti nama file sesuai dengan gambar milikmu)
# Catatan: Jika belum ada gambar, Pygame akan error. Buat Surface cadangan sebagai antisipasi:
def load_image_safe(file_path, default_color, default_size):
    try:
        image = pygame.image.load(file_path).convert_alpha()
        return pygame.transform.scale(image, default_size)
    except FileNotFoundError:
        # Jika file belum ditemukan, buat kotak warna sebagai placeholder sementara
        surf = pygame.Surface(default_size, pygame.SRCALPHA)
        pygame.draw.ellipse(surf, default_color, (0, 0, default_size[0], default_size[1]))
        return surf

# Daftar Properti Jenis Ikan (Gambar, Skor, Kecepatan, Ukuran)
FISH_TYPES = {
    "small": {
        "image": load_image_safe("fish_small.png", (255, 165, 0), (24, 16)),
        "score": 10,
        "speed_range": (3, 5),
        "size": (24, 16)
    },
    "medium": {
        "image": load_image_safe("fish_medium.png", (50, 205, 50), (36, 24)),
        "score": 25,
        "speed_range": (2, 4),
        "size": (36, 24)
    },
    "rare": {
        "image": load_image_safe("fish_rare.png", (147, 112, 219), (48, 30)),
        "score": 60,
        "speed_range": (5, 8),  # Ikan langka bergerak sangat cepat
        "size": (48, 30)
    }
}

# Variable Game
boat_x = WIDTH // 2 - 40
boat_y = 100

hook_x = boat_x + 40
hook_y = 130
hook_speed = 6
hook_state = "IDLE"  # "IDLE", "DROPPING", "RETRACTING"

score = 0
caught_fish = None  # Menyimpan ikan yang sedang tersangkut kail

# 3. Class Ikan yang Diperbarui
class Fish:
    def __init__(self):
        self.reset_position()

    def reset_position(self):
        # Acak tipe ikan berdasarkan peluang
        # 60% Kecil, 30% Sedang, 10% Langka
        choice = random.choices(["small", "medium", "rare"], weights=[60, 30, 10])[0]
        type_info = FISH_TYPES[choice]

        self.type = choice
        self.base_image = type_info["image"]
        self.score_value = type_info["score"]
        self.width, self.height = type_info["size"]

        # Penentuan posisi awal (Kiri atau Kanan layar)
        self.moving_right = random.choice([True, False])
        if self.moving_right:
            self.x = -self.width - 20
            self.speed = random.randint(*type_info["speed_range"])
        else:
            self.x = WIDTH + 20
            self.speed = -random.randint(*type_info["speed_range"])

        self.y = random.randint(220, HEIGHT - 60)

        # Mirror/Flip gambar jika bergerak ke kanan (asumsi gambar asli menghadap ke kiri)
        if self.moving_right:
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            self.image = self.base_image

    def move(self):
        self.x += self.speed
        # Reset jika keluar jauh dari tepi layar
        if self.speed > 0 and self.x > WIDTH + 50:
            self.reset_position()
        elif self.speed < 0 and self.x < -self.width - 50:
            self.reset_position()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# Buat beberapa ikan
fishes = [Fish() for _ in range(6)]

# 4. Game Loop Utama
running = True
while running:
    clock.tick(60)
    screen.fill(SKY_BLUE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and hook_state == "IDLE":
                hook_state = "DROPPING"

    # Kontrol kapal (Kiri/Kanan)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and boat_x > 0 and hook_state == "IDLE":
        boat_x -= 4
    if keys[pygame.K_RIGHT] and boat_x < WIDTH - 80 and hook_state == "IDLE":
        boat_x += 4

    # Update posisi kail saat IDLE
    if hook_state == "IDLE":
        hook_x = boat_x + 40
        hook_y = 130

    # Gerakan Kail
    if hook_state == "DROPPING":
        hook_y += hook_speed
        if hook_y >= HEIGHT - 20:
            hook_state = "RETRACTING"
    elif hook_state == "RETRACTING":
        hook_y -= hook_speed

        # Jika ada ikan yang menyangkut, posisikan ikan tepat di kail
        if caught_fish:
            caught_fish.x = hook_x - (caught_fish.width // 2)
            caught_fish.y = hook_y

        # Kail sudah kembali ke atas
        if hook_y <= 130:
            hook_state = "IDLE"
            if caught_fish:
                score += caught_fish.score_value
                caught_fish.reset_position()
                caught_fish = None

    # Draw Laut
    pygame.draw.rect(screen, OCEAN_BLUE, (0, 140, WIDTH, HEIGHT - 140))

    # Draw Kapal & Tali Pancing
    pygame.draw.rect(screen, BOAT_BROWN, (boat_x, boat_y, 80, 40))
    pygame.draw.line(screen, WHITE, (boat_x + 40, 130), (hook_x, hook_y), 2)
    pygame.draw.circle(screen, HOOK_GRAY, (hook_x, hook_y), 5)

    # Draw & Update Ikan
    hook_rect = pygame.Rect(hook_x - 4, hook_y - 4, 8, 8)

    for fish in fishes:
        # Hanya menggerakkan ikan yang sedang TIDAK tersangkut kail
        if fish != caught_fish:
            fish.move()

            # Deteksi tabrakan jika kail belum membawa ikan
            if caught_fish is None and hook_state != "IDLE":
                if hook_rect.colliderect(fish.get_rect()):
                    caught_fish = fish
                    hook_state = "RETRACTING"  # Langsung tarik kail ke atas

        fish.draw(screen)

    # Tampilkan UI Skor
    score_text = font.render(f"Skor: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()