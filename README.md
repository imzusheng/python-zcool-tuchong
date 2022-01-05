需要修改的代码在[works.py](./blogWorks/spiders/works.py)
```bash
def __init__(self):
    self.username = '<站酷账号>'
    self.password = '<站酷账号>'
    # mongodb uri
    self.client = pymongo.MongoClient('mongodb://localhost:27017')
    # 数据库名
    db = self.client['blog']
    # 集合名
    self.col = db['works']
    ...
```

`chromedriver`版本要和PC安装的chrome版本匹配, 这个版本是`96.0.4664.45`

在根目录执行
```bash
scrapy crawl works
```

站酷保存的数据格式
```json lines
{
    "_id": "1641377714527066",  // 时间戳
    "describeTitle": "P50 Pro", // 标题
    "describeContent": "三维-产品", // 分类
    "describeDate": "153天前",  // 发布时间
    "hot": "94",  // 热度
    "like": "2", // 推荐
    "src": "https://www.zcool.com.cn/work/ZNTQ0MjEwNTI=.html", // 源地址
    "poster": "https://img.zcool.cn/community/****.jpg", // 封面
    "category": "CINEMA 4D" // 分类
}
```

图虫保存的数据格式
```json lines
{
    "_id": "1641377714620644",  // 时间戳
    "category": "Photo", // 分类
    "colSum": [" 3张 "], // 集合照片数量
    "poster": "https:////photo.tuchong.com/14082769/ft640/226613970.webp", // 照片
    "like": "16", // 喜欢
    "src": "https://tuchong.com/14082769/76355838/", // 源地址
    "height": "289", // 高度
    "width": "433" // 宽度
}
```

