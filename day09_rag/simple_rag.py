documents = [
    "公司年假制度：正式员工每年享有10天带薪年假。",
    "公司报销制度：员工出差产生的交通费可以申请报销。",
    "公司办公时间：工作日上班时间为上午9点到下午6点。",
    "公司退款制度：符合条件的订单可以在7天内申请退款。"
]


question = input("请输入你的问题：")


for document in documents:
    if "年假" in question and "年假" in document:
        print("\n找到相关资料：")
        print(document)

    elif "报销" in question and "报销" in document:
        print("\n找到相关资料：")
        print(document)

    elif "办公时间" in question and "办公时间" in document:
        print("\n找到相关资料：")
        print(document)

    elif "退款" in question and "退款" in document:
        print("\n找到相关资料：")
        print(document)