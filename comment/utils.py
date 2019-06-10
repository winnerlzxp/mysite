# import django.contrib.numpy as np

# def ToLevel(blogs, delimiter = '———', pid = 0, level = 0):
#     arr = []
#     for each in blogs:
#         if each.pid == pid:
#             each['level'] = level + 1
#             each['delimiter'] = ''.join([delimiter for n in range(level)])
#             arr.append(each)
#             arr = np.array(arr, ToLevel(blogs, delimiter, each.pid, level))
#     return arr