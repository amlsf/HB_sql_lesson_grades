#!c:\python27\Scripts\ENV\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'howdoi==1.1.6','console_scripts','howdoi'
__requires__ = 'howdoi==1.1.6'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('howdoi==1.1.6', 'console_scripts', 'howdoi')()
    )
