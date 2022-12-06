<div align="right">
  Language:
  cn
  <a title="English" href="/README.md">us</a>
</div>

# 需求分析

## 输入输出约定

输入：需要编译的c语言程序、文法规则json格式文件。

输出：在项目一的词法分析表、语法分析树、ACTION+GOTO表、栈过程的基础上添加中间代码表, 静态检查错误列表。

### 源程序输入

在输入框中输入含过程调用或不含过程调用的类c语言程序代码，示例请参见提交文件夹里面以下文件:

3_程序测试代码(实例)

```
├───文法规则
│       grammer.json
│
├───类c语言
│       不含过程调用.c
│       含过程调用.c
│       错误示例1-变量重复定义.c
│       错误示例2-变量未定义.c
│       错误示例3-函数重复定义.c
│       错误示例4-函数未定义.c
│       错误示例5-类型错误.c
│       错误示例6-函数参数数目不对.c
│       错误示例7-函数参数类型不对.c
│
└───运行截图请参见报告
```

对于不同类型的错误代码, 本报告的第四部分将给出简化的示例.

### 语义分析输出

- 中间代码分析表

### 静态检查分析输出

- 静态检查发现的错误列表

## 程序功能

### 语义分析器

我们实现了含过程调用的类C语言的语义分析与中间代码生成, 用户可以自己进行任意程序的测试与翻译, 并且实时查看任意项目的分析结果.

### 静态语义检查

在语义分析的过程中, 我们实现了对于类型不匹配, 变量定义等7种语义错误的检查, 给出了用户友好的错误提示, 并且实现了基本的错误恢复的功能, 即在一次检查中可以实现对于程序完整的扫描, 发现程序里面绝大多数的错误.

# 概要设计

## 任务分解

从用户的角度上，我们将任务分解为以下两个方面：

### 中间代码展示:

中间代码以表格的形式加以呈现

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=ZDIwZjZjOTVhMGZmMjRkOThiOWI4YjgyNjIwOTVkNGFfRE1xVlBjMFlzdXpCelo2UndsS01NZWZJb3IwS083d3VfVG9rZW46Ym94Y256SGdjbEhwMWVTbTJmMEthOWhQS1RiXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

 

### 静态检查结果展示

静态检查结果结果同样以表格的形式加以展现, 

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MWE5Y2UzMzc3Zjk2OTBiNjY0NDAxNGE2ZGQ1ZTE2MGVfcWF6SWkxTEczbWlacjlBUk1NVmE1OHVocTRWZUQzMmdfVG9rZW46Ym94Y25zbzdBckhjRUtNTWQ5Z0NvNmxxTFZkXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

##  主程序流程

启动程序, 可以通过命令行启动程序, 或者，直接访问http://yuanxinhang.fun:5000/

命令行环境配置方法:

1.安装依赖。pip3 install -r requirements.txt2.运行flask。python top.py3.在浏览器中打开127.0.0.1:5000

程序初始界面如下:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=NmY0MzQ2NGM5ZjA2ZjE5YzBkMWUxZTllOWE3OTAyNGVfeXlIR2lpcEpiM0p2a09GTFJwaEdPck1hMmlSU0VaQnFfVG9rZW46Ym94Y25hWWlVa2IwWmI2ZW9BaWFzdktHbnliXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

此时网页会加载默认程序, 进行词法, 语法, 语义分析, 屏幕左侧是分析结果, 点击相应的标签页会自动加载相应的分析结果.

用户可以输入自己的c程序(带代码高亮), 点击右下角的提交按钮可以对用户输入进行语义分析, 结果呈现在屏幕左侧, 如果用户输入有错, 则会提示相应的错误信息, 静态检查结果在最后一个标签页里面显示

同时, 用户还可以提交自己的语法文件, (语法文件格式可以参见源代码里面的grammar.json), 程序将读取用户定义的语法格式, 建立相应的语法分析表(利用LR(1)), 并且应用新的规则对之后的程序进行相应的分析

##  模块间的调用关系

### 前端模块调用关系展示：

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=NGQwZjcwZDY0MTUxYzZlMjk2MmUzZGVkYTI3YTkyYjRfbkZnVUJKQ2RDNnFLcnhjS3FId0VBTmEwMVYzamN5OE5fVG9rZW46Ym94Y24xQ25hV1UwWGhWbjh6bjR2TVZ3ZW5lXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

### 后端模块间调用关系展示

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=YzYwNWQwYzAyOTA2YWU5OWQ4YWI4MTgxNTc3YzRjZDRfOVhRRXNVenlnOWN6TlIyRFdHOTM5OWRyN2oyUUNrQjNfVG9rZW46Ym94Y24wTUxwb0hzeWJYTHlsc2V0V1RLRm9jXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

# 详细设计

## 顶层模块设计

项目总体由 flask 框架进行搭建，Flask 是一个轻量级的可定制框架，使用 Python语言编写，较其他同类型框架更为灵活、轻便、安全且容易上手，可以很好地结合MVC 模式进行开发。本项目总体结构如下图所示：

```SQL
│  Readme.md (说明文件)
│  top.py(Flask启动程序)
├─.idea（中间文件）
├─basic
│  │  main.py （算法）
│  │  maketree.py （绘制语法树）
│  │  views.py （前端控件）
│  └─__pycache__（中间文件） 
├─source_file（资源文件）
│      analysis.table
│      analysis_key.json
│      basic.json
│      data.txt
│      grammer.json
│      lr1.table
│      test.c
├─static(JavaScript和CSS)
│      d3.js
│      index.css
├─templates(Html)
│      index.html
└─__pycache_（中间文件）    
```

##  前端部分详细设计

在编译结果的展示上, 我们采用模块化设计的思想, 先利用HTML实现前端的界面设计,在此基础上进一步利用JavaScript实现每一部分的功能, 最后利用CSS进行界面的美化.

下面分功能叙述具体的函数设计过程

### 词法分析:

词法分析的结果简单明了, 只需要利用一个表格展示每一个词的属性(Type)与值(Value)即可. 后端将分析结果包装成结构体数组的形式发送到页面前端, 前端利用jQuery将数据解码成HTML的表格对象即可进行展示。

### 语法分析:

#### 语法树的展示

语法树的实现较为复杂, 因为LR(1)分析得到的是每一步栈内的符号变化, 我们首先需要将分析过程转化为便于展示的数据结构, 再将数据发送到前端进行展示, 大致步骤如下图所示:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MzcwMGYwNzJjYjEyNmZkMjljMjA3M2M5MTVkNWM4NzBfODdyRkFkQ1llOU9TQmE5WWVkaURkN2x2NENxTkdhTUZfVG9rZW46Ym94Y25XTlJFZW5ZTkg0bTIwZWV0eG50a0doXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

前端树形结构的展示我们选用了应用广泛的D3.js图形可视化库, 其主要特点是生成的图形界面可交互, 简单直观.

我们选择嵌套的结构体作为语法树的数据结构, 每个节点的children属性作为一个数组存储了它所有的孩子节点, 代表了一次推导过程:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=Mzc3NGU0YjQ5ODA3OTYzZGE2YzRjOWE0Mzg2YmU4MzNfZUJCMEZJZ0JJT2RZcDdQUFFWNkFEWkR2aEtVOXI0bFdfVG9rZW46Ym94Y25iMDE2YVlvMG1tdGlKZDBRRVJvcG5nXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

在语法树的可视化中,重点需要解决两个问题: 

1、SVG图形对象的生成

图形对象包括节点对象和边对象, 关键问题是怎样建立节点与边的联系, 让图像整体呈树状分布, 上述功能由以下函数加以实现:

```SQL
d3.layout.tree() //处理树的结构分布
d3.svg.diagonal() //实现SVG图像的坐标转换
tree.nodes(root).reverse(), // 树内节点的转换
tree.links(nodes); // 建立节点与边的联系
```

2、用户交互的处理(缩放, 点击, 节点信息显示等)

视图缩放我们采用D3自带的Zoom模块来实现, 而点击操作的实现较为复杂, 主要由Update()来进行节点位置的重新计算, 其中又可以细分为进入所点击节点下的子树, 和关闭所点击节点下的子树两个相反的操作, 最后重新计算所有图形对象的坐标分布, 并刷新显示区域.

节点信息的显示由tooltip函数加以实现, 其功能为在整个图像上面创建一个透明的蒙版, 并随时监测鼠标的位置, 如果鼠标移动到了节点上面, 就更新蒙版的信息为当前节点的属性, 并且调整透明度以显示节点信息.

