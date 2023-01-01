my_list = ["None", "asd", 'asd']

if all(item is True for item in my_list):
    # 👇️ this runs
    print('All list elements are True')
else:
    print('Not all list elements are True')


# 👇️ True
if any(item is None for item in my_list) is False :
    print("asda")
