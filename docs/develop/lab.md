## 试验性函数

!>这里提供的均为试验性函数，后期随时可能更改或移除。如果使用这里的函数，请修改兼容性标识符为： `["2.0.0-beta.3-beta"]`

### 配置文件读取
导入：`from core import config_tools`

#### ini配置文件
函数名：`config_tools.read_ini()`
##### 说明
读取单个配置置设文件

注：您可以对返回的对象修改后使用`.write()`进行写入操作
##### 参数
| 字段名        | 数据类型     | 默认值    | 说明      |
|:-----------|:---------|:-------|:--------|
| `file`     | str      | -      | 文件所在的路径 |
| `encoding` | str、None | `None` | 可选，文件编码 |
##### 返回
| 数据类型      | 可能的值 | 说明             |
|:----------|:-----|:---------------|
| ConfigObj | -    | 可以像字典一样，读取或者修改 |


#### 读取文本
函数名：`config_tools.read_file_as_text()`
##### 说明
读取文本并返回字符串
##### 参数
| 字段名        | 数据类型     | 默认值    | 说明      |
|:-----------|:---------|:-------|:--------|
| `file`     | str      | -      | 文本文件路径  |
| `encoding` | str、None | `None` | 可选，文件编码 |
##### 返回
| 数据类型 | 可能的值 | 说明         |
|:-----|:-----|:-----------|
| str  | -    | 字符串形式的文本内容 |


`我累了，文档写不下去了，所有的源码都有注释，你们看源码吧 555...`
### 数据库操作
#### 说明
导入：`from core.keiyume import Sqlite` 或 `from core.sqlite import Sqlite`

类名：`Sqlite`

对 Sqlite3 的原始函数做了简易封装
- 相对路径以框架主程序所在位置为准，您可以通过在插件中与 `__init__.py` 同一目录的文件下使用 `os.path.dirname(__file__)` 在插件内获取插件文件夹所在的路径

!>由于本框架属于多线程框架，受限于 `sqlite` 暂时不能跨线程调用，`Sqlite` 可能需要在每次插件运行的时候进行实例化，不可以将实例化后的对象留到下次运行时调用，调用完成后记得及时使用 `sql.close()` 断开数据库


#### 连接数据库
函数名：`sql = Sqlite()`
##### 说明
用于连接 Sqlite 数据库，若不存在则自动创建

请修改兼容性标识符为： `["2.0.0-beta.3-beta"]`
##### 参数
| 字段名        | 数据类型 | 默认值 | 说明                   |
|:-----------|:-----|:----|:---------------------|
| `database` | str  | -   | Sqlite（.db）数据库文件所在路径 |
##### 返回
无
##### 示例
`sql = Sqlite("./data.test.db")`


#### 新建数据表
函数名：`sql.new()`
##### 说明
如果数据表不存在则新建数据表（数据表含有id列）
##### 参数
| 字段名          | 数据类型 | 默认值 | 说明                                                                                                                  |
|:-------------|:-----|:----|:--------------------------------------------------------------------------------------------------------------------|
| `table_name` | str  | -   | 创建的数据表的名字                                                                                                           |
| `**kwargs`   | dict | -   | 需要创建的列名（字典的 `key`）和列的数据类型（字典的 `value`）<br>常用的数据类型有：<br>`INT` 整数值<br>`BIGINT` 极大整数值<br>`BLOB` 二进制数据<br>`TEXT` 文本数据 等 |
##### 返回
| 数据类型 | 可能的值   | 说明  |
|:-----|:-------|:----|
| None | `None` | -   |
##### 示例A
`sql.new('数据表表名', info1 = 'INT', info2 = 'TEXT')`
##### 示例B
`sql.new('数据表表名', **{'info1': 'INT', 'info2': 'TEXT'})`


