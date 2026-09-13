def create_plan(name, goal):

    print("================")
    print(f"{name}的AI学习计划")
    print("================")

    print("阶段1：Python基础")
    print("阶段2：AI API调用")
    print("阶段3：RAG知识库")
    print("阶段4：AI Agent")

    print()
    print("最终目标：")
    print(goal)


name = input("请输入你的名字：")

goal = input("请输入你的目标：")


create_plan(name, goal)


def generate_plan(goal):

    plans = {
        "找工作": [
            "Python基础",
            "AI API调用",
            "RAG项目",
            "AI Agent"
        ],

        "创业": [
            "AI工具开发",
            "自动化工作流",
            "产品设计"
        ]
    }

    return plans.get(goal, ["暂无计划"])



goal = input("你的目标是什么？")


result = generate_plan(goal)


print("你的学习路线：")

for item in result:
    print("-", item)


