# Online Judge Interfaces

## HTTP POST

### /oj/submit/

##### Request
```json
{
  "pid": 1,
  "lang": "py",
  "code": "dGVzdA=="
}
```

pid: 题目编号

lang: 语言(py, c)

code: base64编码后的代码

##### Response
```json
{
  "success": true,
  "err_code": 0,
  "fid": "7abd35c9146fa4b56a2b73667b91d6ed"
}
```

success: 提交成功与否

err_code: 错误信息, 0 代表 post body 不可解析, 1 代表 json 的键不符合要求, 2 代表 base64 解码错误, 3 表示该 lang 不支持

fid: 之后用于抓取本次 judge 结果的 md5 码

## HTTP GET

###  /oj/status/:fid

fid: submit 时返回的 fid

##### Response
```json
{
  "ac": true,
  "status_code": 0
}
```

ac: 是否通过 judge

status_code: judge 状态, 0 表示正在处理, 1 表示完毕

### /oj/problems/random/:difficulty

difficulty: 题目难度, 0-2

##### Response
```json
{
  "pid": 1,
  "desc": "题目描述，没有标题",
  "swt_time_range": [10, 20],
  "total_time": 300
}
```

pid: 题目 id
desc: 题目描述，没有标题
swt_time_range: 一个人写一段代码的时间范围
total_time: 一道题的上限时间
