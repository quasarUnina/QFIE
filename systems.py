import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import QFIE
from skfuzzy import control as ctrl

##IT CONTAINS THE DEFINITION OF THE VARIABLES AND THEIR LINGUISTIC TERMS IN THE PENDULUM SYSTEM

def q_pendulum():
    ###  SYSTEM DEFINITION
    theta = np.linspace(-8, 8, 150)
    omega = np.linspace(-2, 2, 150)
    current = np.linspace(-5, 5, 150)

    theta_neg = fuzz.trapmf(theta, [-8, -8, -1, 0])
    theta_zero = fuzz.trimf(theta, [-1, 0, 1])
    theta_pos = fuzz.trapmf(theta, [0, 1, 8, 8])

    omega_neg = fuzz.trapmf(omega, [-2, -2, -1, 0])
    omega_zero = fuzz.trimf(omega, [-1, 0, 1])
    omega_pos = fuzz.trapmf(omega, [0, 1, 2, 2])

    current_neg_medium = fuzz.trapmf(current, [-5, -5, -2, -1])
    current_neg_small = fuzz.trimf(current, [-2, -1, 0])
    current_zero = fuzz.trimf(current, [-1, 0, 1])
    current_pos_small = fuzz.trimf(current, [0, 1, 2])
    current_pos_medium = fuzz.trapmf(current, [1, 2, 5, 5])

    # Visualize these universes and membership functions
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 10))

    ax0.plot(theta, theta_neg, 'b', linewidth=1.5, label=r'$\theta_n$')
    ax0.plot(theta, theta_zero, 'g', linewidth=1.5, label=r'$\theta_z$')
    ax0.plot(theta, theta_pos, 'r', linewidth=1.5, label=r'$\theta_p$')
    #ax0.set_title(r'$\theta$')
    ax0.set_ylabel(r'$\theta$')
    ax0.legend()

    ax1.plot(omega, omega_neg, 'b', linewidth=1.5, label=r'$\omega_n$')
    ax1.plot(omega, omega_zero, 'g', linewidth=1.5, label=r'$\omega_z$')
    ax1.plot(omega, omega_pos, 'r', linewidth=1.5, label=r'$\omega_p$')
    #ax1.set_title(r'$\omega$')
    ax1.set_ylabel(r'$\omega$')
    ax1.legend()


    ax2.plot(current, current_neg_medium, 'b', linewidth=1.5, label='I_NM')
    ax2.plot(current, current_neg_small, 'g', linewidth=1.5, label='I_NS')
    ax2.plot(current, current_zero, 'r', linewidth=1.5, label='I_Z')
    ax2.plot(current, current_pos_small, 'y', linewidth=1.5, label='I_PS')
    ax2.plot(current, current_pos_medium, 'c', linewidth=1.5, label='I_PM')
    #ax2.set_title(r'$i$')
    ax2.set_ylabel(r'$I$')
    ax2.legend()

    # Turn off top/right axes
    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()


    plt.show()


    ### RULE BASE DEFINITION
    rules = ['if theta is zero and omega is zero then current is zero',
             'if theta is zero and omega is neg then current is pos_small',
             'if theta is zero and omega is pos then current is neg_small',
             'if theta is pos and omega is zero then current is neg_small',
             'if theta is pos and omega is pos then current is neg_medium',
             'if theta is pos and omega is neg then current is zero',
             'if theta is neg and omega is zero then current is pos_small',
             'if theta is neg and omega is pos then current is zero',
             'if theta is neg and omega is neg then current is pos_medium']


    ### QFIE INITIALIZATION
    qfie = QFIE.QFIE()
    qfie.input_variable(name='theta', range=theta)
    qfie.input_variable(name='omega', range=omega)
    qfie.output_variable(name='current', range=current)

    qfie.add_input_fuzzysets(var_name='theta', set_names=['neg', 'zero', 'pos'], sets=[theta_neg, theta_zero, theta_pos])
    qfie.add_input_fuzzysets(var_name='omega', set_names=['neg', 'zero', 'pos'], sets=[omega_neg, omega_zero, omega_pos])
    qfie.add_output_fuzzysets(var_name='current', set_names=['neg_medium', 'neg_small', 'zero', 'pos_small', 'pos_medium'],
                              sets=[current_neg_medium, current_neg_small, current_zero, current_pos_small, current_pos_medium])
    qfie.set_rules(rules)
    return qfie


def c_pendulum():
    
    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    theta = ctrl.Antecedent(np.linspace(-8, 8, 150), 'theta')
    omega = ctrl.Antecedent( np.linspace(-2, 2 , 150), 'omega')
    current = ctrl.Consequent(np.linspace(-5, 5, 150), 'current')


    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    theta['neg'] = fuzz.trapmf(theta.universe, [-8, -8, -1, 0])
    theta['zero'] = fuzz.trimf(theta.universe, [-1, 0, 1])
    theta['pos'] = fuzz.trapmf(theta.universe, [0, 2, 8, 8])

    omega['neg'] = fuzz.trapmf(omega.universe, [-2, -2, -1, 0])
    omega['zero'] = fuzz.trimf(omega.universe, [-1, 0, 1])
    omega['pos'] = fuzz.trapmf(omega.universe, [0,1, 2, 2])

    current['neg_medium'] = fuzz.trapmf(current.universe, [-5, -5, -2, -1])
    current['neg_small'] = fuzz.trimf(current.universe, [-2, -1, 0])
    current['zero'] = fuzz.trimf(current.universe, [-1, 0, 1])
    current['pos_small'] = fuzz.trimf(current.universe, [0, 1, 2])
    current['pos_medium'] = fuzz.trapmf(current.universe, [1, 2, 5, 5])


    rule1 = ctrl.Rule(theta['zero'] & omega['zero'], current['zero'])
    rule2 = ctrl.Rule(theta['zero'] & omega['neg'], current['pos_small'])
    rule3 = ctrl.Rule(theta['zero'] & omega['pos'], current['neg_small'])
    rule4 = ctrl.Rule(theta['pos'] & omega['zero'], current['neg_small'])
    rule5 = ctrl.Rule(theta['pos'] & omega['pos'], current['neg_medium'])
    rule6 = ctrl.Rule(theta['pos'] & omega['neg'], current['zero'])
    rule7 = ctrl.Rule(theta['neg'] & omega['zero'], current['pos_small'])
    rule8 = ctrl.Rule(theta['neg'] & omega['pos'], current['zero'])
    rule9 = ctrl.Rule(theta['neg'] & omega['neg'], current['pos_medium'])

    pendulum_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    pendulum = ctrl.ControlSystemSimulation(pendulum_ctrl)
    return pendulum
