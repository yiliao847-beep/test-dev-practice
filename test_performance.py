# test_performance.py
"""
性能测试脚本 - 使用 Locust 框架
测试 JSONPlaceholder API 的性能表现
"""

from locust import HttpUser, task, between
import random

BASE_URL = "https://jsonplaceholder.typicode.com"


class APITestUser(HttpUser):
    """
    模拟真实用户的行为
    between(1, 2)：用户在请求之间等待 1-2 秒
    """
    wait_time = between(1, 2)

    def on_start(self):
        """
        每个虚拟用户开始前执行一次
        用于初始化数据或登录
        """
        print("🤖 虚拟用户开始测试")

    @task(3)
    def get_posts(self):
        """
        @task(3)：这个任务的权重是 3
        意思是：相对于其他 task，这个任务被执行 3 倍的次数
        """
        # 模拟获取不同的文章
        post_id = random.randint(1, 100)
        url = f"/posts/{post_id}"
        
        response = self.client.get(
            url,
            name="/posts/[post_id]"  # 将所有 post_id 归为一个指标
        )
        
        # 检查响应
        if response.status_code != 200:
            response.failure(f"获取文章失败: {response.status_code}")
        else:
            print(f"✓ 成功获取文章 {post_id}")

    @task(2)
    def get_comments(self):
        """
        权重 2：执行频率是 get_posts 的 2/3
        """
        post_id = random.randint(1, 100)
        url = f"/posts/{post_id}/comments"
        
        response = self.client.get(
            url,
            name="/posts/[post_id]/comments"
        )
        
        if response.status_code != 200:
            response.failure(f"获取评论失败: {response.status_code}")

    @task(1)
    def create_post(self):
        """
        权重 1：最少执行
        """
        payload = {
            "title": f"性能测试文章 {random.randint(1, 1000)}",
            "body": "这是一篇性能测试的文章",
            "userId": random.randint(1, 10)
        }
        
        response = self.client.post(
            "/posts",
            json=payload,
            name="/posts"
        )
        
        if response.status_code not in [200, 201]:
            response.failure(f"创建文章失败: {response.status_code}")

    @task
    def get_users(self):
        """
        权重 1（默认）
        """
        user_id = random.randint(1, 10)
        response = self.client.get(
            f"/users/{user_id}",
            name="/users/[user_id]"
        )
        
        if response.status_code != 200:
            response.failure(f"获取用户失败: {response.status_code}")


# ============= 高级用户行为模拟 =============

class BrowsingUser(HttpUser):
    """
    模拟浏览用户的行为
    主要是 GET 请求
    """
    wait_time = between(2, 4)
    weight = 2  # 权重：这类用户占总用户数的 2/3

    @task
    def browse_posts(self):
        """浏览文章列表"""
        response = self.client.get(
            "/posts?_limit=10",
            name="/posts?_limit=10"
        )

    @task
    def view_post_details(self):
        """查看文章详情"""
        post_id = random.randint(1, 100)
        self.client.get(f"/posts/{post_id}", name="/posts/[post_id]")


class AdminUser(HttpUser):
    """
    模拟管理员用户的行为
    会执行增删改查操作
    """
    wait_time = between(0.5, 1.5)
    weight = 1  # 权重：这类用户占总用户数的 1/3

    @task
    def manage_posts(self):
        """管理文章：创建、更新、删除"""
        post_id = random.randint(1, 100)
        
        # 创建
        self.client.post(
            "/posts",
            json={"title": "新文章", "body": "内容", "userId": 1},
            name="/posts [POST]"
        )
        
        # 更新
        self.client.put(
            f"/posts/{post_id}",
            json={"title": "更新", "body": "更新内容", "userId": 1},
            name="/posts/[post_id] [PUT]"
        )


# ============= 备注 =============
"""
运行方式：

1. 命令行运行（推荐学习用）：
   locust -f test_performance.py --host=https://jsonplaceholder.typicode.com

2. Web UI 运行（更直观）：
   locust -f test_performance.py --host=https://jsonplaceholder.typicode.com --web
   然后打开浏览器访问 http://localhost:8089

3. 无头运行（自动化用）：
   locust -f test_performance.py --host=https://jsonplaceholder.typicode.com \
          --users 100 --spawn-rate 10 --run-time 60s --headless

参数说明：
  --users：虚拟用户数
  --spawn-rate：每秒启动的用户数
  --run-time：运行时长（例如 60s = 60 秒）
  --headless：无 Web UI，直接输出结果
"""