#### LR分析表ACTION GOTO与分析过程的展示

我们同样采用jQuery来实现表格数据到HTML对象的转换, 有所不同的是, 由于ACTION与GOTO表较为庞大, 我们需要设置横纵两个方向上的移动条, 方便用户查找.

## 函数调用关系:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=YTBjZjkxZWQxYTFlNWM1MWM5MjQ0YTZmODUxMGFlOWFfWmhhWGRnT0szYVRUUEo5bW5RSW9qcUMxTXhsc3A0VVFfVG9rZW46Ym94Y25Sb1lMcFlIR3E0eDBSRkpoVnFveEdkXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

## 后端部分详细设计

### 算法思路

#### 预置工作——词法分析和语法分析

在前期的工作当中我们完成了词法分析和语法分析对应模块的构建工作。

在词法分析中，我们借鉴了工具lex的词法分析算法，以正则表达式匹配的方法代替DFA进行词法分析，通过6个正则表达式并行匹配词法元素，每一次将位于开头的最长匹配序列识别为对应的正则表达式所代表的token，从而实现了词法分析。

语法分析中，我们通过求解文法中产生式非终结符的FIRST集存在相互依赖关系，其次通过CLOSURE(I)算法识别同样活前缀的所有项目的集合。建立有限状态自动机DFA、哈希表H、项目集队列P，进一步完成LR(1)预测表的构建，最后根据语法分析的结果生成语法分析树。

#### 语义分析

我们采用一遍扫描的方式——我们根据预先定义好的文法，针对于不同的文法完成语义分析工作。对于每一个规约的产生式，针对于不同的文法规则在依据不同于局的翻译模式生成不同的四元式作为中间代码的体现形式；最终在通过翻译中间代码得到最终的结果。

针对于文法和语句而言，我们主要包括：说明语句的翻译、赋值语句的翻译、布尔表达式的翻译、控制语句的翻译、过程调用的处理五个大类，并在五个大类的基础之上针对于其中一些小的板块进行处理。

说明语句的翻译

针对于过程中的说明语句，我们通过构建符号表的方式讲对应的说明的变量或函数存储到符号表当中的相应位置。在语义规则当中我们用到如下操作：

(1)inktable(previous)建一张新符号表，并返回指向新表的一个指针。参数previous 指向一张先前创建的符号表，譬如刚好包围嵌入过程的外围过程符号表。指针previous 之值放在新符号表表头，表头中还可存放一些其它信息如过程嵌套深度等等。我们也可 以g过程被说明的顺序对过程编号，并把这一编号填入表头。

(2)enter(table,name,type,offset)在指针table指小的符号表中为名字name建立一个 新项，并把类型type、相对地址offset填入到该项中。

(3)addwidth(table,width)在指针table指ZK的符号表表头中记录下该表中所有名字占 用的总宽度。

(4)enterproc (table, name, newtable)在指针table指7K的符号表中为名字为name的过程 建立一个新项。参数newtable指向过程name的符号表。

在记录符号表的过程当中，我们改进域名产生的翻译模式“T—record D end”，以及每个过程一个符号表的操作“inktable(previous)”，转变为全局只维护一张大的符号表；在符号表当中添加新字段的方式，从而能够更加精准的确定全局变量、函数变量的访问。

赋值语句的翻译

赋值语句的翻译的主要工作为把简单算术表达式及赋值语句翻译为三地址代码的翻译。需要说明了如何査找符号表的人口。属性id. name表示id所代表的名字本身。我们通过过程lookup (id. name)检査是否在符号表中存在相应此名字的入口。如果有，则返回一个指向该表项的内容，否则，返回未找到信息。主要的翻译模式包括如下内容：

| S→id:=E | S.code:=E.code \|\| gen(id.place ‘:=’ E.place)               |
| ------- | ------------------------------------------------------------ |
| E→E1+E2 | E.place:=newtemp;E.code:=E1.code \|\| E2.code \|\|gen(E.place ‘:=’ E1.place ‘+’ E2.place) |
| E→E1*E2 | E.place:=newtemp;E.code:=E1.code \|\| E2.code \|\|  gen(E.place ‘:=’ E1.place ‘*’ E2.place) |
| E→-E1   | E.place:=newtemp;E.code:=E1.code \|\|  gen(E.place ‘:=’ ‘uminus’ E1.place) |
| E→ (E1) | E.place:=E1.place;E.code:=E1.code                            |
| E→id    | E.place:=id.place;E.code=‘ ’                                 |

布尔表达式的翻译

布尔表达式通过用布尔运算符把布尔量、关系表达式联结起来，主要包含的运算关系为：and, or, not；关系运算符包括：＜,≤,＝, ≠，＞ ,≥；布尔表达式主要用于逻辑演算、计算逻辑值，以及用于控制语句的条件式.。

在本例中主要通过以下文法产生布尔表达式：

```SQL
E→E or E
E→E and E 
E→~E 
E→(E) 
E→id rop id 
E→id
```

我们采用一边扫描的方式用于布尔表达式的产生工作，主要包含的操作合约定位：四元式：(jnz, a, -, p)表示‘f a goto p’；(jrop, x, y, p)表示‘if x rop y goto  p’；(j, -, -, p)表示‘goto p’。

函数makelist(i)，它将创建一个仅含i的新链表，其中i是四元式数组的一个下标(标号)；函数返回指向这个链的指针。函数merge(p1,p2)，把以p1和p2为链首的两条链合并为一，作为函数值，回送合并后的链首。过程backpatch(p, t)，其功能是完成“回填”，把p所链接的每个四元式的第四区段都填为t。主要的翻译模式如下所示：

```SQL
(1) E→E1 or M E2
{ backpatch(E1.falselist, M.quad);
  E.truelist:=merge(E1.truelist, E2.truelist);
  E.falselist:=E2.falselist }
(2) E→E1 and M E2
{ backpatch(E1.truelist, M.quad);
  E.truelist:=E2.truelist;
      E.falselist:=merge(E1.falselist,E2.falselist) }
(3) E→not E1
{ E.truelist:=E1.falselist;
  E.falselist:=E1.truelist}
(4) E→(E1)
{ E.truelist:=E1.truelist;
  E.falselist:=Efalselist}
(5) E→id1 relop id2    { E.truelist:=makelist(nextquad);
  E.falselist:=makelist(nextquad+1);
      emit(‘j’ relop.op ‘,’ id 1.place ‘,’ id 2.place‘,’　‘0’);
  emit(‘j, －, －, 0’) }
(6) E→id
{ E.truelist:=makelist(nextquad);
  E.falselist:=makelist(nextquad+1);
      emit(‘jnz’ ‘,’ id .place ‘,’ ‘－’ ‘,’　‘0’)；
  emit(‘ j, -, -, 0’) }
(7) M→{ M.quad:=nextquad }
```

控制语句的翻译

控制语句主要包含——if-then(-else)语句，while循环语句，return返回语句。

主要涉及文法包括：

```SQL
S→if E then S
S→if E then S else S
S→while E do S
S→begin L end
S→A
L→L;S
L→S
```

其中，S表示语句，L表示语句表，A为赋值语句，E为布尔表达式。

主要的翻译模式包括：

```SQL
IF-THEN-ELSE语句：
S→if  E  then  M  S1
 { backpatch(E.truelist, M.quad);
S.nextlist:=merge(E.falselist, S1.nextlist) }
S→if  E  then  M1  S1  N  else  M2  S2
 {backpatch(E.truelist, M1.quad);
backpatch(E.falselist, M2.quad);
S.nextlist:=merge(S1.nextlist, N.nextlist, S2.nextlist) }
M→{ M.quad:=nextquad }
N→{ N.nextlist:=makelist(nextquad);
   emit(‘j,－,－,－’) }
   
WHILE语句
S→while M1 E do M2 S1
        {backpatch(S1.nextlist, M1.quad);
      backpatch(E.truelist, M2.quad);
      S.nextlist:=E.falselist
      emit(‘j,－,－,’ M1.quad) }
M→{ M.quad:=nextquad }

其他语句：
L→L1; M S        { backpatch(L1.nextlist, M.quad);
                     L.nextlist:=S.nextlist }
M→        { M.quad:=nextquad }
S→begin L end{ S.nextlist:=L.nextlist }
S→A{ S.nextlist:=makelist( ) }
L→S{ L.nextlist:=S.nextlist } 
```

过程调用的处理

