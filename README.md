<div align="right">
  Language:
  🇺🇸
  <a title="Chinese" href="/README_CN.md">🇨🇳</a>
</div>

# Requirements analysis

## Input-output convention

Input: C language program that needs Compilation, grammar rules json format file.

Output: Add intermediate code table on the basis of lexical analysis table, parse tree, ACTION + GOTO table and stack process of project 1, and statically check the error list.

### Source program input

Enter the C-like language program code with or without a procedure call in the text box. For examples, please refer to the following files in the submission folder:

3_ test code (example)

```SQL
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

For different types of BigInt, the fourth part of this report will give simplified examples.

### Semantic analysis output

- Intermediate code analysis table

### Static inspection analysis output

- List of errors found by static inspection

## program functions

### Semantic analyzer

We realize the semantic analysis and intermediate code generation of C-like language with procedure call, users can test and translate any program by themselves, and view the analysis results of any project in real time.

### static semantic checking

In the process of semantic analysis, we realize the check of 7 semantic errors such as type mismatch and variable definition, give user-friendly error prompts, and realize the basic error recovery function, that is, in one check, we can achieve a complete scan of the program and find most of the errors in the program.

# outline design

## task breakdown

From the user's perspective, we break down the task into the following two aspects:

### Intermediate code display:

The intermediate code is presented in the form of a table

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=OGZjMzhhZjQyY2Y2MDIyNTMxOTAzOGZiOWJmY2FjNjVfbnpEcXpsVVR0R3VoejZmdXc0R2JoY3B6ZzEzRmpwNHZfVG9rZW46Ym94Y256SGdjbEhwMWVTbTJmMEthOWhQS1RiXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

 

### Static check result display

The results of the static inspection results are also displayed in the form of a table,

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MmMwODIwZjVhYjBmZTExNzViMzFkNjRlY2E1MmQxNTdfRDRnUXJIbnY5MmFDTW1LcldMRzF5UDhIeExYVmJWOGZfVG9rZW46Ym94Y25zbzdBckhjRUtNTWQ5Z0NvNmxxTFZkXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

## main program flow

Start the program, you can start the program from the command line, or directly access the http://yuanxinhang.fun:5000/

Command line environment configuration method:

Install dependencies.pip3 install -r requirements.txt2. Run flask.python top.py3. Open the 127.0.0.1:5000 in your browser

The initial interface of the program is as follows:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MTJiNjExMjJkOTliNzcxYTU1N2I2ZTQ4YmYxMzhjYjFfNW9ObXRvcjBIOXU4dlc1eXd1amZpdnAyVFB2OTRHcUtfVG9rZW46Ym94Y25hWWlVa2IwWmI2ZW9BaWFzdktHbnliXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

At this time, the web page will load the default program for lexical, grammatical, and semantic analysis. The analysis results are on the left side of the screen, and clicking on the corresponding tab will automatically load the corresponding analysis results.

Users can enter their own c program (with code highlighting), click the submit button in the lower right corner to perform semantic analysis on user input, the result is presented on the left side of the screen, if the user input is wrong, it will prompt the corresponding error message, static check results are displayed in the last tab

At the same time, users can also submit their own syntax files, (syntax file format can be found in the source code inside the grammar.json), the program will read the user-defined syntax format, establish the corresponding syntax analysis table (using LR (1)), and apply new rules to the subsequent program corresponding analysis

## Call relationship between modules

### front end Module call relationship display:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=NjMxMGMzMTkxMzdlMDhiNjAwYjgzZDk4OWIwZjQ3ZjlfdW4wclRQdnJ0Wm9tRDIxbmViWVdncEhWRDNzZXB6OElfVG9rZW46Ym94Y24xQ25hV1UwWGhWbjh6bjR2TVZ3ZW5lXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

### Show the call relationship between back-end modules

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MTBjMjM5ODQ1YmVmOWU2OTgxZWY0NDJjNTZhOGY3YzBfcVk3d1phdllRVGM3aThvNHYyV3NyallIenhWcUM0bW9fVG9rZW46Ym94Y24wTUxwb0hzeWJYTHlsc2V0V1RLRm9jXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

# detailed design

## Top-level module design

The overall project is built by the flask framework. Flask is a lightweight customizable framework written in Python language. Compared with other similar frameworks, it is more flexible, lightweight, safe and easy to use. It can be developed well in combination with the MVC mode. The overall structure of the project is shown in the following figure:

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

##  Front end Part of the detailed design

In the display of Compilation results, we adopt the idea of Modularization design, first use the HTML to realize the front-end interface design, on this basis, further use JavaScript to realize the functions of each part, and finally use the CSS to beautify the interface.

The following describes the specific Function design process by function

### Lexical analysis:

The result of lexical analysis is simple and clear, only need to use a table to display the attributes (Type) and value (Value) of each word. The back end packages the analysis result into a structure array and sends it to the front end of the page, and the front end uses jQuery to decode the data into HTML table objects for display.

### Syntax analysis:

#### Syntax tree display

The implementation of syntax tree is more complicated, because LR (1) analysis obtains the symbol change in each step of the stack. We first need to convert the analysis process into a data structure that is easy to display, and then send the data to the front end for display. The general steps are as shown in the following figure:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=ODI2OGNkMzE0N2JmMWVkNGU3MDdjMzQyOTk3OWViNGRfdkNWUWNWWDNkc1FhQjBzZThBMklMeHFTSUxnNVU3M0ZfVG9rZW46Ym94Y25XTlJFZW5ZTkg0bTIwZWV0eG50a0doXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

For the display of the front-end tree structure, we have selected a widely used D3.js graphics visualization library, the main feature of which is that the generated graphical interface can be interactive, simple and intuitive.

We choose the nested structure as the data structure of the syntax tree, and the children property of each node is stored as an array of all its child nodes, representing a derivation process:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=NTFjNDdhODU1N2E2MTA3ZjBhNmU4NTY0NGJhNTQ3ZmZfVVFGbWpHQVVOSDcxS0pRNWtEUklSblk2ZTNrWFp0U1RfVG9rZW46Ym94Y25iMDE2YVlvMG1tdGlKZDBRRVJvcG5nXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

In the visualization of syntax trees, two problems need to be solved:

\Generation of SVG graphic objects

Graphical objects include node objects and edge objects. The key problem is how to establish the connection between nodes and edges, so that the whole image is distributed in a tree shape. The above functions are realized by the following Functions:

```SQL
d3.layout.tree() //处理树的结构分布
d3.svg.diagonal() //实现SVG图像的坐标转换
tree.nodes(root).reverse(), // 树内节点的转换
tree.links(nodes); // 建立节点与边的联系
```

\2. Processing of user interaction (zoom, click, node information display, etc.)

View scaling we use D3 comes with the Zoom module to achieve, and click operation implementation is more complex, mainly by Update () to recalculate the node position, which can be subdivided into entering the clicked node under the subtree, and close the clicked node under the subtree two opposite operations, and finally recalculate the coordinate distribution of all graphic objects, and refresh the display area.

The display of node information is realized by the tooltip Function, whose function is to create a transparent mask on the entire image, and to monitor the position of the mouse at any time.

#### LR Analysis table ACTION GOTO and presentation of the analytical process

We also use jQuery to achieve the conversion of table data to HTML objects, the difference is that because the ACTION and GOTO tables are relatively large, we need to set the horizontal and vertical direction of the moving bar, which is convenient for users to find.

## Function call relationship:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MDZmZTFhMmMyNTRlY2JjNmVmMzcxYzAxNzY1OTI4ZmRfQVcyMDJNYjd1NWhJNjhZWVFYVWR0NTZOTmxrZ0Q1NGZfVG9rZW46Ym94Y25Sb1lMcFlIR3E0eDBSRkpoVnFveEdkXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

## Detailed design of the back end part

### Algorithm idea

#### Preset work - lexical and grammatical analysis

In the previous work, we completed the construction of the corresponding modules of lexical analysis and grammatical analysis.

In the lexical analysis, we use the lexical analysis algorithm of the tool lex to replace DFA with Regular Expression matching method for lexical analysis. Through 6 Regular Expression parallel matching lexical elements, each time the longest matching sequence at the beginning is recognized as the token represented by the corresponding Regular Expression, thus realizing lexical analysis.

In parsing, we solve the FIRST set of production non-terminators in the grammar, and then identify the set of all items with the same live prefix through CLOSURE (I) Algorithm. We build the finite state automaton DFA, hash table H, item set queue P, and further complete the construction of LR (1) prediction table, and finally generate the parsing tree according to the result of parsing.

#### semantic analysis

We adopt the method of one-time scanning - we complete the semantic analysis work for different grammars according to the pre-defined grammar. For each production of the specification, for different grammar rules, different quaternary forms are generated according to different translation modes of different bureaus as the embodiment of the intermediate code; finally, the final result is obtained by translating the intermediate code.

In terms of grammar and sentences, we mainly include: the translation of descriptive sentences, the translation of assignment sentences, the translation of Boolean expressions, the translation of control sentences, and the processing of procedure calls.

Translation of descriptive sentences

For the description statement in the procedure, we tell the variable or Function of the corresponding description to be stored in the symbol table by building a symbol table. In the semantic rules, we use the following operations:

(1) inktable (previous) Creates a new symbol table and returns a pointer to the new table. The parameter previous points to a previously created symbol table, such as the peripheral procedure symbol table that just surrounds the embedding process. The value of the pointer previous is placed in the header of the new symbol table, which can also store some other information such as procedure nesting depth and so on. We can also number the procedures in the order in which the g procedure is described, and fill this number into the header.

(2) Enter (table, name, type, offset) Creates a new entry for the name name in the pointer table refers to the small symbol table, and fills in the entry with the type type and relative address offset.

(3) addwidth (table, width) Record the total width occupied by all names in the table in the header of the symbol table of the pointer table ZK.

(4) enterproc (table, name, newtable) Creates a new entry for the procedure named name in the symbol table of the pointer table refers to 7K. The parameter newtable points to the symbol table of the procedure name.

In the process of recording the symbol table, we improved the translation mode "T-record D end" generated by Domain Name, and the operation "inktable (previous) " of one symbol table per process, changing to only maintain a large symbol table globally; the way of adding new fields to the symbol table can more accurately determine the access of global variables and Function variables.

Translation of assignment statements

The main job of translation of assignment statements is to translate simple arithmetic expressions and assignment statements into three-address code translation. It needs to be explained how to find the population of the symbol table. The attribute id.name represents the name itself represented by the id. We use the procedure lookup (id.name) to check whether there is an entry corresponding to this name in the symbol table. If there is, return a content pointing to the table entry, otherwise, return the information not found. The main translation modes include the following:

| S→id:=E | S.code:=E.code \|\| gen(id.place ‘:=’ E.place)               |
| ------- | ------------------------------------------------------------ |
| E→E1+E2 | E.place:=newtemp;E.code:=E1.code \|\| E2.code \|\|gen(E.place ‘:=’ E1.place ‘+’ E2.place) |
| E→E1*E2 | E.place:=newtemp;E.code:=E1.code \|\| E2.code \|\|  gen(E.place ‘:=’ E1.place ‘*’ E2.place) |
| E→-E1   | E.place:=newtemp;E.code:=E1.code \|\|  gen(E.place ‘:=’ ‘uminus’ E1.place) |
| E→ (E1) | E.place:=E1.place;E.code:=E1.code                            |
| E→id    | E.place:=id.place;E.code=‘ ’                                 |

Translation of Boolean Expressions

Boolean expressions by using Boolean operators to Boolean quantities, relational expressions linked together, mainly contains the operational relationship: and, or, not; relational operators include ：＜,≤,＝, ≠ ，＞ ,≥； Boolean expressions are mainly used for logical calculus, calculation of logical values, and control statements for conditional expression.

In this example, Boolean expressions are generated mainly by the following grammar:

```SQL
E→E or E
E→E and E 
E→~E 
E→(E) 
E→id rop id 
E→id
```

We use a side scan method for the generation of Boolean expressions, mainly including the operation contract positioning: quaternary: (jnz, a, -, p) means'f a goto p '; (jrop, x, y, p) means'if x rop y goto p'; (j , -, -, p) means'goto p '.

Function makelist (i), which will create a new linked list containing only i, where i is an subscript (label) of the quaternary array; Function returns a pointer to this chain. Function merge (p1, p2), merges the two chains with p1 and p2 as the head of the chain into one, as the Function value, and returns the merged chain head as the function value. The procedure backpatch (p, t), whose function is to complete the "backfill", fills in the fourth section of each quaternary linked by p as t. The main translation mode is as follows:

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

Translation of control sentences

Control statements mainly include - if-then (-else) statements, while loop statements, return statements.

The main grammars involved include:

```SQL
S→if E then S
S→if E then S else S
S→while E do S
S→begin L end
S→A
L→L;S
L→S
```

Among them, S represents a statement, L represents a statement table, A is an assignment statement, and E is a Boolean expression.

The main translation modes include:

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

Handling of procedure calls

Procedure call processing mainly includes two things: passing parameters and rotor (procedure). The address transfer: the address of the real parameter is passed to the corresponding formal parameter; the calling segment first passes the address of the real parameter to the place where the called segment can get it; after the program control is transferred to the called segment, the called segment first copies the address of the real parameter into its corresponding formal unit; in addition, the reference and assignment of the formal parameter by the procedure body are processed as indirect access to the formal unit.

The translation modes of procedure calls in this example mainly include:

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

#### Intermediate code generation:

According to the results of the above semantic analysis, in the combination of other sentences (such as return, compound statements, Function labels), etc., finally all the translation results of emit are integrated into the intermediate code in the form of quaternion, and finally the intermediate code can be translated to get the final result.

### Code idea and implementation architecture

#### Code implementation framework

The figure below shows the Algorithm flow chart of the overall project, in which the parts of lexical analysis and grammatical analysis are not expanded.

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MDEwNTI2OTc3NmIzNWY1YTY5MjQ3NWIyYjY0MDQ4ZGVfVldVa0JtTE9HOHZ3YkIwTEhoU2xEYllQbEhMNGd3eXJfVG9rZW46Ym94Y25QU1BTbkVMazdOYzUxWE1MT3Q1NWJkXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

As can be seen from the figure above, the user enters the program segment and grammar first. A lexical analyzer performs lexical analysis on the program segment and proposes TOKENS. The LR1 analyzer constructs an LR1 analysis table according to the grammar provided. Finally, the TOKENS result of lexical analysis and the LR1 analysis table of grammar analysis are combined to perform grammar analysis and semantic analysis. Since we adopt the method of scanning on one side, the grammar analysis and semantic analysis are performed in parallel in this stage. The state of each step of grammar analysis corresponds to the specified production, and the semantic analysis of the corresponding sentence is scanned. According to different types of grammars in semantic analysis, different types of specifications and analysis operations are performed for assignment statements, control statements, declaration statements, boolean expressions, Function call processing, etc. Finally, two symbol tables (variable table + Function table) and an unadjusted quaternary are generated. Finally, the lines are translated into intermediate code by the quaternary and fed back to the user as the output of the program.

#### Semantic analysis part Function call relationship framework

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MzE0YzkwM2YxYTZiMzVmZjBhYTgyYjEzZmY2NmRjOTFfSGZBUEpzUjBsdUpFZVVVbVVzeGljQjlOaWNCeWhLVEdfVG9rZW46Ym94Y25YbGFXaDRtc3ZqaEdQdEQxRzJDT0ZkXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

The figure above shows the call relationship of the Function in the semantic analysis part. It can be seen from the figure that start_analysis Function is the main Function called by the grammar analysis. Due to the parallelism of grammar analysis and semantic analysis, for each process of grammar analysis specification, the corresponding process of semantic analysis is constructed for the called grammar. The semantic analysis mainly includes five parts: assignment statement, control statement, declaration statement statement, boolean expression, and Function call processing. According to different grammar categories, Function adopts different methods to align and process intermediate code generation.

semantic_analysis has several sub-Functions, where get_new_lable applies a new variable to the scanned declaration and adds the corresponding symbol to the symbol table in a update_symbol_table manner. get_new_temp means to generate a current temporary variable, which is used to store the current temporary variable information for later generation of intermediate code. Similar to the naming of variables and the creation of the Function table is the creation process of the Function table. Create a new Function table in get_new_function_lable way, complete the update operation to the Function table by update_function_lable Function, and its sub-Function find_function_by_name used to find the lable of the corresponding function according to the function Function name, so as to determine whether there is a special case such as Function redefinition. Finally, through disp_SEMANTIC_STACK Function, the content of the stack involved in the semantic analysis process is displayed.

### Function call and implementation

#### Function call relationship architecture

In the last session, we elaborated on the project framework of semantic analysis and intermediate code generation in the whole project. Next, we will walk into each Function and explain the implementation of each module and internal main Function in detail.

#### Function analysis

1, semantic analysis main function semantic_analysis ()

The main function of semantic analysis performs semantic analysis for each step of grammar analysis, because there are many different types of grammars involved in the process of grammar analysis, the main function of semantic analysis also plays a role in making decisions for each type of different grammar.

For each sentence to be analyzed, two symbol tables and corresponding quaternions are generated in combination with the corresponding grammar, and the corresponding analysis state is stored in the parsing stack at the same time.

```SQL
'''
函数名：def semantic_analysis()
函数功能：语义分析主函数，过对于语法分析当中的每一个步骤进行语义分析
输入参数：TOKENS、当前产生式、当前分析站内情况
输出参数：无
时间复杂度：O(1)~O(n)，总体时间复杂度为O(1)+O(1)~O(n)，前者O(1)为有限文法的判断时间，后者O(n)表示在优先文法判断的过程当中，执行到每一步特定的文法规约的时间复杂度为O(1)~O(n)不定，取决于特定的文法，故最坏情况下的时间复杂度为O(n)
'''
```

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=OWM3ZjZmOGQxZmYwNTVmYWNhMTc2ZDEzMTI0NmU2ZTZfMjVpbjFKaTliU3Zad2hKckg5M3RhcFYxZkxsUEJoQVBfVG9rZW46Ym94Y25ONVpRZzJYYjZXUUpSTmduRE1SRHViXzE2NzAzMDE4NDg6MTY3MDMwNTQ0OF9WNA)

Analysis and Translation of Declaration Sentences

In the main program of semantic analysis, we first need to clarify the processing of declaration statements. Declaration statements include variable declarations, constant declarations, Function declarations, etc. In this example, we combine variables and constants to analyze declaration statements; secondly, by analyzing the type of declaration, we determine what symbol table is used to add in the next process of semantic analysis:

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

Analysis and Translation of Assignment Statements

Assignment statements mainly involve assigning new values to variables, temporary variables, etc. Here, the main consideration is to generate quaternary assignment. At the same time, consider whether the corresponding type conversion is needed through the type of the arithmetic expression that needs to be assigned, and at the same time update the type and value in the corresponding symbol table. The main Functions are as follows:

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

Analysis and Translation of Boolean Expressions

In the processing of Boolean expressions, we consider that Boolean expressions can also be used as a category of arithmetic expressions, so we classify Boolean expressions as arithmetic expressions and process them in arithmetic expressions, and at the same time expand the operator variable accordingly, so that it can be more flexible and simple to carry out translation work.

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

Processing of constant expressions (for each arithmetic expression, the final result forms a constant expression, updates to the constant symbol table and for subsequent specification and semantic analysis operations):

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

Integration of expression expressions:

After listing arithmetic expressions, boolean expressions, constant expressions, declaration expressions, and assignment expressions, we need to integrate all expressions, merge corresponding code snippets, integrate, and update the content of the semantic analysis battle. Expression consists of expression and expression_profix, the latter using comma expressions to assemble the content of all subsequent expressions:

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

Analysis and Translation of Control Sentences

Control statements mainly include while statements and IF-THEN (-ELSE) statements, which mainly discuss the translation of these two cases. Due to the scanning method, we need to backfill the jump destination address of some internal nodes:

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

Analysis and Translation of Function Calls

Function call process is relatively simple, in the quaternary which is mainly reflected in the advance of the station which stores the corresponding variables, here temporarily did not consider the default register system call problem, to the subsequent assembly language generation when doing more detailed description and expansion.

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

# Semantic analysis error handling

In this experiment, we make the following assumptions about the C language:

Assumption 1: Integer (int) variables cannot be assigned or operated on with floating-point (float) variables.

Assumption 2: Only int variables can perform logical operations or as conditions for if and while statements; only int and float variables can participate in arithmetic operations.

Assumption 3: Any Function is defined only once and cannot be declared.

Assumption 4: Functions cannot be nested.

Assumptions 1 to 4 above can also be considered requirements, and violations will result in various semantic errors, although we will only examine a few types of errors discussed later. Furthermore, since the lexical and syntactic analysis work has been done, we can safely assume that the input file does not contain comments, octal numbers, hexadecimal numbers, and exponential floating-point numbers, nor any lexical or syntactic errors.

Our program can perform semantic analysis on input files (which may contain procedure calls) and check for errors of the following types:

Error Type 1: Variable is undefined when used.

Error Type 2: Function is not defined when called.

Error Type 3: Duplicate definition of a variable, i.e. the variable is duplicated with a previously defined name.

Error type 4: Duplicate definition of Function (i.e. the same Function name appears more than once).

Error type 5: The expression types on both sides of the assignment number do not match.

Error type 6: Operand types do not match

Error Type 7: The number of actual participating parameters does not match when Function is called.

Error Type 8: The types of the actual participating parameters do not match when Function is called.

## Example

### Sample example:

#### Example 1

**Enter:**

```SQL
int main(){
     int i = 0;
     j = i + 1;
 }
