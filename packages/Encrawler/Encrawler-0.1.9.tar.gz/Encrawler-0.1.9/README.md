# SearchEngineCrawler

#### 介绍
搜索引擎爬虫

#### 接口

- baidu: `https://www.baidu.com/s?wd={}`, method: GET


#### 软件架构
软件架构说明


#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

#### 使用说明

所有的搜索引擎爬虫都是通过search方法作为入口。参数有
- keyword：关键词
- start_page = 

1.  Bing爬虫

```
from spdiers.bing import BingSpider


bing_spider = BingSpider()
proxy_args = {
    "proxies": "ur proxy info",
    "auth": "ur auth info"
}
bing_spider.search("原神 派蒙", start_page = 0, end_page = 1, item_num = 1, **kwargs)

```
#### 关于bing news global
接口:
https://global.bing.com/news/?setlang=en-us&setmkt=en-us

**说明**：





必须要的COOKIE是

```
MUIDB= 007E5F15311D65FF38444D58308964F4;_EDGE_S= SID=33E7CE590CE063403B92DC0E0D86625E&mkt=en-us&ui=en-us;
```

其中_EDGE_S好像是固定的
MUIDB可以通过访问一次获得set-cookie，有效期大概能25天。

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
