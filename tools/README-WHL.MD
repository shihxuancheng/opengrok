# Code Search System of WHL

## Directory Design

原始碼目錄架構

``` bash
${SRC_ROOT}
 └──${SYS_CODE}
     ├── sisapp
     └── web
```

## Installation

### Step1: import source from vcs
使用`vcs-importer`從sv server匯入source code
``` shell
    $ /> vcs-import -c ${CONFIG_FILE_PATH} -a ${ACTION} ${SRC_ROOT}
```
`${CONFIG_FILE_PATH}`: 設定檔路徑  
`${ACTION}`: 要執行的動作  
- **checkout:** svn checkout
- **update:** svn update
- **check:** 驗證remote svn path是否正確？
- **add:** 新增專案(需搭配 -U)

`${SRC_ROOT}`: 本機存放source code路徑


## Issues

1. source無法sync (svn password can't cache)，subversion client在1.11版之後已不允許cache username/password
2. start.py 非預期終止，發生時間不定，目前透過docker restart policy解決
4. 使用container中的svn client checkout svn repositorg 遇到(svn: E200030: sqlite[S14]: unable to open database file)問題