```

**Output:**

The variable "j" in the sample input is undefined, so our program can output the following error message:

Error at line 2: can't find defination of symbol: j

#### Example 2

Enter:

```SQL
int main()
{
  int i = 0;
  inc(i);
}
```

**Output:**

Function "inc" is not defined in the sample input, so our program can output the following error message:

Error at line 4: can't find defination of function: inc

#### Example 3

Enter:

```SQL
int main()
{
  int i, j;
  int i;
}
```

Output:

```SQL
样例输入中变量“i”被重复定义，因此我们的程序可以输出如下的错误提示信息：
Error at line 4: multiple defination of symbol: i
```

#### Example 4

### Enter:

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

Output:

```SQL
样例输入中函数“func”被重复定义，因此我们的程序可以输出如下的错误提示信息：
Error at line 6: multiple defination of function: func
```

#### Example 5

### Enter:

```SQL
int main()
{
  int i;
  i = 3.7;
}
```

Output:

```SQL
样例输入中错将一个浮点常数赋值给一个整型变量，因此我们的程序可以输出如下的错误提示信息：
Warning at line 4: Left Type: int doesn't match with the Right Type: float
```

#### Example 6

Enter:

```SQL
int main()
{
  int i;
  10 = i;
}
```

Output:

```SQL
样例输入中整数“10”出现在了赋值号的左边，因此我们的程序可以输出如下的错误提示信息：
Error type 6 at Line 4: The left-hand side of an assignment must be a varia-ble. -->
```

#### Example 7

Enter:

```SQL
int main()
{
  float j;
  10 + j;
}
```

Output:

```SQL
样例输入中表达式“10 + j”的两个操作数的类型不匹配，因此我们的程序可以输出如下的错误提示信息：
Warning at line 4: Left Type: int doesn't match with the Right Type: float
```

#### Example 8

Enter:

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

Output:

```SQL
样例输入中调用函数“func”时实参类型不正确，因此我们的程序可以输出如下的错误提示信息：
Error at line 8: function func()'s argument a is of type int, but char given.
```

#### Example 9

Enter:

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

Output:

```SQL
样例输入中调用函数“func”时实参数目不正确，因此我们的程序可以输出如下的错误提示信息：
Error at line 8: function func takes 1 arguments, but 2 given
```

### Algorithm idea

In the one-scan analysis method, error handling and semantic analysis are interspersed and carried out simultaneously. We first analyze the possible error types according to some characteristics of the C language: for example, C language is a strongly typed language, and it is necessary to carefully check whether the types of assignment and operation match; the number of parameters of Function must be the same, etc. Then correspond different types of errors to different steps of semantic analysis, write corresponding error handling Functions, and make error handling Function calls in corresponding places. This design idea of separating semantics and error handling Function not only makes the architecture of the program clearer, but also facilitates the division of labor among team members, reduces the coupling between codes, and is similar to the design idea of using implanted Instruction to handle program errors in the operating system.

### Code and Implementation Architecture

#### Code implementation framework

For different problems, we have implemented the following error handling Functions, each Function handles an error type respectively:

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

#### **1.1.1.2 Semantic Analysis Partial Function Call Relation Framework**

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=OWQ4YjU3ZDhjMmVhYzE3MjFhYjdkMDIyNThlYWFmN2ZfanVnZldUVENzaFZ4bWpoYjNYYnRMUXcza0VEbExKV0ZfVG9rZW46Ym94Y25Ha1Y0U1IwODFZRGlMRkpzYmtpdHdnXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

### Function invocation and implementation

The following explains the processing flow of each semantic error separately

#### Function analysis

The general structure of each error handling Function is similar and is of the following form:

```SQL
def error_Handler_RedefinedSymbol(nodename, token):  # 重定义处理
    global ERROR_MSG # 全局错误信息数组
    msg = "Error at line {}: multiple defination of symbol: \"{}\"".format(
        token['row']-1, nodename) # 错误信息
    print(msg) # 打印错误信息
    ERROR_MSG.append(msg) # 将错误信息发送到前端显示
