import Bereshit as D
import Moon as Moon
import matplotlib.pyplot as plt
import math
import PID as PID

# https://www.youtube.com/watch?v=k46nCvOBllA


def main():

    print("Simulating Bereshit's Landing:")

    drone = D.Bereshit()
    moon = Moon.Moon()

    drone.vs = 30               # Vertical Speed
    drone.hs = 1399              # Horizontal Speed
    drone.alt = 33_000             # Altitude
    drone.ang = 65
    time = 0
    dt = 1                  # sec
    print("Starting Simulation!")

    drone.EnginePower = 1    # [0, 1]

    pid_vertical = PID.PidController(4.31715, 0.01, 0.1, 400, -400)
    pid_vertical.setProcessVar(drone.vs)

    pid_horizontal = PID.PidController(1, 0.01, 0.1, 1699, -1699)
    pid_horizontal.setProcessVar(drone.hs)

    while drone.alt > 0:

        velocity = (drone.vs ** 2 + drone.hs ** 2) ** 0.5

        info['vs'].append(drone.vs)
        info['hs'].append(drone.hs)
        info['ang'].append(drone.ang)
        info['alt'].append(drone.alt)
        info['acc'].append(drone.acc)
        info['time'].append(time)
        info['fuel'].append(drone.fuel)
        info['weight'].append(drone.weight)
        info['dt'].append(dt)
        info['power'].append(drone.EnginePower)
        info['velocity'].append(velocity)

        # if time % 10 == 0 or drone.alt < 100:
        #     print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(time, drone.vs, drone.hs,
        #                                                      drone.alt, drone.ang, drone.weight, drone.acc))

        # main computations
        ang_rad = math.radians(drone.ang)
        h_acc = math.sin(ang_rad) * drone.acc
        v_acc = math.cos(ang_rad) * drone.acc
        vacc = moon.getAcc(drone.hs)

        time += dt
        dw = dt * drone.ALL_BURN * drone.EnginePower

        if drone.fuel > 0:
            drone.fuel -= dw
            drone.weight = drone.WEIGHT_EMP + drone.fuel
            drone.acc = drone.EnginePower * drone.accelerate(drone.weight, True, 8)

        else:
            drone.acc = 0

        v_acc -= vacc

        if drone.hs > 0:
            drone.hs -= h_acc * dt

        drone.vs -= v_acc * dt
        drone.alt -= drone.vs * dt

        pid_vertical.setProcessVar(drone.vs)
        vs_res = pid_vertical.control(1)

        pid_horizontal.setProcessVar(drone.hs)
        hs_res = pid_horizontal.control(1)

        ang_ = 90 / (vs_res + hs_res) * hs_res

        drone.ang = 90 if ang_ > 90 else 0 if ang_ < 0 else ang_


if __name__ == '__main__':

    info = {"vs": [],
            "hs": [],
            "ang": [],
            "alt": [],
            "time": [],
            "dt": [],
            "acc": [],
            "fuel": [],
            "weight": [],
            "power": [],
            "velocity": []}

    main()

    print("Simulation Complete!")

    fig, axs = plt.subplots(2, 4)
    fig.suptitle('Observation')

    axs[0, 0].plot(info['time'], info['alt'])
    axs[0, 0].set_ylabel('Altitude')

    axs[0, 1].plot(info['time'], info['vs'])
    axs[0, 1].set_ylabel('Vertical Velocity')

    axs[0, 2].plot(info['time'], info['hs'])
    axs[0, 2].set_ylabel('Horizontal Velocity')

    axs[0, 3].plot(info['time'], info['velocity'])
    axs[0, 3].set_ylabel('Velocity')

    axs[1, 0].plot(info['time'], info['power'])
    axs[1, 0].set_ylabel('Engine Power (%)')
    axs[1, 0].set_xlabel('Time')

    axs[1, 1].plot(info['time'], info['fuel'])
    axs[1, 1].set_ylabel('Fuel')
    axs[1, 1].set_xlabel('Time')

    axs[1, 2].plot(info['time'], info['acc'])
    axs[1, 2].set_ylabel('Acceleration')

    axs[1, 3].plot(info['time'], info['ang'])
    axs[1, 3].set_ylabel('Angle')
    axs[1, 3].set_xlabel('Time')

    plt.show()