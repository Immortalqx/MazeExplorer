import pygame  # 用于制作游戏和多媒体应用的库
import grid  # 导入自定义的网格处理模块
import astar  # 导入自定义的A*算法模块
import jps  # 导入自定义的跳点搜索（JPS）算法模块


# 主函数定义
def main():
    # 打印使用说明
    print(
        # "Right click to set start node and end node"  # 右键点击设置起点和终点
        # + "\nHold left button to draw obstacles"  # 按住左键绘制障碍物
        "\nButtons for calling algorithms:"  # 按键调用算法
        + "\nManhattan heuristic:\n1 - call A* algorithm"  # 曼哈顿启发式：1 - 调用A*算法
        + "\n2 - call JPS algorithm\n3 - call both\n"  # 2 - 调用JPS算法 3 - 调用两者
        + "\nEuclidean heuristic:\n5 - call A* algorithm"  # 欧几里得启发式：5 - 调用A*算法
        + "\n6 - call JPS algorithm\n7 - call both\n"  # 6 - 调用JPS算法 7 - 调用两者
        # + "\nF5 - clear grid\n"  # F5 - 清空网格
    )

    # 无限循环直到正确输入窗口参数
    while True:
        try:
            # 读取用户输入的窗口宽度、高度和节点大小
            width, height, size_node = map(
                int,
                [
                    input(x)
                    for x in ("Window width: ", "Window height: ", "Node size: ")
                ],
            )
            # 检查宽度和高度能否被节点大小整除
            if width % size_node != 0 or height % size_node != 0:
                print(
                    "Width and height should be fully divided by the size of the node\n"
                )
            if width <= 200 or height <= 200:
                print(
                    "Width and height should > 200\n"
                )
            else:
                break  # 如果能整除，跳出循环
        except:
            width, height = 800, 640
            size_node = 16
            break  # 出现异常时，使用默认值并跳出循环

    size = (width, height)  # 设置窗口尺寸

    pygame.init()  # 初始化pygame
    screen = pygame.display.set_mode(size)  # 设置显示窗口
    pygame.display.set_caption("MazeExplorer")  # 设置标题
    running = True  # 标志程序运行状态
    mark_border = False  # 标志是否绘制障碍物
    clear_border = False  # 标志是否清除障碍物

    background = pygame.Surface(size)  # 创建背景表面
    Grid = grid.Grid(size, size_node)  # 初始化网格
    Grid.refresh(background)  # 刷新网格显示
    Grid.generate(background)

    # 主循环，处理事件和更新显示
    while running:
        for event in pygame.event.get():  # 遍历事件队列
            if event.type == pygame.QUIT:  # 处理退出事件
                running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:  # 处理鼠标按下事件
            #     if event.button == 1:  # 左键按下
            #         pos = pygame.mouse.get_pos()  # 获取鼠标位置
            #         if (
            #                 Grid.matrix[pos[1] // size_node][pos[0] // size_node]
            #                 == 0
            #         ):
            #             mark_border = True  # 标记绘制障碍物
            #         else:
            #             clear_border = True  # 标记清除障碍物
            #     elif event.button == 3:  # 右键按下
            #         Grid.mark_node(pygame.mouse.get_pos(), background)  # 设置起点或终点
            # if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # 左键松开
            #     mark_border = False
            #     clear_border = False
            if event.type == pygame.KEYDOWN:  # 键盘按键按下
                # 检测方向键并打印相应的信息
                if event.key == pygame.K_UP:
                    Grid.move(0, background)
                    Grid.lightrefresh(background)
                if event.key == pygame.K_DOWN:
                    Grid.move(1, background)
                    Grid.lightrefresh(background)
                if event.key == pygame.K_LEFT:
                    Grid.move(2, background)
                    Grid.lightrefresh(background)
                if event.key == pygame.K_RIGHT:
                    Grid.move(3, background)
                    Grid.lightrefresh(background)
                # if event.key == pygame.K_F5:  # F5键
                #     Grid.refresh(background)  # 刷新网格
                if event.key == pygame.K_1:  # 数字键1
                    Grid.lightrefresh(background)
                    Grid.drawpath(
                        astar.method(Grid.matrix, Grid.start, Grid.goal, 1),
                        background,
                        1,
                    )  # 调用A*算法（曼哈顿启发式）
                if event.key == pygame.K_2:  # 数字键2
                    Grid.lightrefresh(background)
                    Grid.drawpath(
                        jps.method(Grid.matrix, Grid.start, Grid.goal, 1),
                        background,
                        2,
                    )  # 调用JPS算法（曼哈顿启发式）
                if event.key == pygame.K_3:  # 数字键3
                    Grid.lightrefresh(background)
                    Grid.drawpath(
                        astar.method(Grid.matrix, Grid.start, Grid.goal, 1),
                        background,
                        1,
                    )  # 调用A*算法（曼哈顿启发式）
                    Grid.drawpath(
                        jps.method(Grid.matrix, Grid.start, Grid.goal, 1),
                        background,
                        2,
                    )  # 调用JPS算法（曼哈顿启发式）
                if event.key == pygame.K_5:  # 数字键5
                    Grid.lightrefresh(background)
                    Grid.drawpath(
                        astar.method(Grid.matrix, Grid.start, Grid.goal, 2),
                        background,
                        1,
                    )  # 调用A*算法（欧几里得启发式）
                if event.key == pygame.K_6:  # 数字键6
                    Grid.lightrefresh(background)
                    Grid.drawpath(
                        jps.method(Grid.matrix, Grid.start, Grid.goal, 2),
                        background,
                        2,
                    )  # 调用JPS算法（欧几里得启发式）
                if event.key == pygame.K_7:  # 数字键7
                    Grid.lightrefresh(background)
                    Grid.drawpath(
                        astar.method(Grid.matrix, Grid.start, Grid.goal, 2),
                        background,
                        1,
                    )  # 调用A*算法（欧几里得启发式）
                    Grid.drawpath(
                        jps.method(Grid.matrix, Grid.start, Grid.goal, 2),
                        background,
                        2,
                    )  # 调用JPS算法（欧几里得启发式）
        screen.blit(background, (0, 0))  # 将背景绘制到屏幕上
        pygame.display.update()  # 更新显示

        if mark_border:  # 如果标记绘制障碍物
            Grid.mark_border(pygame.mouse.get_pos(), background)
        if clear_border:  # 如果标记清除障碍物
            Grid.clear_border(pygame.mouse.get_pos(), background)

    pygame.quit()  # 退出pygame


# 如果此脚本作为主程序运行，则调用main函数
if __name__ == "__main__":
    main()
