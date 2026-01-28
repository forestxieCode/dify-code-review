import os
import requests
import sys

# --- 配置部分 ---
# 如果 diff 超过这个字符数，截断它，防止 Token 溢出
MAX_DIFF_LENGTH = 30000 
# 不需要 AI 审查的文件后缀或路径
IGNORE_PATTERNS = [
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", 
    ".svg", ".png", ".jpg", ".min.js", ".map"
]

def get_env_var(name):
    val = os.getenv(name)
    if not val:
        print(f"Error: 环境变量 {name} 未设置")
        sys.exit(1)
    return val

# 获取环境变量
GITHUB_TOKEN = get_env_var("GITHUB_TOKEN")
DIFY_API_KEY = get_env_var("DIFY_API_KEY")
# Dify 基础地址，如果你是自部署的，请修改这里；如果是云端版，保持默认或从 API 文档复制
DIFY_API_URL = os.getenv("DIFY_API_URL", "https://api.dify.ai/v1") 
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
PR_NUMBER = os.getenv("PR_NUMBER")
PR_TITLE = os.getenv("PR_TITLE", "No Title")

def get_pr_diff():
    """获取 PR 的 Diff 内容"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff" # 关键：告诉 GitHub 我们要 diff 格式
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def filter_diff(diff_text):
    """(简易版) 过滤掉不想让 AI 浪费 Token 的文件"""
    filtered_lines = []
    skip_current_file = False
    
    for line in diff_text.splitlines():
        if line.startswith("diff --git"):
            # 检查文件名是否在忽略列表中
            skip_current_file = any(ignored in line for ignored in IGNORE_PATTERNS)
        
        if not skip_current_file:
            filtered_lines.append(line)
            
    return "\n".join(filtered_lines)

def run_dify_workflow(diff_content):
    """调用 Dify API"""
    url = f"{DIFY_API_URL}/workflows/run"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {
            "code_diff": diff_content[:MAX_DIFF_LENGTH],
            "pr_info": PR_TITLE
        },
        "response_mode": "blocking",
        "user": "github-actions-bot"
    }
    
    print("正在发送给 Dify 进行分析...")
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        print(f"Dify API Error: {response.text}")
        sys.exit(1)
        
    result = response.json()
    # 根据你的 workflow 输出结构调整，通常是 result['data']['outputs']['text']
    return result.get('data', {}).get('outputs', {}).get('text', '')

def post_github_comment(comment_body):
    """将 AI 的意见写回 PR 评论"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": comment_body}
    requests.post(url, json=payload, headers=headers)
    print("评论已发布到 GitHub")

if __name__ == "__main__":
    print(f"开始处理 PR #{PR_NUMBER}...")
    
    raw_diff = get_pr_diff()
    clean_diff = filter_diff(raw_diff)
    
    if not clean_diff.strip():
        print("过滤后没有实质代码变更，跳过 AI 评审。")
        sys.exit(0)
        
    ai_response = run_dify_workflow(clean_diff)
    
    if ai_response:
        # 加个装饰头部
        final_comment = f"## 🤖 AI Code Review\n\n{ai_response}\n\n---\n*Powered by Dify & GitHub Actions*"
        post_github_comment(final_comment)
    else:
        print("Dify 返回为空")