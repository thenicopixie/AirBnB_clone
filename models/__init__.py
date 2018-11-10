#!/usr/bin/python3
""" FileStorage instance, for saving to storage
"""
from .engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
