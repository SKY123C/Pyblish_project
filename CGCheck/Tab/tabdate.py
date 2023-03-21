#coding=utf-8
import os
TABMAP = [
    {
        "Aka": "msg_info",
        "Label": "Info",
        "UI": "checkinfo.json",
        "CheckState": True
    },
    {
        "Aka": "validator_info",
        "Label": "Validation Info",
        "UI": "validation.json",
        "CheckState": False
    }
]

WIDGETSPATH = os.path.join(os.path.dirname(__file__), "widgets")
TEMPLATEPATH = os.path.join(os.path.dirname(__file__), "template")

CURRENTAKA = None

