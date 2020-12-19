#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 21:29:43 2020

@author: yavuz
"""

#!pip install scikit-fuzzy

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

x_mud = np.arange(0, 100, 1)
x_axunge = np.arange(0, 100, 1)
x_wash = np.arange(0, 60, 1)

mud_SD = fuzz.trimf(x_mud, [0, 0, 50])
mud_MD = fuzz.trimf(x_mud, [0, 50, 100])
mud_LD = fuzz.trimf(x_mud, [50, 100, 100])

axunge_NG = fuzz.trimf(x_axunge, [0, 0, 50])
axunge_MG = fuzz.trimf(x_axunge, [0, 50, 100])
axunge_LG = fuzz.trimf(x_axunge, [50, 100, 100])

wash_VS = fuzz.trimf(x_wash, [0, 0, 10])
wash_S = fuzz.trimf(x_wash, [0, 10, 25])
wash_M = fuzz.trimf(x_wash, [10, 25, 40])
wash_L = fuzz.trimf(x_wash, [25, 40, 60])
wash_VL = fuzz.trimf(x_wash, [40, 60, 60])

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8,9))
ax0.plot(x_mud, mud_SD, 'b', linewidth=1.5, label='SD')
ax0.plot(x_mud, mud_MD, 'g', linewidth=1.5, label='MD')
ax0.plot(x_mud, mud_LD, 'r', linewidth=1.5, label='LD')
ax0.set_title('MUD')
ax0.legend()
ax1.plot(x_axunge, axunge_NG, 'b', linewidth=1.5, label='NG')
ax1.plot(x_axunge, axunge_MG, 'g', linewidth=1.5, label='MG')
ax1.plot(x_axunge, axunge_LG, 'r', linewidth=1.5, label='LG')
ax1.set_title('axunge')
ax1.legend()
ax2.plot(x_wash, wash_VS, 'b', linewidth=1.5, label='VS')
ax2.plot(x_wash, wash_S, 'g', linewidth=1.5, label='S')
ax2.plot(x_wash, wash_M, 'r', linewidth=1.5, label='M')
ax2.plot(x_wash, wash_L, 'y', linewidth=1.5, label='L')
ax2.plot(x_wash, wash_VL, 'm', linewidth=1.5, label='VL')
ax2.set_title('washing time')
ax2.legend()

for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout()    

mud_level_SD = fuzz.interp_membership(x_mud, mud_SD, 60)
mud_level_MD = fuzz.interp_membership(x_mud, mud_MD, 60)
mud_level_LD = fuzz.interp_membership(x_mud, mud_LD, 60)
print(mud_level_SD)
print(mud_level_MD)
print(mud_level_LD)

axunge_level_NG = fuzz.interp_membership(x_axunge, axunge_NG, 70)
axunge_level_MG = fuzz.interp_membership(x_axunge, axunge_MG, 70)
axunge_level_LG = fuzz.interp_membership(x_axunge, axunge_LG, 70)

active_rule1 = np.fmin(mud_level_MD, axunge_level_MG)
active_rule2 = np.fmin(mud_level_MD, axunge_level_LG)
active_rule3 = np.fmin(mud_level_LD, axunge_level_MG)
active_rule4 = np.fmin(mud_level_LD, axunge_level_LG)
print(active_rule1)

wash_activation1 = np.fmin(active_rule1, wash_M)
wash_activation2 = np.fmin(active_rule2, wash_L)
wash_activation3 = np.fmin(active_rule3, wash_L)
wash_activation4 = np.fmin(active_rule4, wash_VL)
wash0 = np.zeros_like(x_wash)

fig, ax0 = plt.subplots(figsize=(8, 3))
ax0.fill_between(x_wash, wash0, wash_activation1, facecolor='b', alpha=0.7)
ax0.plot(x_wash, wash_M, 'b', linewidth=0.5, linestyle='--', )
ax0.fill_between(x_wash, wash0, wash_activation2, facecolor='g', alpha=0.7)
ax0.plot(x_wash, wash_L, 'g', linewidth=0.5, linestyle='--', )
ax0.fill_between(x_wash, wash0, wash_activation3, facecolor='r', alpha=0.7)
ax0.plot(x_wash, wash_L, 'r', linewidth=0.5, linestyle='--', )
ax0.fill_between(x_wash, wash0, wash_activation4, facecolor='r', alpha=0.7)
ax0.plot(x_wash, wash_VL, 'y', linewidth=0.5, linestyle='--', )
ax0.set_title('Output membership activity')
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout() 

aggregated = np.fmax (wash_activation1, 
                      np.fmax(wash_activation2, np.fmax(wash_activation3, wash_activation4))) 

wash = fuzz.defuzz(x_wash, aggregated, 'centroid')
wash_activation = fuzz.interp_membership(x_wash, aggregated, wash)
fig, ax0 = plt.subplots(figsize=(8, 3))
ax0.plot(x_wash, wash_VS, 'b', linewidth=1.5, linestyle='--')
ax0.plot(x_wash, wash_S, 'g', linewidth=1.5, linestyle='--')
ax0.plot(x_wash, wash_M, 'r', linewidth=1.5, linestyle='--')
ax0.plot(x_wash, wash_L, 'y', linewidth=1.5, linestyle='--')
ax0.plot(x_wash, wash_VL, 'm', linewidth=1.5, linestyle='--')
ax0.fill_between(x_wash, wash0, aggregated, facecolor='Orange', alpha=0.7)
ax0.plot([wash, wash], [0, wash_activation], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Aggregated membership and result (line)')
plt.tight_layout()