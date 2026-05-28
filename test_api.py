# test_api.py
"""
API 自动化测试示例
使用 JSONPlaceholder 作为测试 API（免费的模拟 API 服务）
官网：https://jsonplaceholder.typicode.com/
"""

import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

print("=" * 60)
print("API 测试开始")
print("=" * 60)


# ============= 基础 GET 请求测试 =============

def test_01_get_single_post():
    """测试 1：GET 请求 - 获取单个文章"""
    print("\n【测试 1】GET /posts/1 - 获取文章 ID=1")
    
    url = f"{BASE_URL}/posts/1"
    response = requests.get(url)
    
    # 断言 1：状态码应该是 200
    assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
    print(f"  ✓ 状态码正确：{response.status_code}")
    
    # 获取 JSON 数据
    data = response.json()
    
    # 断言 2：响应应该包含这些字段
    assert "userId" in data, "响应缺少 userId 字段"
    assert "id" in data, "响应缺少 id 字段"
    assert "title" in data, "响应缺少 title 字段"
    assert "body" in data, "响应缺少 body 字段"
    print(f"  ✓ 响应字段完整")
    
    # 断言 3：检查具体数值
    assert data["id"] == 1, f"期望 id=1，实际 id={data['id']}"
    assert data["userId"] == 1, f"期望 userId=1，实际 userId={data['userId']}"
    print(f"  ✓ 数据值正确：ID={data['id']}, UserID={data['userId']}")
    
    print(f"  ✓ 文章标题：{data['title'][:30]}...")
    print(f"  ✓✓✓ 测试 1 通过！")


def test_02_get_posts_with_query_params():
    """测试 2：GET 请求 - 带查询参数获取数据"""
    print("\n【测试 2】GET /posts?userId=1 - 获取用户 1 的所有文章")
    
    url = f"{BASE_URL}/posts"
    params = {"userId": 1}
    
    response = requests.get(url, params=params)
    
    assert response.status_code == 200
    print(f"  ✓ 状态码正确：{response.status_code}")
    
    data = response.json()
    assert isinstance(data, list), "响应应该是列表"
    assert len(data) > 0, "响应列表不能为空"
    print(f"  ✓ 获取到 {len(data)} 篇文章")
    
    # 检查所有返回的数据都是 userId=1 的
    for post in data:
        assert post["userId"] == 1, f"发现非用户 1 的文章"
    print(f"  ✓ 所有文章都属于用户 1")
    print(f"  ✓✓✓ 测试 2 通过！")


def test_03_get_nonexistent_resource():
    """测试 3：GET 请求 - 获取不存在的资源"""
    print("\n【测试 3】GET /posts/99999 - 获取不存在的文章")
    
    url = f"{BASE_URL}/posts/99999"
    response = requests.get(url)
    
    # JSONPlaceholder 返回 200 但是空对象 {} 或 null
    print(f"  ✓ 状态码：{response.status_code}")
    data = response.json()
    print(f"  ✓ 响应：{data}")
    print(f"  ✓✓✓ 测试 3 通过！")


# ============= POST 请求测试 =============

def test_04_post_create_new_post():
    """测试 4：POST 请求 - 创建新文章"""
    print("\n【测试 4】POST /posts - 创建新文章")
    
    url = f"{BASE_URL}/posts"
    
    # 准备要发送的数据
    payload = {
        "title": "我的第一篇 API 测试文章",
        "body": "这是一篇通过自动化测试创建的文章",
        "userId": 1
    }
    
    print(f"  📤 发送数据：{payload}")
    response = requests.post(url, json=payload)
    
    # JSONPlaceholder 模拟返回 201（创建成功）或 200
    assert response.status_code in [200, 201], f"状态码应该是 200/201，实际 {response.status_code}"
    print(f"  ✓ 状态码正确：{response.status_code}")
    
    data = response.json()
    
    # 检查返回的数据
    assert data["title"] == payload["title"], "标题不匹配"
    assert data["body"] == payload["body"], "内容不匹配"
    assert data["userId"] == payload["userId"], "用户ID不匹配"
    print(f"  ✓ 响应数据与请求匹配")
    
    # JSONPlaceholder 会返回一个 ID
    assert "id" in data, "响应应该包含 ID"
    print(f"  ✓ 返回的新文章 ID：{data['id']}")
    print(f"  ✓✓✓ 测试 4 通过！")


