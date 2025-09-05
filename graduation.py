import pygame
import random
import sys
import math

# Inisialisasi Pygame
pygame.init()

# Full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Happy Graduation")

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LOVE_COLOR = (255, 105, 180)

# Font
font_big = pygame.font.SysFont("comicsansms", 80, bold=True)
font_small = pygame.font.SysFont("comicsansms", 50, bold=True)
font_message = pygame.font.SysFont("arial", 32)
font_footer = pygame.font.SysFont("arial", 20, italic=True)

# Pesan utama
special_message = ("Selamat wisuda sayang."
                   "Hari ini abg resmi jadi sarjana, adk bangga sama abg."
                   "Semua kerja keras, begadang, dan perjuangan akhirnya terbayar manis."
                   "Adk tau perjalanan abg nggak gampang, tapi abg bisa buktiin kalau abg kuat dan hebat. "

                   "Semoga ini jadi awal dari langkah besar menuju masa depan yang lebih cerah, "
                   "dan semoga suatu hari nanti adk juga bisa wisuda kaya abgggg aaminn.."

                   "Adk bangga punya abg, love you always")

# =========================
# CLASS KEMBANG API 🎆
# =========================
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.color = [random.randint(100, 255) for _ in range(3)]
        self.particles = []
        self.exploded = False
        self.speed = random.uniform(-8, -12)
        self.is_love = random.choice([False, False, True])  # 1/3 kemungkinan jadi love

    def update(self):
        if not self.exploded:
            self.y += self.speed
            self.speed += 0.15
            if self.speed >= 0:
                self.exploded = True
                if self.is_love:
                    self.create_love_particles()
                else:
                    self.create_normal_particles()
        else:
            for p in self.particles:
                p[0] += p[2]
                p[1] += p[3]
                p[3] += 0.05
                p[5] -= 1

    def create_normal_particles(self):
        for _ in range(80):
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 6)
            vector = pygame.math.Vector2(1, 0).rotate(angle)
            self.particles.append([
                self.x, self.y,
                speed * vector.x,
                speed * vector.y,
                self.color,
                random.randint(40, 100)
            ])

    def create_love_particles(self):
        for _ in range(100):
            # Rumus bentuk LOVE ❤️
            t = random.uniform(0, math.pi)
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) -
                  2 * math.cos(3 * t) - math.cos(4 * t))
            scale = random.uniform(5, 8)
            self.particles.append([
                self.x + x * scale,
                self.y + y * scale,
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                LOVE_COLOR,
                random.randint(60, 120)
            ])

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)
        else:
            for p in self.particles:
                if p[5] > 0:
                    pygame.draw.circle(surface, p[4], (int(p[0]), int(p[1])), 2)

# =========================
# CLASS LOVE JATUH 💕
# =========================
class FallingLove:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.randint(15, 30)
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.y += self.speed
        self.angle += self.rotation_speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, 0)
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        t = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        for i in range(0, 360, 10):
            theta = math.radians(i)
            x = self.size * 16 * math.sin(theta) ** 3
            y = -self.size * (13 * math.cos(theta) - 5 * math.cos(2 * theta) -
                              2 * math.cos(3 * theta) - math.cos(4 * theta))
            pygame.draw.circle(t, LOVE_COLOR, (int(self.size + x), int(self.size + y)), 2)
        rotated = pygame.transform.rotate(t, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)

# Fungsi teks multi-baris
def draw_multiline_text(text, font, color, x, y, max_width):
    words = text.split(" ")
    lines, line = [], ""
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] < max_width:
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    for i, l in enumerate(lines):
        text_surface = font.render(l.strip(), True, color)
        screen.blit(text_surface, (x - text_surface.get_width() // 2, y + i * 35))

# =========================
# MAIN LOOP
# =========================
clock = pygame.time.Clock()
fireworks = []
falling_loves = [FallingLove() for _ in range(30)]  # Banyak love jatuh
running = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Tambahkan kembang api
    if random.randint(1, 15) == 1:
        fireworks.append(Firework())

    # Update dan gambar kembang api
    for f in fireworks[:]:
        f.update()
        f.draw(screen)
        if f.exploded and all(p[5] <= 0 for p in f.particles):
            fireworks.remove(f)

    # Update dan gambar love jatuh 💕
    for love in falling_loves:
        love.update()
        love.draw(screen)

    # Judul
    text1 = font_big.render("Happy Graduation", True, (255, 215, 0))
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 80))

    # Nama
    text2 = font_small.render("Rusydi Mulya Sumantri S.H", True, (173, 216, 230))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 180))

    # Ucapan tengah layar
    draw_multiline_text(special_message, font_message, WHITE, WIDTH // 2, HEIGHT // 2 - 100, WIDTH - 200)

    # Tulisan kecil di bawah kanan
    footer = font_footer.render("by: imelda cantik", True, WHITE)
    screen.blit(footer, (WIDTH - footer.get_width() - 20, HEIGHT - footer.get_height() - 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
