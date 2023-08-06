# standard imports
import random
import sys
import time
from typing import Tuple

# installed imports
import pygame
import typer
from loguru import logger

# module imports
from tykes import color
from tykes.utils import (
    centralize,
    create_text_box,
    create_text_box_fixed,
    frame_rate,
    generate_easy,
    generate_experiment,
)

app = typer.Typer(no_args_is_help=True)


# docs: "It is safe to call the init() function for any module more than once."
pygame.init()


# this variable is used to hold the primary pygame window, when initialized
# it is not initialized here because we want --help to not spawn a window
window = None


class Maze:
    def __init__(self, width: int = 20, height: int = 20, background_color=(120, 120, 120)):
        """Create the screen to be drawn upon and fill it with a white background."""
        # passed parameters
        self.width = width
        self.height = height
        self.background_color = background_color

        # state
        self.complete = False
        self.score = 0
        self.point = None
        self.trail = None
        self.goal = None
        self._connections = []

        # grid pixel values
        self.border = 3
        self.point_interval = 18
        self.half_interval = int(self.point_interval / 2)

        # TODO: the grid should be created in one place, given point_interval and border_width
        # generate where each "point" is on the grid, in pixels
        self.point_map = dict()
        for x in range(width):
            for y in range(height):

                # border additions
                px_xb = (x + 1) * self.border
                px_yb = (y + 1) * self.border

                # exact points
                px_x = px_xb + (x * self.point_interval) + self.half_interval
                px_y = px_yb + (y * self.point_interval) + self.half_interval

                # store the coordinate point map for later drawing
                self.point_map[(x, y)] = px_x, px_y

        # width across plus borders between and on the outside
        self.px_width = (width * self.point_interval) + (self.border * (width + 1))
        self.px_height = (height * self.point_interval) + (self.border * (height + 1))
        self.px_center = (int(self.px_width / 2.0), int(self.px_height / 2.0))

        # define the maze and trail surfaces that will be overlayed onto one another
        self.maze_surface = pygame.Surface((self.px_width, self.px_height))
        self.trail_surface = pygame.Surface((self.px_width, self.px_height))

        # generate defines: _connections, point, trail, goal
        self.generate()
        self.draw_score()

    def connects(self, point_a: tuple, point_b: tuple):
        """Return whether point connects to another."""
        if (point_a, point_b) in self._connections:
            return True
        if (point_b, point_a) in self._connections:
            return True
        return False

    def connections(self, point: tuple):
        """Return the points connected to the current point."""
        results = []
        for point_a, point_b in self._connections:
            if point_a == point:
                results.append(point_b)
            elif point_b == point:
                results.append(point_a)

        return results

    def draw(self, surface):
        """Draw the maze onto the given surface at the (x, y) coordinates."""
        surface.blit(source=self.score_surface, dest=(0, 0))
        info_height = self.score_surface.get_height()
        surface.blit(source=self.maze_surface, dest=(0, info_height))
        surface.blit(source=self.trail_surface, dest=(0, info_height))

    def draw_line(self, start_pos, end_pos):
        """Draw a line on the 'maze' screen."""
        pygame.draw.line(self.maze_surface, color.black, start_pos, end_pos, self.border)

    def generate(self):
        """Draw the maze onto the maze surface."""
        # generate the connections required for a new maze
        self._connections = generate_easy(width=self.width, height=self.height)
        # self._connections = generate_experiment(width=self.width, height=self.height)

        # fill maze black
        self.maze_surface.fill(color.black)

        # inner background grey square dimensions
        px_width = (self.width * self.point_interval) + (self.border * (self.width - 1))
        px_height = (self.height * self.point_interval) + (self.border * (self.width - 1))

        # draw the grey background
        # creating a rectangle starts at (x, y), then (width, height)
        pygame.draw.rect(
            self.maze_surface, self.background_color, pygame.Rect((self.border, self.border), (px_width, px_height))
        )

        # half the interval, half the border, + 1
        # the additional + 1 is because the borders look janky with a border of 3
        # they cut short like thus (a bottom right corner):
        #
        #    ###
        #   ####
        #   ####
        #   ###
        #
        # there is math to do this calculation for overlap but it requires more focus
        wall_offset = self.half_interval + int(self.border / 2) + 1
        for x in range(self.width):
            for y in range(self.height):

                point = (x, y)
                px_x, px_y = self.point_map[point]

                # if there is no connection between the two points, draw a wall
                if not self.connects(point, (x + 1, y)):
                    wall_x = px_x + wall_offset
                    self.draw_line(start_pos=(wall_x, px_y - wall_offset), end_pos=(wall_x, px_y + wall_offset))

                # if the point does not connect to the point below it, draw a wall
                if not self.connects(point, (x, y + 1)):
                    wall_y = px_y + wall_offset
                    self.draw_line(start_pos=(px_x - wall_offset, wall_y), end_pos=(px_x + wall_offset, wall_y))

        # totally random
        # self.point = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        # self.goal = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

        # x, width
        if "x" == random.choice(("x", "y")):
            z = random.randint(0, self.width - 1)
            ys = [0, self.height - 1]
            random.shuffle(ys)
            self.point = (z, ys.pop(0))
            self.goal = (abs(z - (self.width - 1)), ys.pop(0))

        # y, height
        else:
            y = random.randint(0, self.height - 1)
            xs = [0, self.width - 1]
            random.shuffle(xs)
            self.point = (xs.pop(0), y)
            self.goal = (xs.pop(0), abs(y - (self.height - 1)))

        self.trail = [self.point]
        self.complete = False

        # redraw (or draw) the trail surface
        self.draw_trail()

        # draw the exit portal?
        pygame.draw.circle(self.maze_surface, color.green, center=self.point_map[self.goal], radius=5)

    def draw_trail(self):
        """Draw the trail from the start to the current position."""
        # check state
        if not hasattr(self, "point") or self.point is None:
            raise RuntimeError("The point must be defined before drawing a trail!")
        if not hasattr(self, "trail") or self.trail is None:
            raise RuntimeError("The trail must be defined before drawing it!")

        # TODO: when moving backwards, simply write a transparant rect over the space where trails marking
        #   were previously
        self.trail_surface.fill(color.transparent)
        self.trail_surface.set_colorkey(color.transparent)

        if len(self.trail) > 1:
            for trail_point in self.trail:
                # pygame.draw.circle(self.trail_surface, green, center=self.point_map[trail_point], radius = 1)
                pygame.draw.circle(self.trail_surface, (200, 200, 200), center=self.point_map[trail_point], radius=1)

        # if we have not arrived, draw a red circle over the destination
        if self.point != self.goal:
            pygame.draw.circle(self.trail_surface, color.red, center=self.point_map[self.point], radius=5)
            return False

        # create the image text box to be displayed
        img = create_text_box(text="You Won!", size=24, border=self.border)

        # draw the text into the center of the image
        self.trail_surface.blit(img, centralize(self.trail_surface, img))

        # TODO: draw a score box to the top right
        self.complete = True
        self.score += 1
        self.draw_score()
        return True

    def draw_score(self):
        """Draw the score text box surface."""
        if not hasattr(self, "maze_surface") or self.maze_surface is None:
            raise RuntimeError("Define the maze surface before defining the score surface.")

        # if the score has been updated, redraw the score surface
        self.score_surface = create_text_box_fixed(
            text=f"SCORE: {self.score: 2}", border=0, size=20, width=self.maze_surface.get_width(), height=40
        )

    def move(self, point):
        """Try to move to the specified point."""
        if self.complete:
            return False

        # if it does not connect, return False
        if not self.connects(self.point, point):
            return False

        # check if the desired path is the latest on the trail
        if len(self.trail) > 1 and point == self.trail[-2]:
            self.trail.pop(-1)
            self.point = point
            self.draw_trail()
            return True

        # not the last point in the trail, simply move to connected space
        self.trail.append(point)
        self.point = point
        self.draw_trail()
        return True

    def move_back(self):
        """Attempt to move backwards on the trail."""
        # the trail must be longer than 1
        if len(self.trail) == 1:
            return False

        # trail longer than one, we can go backwards
        self.trail.pop(-1)
        self.point = self.trail[-1]
        self.draw_trail()
        return True

    def move_rel(self, mod: Tuple[int]):
        """Move relative to the current point."""
        return self.move((self.point[0] + mod[0], self.point[1] + mod[1]))


