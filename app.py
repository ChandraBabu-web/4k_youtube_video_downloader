import pygame
import sys
from pytube import YouTube

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('YouTube 4K Downloader')

# Set up font and colors
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 28)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Function to draw text
def draw_text(text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Function to download the video
def download_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res="2160p", progressive=True, file_extension="mp4").first()

        if stream:
            stream.download()
            return "Download successful!"
        else:
            return "4K stream not available."
    except Exception as e:
        return f"Error: {e}"

# Game loop
url_input = ''
downloading_message = ''
input_active = False
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle the input field active state
            input_rect = pygame.Rect(150, 150, 300, 40)
            if input_rect.collidepoint(event.pos):
                input_active = not input_active

        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    # When the user presses Enter, attempt to download the video
                    downloading_message = download_video(url_input)
                    url_input = ''  # Clear input field
                elif event.key == pygame.K_BACKSPACE:
                    url_input = url_input[:-1]
                else:
                    url_input += event.unicode

    # Draw the input box
    input_rect = pygame.Rect(150, 150, 300, 40)
    pygame.draw.rect(screen, BLACK, input_rect, 2)

    # Draw the current input text
    draw_text(url_input, input_font, BLACK, 160, 160)

    # Draw the message after attempting the download
    if downloading_message:
        draw_text(downloading_message, font, GREEN if "successful" in downloading_message else RED, 150, 220)

    # Update the display
    pygame.display.flip()
    clock.tick(30)
