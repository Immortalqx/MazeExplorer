import random
import numpy
import pygame

# 定义颜色的RGB值
white = (255, 255, 255)  # 白色
lightgrey = (205, 205, 205)  # 浅灰色
startcolor = (80, 240, 104)  # 起点颜色（绿色）
goalcolor = (238, 68, 0)  # 终点颜色（红色）
bordercolor = (128, 128, 128)  # 障碍物颜色（灰色）
astarcolor = (255, 255, 0)  # A*路径颜色（黄色）
jpscolor = (230, 0, 230)  # JPS路径颜色（紫色）


# 定义Grid类
class Grid:
    def __init__(self, size_screen, size_node):
        # 初始化网格的尺寸和节点大小
        self.size = size_screen
        self.size_node = size_node
        self.matrix = numpy.zeros(1)  # 初始化矩阵
        self.start, self.goal = (0, 0), (0, 0)  # 初始化起点和终点
        self.flagstart = False  # 标记是否设置了起点
        self.flaggoal = False  # 标记是否设置了终点

        # 创建多个表面用于绘制
        self.SGB = pygame.Surface(size_screen)
        self.PathA = pygame.Surface(size_screen)
        self.PathJ = pygame.Surface(size_screen)
        # 设置透明色
        self.SGB.set_colorkey(white)
        self.PathA.set_colorkey(white)
        self.PathJ.set_colorkey(white)

    def refresh(self, layer):
        # 刷新网格，重置起点和终点，清空矩阵
        self.start, self.goal = (0, 0), (0, 0)
        self.flagstart = False
        self.flaggoal = False
        self.matrix = numpy.zeros(
            (self.size[1] // self.size_node, self.size[0] // self.size_node)
        )

        # 填充背景和网格表面为白色
        layer.fill(white)
        self.SGB.fill(white)
        self.PathA.fill(white)
        self.PathJ.fill(white)
        # 绘制网格线
        for x in range(0, self.size[0], self.size_node):
            pygame.draw.line(layer, lightgrey, (x, 0), (x, self.size[1]))
        for y in range(0, self.size[1], self.size_node):
            pygame.draw.line(layer, lightgrey, (0, y), (self.size[0], y))

    def lightrefresh(self, layer):
        # 轻量刷新网格，只清空路径图层，不重置起点和终点
        layer.fill(white)
        self.PathA.fill(white)
        self.PathJ.fill(white)
        # 绘制网格线
        for x in range(0, self.size[0], self.size_node):
            pygame.draw.line(layer, lightgrey, (x, 0), (x, self.size[1]))
        for y in range(0, self.size[1], self.size_node):
            pygame.draw.line(layer, lightgrey, (0, y), (self.size[0], y))
        # 将障碍物图层绘制到主图层上
        layer.blit(self.SGB, (0, 0))

    def drawrect(self, layer, color, pos):
        # 绘制矩形，表示障碍物、起点、终点或路径
        pygame.draw.rect(
            layer,
            color,
            (
                pos[0] // self.size_node * self.size_node + 1,
                pos[1] // self.size_node * self.size_node + 1,
                self.size_node - 1,
                self.size_node - 1,
            ),
        )

    def drawpath(self, path, main_layer, flag):
        # 绘制路径
        font = pygame.font.Font(None, 25)
        font1 = pygame.font.Font(None, 25)

        # 根据flag值显示A*或JPS的时间信息
        if flag == 1:
            time = font.render("A*:" + str(path[1]), True, (34, 177, 86))
            time1 = font1.render("A*:" + str(path[1]), True, (255, 255, 255))
            main_layer.blit(time1, (16, 11))
            main_layer.blit(time, (15, 10))
        else:
            time = font.render("JPS:" + str(path[1]), True, (34, 177, 86))
            time1 = font1.render("JPS:" + str(path[1]), True, (255, 255, 255))
            main_layer.blit(time1, (6, 36))
            main_layer.blit(time, (5, 35))

        # 如果路径未找到，显示提示信息
        if path[0] == 0:
            noway = font.render("Path not found", True, (34, 177, 86))
            noway1 = font1.render("Path not found", True, (255, 255, 255))
            main_layer.blit(noway1, (6, 56))
            main_layer.blit(noway, (5, 55))
            return

        # 根据flag值绘制A*或JPS路径
        if flag == 1:
            i = 0
            while i < len(path[0]) - 1:
                pygame.draw.line(
                    self.PathA,
                    astarcolor,
                    (
                        path[0][i][1] * self.size_node + self.size_node // 2,
                        path[0][i][0] * self.size_node + self.size_node // 2,
                    ),
                    (
                        path[0][i + 1][1] * self.size_node
                        + self.size_node // 2,
                        path[0][i + 1][0] * self.size_node
                        + self.size_node // 2,
                    ),
                    self.size_node // 2,
                )
                i += 1
            main_layer.blit(self.PathA, (0, 0))
        else:
            i = 0
            while i < len(path[0]) - 1:
                pygame.draw.line(
                    self.PathJ,
                    jpscolor,
                    (
                        path[0][i][1] * self.size_node + self.size_node // 2,
                        path[0][i][0] * self.size_node + self.size_node // 2,
                    ),
                    (
                        path[0][i + 1][1] * self.size_node
                        + self.size_node // 2,
                        path[0][i + 1][0] * self.size_node
                        + self.size_node // 2,
                    ),
                    self.size_node // 2,
                )
                i += 1
            main_layer.blit(self.PathJ, (0, 0))

    def mark_border(self, pos, main_layer):
        # 标记障碍物
        if (
                (pos[1] // self.size_node, pos[0] // self.size_node) != self.start
                and (pos[1] // self.size_node, pos[0] // self.size_node)
                != self.goal
        ):
            if (
                    self.matrix[pos[1] // self.size_node][pos[0] // self.size_node]
                    == 0
            ):
                self.matrix[pos[1] // self.size_node][
                    pos[0] // self.size_node
                    ] = 1
                self.drawrect(self.SGB, bordercolor, pos)
                main_layer.blit(self.SGB, (0, 0))

    def clear_border(self, pos, main_layer):
        # 清除障碍物
        if (
                (pos[1] // self.size_node, pos[0] // self.size_node) != self.start
                and (pos[1] // self.size_node, pos[0] // self.size_node)
                != self.goal
        ):
            if (
                    self.matrix[pos[1] // self.size_node][pos[0] // self.size_node]
                    == 1
            ):
                self.matrix[pos[1] // self.size_node][
                    pos[0] // self.size_node
                    ] = 0
                self.drawrect(self.SGB, (254, 254, 254), pos)
                main_layer.blit(self.SGB, (0, 0))

    def mark_node(self, pos, main_layer):
        # 标记起点和终点
        if not self.flagstart:
            self.start = (pos[1] // self.size_node, pos[0] // self.size_node)
            self.drawrect(self.SGB, startcolor, pos)
            self.flagstart = True
            main_layer.blit(self.SGB, (0, 0))
            return

        if (
                not self.flaggoal
                and (pos[1] // self.size_node, pos[0] // self.size_node)
                != self.start
        ):
            self.goal = (pos[1] // self.size_node, pos[0] // self.size_node)
            self.drawrect(self.SGB, goalcolor, pos)
            self.flaggoal = True
            main_layer.blit(self.SGB, (0, 0))
            return

    def generate(self, main_layer):
        # 起点设置为左上角，终点设置为右下角
        self.start = (0, 0)
        self.goal = (self.matrix.shape[0] - 1, self.matrix.shape[1] - 1)
        self.flagstart = True
        self.flaggoal = True

        # 初始化迷宫，所有单元格为墙
        self.matrix = numpy.ones((self.size[1] // self.size_node, self.size[0] // self.size_node))

        # 迷宫生成算法：深度优先搜索
        stack = [(0, 0)]
        while stack:
            current = stack[-1]
            neighbors = []

            # 检查每个方向的邻居
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < self.matrix.shape[0] and 0 <= ny < self.matrix.shape[1] and self.matrix[nx, ny] == 1:
                    neighbors.append((nx, ny))

            if neighbors:
                next_cell = random.choice(neighbors)
                stack.append(next_cell)
                self.matrix[next_cell[0], next_cell[1]] = 0
                self.matrix[(current[0] + next_cell[0]) // 2, (current[1] + next_cell[1]) // 2] = 0
            else:
                stack.pop()

        # 绘制起点和终点
        self.drawrect(self.SGB, startcolor, (0, 0))
        self.drawrect(self.SGB, goalcolor, (self.goal[1] * self.size_node, self.goal[0] * self.size_node))

        # 确保起点和终点四周是空的
        self.matrix[self.start[0], self.start[1]] = 0
        self.matrix[self.start[0] + 1, self.start[1]] = 0
        self.matrix[self.start[0], self.start[1] + 1] = 0
        self.matrix[self.goal[0], self.goal[1]] = 0
        self.matrix[self.goal[0] - 1, self.goal[1]] = 0
        self.matrix[self.goal[0], self.goal[1] - 1] = 0

        # 绘制迷宫
        for y in range(self.matrix.shape[0]):
            for x in range(self.matrix.shape[1]):
                if self.matrix[y, x] == 1:
                    self.drawrect(self.SGB, bordercolor, (x * self.size_node, y * self.size_node))
        main_layer.blit(self.SGB, (0, 0))

    def move(self, direction, main_layer):
        new_start = list(self.start)

        if direction == 0 and self.start[0] > 0:  # 上移
            new_start[0] -= 1
        elif direction == 1 and self.start[0] < self.matrix.shape[0] - 1:  # 下移
            new_start[0] += 1
        elif direction == 2 and self.start[1] > 0:  # 左移
            new_start[1] -= 1
        elif direction == 3 and self.start[1] < self.matrix.shape[1] - 1:  # 右移
            new_start[1] += 1

        # 检查新位置是否在白色区域
        if self.matrix[new_start[0]][new_start[1]] == 0:
            # 清除旧的start节点
            self.drawrect(self.SGB, white, (self.start[1] * self.size_node, self.start[0] * self.size_node))
            # 更新start节点位置
            self.start = tuple(new_start)
            self.drawrect(self.SGB, startcolor, (self.start[1] * self.size_node, self.start[0] * self.size_node))
            main_layer.blit(self.SGB, (0, 0))

            self.check_success(main_layer)

    def check_success(self, main_layer):
        # 检查起点和终点是否重合，重合则显示 "game success"
        if self.start == self.goal:
            # font = pygame.font.Font(None, 50)
            # success_message = font.render("Game Success!!!!!!", True, (34, 177, 86))
            # main_layer.blit(success_message, (6, 56))
            print("\n\n\nGame Success!!!")
            exit()
