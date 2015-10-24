# YueMa Interfaces

TODO: 异常通知。

## HTTP

`/avatar/$userId`
获取用户的头像。

## Socket.IO

### 服务端事件

#### Namespace: /YueMa

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

`GetTasks`
获取任务列表

`CreateRoom`
创建房间
```javascript
{
	taskId: 1,
	taskName: "",
}
```

`MatchRoom`
匹配房间
```javascript
{
	taskId: 1
}
```

`JoinRoom`
加入房间
```javascript
{
	roomId: 1,
}
```

`Start`
开始游戏
```javascript
{
	roomId: 1,
}
```

#### Namespace: /YueMa/room/$roomId

`Update`
更新光标
```javascript
{
	column: 1,
	row: 1,
}
```

`Commit`
更新修改
```javascript
{
	content: "",
}
```

`Blame`
Blame
```javascript
{
	from: 1,
	to: 1,
}
```

`Fix`
Fix
```javascript
{
	blameId: 1,
}
```

`Confirm`
Confirm
```javascript
{
	blameId: 1,
}
```

`Submit`
提交

### 客户端事件

#### Namespace: /YueMa

`Identity`
返回的登录信息
```javascript
{
	userId: 1,
	nickname: "",
	token: "", // 用户的临时唯一标识符，记录在Cookies或者localstorage里，用于恢复用户会话。
}
```

`GetProfile`
返回的用户信息
```javascript
{
	userId: 1,
	nickname: "",
	attributes: {
		responsibility: 5.0,
		efficiency: 5.0,
		reputation: 5.0,
	}
}
```

`GetHistory`
返回的战绩信息
```javascript
[
	{
		historyId: 1,
		taskId: 1,
		userId: 1,
		partnerId: 2,
		blamingCount: 4,
		blamedCount: 2,
		fixedCount: 2,
		characterCount: 24,
		elapsedTime: 20000,
		efficiency: 0.5,
		result: "void main() { printf(\"Helloworld!\"); }",
	}, ...
]
```

`GetUsers`
返回的用户列表信息
```javascript
[
	{
		userId: 1,
		nickname: "",
		status: "IDLE",
	}, ...
]
```

`GetRooms`
返回的房间列表信息
```javascript
[
	{
		roomId: 1,
		taskId: 1,
		taskName: "",
		users: [
			userId: 1,
			nickname: "",
		]
		status: "WAIT",
	}, ...
]
```

`GetTasks`
返回的任务列表信息
```javascript
[
	{
		taskId: 1,
		name: "",
		tags: [
			"Java",
		],
		description: "",
	}, ...
]
```

`UserConnected`
用户连接事件
```javascript
{
	userId: 1,
	nickname: "",
	status: "IDLE",
}
```

`UserUpdate`
用户更新事件
```javascript
{
	userId: 1,
	nickname: "",
	status: "PLAY",
}
```

`UserDisconnected`
用户断开事件
```javascript
{
	userId: 1,
}
```

`CreateRoom`
返回的创建房间的信息
```javascript
{
	roomId: 1,
	taskId: 1,
	taskName: "",
}
```

`JoinRoom`
返回的加入房间的信息
```javascript
{
	roomId: 1,
	taskId: 1,
	taskName: "",
}
```

`Start`
返回的开始游戏的信息
```javascript
{
	roomId: 1,
	taskId: 1,
	taskName: "",
	taskTags: [
		"Java",
	],
	taskDescription: "",
	taskDetail: "",
	taskDeadline: 300000,
}
```

#### Namespace: /YueMa/room/$roomId

`Acquire`
取得控制权
```javascript
{
	from: 1,
}
```

`Release`
释放控制权

`Result`
结果
```javascript
{
	efficiency: 0.5,
	user: {
		
	},
	partner: {
	
	}
}
```
