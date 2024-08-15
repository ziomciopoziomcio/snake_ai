import pygame


def draw_border(screen, color, board_width, board_height, window_width, window_height):
    cell_size = min(window_width // board_width, window_height // board_height)
    thickness = cell_size
    pygame.draw.rect(screen, color, pygame.Rect(0, 0, board_width * cell_size, thickness))  # Top border
    pygame.draw.rect(screen, color, pygame.Rect(0, 0, thickness, board_height * cell_size))  # Left border
    pygame.draw.rect(screen, color, pygame.Rect(0, (board_height - 1) * cell_size, board_width * cell_size,
                                                thickness))  # Bottom border
    pygame.draw.rect(screen, color,
                     pygame.Rect((board_width - 1) * cell_size, 0, thickness, board_height * cell_size))  # Right border
