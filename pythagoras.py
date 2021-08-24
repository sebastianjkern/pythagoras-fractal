
# %%
from anim import Anim
import skia
import math
from vectors import Vector

def drawOutlinedRect(canvas, paint, points):
    canvas.drawPoints(canvas.PointMode.kPolygon_PointMode, points, paint)
    canvas.drawLine(*points[0], *points[-1], paint)

def pythagoras(canvas, paint, vars):
    l = vars.L

    paint.setShader(skia.GradientShader.MakeLinear(
        points=[(0.0, 0.0), (1920.0, 1200.0)],
        colors=[0xFF3A1C71, 0xFFD76D77, 0xFFFFAF7B]))

    n0 = Vector(0, 1, 0)
    p1 = vars.p1
    p2 = vars.p1.sum(vars.L)
    p3 = p1.sum(n0.multiply(l.magnitude()))
    p4 = p2.sum(n0.multiply(l.magnitude()))

    paint.setColor(skia.ColorBLACK)
    drawOutlinedRect(canvas, paint, [skia.Point(tuple(x.to_points()[:2])) for x in [p1, p2, p4, p3]])

    def next(point: Vector, L: Vector, iteration, miterations):
        if iteration > miterations:
            return
            
        alpha = vars.theta
        beta = math.pi / 2 - vars.theta

        LI_mag = math.sin(beta) * L.magnitude()

        def left(point: Vector, L: Vector):
            paint.setColor(0xFFFFA500)

            a = 2 * math.pi - alpha

            LIn = Vector(L.x * math.cos(a) + L.y * math.sin(a), -L.x * math.sin(a) + L.y * math.cos(a), 0)
            LI = LIn.multiply(1/LIn.magnitude()).multiply(LI_mag)

            p_LI = Vector(-LI.y, LI.x, 0)

            p2 = LI.sum(point)
            p1 = point

            p3 = p1.sum(p_LI)
            p4 = p2.sum(p_LI)

            drawOutlinedRect(canvas, paint, [skia.Point(tuple(x.to_points()[:2])) for x in [p1, p2, p4, p3]])

            return p3, LI

        OPI1, LI = left(point, L)

        def right(point: Vector, L: Vector):
            OP3 = LI.sum(point)
            OP2 = point.sum(L)

            LII = OP2.subtract(OP3)

            p_LI = Vector(-LII.y, LII.x, 0)

            p1 = OP3
            p2 = OP2

            p3 = OP3.sum(p_LI)
            p4 = OP2.sum(p_LI)

            drawOutlinedRect(canvas, paint, [skia.Point(tuple(x.to_points()[:2])) for x in [p1, p2, p4, p3]])

            return p3, LII

        OPII1, LII = right(point, L)

        return next(OPI1, LI, iteration+1, miterations), next(OPII1, LII, iteration+1, miterations)

    next(p1, vars.L, 1, 15)

def drawVec(canvas, paint, p1: Vector):
    canvas.drawCircle(p1.x, p1.y, 5, paint)

with Anim(iterations=1, shape=(1200, 1920, 4)) as anim:
    anim.name = "pythagoras"
    anim.func = pythagoras

    anim.vars.L = Vector(-200, 0, 0)
    anim.vars.p1 = Vector(1250, 1200-420, 0)
    
    anim.vars.theta = 60 * (math.pi / 180)
    anim.background_color = skia.ColorWHITE

# %%
