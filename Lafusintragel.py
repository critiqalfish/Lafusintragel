import requests
import os, sys
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import pygame._sdl2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Lafusintragel:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Lafusintragel")
        self.running = True
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.custom_font = pygame.font.Font("Hack-Regular.ttf", 36)
        self.icon_image = pygame.image.load("Lafusintragel256x.png")
        pygame.display.set_icon(self.icon_image)
        window = pygame._sdl2.Window.from_display_module()
        window.maximize()
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.screen_height -= window.position[1]

        self.usable = (0, 53, self.screen_width, self.screen_height - 106)
        self.content_surface = pygame.Surface((self.usable[2], self.usable[3]))
        self.content = ""
        self.content_type = ""
        self.url_switcher = [0, ["file://", "http://", "https://"]]
        self.url = self.url_switcher[1][self.url_switcher[0]]
        self.message = ""

    def run(self):
        print("hell yeah!")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.key_event(event)

            self.render()
        pygame.quit()
        sys.exit()
    
    def render(self):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.screen_width, 44))
        pygame.draw.rect(self.screen, RED, (0, 44, self.screen_width, 3))
        pygame.draw.rect(self.screen, GREEN, (0, 47, self.screen_width, 3))
        pygame.draw.rect(self.screen, BLUE, (0, 50, self.screen_width, 3))
        url_surface = self.custom_font.render(self.url, True, WHITE)
        self.screen.blit(url_surface, (10, 0))

        pygame.draw.rect(self.screen, BLACK, (0, self.screen_height - 44, self.screen_width, 44))
        pygame.draw.rect(self.screen, RED, (0, self.screen_height - 47, self.screen_width, 3))
        pygame.draw.rect(self.screen, GREEN, (0, self.screen_height - 50, self.screen_width, 3))
        pygame.draw.rect(self.screen, BLUE, (0, self.screen_height - 53, self.screen_width, 3))
        message_surface = self.custom_font.render(self.message, True, WHITE)
        self.screen.blit(message_surface, (10, self.screen_height - 43))

        self.content_surface.fill(WHITE)
        if self.content_type == "html":
            pass
        elif self.content_type == "text":
            lines = self.content.split('\n')
            for line, y in zip(lines, range(len(lines))):
                content_line_surface = self.custom_font.render(line, True, BLACK)
                self.content_surface.blit(content_line_surface, (0, y * 36))

        self.screen.blit(self.content_surface, (self.usable[0], self.usable[1]))

        pygame.display.flip()

    def key_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_RETURN:
            self.process_url()
        elif event.key == pygame.K_UP:
            if self.url_switcher[0] > 0:
                self.url_switcher[0] -= 1
                self.url = self.url_switcher[1][self.url_switcher[0]]
        elif event.key == pygame.K_DOWN:
            if self.url_switcher[0] < len(self.url_switcher[1]) - 1:
                self.url_switcher[0] += 1
                self.url = self.url_switcher[1][self.url_switcher[0]]
        elif event.key == pygame.K_BACKSPACE:
            self.url = self.url[:-1]
        else:
            self.url += event.unicode

    def process_url(self):
        self.content = ""
        self.content_type = ""
        self.message = ""
        if self.url.startswith("file://"):
            url = self.url[7:]
            try:
                with open(url, "r") as f:
                    self.content = f.read()
                    if f.name.endswith(".html"):
                        self.content_type = "html"
                    else:
                        self.content_type = "text"
                        self.message = f"Warning: \"{url}\" rendered as text"
            except FileNotFoundError as e:
                self.message = f"Error: the file \"{url}\" was not found"
            except IOError as e:
                self.message = f"Error: could not open the file \"{url}\""
            except Exception as e:
                self.message = str(e)
        elif self.url.startswith("http://"):
            pass
        elif self.url.startswith("https://"):
            # dont even think about it
            self.running = False
        else:
            self.message = "Error: no valid url scheme"


if __name__ == "__main__":
    yeah = Lafusintragel()
    yeah.run()
