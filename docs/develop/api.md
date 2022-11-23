## 接口函数
?> 2.0.0-beta.2

>框架为早期版本，对某些 Api 并没有封装，如需使用，请参照 [go-cqhttp 文档](https://docs.go-cqhttp.org/api) 并结合 `Api.Send_Data()` 函数使用

!> 此文档为早期版本，说明并不完善，也可能存在错误，如有错误请加群进行反馈，或在 Github 中提出

### 基本函数
#### 基本接口调用
函数名：`Api.Send_Data()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `action` | str | - | 终结点名称 |
| `params` | dict | - | 要发送的参数 |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |



### 消息管理

#### 发送私聊消息
函数名：`Api.send_private_msg()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `user_id` | int | - | 对方 QQ 号 |
| `message` | str | - | 要发送的内容 |
| `group_id` | int | `0` | 主动发起临时会话群号(自身账号本身必须是管理员/群主) |
| `auto_escape` | bool | `False` | 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效 |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |


#### 发送群聊消息
函数名：`Api.send_group_msg()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `group_id` | int | - | 群号 |
| `message` | str | - | 要发送的内容 |
| `auto_escape` | bool | `False` | 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效 |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |


#### 撤回指定消息
函数名：`Api.delete_msg()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `message_id` | int | - | 消息 ID |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |



### 群聊管理

#### 群组匿名用户禁言
函数名：`Api.set_group_anonymous_ban()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `group_id` | int | - | 群号 |
| `anonymous` | dict | `{}` | 可选, 要禁言的匿名用户对象（群消息上报的 `anonymous` 字段） |
| `flag` | str | `''` | 可选, 要禁言的匿名用户的 flag（需从群消息上报的数据中获得） |
| `duration` | int | `30*60` | 禁言时长, 单位秒, 无法取消匿名用户禁言 |
| `echo` | Any | `None` | 无特殊需求请勿填写 |

>上面的 `anonymous` 和 `flag` 两者任选其一传入即可, 若都传入, 则使用 `anonymous`。
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |


#### 群组单人禁言
函数名：`Api.set_group_ban()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `group_id` | int | - | 群号 |
| `user_id` | int | - | 要禁言的 QQ 号 |
| `duration` | int | `30*60` | 禁言时长, 单位秒, 无法取消匿名用户禁言 |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |


#### 群组全员禁言
函数名：`Api.set_group_whole_ban()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `group_id` | int | - | 群号 |
| `enable` | bool | - | 是否禁言 |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |


#### 群组设置管理员
函数名：`Api.set_group_admin()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `group_id` | int | - | 群号 |
| `user_id` | int | - | 要设置管理员的 QQ 号 |
| `enable` | bool | - | `True` 为设置, `False` 为取消 |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |


#### 处理加群请求／邀请
函数名：`Api.set_group_add_request()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `flag` | str | - | 加群请求的 flag（需从上报的数据中获得） |
| `sub_type` | str | - | `add` 或 `invite`, 请求类型（需要和上报消息中的 `sub_type` 字段相符） |
| `approve` | bool | - | 是否同意请求／邀请 |
| `reason` | str | - | 拒绝理由（仅在拒绝时有效） |
| `group_id` | int、None | `None` | 群号，用于控制台输出详细信息（非必须） |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |

#### 群组踢人
函数名：`Api.set_group_kick()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `group_id` | int | - | 群号 |
| `user_id` | int | - | 要踢的 QQ 号 |
| `reject_add_request` | bool | `False` | 拒绝此人的加群请求 |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |



### 信息获取

#### 获取状态
函数名：`Api.get_status()`
##### 参数
| 字段名 | 数据类型 | 默认值 | 说明 |
| :---- | :---- | :---- | :---- |
| `echo` | Any | `None` | 无特殊需求请勿填写 |
##### 返回
| 数据类型 | 可能的值 | 说明 |
| :---- | :---- | :---- |
| dict | - | [详见 go-cqhttp 文档](https://docs.go-cqhttp.org/api) |