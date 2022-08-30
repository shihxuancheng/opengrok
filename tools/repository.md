
## system-repository definition sample

``` yaml
repositories:
  whl-svn:
    host: http://svn.wanhai.com/svn
    username: 
    password: 
systems:
  dgs:
    repository: whl-svn
    web-path: /whl/web/dgs
    sisapp-path: /whl/sisapp/DGS
```