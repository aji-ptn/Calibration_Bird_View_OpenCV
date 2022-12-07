my_list = [True, True, True]

if all(item is True for item in my_list):
    # 👇️ this runs
    print('All list elements are True')
else:
    print('Not all list elements are True')


# 👇️ True
print(all(item is True for item in my_list))
