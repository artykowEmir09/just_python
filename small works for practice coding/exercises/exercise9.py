# 1
# doubles = [x*2 for x in range(1,11)]
# # print(doubles)

# 2
# numbers = [1,-2,3,-4,5,-6]
# positive_num = [num for num in numbers if num >0]
# print (positive_num)

#3
def days_of_week(day):
    match day :
        case 1:
             return "It is Sunday"
        case 2:
            return "It is Monday"
        case 3:
             return "It is Tuesday"
        case 4:
            return "It is Wednesday"
        case 5:
            return "It is Thurday"
        case 6:
            return "It is Friday"
        case 7:
            return "It is Saturday"
        case _:
            return "Not invalid Day"
print(days_of_week(2))
    
    