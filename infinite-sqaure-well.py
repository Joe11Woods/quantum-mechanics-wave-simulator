# CS50 Final Project
# Quantum Mechanic Wave Simulator

import numpy as np #type: ignore
import matplotlib.pyplot as plt #type: ignore
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy import constants

#Useful constants
HBAR = 1.054571817e-34



class Particle:

    def __init__(self, mass, charge=0):
        self.mass = mass
        self.charge = charge

    def energy(self, ns, L): #calculates the energy value for each state

        energys = {}

        for n in ns:
            energy = n**2 * np.pi**2 * HBAR**2 / (2 * self.mass * L**2)
            energys[n] = energy

        return energys


def main():

    particle = particle_selector() #user selects particle

    L = get_L() #retrieves the length of the well from user

    ns, cs = get_nc() #retrieves energy quantum numbers from user

    E = particle.energy(ns,L) #calculates energy

    x_values = np.linspace(0, L, 100) #generates x values for calculations and plots

    stationary_psi = stationary_state(ns,cs, L, x_values) #calculates wavefunction at each x

    print("Loading...")

    give_plot(x_values, stationary_psi, L, E) #plots the function

    print("Finished!")



def particle_selector():

    while True:

        particle = input("Particle: ").strip().lower()

        try:
            return Particle(getattr(constants, f"{particle}_mass"))

        except AttributeError:
            print("Invalid Particle")




def get_L():

    while True:
        L = input("Size of the well (m) = ")
        try:
            L = float(L)
            if L > 0:
                return L
            else:
                print("L must be greater than 0")

        except ValueError:
            print("Invalid L")


def get_n(tally):

    while True:
        n = input(f"n{tally} = ")
        try:
            n = int(n)
            if n > 0:
                return n
            else:
                print("n must be greater than 0")
        except ValueError:
            print("Invalid n")



def get_c(tally):

    while True:
        c = input(f"c{tally} = ")
        try:
            c = float(c)
            return c
        except ValueError:
            print("Invalid c")


def get_nc():

    while True:
        ns = []
        cs = []
        tally = 1
        while True:
            try:
                n = get_n(tally)
                ns.append(n)
                c = get_c(tally)
                cs.append(c)
                tally += 1
            except EOFError:
                print("")
                break
        cs = np.array(cs)
        if not np.isclose(np.sum(cs**2),1, rtol=0.1):
            print("Invalid Wavefunction: probability must sum to 1")
        elif len(ns) != len(cs):
            print("Invalid Wavefunction: each energy state must have a coefficient")
        else:
            return np.array(ns), cs



def stationary_state(ns,cs, L, x_values):

    stationary_states = {}

    for n, c in zip(ns, cs):

        stationary_psi = c * np.sqrt(2 / L) * np.sin(n * np.pi * x_values / L) #this is the normalized infinite well solution to schrodinger

        stationary_states[n] = stationary_psi #adds to dictionary

    return stationary_states


def get_time_period(Psi, E): #gets time period of function

    if len(E) == 1:
        E1 = list(E.values())[0]
        return 2* np.pi * HBAR / E1

    elif len(E) == 2:
        E1 = list(E.values())[0]
        E2 = list(E.values())[1]
        dE = np.abs(E1-E2)
        return 2 * np.pi * HBAR / dE

    else:
        return numerical_time_period(Psi,E)



def numerical_time_period(Psi, E):

    energies = list(E.values())

    dE_min = min(
        abs(E1 - E2)
        for i, E1 in enumerate(energies)
        for E2 in energies[i+1:]
    )

    T_est = 2 * np.pi * HBAR / dE_min

    N = 1000
    dt = T_est / N
    t = dt

    while t < 10 * T_est:

        check_psi, _, _, _ = rip(Psi, E, t)

        if np.allclose(check_psi, Psi):
            return t

        t += dt

    print("Using an estimated Time Period")
    return T_est




def rip(psi, E, t=0): #real, imaginary, probability density

    time_psi = {}

    for n in E:

        time_psi[n] = np.array(psi[n]) * np.exp((-E[n]*t/HBAR)*1j) #applys time dependacy

    Psi = np.array(list(time_psi.values())) #creates a 2D array

    Psi = np.sum(Psi, axis=0) #sums across all wavefunctions

    real_values = np.real(Psi) #gets real part of wave function
    imag_values = np.imag(Psi) #gets imaginary part of wave function. at this point, wave function is fully real, it just makes things easier later
    probability_density = np.abs(Psi) ** 2 #calculates probability data

    return Psi, real_values, imag_values, probability_density




def give_plot(x_values, stationary_psi, L, E):

    fig, ax = plt.subplots() #generates figure and an axis

    Psi, real_values, imag_values, probability_density = rip(stationary_psi, E) #unpacks

    real_line, = ax.plot(x_values,
                         real_values,
                         label="Real") #plots real line

    imaginary_line, = ax.plot(x_values,
                              imag_values,
                              label="Imaginary") #plots imaginary line

    probability_line, = ax.plot(x_values,
                                probability_density,
                                label="Prob. Density") #plots probability density

    ax.set_xlabel("x (m)")
    ax.set_xlim(-L/2, 3*L/2)

    maximum = max(
    np.max(np.abs(real_values)),
    np.max(np.abs(imag_values)),
    np.max(probability_density)
)
    ax.set_ylim(-maximum-0.1, maximum+0.1)

    ax.get_yaxis().set_visible(False) #makes y axis invisble
    ax.spines["top"].set_visible(False) #makes box invisble
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0)) #positions x axis on 0

    ax.axvline(L, color='red', linewidth=3) #produces the infinite potential areas
    ax.axvline(0, color='red', linewidth=3)
    ax.axvspan(L, 3*L/2, color="red", alpha=0.2)
    ax.axvspan(-L/2, 0 , color="red", alpha=0.2)

    ax.legend(loc="upper right")

    def update(t): #introduces time dependace. it is defined within give_plot as it needs access to variables

        _, real_values_t, imag_values_t, probability_density_t = rip(stationary_psi, E, t)

        real_line.set_ydata(real_values_t)
        imaginary_line.set_ydata(imag_values_t)
        probability_line.set_ydata(probability_density_t)

        return real_line, imaginary_line, probability_line

    T = get_time_period(Psi, E) #gets time period

    t = np.linspace(0,T,100) #produces 100 frames within one time period

    animation = FuncAnimation(fig, update, t)

    animation.save('animation.gif', writer=PillowWriter(fps=20))


if __name__ == "__main__":
    main()
















