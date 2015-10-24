# YueMa API

## 服务端事件

`Ready`
请求开始游戏
```javascript
{
	username: "",
}
```

`Push`
推送完整代码
```javascript
{
	code: "",
}
```

`Submit`
提交

`Message`
发送信息
```javascript
{
	message: "",
}
```

## 客户端事件

`Start`
玩家匹配 -> 开始游戏
```javascript
{
	task: "",
	deadline: 300000,
}
```

`Acquire`
得到控制权

`Release`
失去控制权

`Push`
推送完整代码
```javascript
{
	code: "",
}
```

`Result`
结果
```javascript
{
	// TODO:
}
```

`Message`
收到信息
```javascript
{
	message: "",
}
```