from PyQt5 import uic

with open('SayfaUi.py', 'w', encoding="utf-8") as fout:
        uic.compileUi('Sayfa.ui', fout)
