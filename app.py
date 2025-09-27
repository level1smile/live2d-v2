import pygame
from OpenGL.GL import *  # 新增导入
from live2d.core import Live2D
from live2d.framework import Live2DFramework
from live2d.lapp_model import LAppModel
from live2d.platform_manager import PlatformManager
from typing import Optional
# 在 app.py 的开头添加，查看当前目录结构
import os
print("当前目录:", os.getcwd())
print("文件列表:", os.listdir('.'))
if os.path.exists('shaders'):
    print("shaders目录:", os.listdir('shaders'))



SCR_WIDTH = 500
SCR_HEIGHT = 500

pygame.init()
# ==== 新增的OpenGL 2.1初始化代码 ====
# 设置OpenGL 2.1兼容模式
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 2)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_COMPATIBILITY)
pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
print("OpenGL版本:", glGetString(GL_VERSION).decode())
print("GLSL版本:", glGetString(GL_SHADING_LANGUAGE_VERSION).decode())




Live2D.init()

Live2DFramework.setPlatformManager(PlatformManager())

model = LAppModel()

name = "nito"
model.LoadModelJson(f"resources/{name}/{name}.model.json")

drag = False
scaling =0.6
dx = 0
dy = 0

model.SetAutoBreathEnable(True)
model.SetAutoBlinkEnable(False)

# last_part_id: str | None = None
last_part_id: Optional[str] = None

def onEvent(e):
    global scaling, dx, dy, last_part_id
    ds = 0.1
    if e.type == pygame.MOUSEMOTION:
        x, y = pygame.mouse.get_pos()
        model.Drag(x, y)
    elif e.type == pygame.MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        ids = model.HitPart(x, y)
        print(ids)
        if len(ids) > 0:
            if last_part_id is not None:
                model.SetPartOpacity(partIds.index(last_part_id), 1)
            last_part_id = ids[0]
        # model.Touch(*pygame.mouse.get_pos())
        # model.StartRandomMotion(priority=MotionPriority.FORCE)
    elif e.type == pygame.KEYDOWN:
        if e.key == pygame.K_a:
            dx -= 0.1
            model.SetOffset(dx, dy)
        elif e.key == pygame.K_d:
            dx += 0.1
            model.SetOffset(dx, dy)
        elif e.key == pygame.K_w:
            dy += 0.1
            model.SetOffset(dx, dy)
        elif e.key == pygame.K_s:
            dy -= 0.1
            model.SetOffset(dx, dy)
        elif e.key == pygame.K_EQUALS:
            scaling += ds
            model.SetScale(scaling)
        elif e.key == pygame.K_MINUS:
            scaling = max(scaling - ds, 0.1)
            model.SetScale(scaling)


model.Resize(SCR_WIDTH, SCR_HEIGHT)

for i in range(model.GetParameterCount()):
    print(model.GetParameter(i))

print(model.GetPartCount())
partIds = model.GetPartIds()
print(partIds)
# model.SetPartOpacity(partIds.index('PARTS_01_HAIR_BACK_001'), 0.8)

running = True
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            break
        onEvent(e)

    if not running:
        break

    Live2D.clearBuffer()

    model.Update()
    if last_part_id is not None:
        model.SetPartOpacity(partIds.index(last_part_id), 0.5)
    model.Draw()
    pygame.display.flip()

Live2D.dispose()
pygame.quit()