过程调用处理主要包含应两种事：传递参数、转子（过程）。其中传地址:把实在参数的地址传递给相应的形式参数；调用段预先把实在参数的地址传递到被调用段可以拿到的地方；程序控制转入被调用段之后，被调用段首先把实在参数的地址抄进自己相应的形式单元中；另外，过程体对形式参数的引用与赋值被处理成对形式单元的间接访问。

本例当中过程调用的翻译模式主要包括：

```SQL
Elist→E
{ 初始化queue仅包含E.place }
Elist→Elist, E
{ 将E.place加入到queue的队尾 }
S→call id (Elist)
{ for 队列queue中的每一项p  do
        emit(‘param’ p);
emit(‘call’ id.place) }
```

#### 中间代码生成:

依据上述语义分析的结果，在融合其他语句（如return、复合语句、函数标号）等等的组合，最终讲所有的emit的翻译结果以四元组的形式整合到中间代码中，最后讲中间代码进行翻译即可得到最终的结果。

### 代码思想及实现架构

#### 代码实现总体框架

下图为项目总体的算法流程图，其中词法分析和语法分析的部分不在展开。

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=OWZlNGFjZTM5ZjllZTE0NDkzYjM3MjJhMWQ3Y2NkNTRfZTc4U1Q5RFNrajJ1b3pwY3U1ZG1IVEJnNlIwYVhoWlJfVG9rZW46Ym94Y25QU1BTbkVMazdOYzUxWE1MT3Q1NWJkXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

由上图可知，首先由用户输入程序段和语法，有词法分析器对于程序段进行词法分析并提出其中的TOKENS，语法由LR1分析器，依据所提供的文法构建LR1分析表。最后结合词法分析的结果TOKENS以及语法分析的结果LR1分析表相结合，进行语法分析以及语义分析。由于我们采用一边扫描的方式，因此语法分析和语义分析二者在该阶段并行执行，由每一步语法分析的状态，对应到所规约的产生式，进行相应语句的语义分析的扫描。依据语义分析当中对于赋值语句、控制语句、声明语句、布尔表达式、函数调用处理等等的不同类型文法进行不同类型的规约以及分析操作。最终生成两个符号表（变量表+函数表）、以及没有经过调整的四元式。最终由四元式翻译行成中间代码并反馈给用户作为程序的输出。

#### 语义分析部分函数调用关系框架

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=ZGY5Y2UyOTc4NTI0MzFiY2E2NWZjMzgxMjA0Y2ZmNjBfNXB1ZDFFcWFobzZXR2tGMmNZV1lZMm1OYXE0YnFDRU5fVG9rZW46Ym94Y25YbGFXaDRtc3ZqaEdQdEQxRzJDT0ZkXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

上图为语义分析部分的函数调用关系展示，由图可知，start_analysis函数为语法分析调用的主函数，由于语法分析和语义分析的并行性，对于每一个语法分析规约的过程，针对于调用的文法构建对应的语义分析的过程。其中语义分析主要包括赋值语句、控制语句、声明语句、布尔表达式、函数调用处理五个部分，依据不同的文法类别，函数采用不同的方法对齐进行中间代码生成的处理。

semantic_analysis有下分诸多子函数，其中get_new_lable将对扫描到的声明申请一个新的变量，并且将对应的符号通过update_symbol_table的方式加入到符号表当中。get_new_temp表示生成当前的一个临时变量，用于存储当前的临时变量信息以便于之后的中间代码的生成。与变量的命名与函数表的创建相类似的是函数表的创建过程。通过get_new_function_lable的方式创建新的函数表，通过update_function_lable函数完成对于函数表的更新操作，其子函数find_function_by_name用于根据function函数名找到对应的function的lable，从而判断是否出现函数重定义等特殊情况。最后，通过disp_SEMANTIC_STACK函数将语义分析过程当中所涉及到的堆栈的内容进行展示。

### 函数调用及实现

#### 函数调用关系架构

我们在上一届当中较为详细的阐述了整个项目当中语义分析和中间代码生成部分的项目框架，接下来我们将走进每一个函数内，详细的对于每个模块和内部主要函数的实现情况进行说明。

#### 函数分析

1、语义分析主函数semantic_analysis()

语义分析主函数通过对于语法分析当中的每一个步骤进行语义分析，因为语法分析过程当中涉及到很多的不同类型的文法，因此语义分析主函数也起到针对于每一类型不同文法进行决策的作用。

针对于每一待分析的语句，结合对应的文法生成两个符号表及对应的四元式，同时将对应的分析状态存入语法分析栈当中。

```SQL
'''
函数名：def semantic_analysis()
函数功能：语义分析主函数，过对于语法分析当中的每一个步骤进行语义分析
输入参数：TOKENS、当前产生式、当前分析站内情况
输出参数：无
时间复杂度：O(1)~O(n)，总体时间复杂度为O(1)+O(1)~O(n)，前者O(1)为有限文法的判断时间，后者O(n)表示在优先文法判断的过程当中，执行到每一步特定的文法规约的时间复杂度为O(1)~O(n)不定，取决于特定的文法，故最坏情况下的时间复杂度为O(n)
'''
```

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MzE4MzUyZmE3ZjI3NzhmZWZiOWFlODA0Y2Q5Mzg2OGZfTngxODFURjJacWFCNHVRQXU5TmNtNm5YdldtTEFHempfVG9rZW46Ym94Y25ONVpRZzJYYjZXUUpSTmduRE1SRHViXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

声明语句的分析及翻译

在语义分析主程序当中，我们首先需要明确对于声明语句的处理。声明语句包括变量声明、常量声明、函数声明等等形式，在本例当中，我们使变量与常量相结合的方式来进行声明语句的分析；其次通过分析声明的类型来确定接下来的语义分析的过程当中采用怎样的符号表进行添加：

```SQL
'''
处理文法：PPT_function_declaration PPT_variable_declaration 'declaration'
函数功能：主要处理对于函数、变量、部分的声明相关四元式生成，符号表的维护
输入参数：TOKENS、当前产生式、当前分析站内情况
输出参数：无
'''
elif none_terminal ==  'PPT_function_declaration':
    node_new = SEMANTIC_STACK.pop(-1)
    node_definition=SEMANTIC_STACK.pop(-1)
    node_new.name = 'function_implement'
    code_temp=[]
    code_temp.append((node_definition.data,':','_','_'))
    for node in node_definition.stack:
        code_temp.append(('pop','_',4*node_definition.stack.index(node),node.place))
    if len(node_definition.stack)>0:
        code_temp.append(('-', 'fp', 4*len(node_definition.stack), 'fp'))
    for code in reversed(code_temp):
        node_new.code.insert(0,code)
    code_end=node_new.code[-1]
    if code_end[0][0]=='l':
        lable=code_end[0]
        node_new.code.remove(code_end)
        for code in node_new.code:
            if code[3]==lable:
                node_new.code.remove(code)
    SEMANTIC_STACK.append(node_new)
    
# 变量声明部分：
elif none_terminal ==  'PPT_variable_declaration':
    node_new = Node()
    id = OP_STACK[-1]['data'] # 其实此时也就是; 对于int a;这种情况而言
    node_new.id = id
    SEMANTIC_STACK.append(node_new) # 这个也就象是普通增加一个变量，啥名字都没有
    
# 声明归纳部分：
elif none_terminal=='declaration':
    node_new = SEMANTIC_STACK.pop(-1)
    node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
    node_new.name= 'declaration'
    type=SEMANTIC_STACK.pop(-1).type
    for node in node_new.stack:
        symbol = find_symbol(node.id, CURRENT_FUNCTION_SYMBOL.lable)
        if symbol!=None and symbol.function==CURRENT_FUNCTION_SYMBOL.lable:
            token = TOKENS[0]
            print("multiple defination of {} in row{}".format(node.id,token['row']))
        else:
            symbol=Symbol()
        if node.place==None:
            symbol.name=node.id
            symbol.place=get_new_temp()
            symbol.type=type
            symbol.function=CURRENT_FUNCTION_SYMBOL.lable
            symbol.size = 4
            symbol.offset = CURRENT_OFFSET
            CURRENT_OFFSET += symbol.size
            update_symbol_table(symbol)
            if node.data!=None:
                if(node.type!=type):
                    token = TOKENS[0]
                    print("type error in row{}".format(token['row']))
                code=(':=',node.data,'_',symbol.place)
                node_new.code.append(code)
        else:
            symbol.name=node.id
            symbol.place=node.place
            symbol.type=type
            symbol.function = CURRENT_FUNCTION_SYMBOL.lable
            symbol.size = 4
            symbol.offset = CURRENT_OFFSET
            CURRENT_OFFSET += symbol.size
            update_symbol_table(symbol)
            for code in node.code:
                node_new.code.append(code)
    node_new.stack=[]
    SEMANTIC_STACK.append(node_new)
```

