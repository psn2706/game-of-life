import math

import pygame


class CellStorage:
    x, y = 0, 0  # смещение
    x2, y2 = 0, 0
    size = 64
    size2 = 64
    pause = True
    point_mode = True
    erase_mode = False
    frames = [{}]
    frame = 0
    dict_cell = {}
    new_cells = {}
    del_cells = {}
    colors = {
        "red": (230, 0, 0),
        "green": (0, 200, 0),
        "blue": (0, 0, 200),
        "yellow": (255, 255, 0),
        "black": (0, 0, 0),
        "false": (190, 190, 190),
        "pale red": (255, 180, 180),
        "pale green": (152, 251, 152),
        "pale blue": (175, 238, 238),
        "pale yellow": (255, 255, 102),
        "pale black": (181, 184, 177),
        "pale false": (225, 225, 225),
    }
    color_name = "red"
    neigh = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    point = [(0, 0)]
    figure = [(0, 0)]
    figure_index = 0
    figures = [
        [
            (0, 1),
            (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ],
        [(i, j) for i in range(-1, 2) for j in range(-1, 2)],
        []
    ]
    screen = None

    @staticmethod
    def rotate(figure=None):
        if figure is None:
            x = CellStorage.figures[CellStorage.figure_index]
            x = [(j, -i) for i, j in x]
            CellStorage.figures[CellStorage.figure_index] = x
            CellStorage.figure = x
        else:
            return [(j, -i) for i, j in figure]

    @staticmethod
    def left_frame():
        if CellStorage.frame >= 1:
            CellStorage.frame -= 1
            CellStorage.dict_cell = CellStorage.frames[CellStorage.frame]

    @staticmethod
    def right_frame():
        if CellStorage.frame == len(CellStorage.frames) - 1:
            CellStorage.new_stage()
        else:
            CellStorage.frame += 1
            CellStorage.dict_cell = CellStorage.frames[CellStorage.frame]

    @staticmethod
    def s_draw(i, j, color, s2=False):
        if not s2:
            x, y = CellStorage.x + i * CellStorage.size, CellStorage.y - j * CellStorage.size
            a, b = CellStorage.screen.get_size()
            if -CellStorage.size <= x <= a and -CellStorage.size <= y <= b:
                pygame.draw.rect(CellStorage.screen, color,
                                 (x, y, CellStorage.size, CellStorage.size))
        else:
            x, y = CellStorage.x2 + i * CellStorage.size2, CellStorage.y2 - j * CellStorage.size2
            a, b = CellStorage.screen.get_size()
            if -CellStorage.size2 <= x <= a and -CellStorage.size2 <= y <= b:
                pygame.draw.rect(CellStorage.screen, color,
                                 (x, y, CellStorage.size2, CellStorage.size2))

    @staticmethod
    def draw_pale(i, j):
        if "pale " + CellStorage.color_name in CellStorage.colors:
            for x, y in CellStorage.figure:
                CellStorage.s_draw(x + i, y + j, CellStorage.colors["pale " + CellStorage.color_name])
        else:
            for x, y in CellStorage.figure:
                CellStorage.s_draw(x + i, y + j, CellStorage.color_name)

    @staticmethod
    def set_color(color):
        if isinstance(color, str):
            CellStorage.color_name = color

    @staticmethod
    def set_figure_i(i):
        CellStorage.figure_index = i

    @staticmethod
    def get_figure_i():
        return CellStorage.figure_index

    @staticmethod
    def count_neigh(i, j):
        cnt = 0
        for di, dj in CellStorage.neigh:
            cnt += (i + di, j + dj) in CellStorage.dict_cell
        return cnt

    @staticmethod
    def medium_neigh_color(i, j):
        lst = []
        for p in CellStorage.neigh:
            if (i + p[0], j + p[1]) in CellStorage.dict_cell:
                lst.append(CellStorage.dict_cell[(i + p[0], j + p[1])])
        r, g, b = 0, 0, 0
        for cell in lst:
            r += cell.color[0] ** 2
            g += cell.color[1] ** 2
            b += cell.color[2] ** 2
        if len(lst):
            r, g, b = map(lambda x: math.ceil((x // len(lst)) ** 0.5), [r, g, b])
        return r, g, b

    @staticmethod
    def new_stage():
        if CellStorage.frame != len(CellStorage.frames) - 1:
            CellStorage.frame += 1
            CellStorage.dict_cell = CellStorage.frames[CellStorage.frame]
        else:
            CellStorage.frames[CellStorage.frame] = CellStorage.dict_cell.copy()
            for cell in CellStorage.dict_cell.values():
                cell.update()
            for cell in CellStorage.del_cells:
                CellStorage.delitem(cell)
            for cell, color in CellStorage.new_cells.items():
                Cell(cell[0], cell[1], color)
            CellStorage.del_cells, CellStorage.new_cells = {}, {}
            CellStorage.frame += 1
            CellStorage.frames.append(CellStorage.dict_cell.copy())

    @staticmethod
    def mouse_cell_coord(s2=False):
        x, y = pygame.mouse.get_pos()
        i, j = CellStorage.get_ij(x, y, s2)
        return i, j

    @staticmethod
    def resize(k, s2=False):
        if not s2:
            if 1 <= CellStorage.size * k <= 64:
                x, y = pygame.mouse.get_pos()
                i, j = CellStorage.mouse_cell_coord()
                CellStorage.size *= k
                CellStorage.x = x - i * CellStorage.size
                CellStorage.y = y + j * CellStorage.size
        else:
            if 1 <= CellStorage.size2 * k <= 64:
                CellStorage.size2 *= k

    @staticmethod
    def create(i, j):
        for x, y in CellStorage.figure:
            Cell(x + i, y + j)
        CellStorage.frames = CellStorage.frames[:CellStorage.frame + 1]

    @staticmethod
    def create_with_del(i, j):
        for x, y in CellStorage.figure:
            if (x + i, y + j) in CellStorage.dict_cell:
                CellStorage.delitem(x + i, y + j)
            else:
                Cell(x + i, y + j)
        CellStorage.frames = CellStorage.frames[:CellStorage.frame + 1]

    @staticmethod
    def del_by_figure(i, j):
        for x, y in CellStorage.figure:
            CellStorage.delitem(x + i, y + j)
        CellStorage.frames = CellStorage.frames[:CellStorage.frame + 1]

    @staticmethod
    def delitem(key, j=None):
        if j is not None:
            key = (key, j)
        if key in CellStorage.dict_cell:
            CellStorage.dict_cell.pop(key)

    @staticmethod
    def get_ij(x, y, s2=False):
        if not s2:
            i = (x - CellStorage.x) // CellStorage.size
            j = (CellStorage.y - y) // CellStorage.size + 1
            return i, j
        else:
            i = (x - CellStorage.x2) // CellStorage.size2
            j = (CellStorage.y2 - y) // CellStorage.size2 + 1
            return i, j

    @staticmethod
    def keys():
        return CellStorage.dict_cell.keys()

    @staticmethod
    def values():
        return CellStorage.dict_cell.values()

    @staticmethod
    def cell_colors():
        return [cell.color for cell in CellStorage.dict_cell.values()]

    @staticmethod
    def clear():
        CellStorage.dict_cell.clear()
        CellStorage.frames = CellStorage.frames[:CellStorage.frame + 1]

    @staticmethod
    def set_point():
        CellStorage.figure = CellStorage.point

    @staticmethod
    def set_figure(i=None, f=None):
        if i is None:
            CellStorage.figure = CellStorage.figures[CellStorage.figure_index]
        elif f is None:
            if isinstance(i, list):
                CellStorage.figure = i
            if isinstance(i, int):
                CellStorage.figure = CellStorage.figures[i]
        else:
            CellStorage.figures[i] = f

    @staticmethod
    def set_left_figure():
        CellStorage.figure_index = max(CellStorage.figure_index - 1, 0)
        if not CellStorage.point_mode:
            CellStorage.figure = CellStorage.figures[CellStorage.figure_index]

    @staticmethod
    def set_right_figure(empty_allow=True):
        fi = CellStorage.figure_index
        fs = CellStorage.figures
        if fi == len(fs) - 1 and len(fs[fi]) > 0:
            CellStorage.figures.append([])
        fi = min(fi + 1, len(CellStorage.figures) - 1)
        if not empty_allow and len(CellStorage.figures[fi]) == 0 and fi > 0:
            fi -= 1
        if not CellStorage.point_mode:
            CellStorage.figure = CellStorage.figures[fi]
        CellStorage.figure_index = fi

    @staticmethod
    def get_figure(i=None):
        if i is None:
            return CellStorage.figure
        else:
            return CellStorage.figures[i]

    @staticmethod
    def upd_point(i, j, s2=False):
        if s2:
            if (i, j) in CellStorage.figures[CellStorage.figure_index]:
                CellStorage.figures[CellStorage.figure_index].remove((i, j))
            else:
                if not CellStorage.erase_mode:
                    CellStorage.figures[CellStorage.figure_index].append((i, j))

    @staticmethod
    def upd_point_by_motion(s2=False):
        i, j = CellStorage.mouse_cell_coord(s2)
        if (i, j) not in CellStorage.figures[CellStorage.figure_index]:
            if not CellStorage.erase_mode:
                CellStorage.figures[CellStorage.figure_index].append((i, j))
        if CellStorage.erase_mode:
            if (i, j) in CellStorage.figures[CellStorage.figure_index]:
                CellStorage.figures[CellStorage.figure_index].remove((i, j))

    @staticmethod
    def upd_figures(new_figures=None):
        if new_figures is None:
            figure = CellStorage.figures[CellStorage.figure_index]
            CellStorage.figures = list(filter(lambda x: len(x) > 0, CellStorage.figures))
            CellStorage.figures.append([])
            CellStorage.figure_index = CellStorage.figures.index(figure)
        else:
            CellStorage.figures = new_figures

    @staticmethod
    def draw_figure(s2=False):
        for i, j in CellStorage.figures[CellStorage.figure_index]:
            CellStorage.s_draw(i, j, CellStorage.colors[CellStorage.color_name], s2)


class Cell:
    def __init__(self, i=0, j=0, color=None):
        if (i, j) not in CellStorage.dict_cell:
            self.i, self.j = i, j  # нумерация столбцов и строк
            if color is None:
                self.color = CellStorage.colors[CellStorage.color_name]
            else:
                self.color = color
            CellStorage.dict_cell[(i, j)] = self

    def draw(self):
        CellStorage.s_draw(self.i, self.j, self.color)

    def update(self):
        i, j = self.i, self.j
        for p in CellStorage.neigh:
            x, y = i + p[0], j + p[1]
            if CellStorage.count_neigh(x, y) == 3:
                if (x, y) not in CellStorage.new_cells and (x, y) not in CellStorage.dict_cell:
                    CellStorage.new_cells[(x, y)] = CellStorage.medium_neigh_color(x, y)
        cnt = CellStorage.count_neigh(i, j)
        if cnt < 2 or cnt > 3:
            CellStorage.del_cells[(i, j)] = True
