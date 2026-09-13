def ask_ai(question):
    """
    模拟AI回答
    """

    answer = f"""
你问的问题：

{question}

AI正在分析中...

这是我的模拟回答：
继续学习Python，你会成为AI开发者！
"""

    return answer


user_input = input("请输入你的问题：")

response = ask_ai(user_input)

print(response)