赋值语句的分析及翻译

赋值语句主要包含对于变量的、临时变量等赋予新的数值，这里主要考虑产生四元式的方式赋值，同时通过需要赋予的值的算数表达式的类型考虑吧是否需要进行相应的类型转换，同时在对应的符号表当中进行类型和值的更新。主要函数如下所示：

```SQL
'''
处理文法：assignment_expression
函数功能：实现赋值表达式、语句、逗号表达式的规约操作中的语义分析
输入参数：TOKENS、当前产生式、当前分析站内情况
输出参数：无
时间复杂度：O(1)，无循环调度、简单判断实现
'''
变量赋值——创建节点、判断节点类型和属性、更新符号表
elif none_terminal=='assignment_expression':
    node_new = SEMANTIC_STACK.pop(-1)
    node_op=SEMANTIC_STACK.pop(-1)
    id=OP_STACK[-3]['data']
    symbol = find_symbol(id, CURRENT_FUNCTION_SYMBOL.lable)
    if symbol == None:
        token = TOKENS[0]
        print("none defination of {} in row{}".format(id, token['row']))
        symbol = Symbol()
        symbol.place=get_new_temp()
        symbol.name=id
        symbol.type=node_new.type
        symbol.function = CURRENT_FUNCTION_SYMBOL.lable
        symbol.size=4
        symbol.offset=CURRENT_OFFSET
        CURRENT_OFFSET+=symbol.size
        update_symbol_table(symbol)
    if node_new.place==None:
        arg=node_new.data
    else:
        arg = node_new.place
    if len(node_op.type)==1:
        code=(':=',arg,'_',symbol.place)
        node_new.code.append(code)
    else:
        code=(node_op.type[0],symbol.place,arg,symbol.place)
        node_new.code.append(code)
    node_new.name = 'assignment_expression'
    SEMANTIC_STACK.append(node_new)
```

布尔表达式的分析及翻译

我们在对于布尔表达式的处理时，考虑到布尔表达式也可以作为算术表达式当中的一种类别，因此我们将布尔表达式也作为算术表达式归为一类在算术表达式当中进行处理，同时将operator变量进行相应的拓展，使其能够更灵活和简便的展开翻译工作。

```SQL
'''
处理文法：arithmetic_expression constant_expression
函数功能：实现算术表达式、常量达式的规约操作中的语义分析
输入参数：TOKENS、当前产生式、当前分析站内情况
输出参数：无
时间复杂度：O(n)，单重循环，实现的时间取决语义分析于栈内当前中间代码的长度
'''
对于算术表达式的处理工作：
elif none_terminal=='arithmetic_expression':
    node_new=Node()
    node_new.name= 'arithmetic_expression'
    if len(expressions)==1:
        node_new.stack=[]
    else:
        node_new=copy.deepcopy(SEMANTIC_STACK.pop(-1))
        node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
    SEMANTIC_STACK.append(node_new)
```

对常量表达式的处理工作（对于每一个算术表达式而言，最终的结果会形成一个常量表达式，对于该常量符号表的更新以及用于后续的规约和语义分析操作）：

```SQL
elif none_terminal=='constant_expression':
    node_new = SEMANTIC_STACK.pop(-1)
    node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
    node_new.name= 'constant_expression'
    if len(node_new.stack)==1:
        node_new=copy.deepcopy(node_new.stack[0])
    else:
        node_left=node_new.stack.pop(0)
        while len(node_new.stack)>0:
            node_op=node_new.stack.pop(0)
            node_right=node_new.stack.pop(0)
            if node_left.place==None:
                arg1=node_left.data
            else:
                arg1 =node_left.place
            if node_right.place==None:
                arg2=node_right.data
            else:
                arg2 =node_right.place
            if len(node_left.code)>0:
                for code in node_left.code:
                    node_new.code.append(code)
            if len(node_right.code)>0:
                for code in node_right.code:
                    node_new.code.append(code)
            node_result = Node()
            node_result.name = 'primary_expression'
            node_result.place = get_new_temp()
            node_result.type = node_right.type
            code=(node_op.type,arg1,arg2,node_result.place)
            node_new.code.append(code)
            node_left=node_result
            node_new.type=node_right.type
        node_new.place=node_new.code[-1][3]
    SEMANTIC_STACK.append(node_new)
```

expression表达式的整合：

在已经列举算数表达式、布尔表达式、常量表达式、声明表达式、赋值表达式之后，我们需要对所有的表达式进行整合处理，合并对应的代码段、整合并更新语义分析对战当中的内容。expression包括expression和expression_profix组成，后者用逗号表达式集结了后续所有的expression的内容：

```SQL
elif none_terminal=='expression':
    node_new = SEMANTIC_STACK.pop(-1)
    node_new.name = 'expression'
    SEMANTIC_STACK.append(node_new)
elif none_terminal=='expression_profix':
    node_new = Node()
    node_new.name = 'expression_profix'
    if len(expressions)==1:
        node_new.stack=[]
    else:
        node_new=SEMANTIC_STACK.pop(-1)
        node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
    SEMANTIC_STACK.append(node_new)
elif none_terminal=='expression_list':
    node_new = Node()
    node_new.name = 'expression_list'
    if len(expressions)==1:
        node_new.stack=[]
    else:
        node_new=SEMANTIC_STACK.pop(-1)
        node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        for node in reversed(node_new.stack):
            for code in node.code:
                node_new.code.insert(0,code)
    SEMANTIC_STACK.append(node_new)
```

控制语句的分析及翻译

控制语句主要包括while语句以及IF-THEN(-ELSE)语句，在这主要对于该两种情况的翻译进行讨论。由于采用一边扫描的方式，我们需要对于内部的部分节点的跳转目的地址采用回填的操作来进行：

```SQL
'''
处理文法：IF-THEN(-ELSE) WHILE FOR
函数功能：实现控制达式的规约操作中的语义分析
输入参数：TOKENS、当前产生式、当前分析站内情况
输出参数：无
时间复杂度：O(n)，有限个单重循环，实现的时间取决控制语句当中四元式代码的长度
'''
IF-THEN(-ELSE)
创建新的后足节点同时记录后续节点的起始地址，通过添加TrueList和FalseList的方式在对应的结点之后进行相应结果的更新，将对应连标志进行更新同时将结果进行存储。
elif none_terminal=='selection_statement':
    node_new = Node()
    node_new.name = 'selection_statement'
    Node.true=get_new_label()
    Node.false=get_new_label()
    Node.end = get_new_label()
    FalseStmt=SEMANTIC_STACK.pop(-1)
    TrueStmt = SEMANTIC_STACK.pop(-1)
    expression=SEMANTIC_STACK.pop(-1)
    for code in  expression.code:
        node_new.code.append(code)
    node_new.code.append(('j>',expression.place,'0',Node.true))
    node_new.code.append(('j','_','_',Node.false))
    node_new.code.append((Node.true,':','_','_'))
    for code in TrueStmt.code:
        node_new.code.append(code)
    node_new.code.append(('j', '_', '_', Node.end))
    node_new.code.append((Node.false,':','_','_'))
    for code in FalseStmt.code:
        node_new.code.append(code)
    node_new.code.append((Node.end,':','_','_'))
    SEMANTIC_STACK.append(node_new)
while循环语句的处理：
对while循环语句的处理相对分支判断语句的处理要更加复杂一些，需要考虑到四个分支的入口、以及内部continue和break的情况，都需要在while循环的对应位置更新跳转的地址。
elif none_terminal=='iteration_statement':
    node_new = Node()#生成新节点
    node_new.name = 'iteration_statement'
    node_new.true = get_new_label()#四个分支的入口
    node_new.false = get_new_label()
    node_new.begin = get_new_label()
    node_new.end = get_new_label()
    if expressions[0]['type']=='while':
        statement = SEMANTIC_STACK.pop(-1)#获得expression结点和statement结点
        expression=SEMANTIC_STACK.pop(-1)
        node_new.code.append((node_new.begin,':','_','_'))#begin入口
        for code in expression.code:#传递expression的中间代码
            node_new.code.append(code)
        node_new.code.append(('j>',expression.place,'0',node_new.true))#当expression的计算结果大于0时，跳转到true
        node_new.code.append(('j','_','_',node_new.false))#否则，跳转到false
        node_new.code.append((node_new.true,':','_','_'))#true入口
        for code in statement.code:#传递statement的中间代码
            if code[0]=='break':#当中间代码为break时，添加跳转到false的中间代码
                node_new.code.append(('j','_','_',node_new.false))
            elif code[0]=='continue':#当中间代码为continue时，添加跳转到begin的中间代码
                node_new.code.append(('j','_','_',node_new.begin))
            else:
                node_new.code.append(code)
        node_new.code.append(('j', '_', '_', node_new.begin))#跳转回begin
        node_new.code.append((node_new.false,':','_','_'))#false入口
    elif expressions[0]['type']=='for':
        statement= SEMANTIC_STACK.pop(-1)
        assign= SEMANTIC_STACK.pop(-1)
        expression=SEMANTIC_STACK.pop(-1)
        Declaration=SEMANTIC_STACK.pop(-1)
        for code in  Declaration.code:
            node_new.code.append(code)
        node_new.code.append((node_new.begin,':','_','_'))
        for code in  expression.code:
            node_new.code.append(code)
        node_new.code.append(('j>',expression.place,'0',node_new.true))
        node_new.code.append(('j','_','_',node_new.false))
        node_new.code.append((node_new.true,':','_','_'))
        is_continue_existed=False
        for code in statement.code:
            if code[0]=='break':
                node_new.code.append(('j','_','_',node_new.false))
            elif code[0]=='continue':
                node_new.code.append(('j','_','_',node_new.end))
                is_continue_existed=True
            else:
                node_new.code.append(code)
        if is_continue_existed:
            node_new.code.append((node_new.end,':','_','_'))
        for code in assign.code:
            node_new.code.append(code)
        node_new.code.append(('j', '_', '_', node_new.begin))
        node_new.code.append((node_new.false,':','_','_'))
    SEMANTIC_STACK.append(node_new)
```