#### 查询数据
函数名：`sql.read()`
##### 说明
根据 [条件语句](https://blog.csdn.net/csucsgoat/article/details/115357650) 查询数据库内容，注意：别忘了填写 ``
##### 参数
| 字段名          | 数据类型  | 默认值  | 说明         |
|:-------------|:------|:-----|:-----------|
| `table_name` | str   | -    | 数据表表名      |
| `condition`  | str   | `''` | 条件语句       |
| `*args`      | tuple | -    | 可选，需要查询的列名 |
##### 返回
| 数据类型        | 可能的值 | 说明        |
|:------------|:-----|:----------|
| list[tuple] | -    | 符合条件的数据列表 |
##### 示例A
`sql.read('数据表表名', 'id = 1' ,'info1', 'info2')`
##### 示例B
`sql.read('数据表表名', 'id = 1' ,*('info1', 'info2'))`


#### 写入数据
函数名：`sql.write()`
##### 说明
向数据库中新写入一行数据
##### 参数
| 字段名          | 数据类型 | 默认值    | 说明                    |
|:-------------|:-----|:-------|:----------------------|
| `table_name` | str  | -      | 数据表表名                 |
| `commit`     | bool | `True` | 是否提交更改，批量写入建议全部更改完再提交 |
| `**kwargs`   | dict | -      | 需要写入的数据（可变参数）         |
##### 返回
| 数据类型 | 可能的值   | 说明  |
|:-----|:-------|:----|
| None | `None` | -   |
##### 示例A
`sql.write('数据表表名', info1 = '数据1', info2 = '数据2')`
##### 示例B
`sql.write('数据表表名', **{'info1': '测试', 'info2': '测试2'})`


#### 删除数据
函数名：`sql.delete()`
##### 说明
根据 [条件语句](https://blog.csdn.net/csucsgoat/article/details/115357650) 删除数据库内容
##### 参数
| 字段名          | 数据类型 | 默认值    | 说明                    |
|:-------------|:-----|:-------|:----------------------|
| `table_name` | str  | -      | 数据表表名                 |
| `condition`  | str  | `''`   | 条件语句                  |
| `commit`     | bool | `True` | 是否提交更改，批量删除建议全部更改完再提交 |
##### 返回
| 数据类型 | 可能的值   | 说明  |
|:-----|:-------|:----|
| None | `None` | -   |
##### 示例
`sql.delete('数据表表名', 'info1="测试"')`


#### 更新数据
函数名：`sql.update()`
##### 说明
根据 [条件语句](https://blog.csdn.net/csucsgoat/article/details/115357650) 更新数据库中已存在的内容
##### 参数
| 字段名          | 数据类型 | 默认值    | 说明                    |
|:-------------|:-----|:-------|:----------------------|
| `table_name` | str  | -      | 数据表表名                 |
| `condition`  | str  | `''`   | 条件语句                  |
| `commit`     | bool | `True` | 是否提交更改，批量更新建议全部更改完再提交 |
| `**kwargs`   | dict | -      | 需要更新的数据（可变参数）         |
##### 返回
| 数据类型 | 可能的值   | 说明  |
|:-----|:-------|:----|
| None | `None` | -   |
##### 示例A
`sql.update('数据表表名', info1 = "测试2")`
##### 示例B：
`sql.update('数据表表名', {info1: "测试2"})`


#### 智能写入数据
函数名：`sql.auto_write()`
##### 说明
根据 [条件语句](https://blog.csdn.net/csucsgoat/article/details/115357650) 更新或写入数据库中已存在的内容。若数据不存在则新写入一行，若数据存在则更新数据
##### 参数
| 字段名          | 数据类型 | 默认值  | 说明            |
|:-------------|:-----|:-----|:--------------|
| `table_name` | str  | -    | 数据表表名         |
| `condition`  | str  | `''` | 条件语句          |
| `**kwargs`   | dict | -    | 需要更新的数据（可变参数） |
##### 返回
| 数据类型 | 可能的值   | 说明  |
|:-----|:-------|:----|
| None | `None` | -   |
##### 示例A
`sql.auto_write('数据表表名', 'id=2', info2 = "测试3")`
##### 示例B
`sql.auto_write('数据表表名', 'id=2', {info2: "测试3"})`


#### 提交更改
函数名：`sql.commit()`
##### 说明
提交对数据库的更改
- 之前的函数均默认自动提交更改，若特别指定了不自动提交更改，请记得运行此函数提交更改
##### 参数
- 此函数不存在参数
##### 返回
| 数据类型 | 可能的值   | 说明  |
|:-----|:-------|:----|
| None | `None` | -   |
##### 示例
`sql.commit()`


#### 撤销更改
函数名：`sql.rollback()`
##### 说明
撤销上次对数据库提交的更改
##### 参数
- 此函数不存在参数
##### 返回
| 数据类型 | 可能的值   | 说明  |
|:-----|:-------|:----|
| None | `None` | -   |
##### 示例
`sql.rollback()`


#### 断开数据库
函数名：`close()`
##### 说明
断开与数据库的连接
- 为了数据安全，建议您在程序关闭前，或完全不用时断开与数据库的连接
##### 参数
- 此函数不存在参数
##### 返回
| 数据类型 | 可能的值   | 说明  |
|:-----|:-------|:----|
| None | `None` | -   |
##### 示例
`sql.close()`



## 框架交互

导入方法：`from core.keiyume import frame`

### 修改设置
函数名：`frame.change_setting()`
#### 说明
修改框架配置文件并立即应用当前设置
#### 参数
| 字段名         | 数据类型         | 默认值 | 说明                                                                                                                                  |
|:------------|:-------------|:----|:------------------------------------------------------------------------------------------------------------------------------------|
| `operation` | str          | -   | 操作类型，可以用的类型有：<br>`add` 添加指定值<br>`del` 删除指定值<br>`clear` 删除全部值<br>`change` 修改指定值                                                      |
| `keyword`   | str          | -   | 需要修改的设置，可以用的类型有：<br>`super_user` 超级用户<br>`super_admin` 超级管理员<br>`enable_group` 启用插件的群聊<br>`disable_group` 禁用插件的群聊                   |
| `content`   | str、int、list | -   | 如果操作类型为 `add` 添加指定值 或 `del` 删除指定值，只支持输入 str、int 类型的数字<br>如果操作类型为 `clear` 删除全部值，不需要输入此变量<br>如果操作类型为 `change` 修改指定值，需要输入一个内部数据均为整数的列表 |
#### 返回
| 数据类型      | 可能的值                  | 说明                                            |
|:----------|:----------------------|:----------------------------------------------|
| bool、None | `True`、`False`、`None` | 操作成功返回 `True`，不需要执行操作 `False`，不支持的操作类型 `None` |
#### 示例
添加一个 `用户 ID` 为 `123456` 的超级用户：
`frame.change_setting("add", "super_user", 123456)`

### 读取设置
函数名：`frame.read_settings()`
#### 说明
读取框架配置文件，返回一个 `ConfigObj` 对象，但是可以像字典一样，读取或者修改其中的值，修改值之后使用 `.write()` 将更改写入到配置文件
#### 参数
无
#### 返回
| 数据类型      | 可能的值 | 说明             |
|:----------|:-----|:---------------|
| ConfigObj | -    | 可以像字典一样，读取或者修改 |
#### 示例
输出配置文件中 `info` 节中的 `wizard` 键的值
```
print(frame.read_settings()["info"]["wizard"])

# 0
```

### 获取框架版本
函数名：`frame.get_version()`
#### 说明
获取框架版本
#### 参数
无
#### 返回
| 数据类型 | 可能的值           | 说明      |
|:-----|:---------------|:--------|
| str  | `2.0.0-beta.3` | 当前的框架版本 |
#### 示例
输出配置文件中 `info` 节中的 `wizard` 键的值
```
print(frame.get_version())

# 2.0.0-beta.3
```

### 断开连接
函数名：`frame.disconnect()`
#### 说明
使框架与 go-cqhttp 断开连接
#### 参数
无
#### 返回
`None`
#### 示例
`frame.disconnect()`

### 退出程序
函数名：`frame.exit_frame()`
#### 说明
断开连接并退出框架
#### 参数
无
#### 返回
`None`
#### 示例
`frame.exit_frame()`



## 试验性功能

### 特殊用法

#### 与其他插件共享变量或对象
- 敬请期待（这个东西好像很不规范呐）
