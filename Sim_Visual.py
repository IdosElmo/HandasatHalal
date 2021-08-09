from vpython import *
from Moon import Moon
import math
from Bereshit import Bereshit
import sys
import os

G = 6.67e-11

scene = canvas(witdh=1000, height=600, center=vector(0, 0, 0), align='right')
craft = Bereshit()


def Run(b):
    global running
    running = not running
    if running:
        b.text = 'Pause'
    else:
        b.text = 'Run'


running = False
button(text='Run', pos=scene.title_anchor, bind=Run)


def crash(drone, dt):
    vex = 10000
    rmax = Moon.RADIUS / 10
    boom = sphere(pos=drone.pos, radius=drone.radius, color=color.yellow, opacity=0.5)

    while boom.radius < rmax:
        rate(1 / dt)
        boom.radius = boom.radius + vex * dt


def control(vx, vy, distance, nn, angle):
    engine_power = nn
    theta = 0

    # Handle horizontal velocity
    # if vx < -2:
    #     if theta > 0:
    #         theta = 60
    #     # else:
    #     #     theta += 3
    # elif vx >= 0:
    #     theta = 0

    # Handle vertical velocity
    if 20_000 < distance < 50_000:

        if vy < 10:
            engine_power += 0.002
        elif vy > 15:
            engine_power -= 0.003

    if distance < 20_000:
        if distance < 4000:
            engine_power = 0.4
            theta = 0
        elif distance < 1000:
            if vy < 0:
                engine_power = 0.5
        else:
            if -1 < vy < 1:
                engine_power = 0
                theta = 0
            else:
                engine_power -= 0.0001
    elif distance > 50000:
        engine_power = 0.8

    return engine_power, theta


moon = box(pos=vector(0, 0, 0), size=Moon.RADIUS * vector(1, 0, 1), texture=textures.granite)

moon.m = Moon.MASS

drone = sphere(pos=vector(500_000, craft.alt, 0), radius=10000, color=color.blue, make_trail=True, trail_type="points")

drone.v = vector(-craft.hs, -craft.vs, 0)
drone.a = vector(0, 0, 0)
drone.theta = craft.ang
drone.fuel = craft.fuel
drone.m = Bereshit.WEIGHT_FULL

velxg = graph(xtitle="Time", ytitle="Vel_x", align='right')
velyg = graph(xtitle="Time", ytitle="Vel_y", align='right')
fuelg = graph(xtitle="Time", ytitle="Fuel", align='left', width=300, height=300)
altg = graph(xtitle="Time", ytitle="alt", align='left', width=550, height=500)

velx = gcurve(color=color.orange, graph=velxg)
vely = gcurve(color=color.red, graph=velyg)
fuel_ = gcurve(color=color.green, graph=fuelg)
alt = gcurve(color=color.blue)

sv = drone.v
spos = drone.pos

t = 0
dt = 1
NN = craft.EnginePower

while True:
    if running:
        rate(20)

        dis = (drone.pos - moon.pos).y

        NN, drone.theta = control(drone.v.x, drone.v.y, dis, NN, drone.theta)

        if drone.fuel > 0:

            if NN > 0:

                dw = dt * Bereshit.ALL_BURN * NN
                drone.fuel -= dw
                drone.m = Bereshit.WEIGHT_EMP + drone.fuel
                acc = NN * Bereshit.accelerate(drone.m, True, 8)

            else:
                acc = 0
        else:
            acc = 0

        vacc = -1.622  # m / s^2
        ang_rad = math.radians(drone.theta)

        drone.a.y = vacc + acc * cos(ang_rad)
        drone.a.x = 0 + acc * sin(ang_rad)

        drone.v = sv + drone.a * t
        drone.pos = spos + sv * t + 0.5 * drone.a * (t ** 2)

        # did you hit the ground?
        if drone.pos.y <= moon.pos.y:
            print("Ground Hit! - {0}".format(drone.pos))
            print("Final Velocity - {0}".format(drone.v))
            crash(drone, dt)
            drone.pos.y = moon.pos.y + 3
            break

        alt.plot(t, drone.pos.y)
        velx.plot(t, drone.v.x)
        vely.plot(t, drone.v.y)
        fuel_.plot(t, drone.fuel)

        t += dt

print("Simulation complete.")
# os._exit(1)