函数调用的分析及翻译

函数调用的过程相对来说较为简单，在四元式当中主要体现在提前在对站当中存储相应的变量，这里暂时没有考虑默认寄存器的系统调用问题，交给后续的汇编语言生成的时候在做较为详细的说明和展开。

```SQL
'''
处理文法：function_expression
函数功能：实现函数跳转表达式的规约操作中的语义分析
输入参数：TOKENS、当前产生式、当前分析站内情况
输出参数：无
时间复杂度：O(n)，有限个单重循环，n值取决当前子函数长度及其定义变量的个数
'''
function_expression：对于函数调用和返回的处理
此处我们通过修改动态修改栈帧sp的方式确定对应函数的调用位置，call时跳转sp-=4，return时增加sp+=4，同时通果push和pop操作在对应的对站当中添加需要调用的参数。
elif none_terminal == 'function_expression':
    function = find_function_by_name(OP_STACK[-4]['data'])
    node_new = SEMANTIC_STACK.pop(-1)
    node_new.name = 'function_expression'
    code_temp=[]
    symbol_temp_list = copy.deepcopy(CURRENT_FUNCTION_SYMBOL.params)
    code_temp.append(('-', 'sp', 4 * len(symbol_temp_list)+4, 'sp'))
    code_temp.append(('store', '_', 4 * len(symbol_temp_list), 'ra'))
    for symbol in symbol_temp_list:
        code_temp.append(('store','_',4 * symbol_temp_list.index(symbol),symbol[2]))
    for code in reversed(code_temp):
        node_new.code.insert(0,code)

    if len(function.params)>0:
        node_new.code.append(('+', 'fp', 4*len(function.params), 'fp'))
    for node in node_new.stack:
        if node.place!=None:
            node_result=node.place
        else:
            node_result = node.data
        node_new.code.append(('push','_',4*node_new.stack.index(node),node_result))
    node_new.code.append(('call', '_', '_', function.lable))

    symbol_temp_list.reverse()
    for symbol in symbol_temp_list:
        node_new.code.append(('load', '_', 4 * symbol_temp_list.index(symbol), symbol[2]))
    node_new.code.append(('load', '_', 4 * len(symbol_temp_list), 'ra'))
    node_new.code.append(('+', 'sp', 4 * len(CURRENT_FUNCTION_SYMBOL.params) + 4, 'sp'))

    node_new.place=get_new_temp()
    node_new.code.append((':=', 'v0', '_', node_new.place))
    SEMANTIC_STACK.append(node_new)
```

# 语义分析错误处理

在本次实验中，我们对C语言做如下假设：

假设1：整型（int）变量不能与浮点型（float）变量相互赋值或者相互运算。

假设2：仅有int型变量才能进行逻辑运算或者作为if和while语句的条件；仅有int型和float型变量才能参与算术运算。

假设3：任何函数只进行一次定义，无法进行函数声明。

假设4：函数无法进行嵌套定义。

以上假设1至4也可视为要求，违反即会导致各种语义错误，不过我们只对后面讨论的几种错误类型进行考察。此外，因为已经完成了词法和语法分析的工作, 我们可以安全地假设输入文件中不包含注释、八进制数、十六进制数、以及指数形式的浮点数，也不包含任何词法或语法错误。

我们的程序可以对输入文件进行语义分析 (输入文件中可能包含过程调用) 并检查如下类型的错误：

错误类型1：变量在使用时未经定义。

错误类型2：函数在调用时未经定义。

错误类型3：变量出现重复定义，即变量与前面定义过的名字重复。

错误类型4：函数出现重复定义（即同样的函数名出现了不止一次定义）。

错误类型5：赋值号两边的表达式类型不匹配。

错误类型6：操作数类型不匹配

错误类型7：函数调用时实参与形参的数目不匹配。

错误类型8：函数调用时实参与形参的类型不匹配。

## 样例

### 样例示例：

#### 样例1

**输入：**

```SQL
int main(){
     int i = 0;
     j = i + 1;
 }
```

**输出：**

样例输入中变量“j”未定义，因此我们的程序可以输出如下的错误提示信息：

Error at line 2: can't find defination of symbol: j

#### 样例2

输入：

```SQL
int main()
{
  int i = 0;
  inc(i);
}
```

**输出：**

样例输入中函数“inc”未定义，因此我们的程序可以输出如下的错误提示信息：

Error at line 4: can't find defination of function: inc

#### 样例3

输入：

```SQL
int main()
{
  int i, j;
  int i;
}
```

输出：

```SQL
样例输入中变量“i”被重复定义，因此我们的程序可以输出如下的错误提示信息：
Error at line 4: multiple defination of symbol: i
```

#### 样例4

### 输入：

```SQL
int func(int i)
{
  return i;
}
int func()
{
  return 0;
}
int main()
{
}
```

输出：

```SQL
样例输入中函数“func”被重复定义，因此我们的程序可以输出如下的错误提示信息：
Error at line 6: multiple defination of function: func
```

#### 样例5

### 输入：

```SQL
int main()
{
  int i;
  i = 3.7;
}
```

输出：

```SQL
样例输入中错将一个浮点常数赋值给一个整型变量，因此我们的程序可以输出如下的错误提示信息：
Warning at line 4: Left Type: int doesn't match with the Right Type: float
```

#### 样例6

输入：

```SQL
int main()
{
  int i;
  10 = i;
}
```

输出：

```SQL
样例输入中整数“10”出现在了赋值号的左边，因此我们的程序可以输出如下的错误提示信息：
Error type 6 at Line 4: The left-hand side of an assignment must be a varia-ble. -->
```

#### 样例7

输入：

```SQL
int main()
{
  float j;
  10 + j;
}
```

输出：

```SQL
样例输入中表达式“10 + j”的两个操作数的类型不匹配，因此我们的程序可以输出如下的错误提示信息：
Warning at line 4: Left Type: int doesn't match with the Right Type: float
```

#### 样例8

输入：

```SQL
int func(int i)
{
  return i;
}
int main()
{
  func('a');
}
```

输出：

```SQL
样例输入中调用函数“func”时实参类型不正确，因此我们的程序可以输出如下的错误提示信息：
Error at line 8: function func()'s argument a is of type int, but char given.
```

#### 样例9

输入：

```SQL
int func(int i)
{
  return i;
}
int main()
{
  func(1, 2);
}
```

输出：

```SQL
样例输入中调用函数“func”时实参数目不正确，因此我们的程序可以输出如下的错误提示信息：
Error at line 8: function func takes 1 arguments, but 2 given
```

### 算法思路

