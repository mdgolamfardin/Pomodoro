from setuptools import setup

APP = ['main.py']
DATA_FILES = [('resources', ['/Users/fardinmdgolam/Desktop/Contents/Study/Python Cours/PycharmProjects/Day 28 - Pomodoro/pomodoro-start/tomato.png'])]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',  # Path to your .icns icon file
    'packages': ['tkinter', 'subprocess'],
    'plist': {
        'CFBundleName': 'Main',
        'CFBundleDisplayName': 'Main',
        'CFBundleIdentifier': 'com.yourname.main',
        'CFBundleShortVersionString': '0.1.0',
        'CFBundleVersion': '0.1.0',
        'LSUIElement': False,  # Optional: hides the app icon from the Dock
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
