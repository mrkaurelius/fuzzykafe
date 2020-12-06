from aftertaste.aftertaste import AfterTaste

at = AfterTaste()
at.build_memberships()
at.plot()
ms_list = at.calc_memberships(7.25);
print(ms_list)