```

It can be seen that the function of error handling Function is mainly to integrate the specific information in the parameter into a standardized error message, and then send the data to the client. The difficult part of error handling lies in the extraction of error information and the judgment of error conditions, that is, to record the information of related parameters such as symbol table when the program errors.

##### Symbol redefinition error

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

For each newly defined symbol, we check whether the symbol is already in the symbol table, and if so, pass the line number (token) and the repeatedly defined variable name (node.id) to the error handling Function for processing.

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

For each symbol used in the operation, we have to check whether the symbol is already in the symbol table, and if not, pass the line number (token) and undefined variable name (node.id) to the error handling Function for processing.

##### Function undefined error

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

For each Function call, you also need to look up the Function name table, and if it is not found, call the error handling Function.

##### Function redefinition error

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

For each newly defined Function, you need to find the Function name table. If a Function is already defined, the row number and Function name are passed into the error handling Function for processing. It is worth noting that the redundant definition of Function leads to many unrelated parts in the stack, which will interfere with subsequent syntax analysis and need to be discarded.

##### Wrong symbol type

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

At the end of the calculation, the type of the result is compared with the type to the left of the copy number, and if it is inconsistent, the error handling Function is called to prompt.

##### Arithmetic expression type error

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

As above, for each operation, hints are given if the types on both sides of the operator do not match.

##### 7. The wrong number of Function parameters and the wrong type of Function parameters

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

For each call of Function, the object and type of the real parameters of Function are checked, and if it does not meet the definition of Function, it is prompted.

# Debug analysis

   - ##  Test data and test results

The correct output is shown below first, and then the results of different types of error handling are shown separately.

### Normal input

The following are test cases, including complete C-like language functions such as procedure calls:

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

After semantic analysis, the program outputs a complete quaternary intermediate code:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=YzBmMGFlODUxNmFmMjA2YjcxMjc4NWVjM2M0YjQxMmNfckQxYWNNc1Fja1gzUHJDdjR6UzQxS21iWm9MT2xPTklfVG9rZW46Ym94Y25NdjNIb1d0UnYxWGhBaHhieE9RZkJiXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

The sample program has no errors, the semantic error bar is displayed as follows:

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=M2YwMTFhOWNmOWU2N2M1NWQ3NTM1N2VlYTgzM2I2NzJfaU5NTm5YNGpkeTVmM1BFVXVrTUhnR2tVZWJvYjZoc0NfVG9rZW46Ym94Y24xN0lWekFVeWU2dDB6WktPeTFnWk1lXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

### incorrect input

The example program for incorrect input is modified from the correct program above.

#### Symbol undefined error

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

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=NDk3MjA0MDBmMWVkODVhYzQ2YWNjMDUzYmQ2YzM5ZmNfa3AyOURWWjBtMjM2c1BCMHRCUU5zS2VtaVpGVUo0UWlfVG9rZW46Ym94Y25iTGVXTnNsamlYRklldXdueHEwVEFoXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MjBmYzc0YTA4NGI1MTJmMTY1MTg0OWExZWFhYTU2ZTFfU1BOdlpJYnZOR2prSXlSQnJQZm5EZmtWN1lBd1h5ZW1fVG9rZW46Ym94Y25XelJaWElQWnFscEhia3BNYTVFcEFLXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

As you can see from the figure above, the variable undefined error is reported on the correct line number of the program.

#### Symbol redefinition error

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

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MTQ5YWM5NmUzNzEzZTMzYmQyOTUyZTA5NWVhY2M4ZGJfSnBqaEl1dWE3ZlBabE5tQlRjWjJtcllnWnhDNWdPUVpfVG9rZW46Ym94Y25vR0czRTFoOEpxUDhMYll2WkR4ZnlmXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=NjJlYmY2NjAxZmFiMDQ2MWY4YjRlOTllNzJlOGFhNjJfOEZCaENWNjdha0JyY2lrUElHQW9VRU1Jak5uNFZTTm5fVG9rZW46Ym94Y25xRWtPbmExNlV0UTNualhVU2dmSWliXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

As you can see from the figure above, the error of duplicate variable definitions is reported on the correct line number of the program.

#### Function redefinition processing

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

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=ZmE2OGNjZTA4ZWY0NmM3MTQwMmU1Y2NhYWNkOTgyNjJfdkZQN1c5T3hrTVdGUVhuZk1xaEhDZGpBRVJmQ3B1RVNfVG9rZW46Ym94Y25lVkVsdlNqVUxyTlRSVWo4OXgwQlNjXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MzJmMzY0M2IxMzgwYTBiODM4MDVjNWFjODUwNjY5NDVfVkJDZFM2V2N2MmkxZlRsZU5qMVV6SGZTWU0zQmZNV1NfVG9rZW46Ym94Y25zbFlsVUhvYmZMSWFYR2hyNzhwV1JMXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

As you can see from the figure above, the Function duplicate definition error is reported on the correct line number of the program.

#### Function undefined error

Routine: Delete the definition of demo () on the basis of the correct program

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=OTcxODdhNTA1MTQyOTA1ZDAxZTZhMmQzYWUyZTJjM2Nfb2JoUHBXUllZYVR5NW5KRGNjamFUUnN5N2txVkJVVzBfVG9rZW46Ym94Y25PekVXdFI2TWtWWXJjNlZKdDJCbDdnXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MDM3M2FjYmExMjhjYTI2YTQyOTY2YWVmYjMxZWE2ZmJfUHJ2S2p6N1NCSTJTYWliTmJ1cGpJT0ltUWgyNHFFY1dfVG9rZW46Ym94Y24wcU5rZ1BRQ3BtMEtYV0tFRnhITHdnXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

As you can see from the figure above, the Function undefined error is reported on the correct line number of the program.

#### type error

char c=3.28;

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=MThjZDg2NjNlYzEwMTliNTE5MDY4NjQwOGIxMDlkNmNfQnE2Y1B1UGF1blJmaHVxMGRSV29OMWVZMFBrRGVaR2ZfVG9rZW46Ym94Y25VdnU2Tk1ZUHg3Uk1wbFJHZzZvOEVoXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=YjJkZWFiMGI5ZjNlMTk3MTliMGVkZGVhODNlMmJlYmVfUjA1REVjTkd3eTJQTWtTQTdGV1BtRno2WlMzN0lWZUVfVG9rZW46Ym94Y25GbnhGdG5wdzJ4aDFya3JyZ000aWpiXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

As you can see from the figure above, the variable type error is reported on the correct line number of the program.

#### Inconsistent number of Function parameters

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

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=ZTJlMWU1NzFkNWM4NTFjY2ZjM2RhNTYzYjVlNjI1ZTJfR0E0NFRJeGdxVW9aTXZFSU5EeVVzN2I1TjdmczZFNzdfVG9rZW46Ym94Y25WN1ZBZWJCek9hcDNmRXl1S0lBMVJiXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=YjFiNmVlYjllMzQ1ZjdhZDVkMDk1OWM4MmZjYjk0NDBfVmdlQlNNR1FwTlhSNjFWb3hIQW40UW56WTZNZ2tIbFhfVG9rZW46Ym94Y25PeVJDTUw5bkxONm8wN0doSzlxTTVjXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

As you can see from the figure above, the error of inconsistent number of parameters is reported on the correct line number of the program.

#### Inconsistent type of Function parameter

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=N2I3NmEwZWU0NWUxMTM2ODZlYmU4MDA3YzI2ZjM3NmFfaGFidGZaT1FNdjJpeTF2MVRVM0lEYWpiWnVheDZpZHhfVG9rZW46Ym94Y25EVlFtWWNPSGtPVVdhUlZGRUJCbmxkXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

![img](https://p0mv60127x.feishu.cn/space/api/box/stream/download/asynccode/?code=OTdkODc5NmFlMWQ1NDNmODQzYzQyOTEyYWIzNGQzMjJfZDRDZkNzU0pCMmxMdjlOMWZGM0JuUkM0bGtnYUpJU0ZfVG9rZW46Ym94Y24yUnFnTVZDSmF1RmRSTXl4czZRdURjXzE2NzAzMDE4NDk6MTY3MDMwNTQ0OV9WNA)

As you can see from the figure above, the error of inconsistent parameter types is reported on the correct line number of the program.

# Summary and harvest

## Realize the experience

In this Compilation principle work, our team used the visualization method of JavaScript + flask to deploy the results of lexical analysis and syntax analysis on the server, so that users can intuitively, lightly and clearly observe the entire Compilation process of C-like language.

The Compilation project allows us to more in-depth understanding of the bottom-up analysis of some of the concepts, compared to the class and do the problem, do a project can really let us go to the details, grasp the semantic analysis and intermediate code generation process inside every step: to semantic analysis, for example, in the initial semantic analysis of the implementation process is not very able to understand the meaning of the intermediate code, can not be from a global perspective for the entire smell of the analysis process Modeling, but only stay in Boolean expressions, control statements IF-THEN-ELSE Backfill, etc. The entire semantic analysis process can be realized in detail on paper, but there is no overall macro control.

Through this study, on the basis of macro control over the entire process of syntax analysis, the entire process from lexical to grammar to intermediate code generation can be realized.

## Problems and adjustments

During the actual process of semantic analysis, we found that there were some innovative grammars that needed to be greatly adjusted in the semantic analysis environment. Because some grammars that can be passed by syntactic analysis ('relaxation of conditions') have problems in the analysis process, which is relatively strict in the stack specification process of semantic analysis. For example, at the end of the grammar analysis road, there is still a long part of the code in the semantic analysis stack that has not completed the specification. Finally, the process of semantic analysis was completed in the process of continuous adjustment and experimentation.

At the same time, we also encountered some time planning problems. At the beginning, we felt that it was still a long time, so we wanted to figure out the principle of writing the program from start to finish. Then during the debugging process, due to time constraints, frequent errors would make us feel very anxious and solve the problem even worse. We realized that we need to learn to write code while learning. The process of writing code is not likely to be achieved overnight, but will encounter various debugging difficulties.

In the course of this group cooperation, through this experiment, I have a further in-depth understanding of Compilation Principle, a compulsory course for majors. "It is superficial when it comes to paper, but I definitely know that this matter must be practiced." Applying the theoretical knowledge to the experiment also made me re-familiar with the relevant content of C-like language, and deepened my understanding of the knowledge and uses of C-like language. I believe that there can be greater improvements in future graduation projects and further studies.

## Prospects and Reflections - More Common Advanced Language Analysis and Methods

In this experiment, we have completed the inspection of the semantic analysis process of C-like language, and determined the basic error types and corresponding solutions. For more advanced semantic inspection and intermediate code generation, we need to pay more attention to the detailed semantics of the semantic analysis process.

Take python as an example. Python's grammar is very simple and convenient, and there are very rich transformation rules for the definition of various data structures such as Function call forms, variables, arrays, matrices, etc. However, for semantic analysis, the more concise grammar will bring more difficult processing of semantic analysis.

### Example 1 - Variables without type definition

In python, the type of the written variable will be judged and assigned directly according to the actual input content. Then in the process of semantic analysis, it may involve the analysis of the variable to be defined in advance, the internal guess and assignment of the type attribute of the node, and so on.

The corresponding solution can be tokens obtained by lexical analysis to determine the type of the next input content, thereby updating the type type attribute of the variable definition. At the same time, variables without type definition can also be judged according to the processing mode of Function in the next Function call process. For example, the next Function processing mode is "calling the value of array elements", then we can understand the purpose of the operation as the call of array elements, then its type may be list, tuple, etc. variables that can contain array elements, so as to perform syntax and subsequent semantic analysis. Precise determination of the data type can find the problems existing in the corresponding program at the level of semantic analysis.

### Example 2 - Introduction of various libraries and analysis of new semantic rules

Whether it is python, C++ and other high-level languages, a variety of different libraries have been introduced, and some libraries implement more types of data types, such as C++ string, python numpy.array and even pandas dataframe and other very complex data structures. The main methods for the analysis of such complex data structures will be more complicated. How to analyze new semantic rules based on this.

First of all, we need to know that the introduced library Function and new data types are actually just an extension of the original data type (can be understood as another translation on the basis of translation). Then in the process of defining the corresponding variable, such as C++ string, the assignment to string will actually be translated by the library Function itself into the assignment of the corresponding char * variable, and the corresponding translation process can be understood as the processing process of "member Function". Through the "reconstruction of operators and Functions", as the "first" translation, the corresponding content is translated into the grammar that can be directly applied by the high-level language at the basic level; secondly, through the "second translation" of the high-level language to the intermediate code, the complete semantic analysis process is finally completed.

### Summary

From a macro perspective, the role of assembly is to translate high-level languages step by step to code that computers can understand and execute. The various simple operations brought by the library Function in high-level languages can be understood as the "first-level translation" of the simple grammar provided by the high-level language library Function, and then the "second-level" translation work completed by the language itself.

From the above analysis, it can be seen that in the analysis process of high-level languages, we need to integrate the existing semantic analysis methods, combine the introduction of "new rules" on this basis, reuse the old rules, and give new rules based on the above again.

## References

Li Lei. Design and Implementation of C Compilation Intermediate Code Generation and Its Backend [D]. University of Electronic Science and Technology of China, 2016.

"Principles of Programming Language Compilation" (third edition), Chen Huowang, Liu Chunlin, etc., 2000, National Defense Industry Press,

Compilers: Principles,Techniques and Tools (2nd Edition). Alfred V. Aho,Monica S.Lam,Ravi Sethi,Jeffrey D.Ullman,Addison Wesley; 2006

Ren Xiaoqiang, Wang Xuemei, Tang Xiaohua, Wang Chunjia. Design and Practice of Teaching Demonstration Module of Compilation Principle Based on Python [J]. Industrial Control Computer, 2021, 34 (09): 72-73.

Yang Jing. Research on test case generation method of syntax analysis for Compilation [D]. Huazhong University of Science and Technology, 2013.

[Compilation principle] study notes and curriculum design [EB/OL]. https://blog.csdn.net/yukiaustin/article/details/108623998.

Ustcsse308.Compilation project 1: lexical analysis [EB/OL] https://zhuanlan.zhihu.com/p/65490271.

W3Cschool. Flask 教程[EB/OL]. https://www.w3cschool.cn/flask/.

Ziheng. [Compilation principle] Python implementation of the parser [EB/OL]. https://chestnutheng.cn/2016/12/27/cmp-grammar/.

Antherd. Tencent cloud centos7 installation graphical interface vnc remote connection [EB/OL] https://blog.csdn.net/REX1129/article/details/78939712