在一遍扫描的分析方法里面, 错误处理的工作与语义分析是相互穿插, 同步进行的。我们先根据C语言的一些特征，分析可能出现的错误类型： 如C语言是强类型语言， 需要仔细核对赋值与运算时的类型是否匹配；函数的参数个数必须相同等等。然后再将不同类型的错误对应到语义分析的不同步骤里面去，编写对应错误处理函数，在相应的地方进行错误处理函数调用。这种分离语义与错误处理函数的设计思想不仅使程序的架构更加清晰，也方便小组成员进行分工，降低了代码之间的耦合性，与操作系统里面利用内陷指令处理程序错误的设计思想有相似之处。

### 代码与实现架构

#### 代码实现总体框架

针对不同的问题，我们一共实现了以下错误处理函数, 每个函数分别处理一种错误类型：

```SQL
# 定义与error有关的东西
ERROR_MSG = []
def error_Handler_RedefinedSymbol(node, token):  # 重定义处理

def error_Handler_RedefinedFunction(func, token):  # 重定义处理

def error_Handler_UndefinedSymbol(id, token): #符号未定义

def error_Handler_UndefinedFunction(funcName, token): # 函数未定义

def error_Handler_TypeError(token): # 赋值类型错误

def error_Handler_ArithmeticTypeError(left, right, token): # 算术表达式类型错误

def error_Handler_FunctionCallArgumentNumber(function, given, token): # 函数参数个数不对

def error_Handler_FunctionCallArgumentType(function, given, token, index):# 函数参数类型不对
```

#### **1.1.1.2 语义分析部分函数调用关系框架**

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MDM4YWIwYTcxZmNmYjkzMDM5MmM5YTY5NmEyNDNmYzBfR3NoVUdJZmlQcHozMWNzd3hzc1RMeFJ0MVlFZ3MzaFFfVG9rZW46Ym94Y25Ha1Y0U1IwODFZRGlMRkpzYmtpdHdnXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

### 函数调用与实现

下面分别讲解每个语义错误的处理流程

#### 函数分析

每个错误处理函数的大致结构是相似的, 都是如下形式:

```SQL
def error_Handler_RedefinedSymbol(nodename, token):  # 重定义处理
    global ERROR_MSG # 全局错误信息数组
    msg = "Error at line {}: multiple defination of symbol: \"{}\"".format(
        token['row']-1, nodename) # 错误信息
    print(msg) # 打印错误信息
    ERROR_MSG.append(msg) # 将错误信息发送到前端显示
```

可以看到错误处理函数的作用主要是: 将参数里面的的具体信息整合成规范的报错信息, 再将数据向用户端进行发送. 而错误处理困难的部分在于错误信息的提取与错误条件的判断, 即记录程序出错时符号表等相关参数的信息.

##### 1、符号重定义错误

```SQL
def error_Handler_RedefinedSymbol(nodename, token):  # 重定义处理
    global ERROR_MSG
    msg = "Error at line {}: multiple defination of symbol: \"{}\"".format(
        token['row']-1, nodename)
    print(msg)
    ERROR_MSG.append(msg)
###### SemanticAnalysis(): 下面是语义分析函数对应的部分################
 elif none_terminal == 'declaration':
        node_new = SEMANTIC_STACK.pop(-1)
        node_new.stack.insert(0, SEMANTIC_STACK.pop(-1))
        node_new.name = 'declaration'
        type = SEMANTIC_STACK.pop(-1).type
        for node in node_new.stack:  # 对于每一个节点
            symbol = find_symbol(node.id, CURRENT_FUNCTION_SYMBOL.lable) # 我们都要检查一下是否已经在符号表里面
            if symbol != None and symbol.function == CURRENT_FUNCTION_SYMBOL.lable:# 如果已经在符号表里面了
                token = TOKENS[0]
                # ! handle multiple defination of variable: Start
                error_Handler_RedefinedSymbol(node.id, token)
                # ! handle multiple defination of variable: End
```

对于每一个新定义的符号, 我们都要检查这个符号是否已经在符号表中, 如果是, 便将行号(token)和重复定义的变量名(node.id)传入错误处理函数进行处理.

```undefined
符号未定义错误def error_Handler_UndefinedSymbol(id, token):
    global ERROR_MSG
    msg = "Error at line {}: can't find defination of symbol: \"{}\"".format(
        token['row'], id)
    print(msg)
    ERROR_MSG.append(msg)
###### SemanticAnalysis(): 下面是语义分析函数对应的部分###########################
elif none_terminal == 'assignment_expression': 
    node_new = SEMANTIC_STACK.pop(-1)
    node_op = SEMANTIC_STACK.pop(-1)
    id = OP_STACK[-3]['data']
    symbol = find_symbol(id, CURRENT_FUNCTION_SYMBOL.lable) # 在符号表里面查找对应的符号
    if symbol == None: # 如果没有找到
        token = TOKENS[0] # 
        # ! Handle undefined symbol: Start
        error_Handler_UndefinedSymbol(id, token) # 将未定义的符号名传入错误处理函数
        # ! Handle undefined symbol: End
```

对于每一个运算中使用的符号, 我们都要检查这个符号是否已经在符号表中, 如果否, 便将行号(token)和未定义的变量名(node.id)传入错误处理函数进行处理.

##### 函数未定义错误

```SQL
def error_Handler_UndefinedFunction(funcName, token):
    global ERROR_MSG
    msg = "Error at line {}: can't find defination of function: \"{}\"".format(
        token['row'], funcName)
    print(msg)
    ERROR_MSG.append(msg)
###### SemanticAnalysis(): 下面是语义分析函数对应的部分###########################
elif none_terminal == 'function_expression':  #错误类型2：函数在调用时未经定义
    function = find_function_by_name(OP_STACK[-4]['data']) # 查找对应的函数名
    #! Error Handling Start
    if function is None: # 如果没找到
        token = TOKENS[0] # 获取行号
        error_Handler_UndefinedFunction(OP_STACK[-4]['data'], token) # 调用错误处理函数进行错误处理
```

对于每一个函数调用, 也需要查找函数名表, 如果没有找到, 则调用错误处理函数。

##### 函数重定义错误

```SQL
def error_Handler_RedefinedFunction(func, token):  # 重定义处理
    global ERROR_MSG
    global FATAL_ERROR_FLAG
    msg = "Error at line {}: multiple defination of function: \"{}\"".format(
        token['row'], func.name)
    print(msg)
    FATAL_ERROR_FLAG = 1
    ERROR_MSG.append(msg)
###### SemanticAnalysis(): 下面是语义分析函数对应的部分###########################
elif none_terminal == 'function_definition':#! 函数重复定义
    node_new = SEMANTIC_STACK.pop(-1)
    node_new.name = 'function_definition' # 在分析到一个函数定义的时候
    # ! Handle function_redefinition Start
    tmpfunction = find_function_by_name(OP_STACK[-4]['data']) # 在函数名表里面查看是否已经有了这个函数
    if tmpfunction is not None: # 如果有了
        token = TOKENS[0]
        error_Handler_RedefinedFunction(tmpfunction, token) # 调用错误处理函数
    # ! Handle function_redefinition End
    else:# 没有定义 继续后面的部分
```

对于每一个新定义的函数, 都需要查找函数名表, 如果函数已经定义, 则将行号和函数名称传入错误处理函数进行处理. 值得注意的是, 函数的冗余定义导致栈里面多了许多无关的部分, 会干扰后面的语法分析, 需要将这部分丢弃掉.

##### 符号类型错误

```SQL
def error_Handler_TypeError(token):
    global ERROR_MSG
    msg = ("Error at line {}: type error".format(token['row']-1))
    print(msg)
    ERROR_MSG.append(msg)
###### SemanticAnalysis(): 下面是语义分析函数对应的部分###########################
elif none_terminal == 'assignment_expression':  # ! 错误类型 1 ：变量在使用时未经定义。错误类型5：赋值号两边的表达式类型不匹配。
    node_new = SEMANTIC_STACK.pop(-1)
......
        update_symbol_table(symbol) # 更新符号表
        # ! Handle type error: Start
        if node_new.type != symbol.type: # 如果结果的类型和变量的类型不一致
            token = TOKENS[0] # 获取行号
            error_Handler_TypeError(token) # 错误处理
        # ! Handle type error: End
```

在计算的最后, 将结果的类型与复制号左边的类型进行比较, 如果不一致, 则调用错误处理函数进行提示.

##### 算术表达式类型错误