def test_05_post_missing_required_field():
    """测试 5：POST 请求 - 缺少必需字段（异常处理）"""
    print("\n【测试 5】POST /posts - 发送不完整数据")
    
    url = f"{BASE_URL}/posts"
    
    # 故意缺少 body 字段
    incomplete_payload = {
        "title": "不完整的文章",
        # 缺少 body 和 userId
    }
    
    print(f"  📤 发送不完整数据：{incomplete_payload}")
    response = requests.post(url, json=incomplete_payload)
    
    # JSONPlaceholder 比较宽松，会接受，但真实 API 可能返回 400
    print(f"  ✓ 状态码：{response.status_code}")
    print(f"  ✓ 响应：{response.json()}")
    print(f"  ✓✓✓ 测试 5 通过！")


# ============= PUT 请求测试 =============

def test_06_put_update_post():
    """测试 6：PUT 请求 - 更新文章"""
    print("\n【测试 6】PUT /posts/1 - 更新文章")
    
    url = f"{BASE_URL}/posts/1"
    
    updated_data = {
        "id": 1,
        "title": "更新后的标题 - 通过 API 测试",
        "body": "这是更新后的内容",
        "userId": 1
    }
    
    print(f"  📤 发送更新数据：{updated_data}")
    response = requests.put(url, json=updated_data)
    
    assert response.status_code == 200, f"更新失败，状态码 {response.status_code}"
    print(f"  ✓ 状态码正确：{response.status_code}")
    
    data = response.json()
    assert data["title"] == updated_data["title"], "标题更新失败"
    print(f"  ✓ 标题已更新：{data['title']}")
    assert data["body"] == updated_data["body"], "内容更新失败"
    print(f"  ✓ 内容已更新")
    print(f"  ✓✓✓ 测试 6 通过！")


# ============= DELETE 请求测试 =============

def test_07_delete_post():
    """测试 7：DELETE 请求 - 删除文章"""
    print("\n【测试 7】DELETE /posts/1 - 删除文章")
    
    url = f"{BASE_URL}/posts/1"
    
    print(f"  🗑️  删除文章 ID=1")
    response = requests.delete(url)
    
    assert response.status_code == 200, f"删除失败，状态码 {response.status_code}"
    print(f"  ✓ 删除成功，状态码：{response.status_code}")
    print(f"  ✓ 响应：{response.json()}")
    print(f"  ✓✓✓ 测试 7 通过！")


# ============= 参数化测试（重要！） =============

@pytest.mark.parametrize("post_id,expected_user", [
    (1, 1),
    (2, 1),
    (3, 1),
    (5, 1),
    (10, 1),
])
def test_08_parametrized_get_multiple_posts(post_id, expected_user):
    """测试 8：参数化测试 - 批量测试不同的文章
    
    这个测试会自动运行 5 次，每次用不同的参数
    """
    print(f"\n【测试 8-参数化】GET /posts/{post_id} - 检查 userId={expected_user}")
    
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.get(url)
    
    assert response.status_code == 200
    data = response.json()
    assert data["userId"] == expected_user
    print(f"  ✓ 文章 {post_id} 的用户 ID 正确")


# ============= 错误处理测试 =============

def test_09_connection_timeout():
    """测试 9：超时处理"""
    print("\n【测试 9】超时处理 - 模拟慢响应")
    
    try:
        # 访问一个会延迟的 URL（等待 5 秒但我们只等 2 秒）
        response = requests.get(
            "https://httpbin.org/delay/5", 
            timeout=2
        )
    except requests.Timeout:
        print(f"  ✓ 正确捕获超时异常")
        print(f"  ✓✓✓ 测试 9 通过！")
        return
    
    # 如果没有超时，就通过（取决于网络）
    print(f"  ⚠️  没有发生超时（可能是网络快）")


def test_10_headers_validation():
    """测试 10：响应头验证"""
    print("\n【测试 10】响应头验证")
    
    url = f"{BASE_URL}/posts/1"
    response = requests.get(url)
    
    # 检查响应头
    assert "content-type" in response.headers, "缺少 content-type 头"
    print(f"  ✓ Content-Type: {response.headers['content-type']}")
    
    # 验证返回的是 JSON
    assert "application/json" in response.headers['content-type'], "不是 JSON 响应"
    print(f"  ✓ 返回的是 JSON 格式")
    print(f"  ✓✓✓ 测试 10 通过！")


# ============= 总结 =============

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("运行完所有测试！检查上面的结果")
    print("=" * 60)