import os
import math
from time import sleep
from enum import Enum
from threading import Lock
from collections import namedtuple
from threading import Thread
from typing import List
import shelve

import pathlib
import datetime

import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

import glfw
import OpenGL.GL as gl
import OpenGL.GL.shaders
import pyrr
import imgui
import imgui.core
import imgui_datascience
from imgui_datascience import imgui_cv
from imgui.integrations.glfw import GlfwRenderer
from imgui.integrations.opengl import BaseOpenGLRenderer
#from cgitb import small
#from math import floor
#from time import sleep
#from turtle import isdown

import instrument_references
from devices.device import Device
#from application import *
