# # # # #1
# # # # def net_price(list_price, discount = 0 , tax= 0.05):
# # # #     return list_price *(1-discount)*(1+tax)
# # # # print(net_price(500,0.1,0))

# # # # 2
# # # import time
# # # def count(end , start=0):
# # #     for x in range(start, end+1):
# # #         print (x)
# # #         time.sleep(1)
# # #     print("Done")
# # # count(10)

# # # 3
# # def phone_num(country,area, first,last,):
# #     print(f"{country}-{area}-{first}-{last}")

# # get_phone = phone_num(area = 11, first = 2719, last=9679, country=60)
# # print(get_phone)


# # 4 *args and **kwargs

# def add(*args):
#     total = 0
#     for arg in args:
#         total += arg
#     return total
# print(add(1,2,3,4,5,6,7,8,9,10))


#5 
def shipping_label (*args, **kwargs):
    for arg in args:
        print(arg, end=" ")
    print()
    for value in kwargs.values():
        print(value , end="")

shipping_label("Dr","Hikaru","Nakamura",
               street="jalan ikram",
               apt="c3-02",
               city="kajang",
               state="selangor ",
               acc="cendi")