```SQL
def error_Handler_ArithmeticTypeError(left, right, token):
    global ERROR_MSG
    if left.type == 'int' and right.type == 'int':
        return
    elif left.type == 'float' and right.type == 'float':
        return
    elif left.type == 'char' and right.type == 'chae':
        return
    else:
        msg = ("Warning at line {}: Left Type: \"{}\" doesn't match with the Right Type: \"{}\"".format(
            token['row'], left.type, right.type))
        print(msg)
        ERROR_MSG.append(msg)
###### SemanticAnalysis(): 下面是语义分析函数对应的部分###########################
for 栈里面的每一个运算
    if node.data != None:
        if(node.type != type):
            token = TOKENS[0]
            # ! Handle type error: Start
            error_Handler_TypeError(token) #运算符两边类型不一致
            # ! Handle type error: End
        code = (':=', node.data, '_', symbol.place)
        node_new.code.append(code)
```

同上, 对于每一个运算, 如果运算符两边的类型不一致, 便进行提示。

##### 7、函数参数个数错误与函数参数类型错误

```SQL
def error_Handler_FunctionCallArgumentNumber(function, given, token):
    global ERROR_MSG
    msg = ("Error at line {}: function \"{}\" takes {} arguments, but received {}".format(
        token['row'], function.name, len(function.params), len(given)))
    print(msg)
    ERROR_MSG.append(msg)
def error_Handler_FunctionCallArgumentType(function, given, token, index):
    global ERROR_MSG
    msg = ("Error at line {}: function \"{}\"()'s argument \"{}\" is of type \"{}\", but \"{}\" was given".format(
        token['row'], function.name, function.params[index][0], function.params[index][1], given.type))
    print(msg)
    ERROR_MSG.append(msg)
###### SemanticAnalysis(): 下面是语义分析函数对应的部分###########################
#! Error Handling Start
    if len(function.params) != len(node_new.stack): # 如果形参实参的个数不一致
        token = TOKENS[0]
        error_Handler_FunctionCallArgumentNumber(# 进行报错
            function, node_new.stack, token)
    for arg in node_new.stack:                   # 对于每一个参数
        index = node_new.stack.index(arg) 
        symbol = find_symbol(
            arg.data, CURRENT_FUNCTION_SYMBOL.lable)
        if symbol != None: 
            if symbol.type != function.params[index][1]: # 判断它们的类型是否符合定义
                token = TOKENS[0]
                error_Handler_FunctionCallArgumentType( # 如果不对, 进行报错
                    function, symbol, token, index)
#! Error Handling End
```

对于函数的每一次调用, 都进行函数实参数目与类型的检查, 如果不符合函数定义, 则进行提示.

# 调试分析

   - ##  测试数据及测试结果

下面首先展示正确的输出结果, 然后再分别展示不同类型的错误处理结果。

### 正常输入情况

以下为测试用例, 包含了过程调用等完整的类C语言功能：

```SQL
int a; 
int b; 
int program(int a, int b, int c) 
{ 
int i; 
int j; 
i = 0; 
if (a > (b + c)) 
{ 
j = a + (b * c + 1); 
} 
else 
{ 
j = a; 
} 
while (i <= 100) 
{ 
i = j * 2; 
} 
return i; 
} 
 
int demo(int a) 
{ 
a = a + 2; 
return a * 2; 
} 
int main() 
{ 
int a; 
int b; 
int c; 
a = 3; 
b = 4; 
c = 2; 
a = program(a, b, demo(c)); 
return; 
}
```

经语义分析后, 程序输出为完整的四元式中间代码:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=YzNhYTM5MWZiNGU4NDc1MmE3MzgwMGZlNDNmMTFhYWFfdnhqRzNFWlpJcjdzcVhBMUhaVWhqcmRKcmZHOENCTzhfVG9rZW46Ym94Y25NdjNIb1d0UnYxWGhBaHhieE9RZkJiXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

示例程序没有错误, 语义错误栏显示如下:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=OTdkNGQzZjAxZThkNDY0Mzk0YjBlNmQxNzU4MmZiZTdfd1JqeWlTaFFPVGlWSDU4aWlnTGNMZHZwdUZYMXE5b3ZfVG9rZW46Ym94Y24xN0lWekFVeWU2dDB6WktPeTFnWk1lXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

### 错误输入情况

错误输入的示例程序是由上面的正确程序修改而来的.

#### 符号未定义错误

```SQL
int program(int a, int b, int c)
{
# 我们删去了对i, j的定义
i = 0;
if (a > (b + c))
{
j = a + (b * c + 1);
}
else
{
j = a;
}
while (i <= 100)
{
i = j * 2;
}
return i;
}
```

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=OWU5YjNkZTRmMjVkNmQxZTg4ZmY1MzRlMzFmMTI2NTRfN3JsdTlBOTVYZG1UelpCbnBOVUdGUThPcnZtUFo4NXBfVG9rZW46Ym94Y25iTGVXTnNsamlYRklldXdueHEwVEFoXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=OWY0ODdiYzI5Y2Y2YTI3NmE1NzFhN2U2NDA4YTg5MmZfdHlIYnA3aGUySGFPS2dqS2J5OHFnaEhCUmw1R2lkWFBfVG9rZW46Ym94Y25XelJaWElQWnFscEhia3BNYTVFcEFLXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

从上图中可以看到, 程序的正确的行号上报告了变量未定义的错误。

#### 符号重定义错误

```SQL
int program(int a, int b, int c) 
{ 
int i; 
int j; 
int i; # 这里重复定义了 i 
int j; # 这里重复定义了 j 
i = 0; 
if (a > (b + c)) 
{ 
j = a + (b * c + 1); 
} 
else 
{ 
j = a; 
} 
while (i <= 100) 
{ 
i = j * 2; 
} 
return i; 
}
```

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MmE4MDM2MjliM2E5MTNjMTBiNjQwZTY5MzZhZWQxNTBfSlpNVjZyRXVFMWs5eTZ4ZUphb0RuMVdLV09kQVJXOWNfVG9rZW46Ym94Y25vR0czRTFoOEpxUDhMYll2WkR4ZnlmXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=YTZkNTE1MGQyMGMzOTQ3NTExYzkyMGExMTIzNzVmMDhfeEZOdkdrV09mbmRVSUlvOG1hZjBQMWZKQlVVZHVXSEFfVG9rZW46Ym94Y25xRWtPbmExNlV0UTNualhVU2dmSWliXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

从上图中可以看到, 程序的正确的行号上报告了变量重复定义的错误。

#### 函数重定义处理

```SQL
int demo(int a) 
{ 
a = a + 2; 
return a * 2; 
} 
int demo() 
{ 
return 2; 
}
```

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MmI0MTM1ZmUxZGU5N2IzMmMyMjg0OTk0YWZiMWUzMjNfR05mQUI3bXdwa0N6NlpIaHRVbk9IT2ZZWDJ1WncwWkpfVG9rZW46Ym94Y25lVkVsdlNqVUxyTlRSVWo4OXgwQlNjXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MzRkYjg4Yjk1YzcxZjQ0NmFjYjc3ODZjNDlkMjY2YWFfMU10eEdJRzhrOTR5aXpKVTRjQzkySjF0WkRjTzJYdjZfVG9rZW46Ym94Y25zbFlsVUhvYmZMSWFYR2hyNzhwV1JMXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

从上图中可以看到, 程序的正确的行号上报告了函数重复定义的错误。

#### 函数未定义错误

例程: 在正确的程序基础上删去demo()的定义

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MmFmZGQ1OWQ3MzdmYzRkZTFlY2M0M2NjZmZmYzFkYzJfcURzMnBBR3pLYjVmZllCaGN6N3VmWlA4aWt6OHRtUWtfVG9rZW46Ym94Y25PekVXdFI2TWtWWXJjNlZKdDJCbDdnXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=NzRiMWU2ZmU2NWY5MThmNTE2N2I0N2UzODI2MTI1ODJfQXg4NzRUNXpSdmkwbTFpNWNURVhNVlZYckUwSzJqVHFfVG9rZW46Ym94Y24wcU5rZ1BRQ3BtMEtYV0tFRnhITHdnXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

从上图中可以看到, 程序的正确的行号上报告了函数未定义的错误。

#### 类型错误

char c=3.28;

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=Nzg1ZmMzN2UwYjA0NDI0MDNhZGFhYzQ4MjI0YmU1ZTFfZ3I1ckxBSzhMbmE2ZUtldDhrbDFudHREaG9SdmNCOXFfVG9rZW46Ym94Y25VdnU2Tk1ZUHg3Uk1wbFJHZzZvOEVoXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=ZjYxNzBiOTlkM2ViY2I4OTMwOTQ4Zjg4ZmI4ZTNlMjNfZ0FheW9lbmc1VXB2T1FUQzFQazhnemhWbnBEWldoNERfVG9rZW46Ym94Y25GbnhGdG5wdzJ4aDFya3JyZ000aWpiXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

