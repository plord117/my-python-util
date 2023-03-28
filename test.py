classmate = """何若兰
金凯琦
郭菁菁
郭威
户晨阳
李秋艳
李姝颖
刘一宏
刘昱昕
刘钰昕
吕鑫
马婧妍
孟凡超
苗嘉琦
邵奇
史亚会
孙德浩
孙金鸽
王天意
孙德浩
孙振林
万富兴
王鹏飞
杨静飞
赵小虎
温芷媛
谢东旭
徐梦娇
杨雪
杨一辉
于源
潘晨熹
张宇
张虎""".split("\n")

d = {}
for i, v in enumerate(classmate):
    cl = classmate[:i] + classmate[i + 1:]
    d[v] = cl

for k in d:
    s = ""
    for j in d[k]:
        s += f"[[{j}]] "
    d[k] = "- classmate " + s

for k in d:
    print(k, d[k], sep='\t')
