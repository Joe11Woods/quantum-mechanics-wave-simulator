# Infinite Potential Sqaure Well Simulator
#### Video Demo:  <(https://youtu.be/O3T43Yoo6i8)>
#### Description:it

A Python program that simulates the time evolution of quantum wavefunctions in an infinite square well.

As a current physics student, the qunatum realm is something that has always fascinated me and this programme allows us to visualise some of the meaning represented by these cryptic wavefunctions. When the user inputs a wave function, the programme displays the probability density, which is where the physical interpretation becomes particularly clear. I choose to display the wavefunction's real and imaginary parts too, as they explain what is going on behind the scenes, as well as being an interesting visual.

 The user is able to chose between an electron, proton and neutron as these are the particles contained in scipy constants. It is possible to run with this code with any made-up particle with any arbitrary mass, however I limited the user to just these three results for the user's sake of simplicity.

 In order to make the GIF a seamless loop, the time period of the wave function needed to be calculated. This is easy enough to do for one state. However, it gets more complicated for superposed states. Therefore I decided to implement a numerical estimate. This involved updating the time-dependent wave function incrementally and checking whether it was close to the initial state. If this could not be found, an estimate was given instead.

Future developments of this work could involve a finite potential well, a harmonic oscillator, and quantum tunnelling.


Installation:
 - Install the required libraries:

    pip install -r requirements.txt

Usage:
 - Run with `python project.py`
 - The user is prompted for a particle
 - The user is prompted for the size of the well (must be a positive real number)
 - The user is prompted for a wave function. This code supports any number of superposed states, but the wavefunction   must be noramlised
 - Press Ctrl+D after all required information has been entered to generate the animation.

Features:
 - Display of the real part, imaginary part, and probability density of any normalised wavefunction
 - Electron, proton, and neutron support
 - Time-dependant wavefunctions
 - For wavefunctions containing 2 or more superpositions, the time period estimated numerically
