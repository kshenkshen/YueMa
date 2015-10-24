# YueMa Interfaces

## HTTP

`/avatar/$userId`
获取用户的头像。

## Socket.IO

### 服务端事件

`Login`
用户登录
```javascript
{
	token: , // 记录在Cookies或者localstorage里，用于恢复用户会话。
	username: ,
	password: ,
}
```

`GetProfile`
获取用户的信息
```javascript
{
	userId: $userId
}
```

`GetUsers`
获取在线用户列表

`GetRooms`
获取房间列表

### 客户端事件

`Identity`
返回的登录信息
```javascript
{
	userId: ,
	nickname: ,
	token: , // 用户的临时唯一标识符，记录在Cookies或者localstorage里，用于恢复用户会话。
}
```

`Profile`
返回的用户信息
```javascript
{
	userId: ,
	nickname: ,
	attributes: {
		responsibility: ,
		efficiency: ,
		reputation: ,
	}
}
```

`Users`
返回的用户列表信息
```javascript
[
	{
		userId: ,
		nickname: ,
		status: ,
	}, ...
]
```

`Rooms`
返回的房间列表信息
```javascript
[
	{
		roomId: ,
		taskId: ,
		taskName: ,
		users: [
			userId: ,
			nickname: ,
		]
		status: ,
	}, ...
]
```

`UserConnected`
用户连接事件
```javascript
{
	userId: ,
	nickname: ,
	status: ,
}
```

`UserUpdate`
用户更新事件
```javascript
{
	userId: ,
	nickname: ,
	status: ,
}
```

`UserDisconnected`
用户断开事件
```javascript
{
	userId: ,
}
```


