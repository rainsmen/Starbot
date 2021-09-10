import random
import os
import global_vars

path = global_vars.get_var('setu_folder')
imgs = []
src = ''
for x in os.listdir(path):
    if x.endswith('jpeg'):
        imgs.append(x)
    if x.endswith('png'):
        imgs.append(x)
    if x.endswith('jpg'):
        imgs.append(x)


def setu_geturl():
    selected_imgs = random.sample(imgs, 1)
    src = os.path.join(path, selected_imgs[0])
    return src
