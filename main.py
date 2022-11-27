import numpy as np

# Given Information
rho = 7800
c = 700
k = 30
alpha = k / (rho * c)
h = 5000
T_inf = 50
del_x = 1e-3
nodes = int(0.1 / del_x) + 1

# Time increment to be specified by the user
print("""Specify the time increment in milliseconds. 
(Note that for stability, it must be less than 78ms)""")
del_t = float(input())*1e-3

# The finite-difference form of the Fourier and the Biot Number
Fo = alpha * del_t / (del_x ** 2)
Bi = h * del_x / k

# Checking for Stability Condition (Explicit Solution)
if Fo * (1 + Bi) > 0.5:
    print("That's not correct. Please try again. (less than 78ms!)")
    raise SystemExit

# Initialisation
T_prev = 1400 * np.ones(nodes)
T_next = 1400 * np.ones(nodes)

# Applying the finite-difference scheme
step = 0
while T_prev[nodes - 1] > 200:
    step += 1
    # Mid-plane node
    T_next[0] = 2 * Fo * T_prev[1] + (1 - 2 * Fo) * T_prev[0]

    # Interior nodes
    for i in range(1, nodes - 1):
        T_next[i] = Fo * (T_prev[i - 1] + T_prev[i + 1]) + (1 - 2 * Fo) * T_prev[i]

    # Surface node
    T_next[nodes - 1] = 2 * Fo * (T_prev[nodes - 2] + Bi * T_inf) + (1 - 2 * Fo - 2 * Bi * Fo) * T_prev[nodes - 1]

    # Update temperature for next iteration
    T_prev[:] = T_next
    
# Time Required
t = (step * del_t)
print("Time required to cool the surface to 200 Celsius: {:.2f} s".format(t))

# Mid-plane Temperature
print("Corresponding temperature at the mid-plane of the slab is: {:.2f} Celsius".format(T_prev[0]))

# Length of cooling section
L = 15e-3 * t
print("Required length of the cooling section is: {:.2f} m".format(L))
