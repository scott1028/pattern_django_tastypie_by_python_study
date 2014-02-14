# coding: utf-8

# 利用 init 機制讓他找到 model folder 內定義的 model
# 因為不再 django 原本定義的位置, 所以命名的 model 必須加上 app_label 在 model meta 內。
from .models import *