from pywebio import input, output, start_server

def vote_app():
    candidates = input.checkbox("请选择候选人：", options=["候选人A", "候选人B", "候选人C"])
    output.put_text("你的投票已经提交！")
    output.put_text("投票结果：")
    for candidate in candidates:
        output.put_text(f"{candidate}: {candidates.count(candidate)} 票")

if __name__ == "__main__":
    start_server(vote_app, port=8080)