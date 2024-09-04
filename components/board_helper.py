import pygame


def draw_border(screen, color, board_width, board_height, window_width, window_height):
    cell_size = min(window_width / board_width, window_height / board_height)
    border_rect = pygame.Rect(0, 0, board_width * cell_size, board_height * cell_size)
    border_rect.center = (window_width // 2, window_height // 2)
    pygame.draw.rect(screen, color, border_rect, 1)