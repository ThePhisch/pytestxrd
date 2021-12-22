# Anton Schwarz
# pytestxrd: conversion of testxrd from perl to python

from core.connect import connect_xrootd


with connect_xrootd() as s:
    print("Hi")