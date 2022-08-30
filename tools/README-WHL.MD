# Code Search System of WHL

## Directory Design

原始碼目錄架構

``` bash
${SYS_CODE}
├── sisapp
└── web

```

## Issues

1. source無法sync (svn password can't cache)
2. start.py 非預期終止，發生時間不定，目前透過docker restart policy解決
3. 使用container中的svn client checkout svn repositorg 遇到(svn: E200030: sqlite[S14]: unable to open database file)問題