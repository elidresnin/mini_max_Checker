import pygame
import time
from checkers.constants import WIDTH, HEIGHT, RED, WHITE, SQUARE_SIZE
from checkers.game import Game
from minimax.algorithm import minimax, DecisionNode

# Initialize Pygame (this includes font initialization)
pygame.init()

FPS = 60
TREE_HEIGHT = 400  # Height for the tree visualization below the board
WINDOW_WIDTH = 3 * WIDTH  # Wider window to fit the full tree
WIN = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT + TREE_HEIGHT))
pygame.display.set_caption('Checkers with Minimax Tree')
BACKGROUND_COLOR = (200, 200, 200)  # Light gray background


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def draw_decision_tree(win, node, x, y, level=0, offset=0):
    if not node:
        return

    NODE_RADIUS = 10
    LEVEL_SPACING = 100
    # Dynamic child spacing based on number of children
    CHILD_SPACING = max(50, min(200, (WINDOW_WIDTH - 200) // max(1, len(node.children))))

    # Adjust x position with scroll offset
    adjusted_x = x - offset

    # Draw node if within or near visible area
    if -NODE_RADIUS <= adjusted_x <= WINDOW_WIDTH + NODE_RADIUS:
        color = RED if node.maximizing else WHITE
        pygame.draw.circle(win, color, (adjusted_x, y + NODE_RADIUS), NODE_RADIUS)

        # Draw score if it's a leaf node
        if node.score is not None:
            font = pygame.font.SysFont('arial', 15)
            score_text = font.render(str(node.score), True, (0, 0, 0))
            text_x = adjusted_x - score_text.get_width() // 2
            text_y = y + NODE_RADIUS * 2 + 5
            win.blit(score_text, (text_x, text_y))

    # Draw children
    if node.children:
        child_x = x - ((len(node.children) - 1) * CHILD_SPACING) // 2
        for i, child in enumerate(node.children):
            child_pos = (child_x + i * CHILD_SPACING, y + LEVEL_SPACING)
            child_adjusted_x = child_pos[0] - offset
            if (-NODE_RADIUS <= adjusted_x <= WINDOW_WIDTH + NODE_RADIUS and
                    -NODE_RADIUS <= child_adjusted_x <= WINDOW_WIDTH + NODE_RADIUS):
                pygame.draw.line(win, (0, 0, 0), (adjusted_x, y + NODE_RADIUS * 2),
                                 (child_adjusted_x, child_pos[1]), 2)
            draw_decision_tree(win, child, child_pos[0], child_pos[1], level + 1, offset)


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    decision_tree = None

    # Create separate surfaces
    board_surface = pygame.Surface((WIDTH, HEIGHT))
    tree_surface = pygame.Surface((WINDOW_WIDTH, TREE_HEIGHT))  # Match window width

    # Scrolling variables
    tree_offset = 0
    tree_width_estimate = 0  # To estimate total tree width

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] < HEIGHT:  # Only handle clicks on the board area
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

            # Mouse wheel scrolling for tree
            if event.type == pygame.MOUSEWHEEL:
                tree_offset -= event.y * 50  # Scroll speed (positive y scrolls left)
                tree_offset = max(0, min(tree_offset, max(0, tree_width_estimate - WINDOW_WIDTH)))

        if game.turn == WHITE and run:
            value, new_board, tree = minimax(game.get_board(), 2, True)
            game.ai_move(new_board)
            decision_tree = tree
            # Estimate tree width based on deepest level (depth 2)
            tree_width_estimate = max(1, len(tree.children)) * 200 * (2 ** 2)  # Rough estimate
            time.sleep(0.5)

        if game.winner() != None:
            print(game.winner())
            run = False

        # Clear and draw on separate surfaces
        board_surface.fill(BACKGROUND_COLOR)
        tree_surface.fill(BACKGROUND_COLOR)

        # Draw board on its surface
        game.board.draw(board_surface)
        game.draw_valid_moves(board_surface)

        # Draw tree on its surface with scroll offset
        if decision_tree:
            draw_decision_tree(tree_surface, decision_tree, WINDOW_WIDTH // 2, 50, offset=tree_offset)

        # Blit both surfaces to the main window
        WIN.fill(BACKGROUND_COLOR)
        WIN.blit(board_surface, (0, 0))  # Board at top-left
        WIN.blit(tree_surface, (0, HEIGHT))  # Tree below board

        pygame.display.flip()

    pygame.quit()


main()