@app.command(name="maze")
def main(width: int, height: int):

    # create the maze object and render it onto the window
    maze = Maze(width=width, height=height)

    # define the primary window size now that the maze's width and height have been defined
    # match the maze width, maze height + information
    window = pygame.display.set_mode((maze.px_width, maze.px_height + maze.score_surface.get_height()))
    window.fill(color.white)

    # draw the maze onto the window
    maze.draw(window)
    pygame.display.set_caption("Maze")
    pygame.display.flip()

    # define the movement keys
    movement_keys = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}

    # enter the event loop
    # 4643 frames drawn prior to frame rate implementation
    for _ in frame_rate(frames_per_second=60):

        # for each of the events in the queue, obtain it
        for event in pygame.event.get():

            # if the window 'close' event occurs
            if event.type == pygame.QUIT:
                return 0

            # key has been pressed
            if event.type == pygame.KEYDOWN:

                # escape key pressed
                if event.key == pygame.K_ESCAPE:
                    return 0

                # backspace, move back on the trail
                if event.key == pygame.K_BACKSPACE:
                    if not maze.move_back():
                        logger.warning("Failed to move backwards.")

                # if an arrow key has been pressed, try to move
                if event.key in movement_keys:

                    # try to move to an adjacent point
                    point_mod = movement_keys[event.key]
                    point = maze.point[0] + point_mod[0], maze.point[1] + point_mod[1]
                    maze.move(point)

        # draw the maze onto the window
        maze.draw(window)
        pygame.display.flip()

        # exit if the game is won
        if maze.complete:
            time.sleep(5)
            maze.generate()

    return 0


if __name__ == "__main__":
    app()
