#导入mc库
from txmc import Minecraft
import time
#创建MC连接  传入服务器前缀和自己的云授权码
mc=Minecraft.Connect(server='mc',guid="YourGUID")
#获取连接状态  true成功  false失败
print('status:',mc.status)
#在服务器中推送一句话
print('toChat:',mc.toChat("Hello我的世界"))
#获取指定坐标点方块的数据  格式 ID,属性
print('getBlock:',mc.getBlock(1,60,1)) 
#在指定的坐标点放置 (使用方块ID放置)
print('setBlock:',mc.setBlock(-64,66,-62,1,0))
#在指定的坐标点放置 (使用方块名称放置)
print('setBlockByName:',mc.setBlockByName(-64,66,-62,'dirt',0))
#在指定的坐标点放置 (使用方块名称放置)
print('drawLine:',mc.drawLine(-64,66,-62,-64,68,-62,251,5))
#在指定的坐标点放置 (使用方块名称放置)
print('setBlocks:',mc.setBlocks(-64,66,-62,-66,68,-62,251,5))
#在指定的坐标点放置 (使用方块名称放置)
time.sleep(1)
print('setBlocksByName:',mc.setBlocksByName(-64,66,-62,-66,68,-62,'stone',0))
#获取玩家的坐标位置 
print('getMyPos:',mc.getMyPos())
#将我设置为飞行
print('setMyFly:',mc.setMyFly())
time.sleep(1)
#开启我的1号编程箱
print('openInventory:',mc.openInventory(1))
time.sleep(1)
#设置我的坐标  这里的Y坐标是有限制的 一般是 2~255之间
print('setMyPos:',mc.setMyPos(-65,70,-66))
time.sleep(1)
#生成雷电 这里的Y坐标是有限制的 一般是 2~255之间
print('setLight:',mc.setLight(-65,70,-66))
#画一个圆   x 轴 y轴
print('drawCircle:',mc.drawCircle(-65,70,-66,10,1,0,'x'))
time.sleep(1)
#画一个球   0 空心 1实心
print('drawSphere:',mc.drawSphere(-65,90,-66,10,2,0,1))

