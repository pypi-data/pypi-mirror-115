# How to Use
* 配置pypi: [pypi guide](http://git.dev.sendbp.com/perfectcode/dev-guide/python-dev-guide/blob/master/pypi.md)

* 安装 bert 包  

```
# 初次安装
pip install mc-zouz

# 强制更新
pip install --force-reinstall --no-deps mc-zouz

# 卸载
pip uninstall mc-zouz
```

* 使用  

```
from MCMC import maxmumclique 

Graph = maxmumclique.PyGraph(int(n), int(m))
# 实例化，V为图点数，E为图边数
Graph._map_init_matrix(mp)
# 载入图边关系，Graph._map_init_matrix(mp)，mp为存储边关系的矩阵
Graph._map_init_line(u,v)
# 载入图边关系，Graph._map_init_line(u,v)，u为存储起始点集合，v为存储终点集合
anslist = Graph.Maximum_Clique()
# 求所有极大完全子图，anslist[0]存储最大图边数，anslist[1]存储极大完全子图个数
# i>1时，anslist[i]存储答案，例如anslist[2]=[[1,2,5]]

# 命令

**初始化**:  

```
git submodule init
git submodule update
```


**同步代码**:

```
git pull
git submodule foreach git pull
```
或者: `git pull --recurse-submodules`  


**venv**:

```
python3 -m venv venv --system-site-packages
```

## 引入新项目
* 命令: `git submodule add ${Git_URL} vendor/${Proj_Name}`  
* 示例: `git submodule add https://github.com/google-research/bert.git bert`  


# 私服地址
http://nexus.dev.perfectcode.tech/