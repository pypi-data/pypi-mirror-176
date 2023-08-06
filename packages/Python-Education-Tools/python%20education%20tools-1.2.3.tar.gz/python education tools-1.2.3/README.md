# Prof.Li's Python Education Tools
## 道法自然
## **pip install -U python-education-tools**
* Python Education Tools模块为教材配套工具 *
* 由作者Prof.Luqun Li团队自主开发。
** 取Python Education Tools 首字母的缩写为pet（英文意思：宠物），简称pet工具 **

![hah](https://tse1-mm.cn.bing.net/th/id/OIP-C.1WzofyXU4XlVG1soFYMmpgHaEc?w=273&h=180&c=7&r=0&o=5&dpr=2&pid=1.7)
`````
模块的安装：
     pip install -U python-education-tools

模块安装后对应的安装包为 pet.data.* 、pet.textbook1.*等。
今后会不断扩充相关教学工具，所有工具包的根目录是pet，pet是Python Education Tools 首字母的缩写。

** Pet相关模块的使用：**

1.	趣谈编程之道：
与“晦涩难懂的”Python编程之禅import this对应，本模块从中国传统文化，心，术，法三个层次，引用古文阐述编程之道。

 import pet.this

Just for Fun！！！（不笑不足以为道!!)

2.	教材配套的案例下载（运行以下1行Python代码）：
  import pet.textbook1.codes
  
  稍后，即可将教学案例下载到桌面教学案例目录。

3.	教材相关的样本数据加载：

from pet.data import load_data

df1 = load_data.load_data('ip_address.xlsx')
'''
提供了如下数据集名称：
输入：ip_address.xlsx  -ip地址分类。返回：dataframe
输入：st.xls -某高校研究生初试成绩。返回：dataframe
输入：subway.xlsx  -上海地铁线路数据。返回：dataframe
输入：ddj.txt -道德经文本。返回：字符串。
输入：tyjhzz.txt-《太乙金华宗旨》。返回：字符串。
今后将陆续增加数据文件
'''
其它数据：
load_data.votes #投票文本数据
load_data.cookies  #某cookies数据

4.	伪数据的随机生成器：
    以下2个函数可以随机生成相关数据。
dffs = load_data.generate_sr(rows=100)
'''
生成一个Series对象，对象内数据条数默认40条，可任意设置。
'''
dfff = load_data.generate_df(rows=200)
'''
生成一个dataframe对象，对象内数据条数默认40条，可任意设置。shape是（n，13），n为数据条数
'''



`````



![hah](https://img.niuqiuyi.com/202210/19/012355471.png)