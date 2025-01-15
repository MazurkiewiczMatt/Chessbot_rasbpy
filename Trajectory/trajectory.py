import sys
import math
import matplotlib.pyplot as plt

l0 = 13  # Length between origin and the two motors
l1 = 22 # Length from motor to passive joints
l2 = 27 # Length from passive joints to end effector
steps_per_revolution = 200
gear_ratio = 10.73
degrees_per_step = 360 / (steps_per_revolution * gear_ratio)

def calc_angles(x, y):
    beta1 = math.atan2(y, (l0 + x))
    beta2 = math.atan2(y, (l0 - x))
    alpha1_calc = (l1**2 + ((l0 + x)**2 + y**2) - l2**2) / (2*l1*math.sqrt((l0 + x)**2 + y**2))
    alpha2_calc = (l1**2 + ((l0 - x)**2 + y**2) - l2**2) / (2*l1*math.sqrt((l0 - x)**2 + y**2))

    if alpha1_calc > 1 or alpha2_calc > 1:
        print("Unreachable coordinates")
        quit()

    alpha1 = math.acos(alpha1_calc)
    alpha2 = math.acos(alpha2_calc)
    shoulder1 = beta1 + alpha1
    shoulder2 = math.pi - beta2 - alpha2

    return shoulder1, shoulder2

def plot_arms(shoulder1, shoulder2, efx, efy):
    p1 = (-l0 + l1*math.cos(shoulder1), l1*math.sin(shoulder1))
    p2 = (l0 + l1*math.cos(shoulder2), l1*math.sin(shoulder2))
    plt.plot([-l0, p1[0], efx], [0, p1[1], efy], 'bo-')
    plt.text(-l0+0.3, 0+0.3, "{:.2f} deg# Left".format(math.degrees(shoulder1)))
    plt.text(p1[0]+0.3, p1[1]+0.3, "({:.2f}, {:.2f}) Left2".format(p1[0], p1[1]))
    plt.plot([l0, p2[0], efx], [0, p2[1], efy], 'bo-')
    plt.text(l0+0.3, 0+0.3, "{:.2f} deg Right".format(math.degrees(shoulder2)))
    plt.text(p2[0]+0.3, p2[1]+0.3, "({:.2f}, {:.2f}) Right2".format(p2[0], p2[1]))
    plt.plot(efx, efy, 'ro')
    plt.text(efx+0.3, efy+0.3, "({:.2f}, {:.2f}) # EF".format(efx, efy))

def plot_plot(efx, efy):
    plt.title('5-Bar Parallel Robot Kinematics')
    plt.plot(-25, -24, 'bo')
    plt.plot(55, 65, 'bo')
    s1, s2 = calc_angles(efx, efy)
    plot_arms(s1, s2, efx, efy)
    plt.draw()
    plt.pause(.01)
    plt.clf()

def traj(x_start, y_start, x_end, y_end, steps=100):
    positions = []
    x_step = (x_end - x_start) / steps
    y_step = (y_end - y_start) / steps
    for i in range(steps + 1):
        x = x_start + i * x_step
        y = y_start + i * y_step
        s1, s2 = calc_angles(x, y)
        positions.append((x, y, s1, s2))
        plot_plot(x, y)
    return positions

def calculate_step_difference(start_angles, end_angles):
    shoulder1_start, shoulder2_start = start_angles
    shoulder1_end, shoulder2_end = end_angles

    steps1 = round((math.degrees(shoulder1_end) - math.degrees(shoulder1_start)) / degrees_per_step)
    steps2 = round((math.degrees(shoulder2_end) - math.degrees(shoulder2_start)) / degrees_per_step)

    return steps1, steps2
