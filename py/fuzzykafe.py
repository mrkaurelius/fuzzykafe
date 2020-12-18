from aftertaste.aftertaste import AfterTaste
from aftertaste.membership import Membership


#%% abdul
at = AfterTaste()

at.build_memberships()
at.plot()
ms_list = at.calc_memberships(7.38)
print(ms_list)

#%% celil virgulden sonra iki basakmakta fark ediyor

# def cal_desc_y(x,start_x,end_x):#azalan
#     return (end_x-x)/(end_x-start_x)

# def cal_asc_y(x,start_x,end_x):
#     return (x-start_x)/(end_x-start_x)


# def cal(x):
#     memberships =  at.memberships
#     my_memberships = []
    
#     for member in memberships:
#         if(member.i_start < x and member.i_end >= x):
#             my_memberships.append(member)


#     if(len(my_memberships) == 0):
#         return list((0,0,0))
#     elif(len(my_memberships) == 1):
#         if(my_memberships[0].name == 'DUSUK'):
#             return list((1,0,0))
#         elif(my_memberships[0].name == 'ORTA'):
#             return list((0,1,0))
#         elif(my_memberships[0].name == 'YUKSEK'):
#             return list((0,0,1))
#     else:#üyelerin listeye atılma sırasından biliyoruz ki ilk üyenin grafiği ilgili bölgede azalandır.
#         first_member = my_memberships[0]
#         second_member = my_memberships[1]

#         first_y = cal_desc_y(x,second_member.i_start, first_member.i_end)
#         second_y = cal_asc_y(x,second_member.i_start, first_member.i_end)

#         if(first_member.name == 'DUSUK'):
#             return list((first_y,second_y,0))
#         else:
#             return list((0,first_y,second_y))

# print(cal(7.38))