从上图中可以看到, 程序的正确的行号上报告了变量类型错误。

#### 函数参数个数不一致

```SQL
int a; 
int b; 
int program(int a, int b, int c) //三个参数 
{ 
... 
} 
int demo(int a) 
{ 
... 
} 
int main() 
{ 
... 
a = program(a, demo(c)); //两个参数 
return; 
}
```

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=ZmE4ZTQ1OTU0NDFiNzNlNWFiOTg5NzZjMWY0N2JlOGZfbXVQNGhZd29aeHp3aUVDYUY4TkVxTVBEQXFOaEFKbjFfVG9rZW46Ym94Y25WN1ZBZWJCek9hcDNmRXl1S0lBMVJiXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=YzM5MWY3ODJlNGRiOGFjZTVjYWVkMGUyMzdmZDI2ZTdfQ0U5eUdUYkg5V1ZIbVdFREpoUDB0bFNERXZmZU5DS05fVG9rZW46Ym94Y25PeVJDTUw5bkxONm8wN0doSzlxTTVjXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

从上图中可以看到, 程序的正确的行号上报告了参数数量不一致的错误。

#### 函数参数类型不一致

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=M2JmOTFiZGZkZTI0MWI3MzZjM2I2NDVkN2MxN2U3ODdfOUIyRk9ma3RReWlXYk5JNlV6MWFyVXhocmdnODM0U2lfVG9rZW46Ym94Y25EVlFtWWNPSGtPVVdhUlZGRUJCbmxkXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=YzEyNmYwOGViZDVmMDk2OTU5ZjkzZWFjMmQ5NDhlYTZfWVZ3RjNPVEtmY2trTmtrQVRqRWdEWjN6aXVhNnBKVE5fVG9rZW46Ym94Y24yUnFnTVZDSmF1RmRSTXl4czZRdURjXzE2NzAzMDE0NjQ6MTY3MDMwNTA2NF9WNA)

从上图中可以看到, 程序的正确的行号上报告了参数类型不一致的错误。

# 总结与收获

##  实现心得

在此次的编译原理大作业中，我们团队采用了JavaScript+flask的可视化方法，将词法分析以及语法分析的成果部署在服务器上，使用户能够直观、轻便、清晰的观察到类c语言的整个编译过程。

这次编译器项目让我们更加深入的了解了自底向上分析里面的一些概念, 相比上课与做题, 做一个项目能够真正的让我们去深入细节, 掌握语义分析和中间代码生成过程里面的每一个步骤: 以语义分析为例, 在最初的语义分析的实现过程当中并不是很能够理解中间代码的含义，不能够从全局的角度来对于整个闻法得分析过程进行建模，而仅仅只停留在布尔表达式、控制语句IF-THEN-ELSE的语句当中如何回填等等。能够在纸面上较为详尽的实现整个语义分析的过程，但无法有整体宏观的把控。

通过这次学习，在对于整个语法分析的过程有了宏观的把控的基础上，能够实现整个词法到语法再到中间代码生成的过程。

##  问题与调整

在我们实际进行语义分析的过程当中，我们发现之前有一些创新性的文法其实到语义分析的环境来需要进行非常大的调整。因为有一些在语法分析（‘放宽条件’）能够通过的一些文法，在语义分析这种栈规约过程较为严格的分析过程当中进场出现问题。例如文法分析道最后语义分析栈当中还有很长的一部分代码没有完成规约。最终在不断地调整和尝试的过程中完成了本次语义分析的过程。

于此同时，我们也遇到了一些时间规划的问题，刚开始的时候感觉时间还很长，就想从头到尾摸清原理写程序，然后就在调试的过程中因为时间紧张而频繁出错，会让我们感到很焦虑，更加解决不好问题。我们认识到了需要边学习编编写代码，编写代码的过程更不可能是一蹴而就的，而是要遇到各种调试方面的难题。

在本次小组合作过程中，我们通过这次实验，我对编译原理这门专业必修课有了进一步的深层次了解。“纸上得来终觉浅，绝知此事要躬行”，把理论知识应用于实验中，也让我重新熟悉了类C语言的相关内容，加深了对类C语言知识的深化和用途的理解。相信在以后的毕业设计以及进一步深造时可以有更大的提升。

##  展望与思考——更通行高级语言分析及方法

在本次实验当中，我们完成了对于类C语言的语义分析过程的检查，以及判断了基本的错误类型及对应的解决方案。而对于更高级的语义检查和中间代码的生成而言，我们需要对语义分析过程的细节语义更多的注意。

以python为例，python的文法非常简单便捷，对于函数调用形式、变量、数组、矩阵等各种数据结构的定义有着非常丰富的变换规律。然而对于语义分析来说，越发简洁的文法会带来更加困难的语义分析的处理过程。

### 例1——无需定义类型的变量

在python当中将会直接根据实际输入的内容来判断并赋予所书写的变量的类型。那么在语义分析的过程当中可能会涉及到提前对于待定义变量的分析，内部对于节点的type属性进行猜测和赋值等等。

对应的解决方案可以为通过词法分析所得的tokens，判断接下来输入内容的类型，从而更新变量定义的类型type属性。与此同时，在函数调用过程当中的无类型定义的变量，还可以根据所接下来函数调用过程当中函数的处理模式来进行判断，比如接下来的函数处理模式当中为“调用数组元素的值”，那么我们可以把该操作的目的理解为数组元素的调用，那么其类型可能为list、tuple等等可以包含数组元素的变量，从而进行语法及后续的语义分析。精确判定数据类型能够在语义分析的层面上找出对应程序存在的问题。

### 例2——各种库的引入和新语义规则的分析

不管是python，C++等高级语言，都引入了多种不同的库，有的库实现了更多种类的数据类型，例如C++的string、python的numpy.array甚至是pandas的dataframe等等非常复杂的数据结构。对于该类复杂数据结构的分析的主要方法会更加的复杂，在该中基础上如何进行新的语义规则的分析呢。

首先我们需要知道，引入的库函数以及新的数据类型其实仅仅是对于原本数据类型的一种拓展（可以理解为在翻译的基础上再进行一次翻译）。那么我们再定义对应的变量的过程中，如C++的string，对于string的赋值其实内部将会由库函数本身翻译为对应char*变量的赋值，而对应的翻译过程可以理解为“成员函数”的处理过程。通过对于“操作符、函数的重构”，作为“第一次”翻译，将对应的内容翻译为基本层面的该高级语言能够直接应用的文法；其次，再通过高级语言到中间代码的“第二次翻译”，最终完成完整的语义分析的过程。

### 总结

从宏观的角度上来说，汇编的作用即将高级语言经过一步步的翻译最终到计算机能够理解和执行的代码。而高级语言当中库函数给我们带来的各种简便运算能够理解为高级语言库函数对于库提供的简便文法本身的“第一层级的翻译”工作，再由语言本身完成“第二层”翻译工作。

由上述分析可知再更为同行的高级语言的分析过程当中我们需要集成现有已有的语义分析的方法，在此基础上结合“新的规则”的引入，通过对于旧规则进行重用，再次基于上赋予新的规则，最终达到不断化简使得程序更为简洁方便的同时，不失语义分析的可行性和可操作性。

## 参考文献

李磊. C编译器中间代码生成及其后端的设计与实现[D].电子科技大学,2016.

《程序设计语言编译原理》（第三版)﹐陈火旺、刘春林等，2000年，国防工业出版社，

Compilers: Principles,Techniques and Tools (2nd Edition). Alfred V. Aho,Monica S.Lam,Ravi Sethi,Jeffrey D.Ullman,Addison Wesley; 2006

任小强,王雪梅,唐晓华,王春佳.基于Python的编译原理教学演示模块设计与实践[J].工业控制计算机,2021,34(09):72-73.

杨静. 编译器的语法分析测试用例生成方法研究[D].华中科技大学,2013.

蝉鸣的夏天. 【编译原理】学习笔记以及课程设计[EB/OL]. https://blog.csdn.net/yukiaustin/article/details/108623998.

ustcsse308. 编译工程1：词法分析[EB/OL].https://zhuanlan.zhihu.com/p/65490271.

W3Cschool. Flask 教程[EB/OL]. https://www.w3cschool.cn/flask/.

子恒. [编译原理]Python实现的语法分析器[EB/OL]. https://chestnutheng.cn/2016/12/27/cmp-grammar/.

antherd.腾讯云centos7 安装图形界面 vnc远程连接[EB/OL]. https://blog.csdn.net/REX1129/article/details/78939712