# import numpy as np
# import sympy as sym
# import math
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt


# n = sym.Symbol('n')
# n_1 = sym.Symbol('n_1')
# n_2 = sym.Symbol('n_2')
# n_3 = sym.Symbol('n_3')
# V_D = sym.Symbol('V_D')
# V_c = sym.Symbol('V_c')
# V_s = sym.Symbol('V_s')
# V_s_neg = sym.Symbol('V_s_neg')

# C_L_max = 1.9
# C_L_max_inv = 1.8
# C_L_c = 1.0

# rho = 1.225

# b = 15
# c = 3
# S_w = b * c
# W = 10000

# U_de_V_c = 15.2400
# U_de_V_D = 7.6200
# g = 9.8
# a = 5.1

# miu = 2 * (W/S_w) / (rho * g * c * a)
# K = 0.88 * miu/(5.3 + miu)


# V_s = math.sqrt(W/(C_L_max * 1/2 * rho * S_w))
# V_s_inv = math.sqrt(W/(C_L_max_inv * 1/2 * rho * S_w))
# V_c = math.sqrt(W/(C_L_c * 1/2 * rho * S_w))
# V_D = 1.4 * V_c

# n_1 = C_L_max * 1/2 * rho * V_s**2 * S_w / W
# n_2 = 0.75 * n_1
# n_3 = C_L_max_inv * 1/2 * rho * V_s_inv**2 * S_w / W


# num_points = 10

# x = np.linspace(0, V_D, num_points)
# y = np.full(num_points, n_1*1.5)
# plt.plot(x, y, '--')


# x = np.linspace(0, V_D, num_points)
# y = np.full(num_points, n_1*1.25)
# plt.plot(x, y, '--')


# x = np.linspace(0, V_s, 1000)
# y = C_L_max * 1/2 * rho * x**2 * S_w / W
# plt.plot(x, y, '--')


# x = [V_s, V_c]
# y = [n_1, n_1]
# plt.plot(x, y, '--')


# x = [V_c, V_D]
# y = [n_1, n_2]
# plt.plot(x, y, '--')


# x = [V_D, V_D]
# y = [n_2, 0]
# plt.plot(x, y, '--')


# x = [V_D, V_c]
# y = [0, -n_3]
# plt.plot(x, y, '--')


# x = [V_c, V_s_inv]
# y = [-n_3, -n_3]
# plt.plot(x, y, '--')


# x = np.linspace(0, V_s_inv, 1000)
# y = C_L_max_inv * 1/2 * rho * x**2 * S_w / W
# plt.plot(x, -y, '--')



# plt.axhline(y=0, color='k')
# plt.axvline(x=0, color='k')
# plt.xlabel('Flight speed')
# plt.ylabel('Manouvering load factor')
# plt.title('Manouvering Flight Envelope')
# plt.legend(['Positive S_wtall', 'Cruise'])
# plt.show()
# plt.savefig('myfig')






# U_1 = U_de_V_c * K	
# U_2 = U_de_V_c * K	
# U_3 = U_de_V_D * K

# delta_alpha_1 = 0
# delta_alpha_2 = U_2/V_c
# delta_alpha_3 = U_3/V_D	

# delta_L_1 = 0.5*rho*0**2*S_w*delta_alpha_1*a	
# delta_L_2 = 0.5*rho*V_c**2*S_w*delta_alpha_2*a
# delta_L_3 = 0.5*rho*V_D**2*S_w*delta_alpha_3*a

# delta_n_1 = 1+delta_L_1/W
# delta_n_2 = 1+delta_L_2/W
# delta_n_3 = 1+delta_L_3/W

# delta_n_inv_1 = 1-delta_L_1/W
# delta_n_inv_2 = 1-delta_L_2/W
# delta_n_inv_3 = 1-delta_L_3/W





# x = [0, V_c]
# y = [delta_n_1, delta_n_2]
# plt.plot(x, y, '--')


# x = [V_c, V_D]
# y = [delta_n_2, delta_n_3]
# plt.plot(x, y, '--')


# x = [V_D, V_D]
# y = [delta_n_3, delta_n_inv_3]
# plt.plot(x, y, '--')


# x = [V_D, V_c]
# y = [delta_n_inv_3, delta_n_inv_2]
# plt.plot(x, y, '--')


# x = [V_c, 0]
# y = [delta_n_inv_2, delta_n_inv_1]
# plt.plot(x, y, '--')



# plt.axhline(y=0, color='k')
# plt.axvline(x=0, color='k')
# plt.xlabel('Flight speed')
# plt.ylabel('Gust load factor')
# plt.title('Gust Flight Envelope')
# plt.legend(['S_wind', 'Cosine'])
# plt.show()
# plt.savefig('myfig2')


