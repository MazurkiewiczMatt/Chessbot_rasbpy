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

def angles_to_steps(positions):
    steps_list = []
    degrees_list = []
    for pos in positions:
        s1, s2 = pos[2], pos[3]
        degrees1 = math.degrees(s1)
        degrees2 = math.degrees(s2)
        steps1 = degrees1 / degrees_per_step
        steps2 = degrees2 / degrees_per_step
        degrees_list.append((degrees1, degrees2))
        steps_list.append((steps1, steps2))
    return degrees_list, steps_list

def shorten_steps(steps_list, factor=2):
    return steps_list[::factor]

if __name__ == "__main__":
    while True:
        try:
            x_start = float(input("Enter x_start: "))
            y_start = float(input("Enter y_start: "))
            x_end = float(input("Enter x_end: "))
            y_end = float(input("Enter y_end: "))
            positions = traj(x_start, y_start, x_end, y_end)
            degrees, steps = angles_to_steps(positions)
            steps_shortened = shorten_steps(steps)
            print("Degrees for each position:", degrees)
            print("Steps for each position:", steps_shortened)

            # Print the shortened steps for Arduino
            print("Send the following into your Arduino code:")
            print("double steps1[] = {", ", ".join(str(round(s[0])) for s in steps_shortened), "};")
            print("double steps2[] = {", ", ".join(str(round(s[1])) for s in steps_shortened), "};")
        except ValueError:
            print("Please enter valid float coordinates.")