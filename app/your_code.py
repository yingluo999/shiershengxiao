"""
十二生肖注册机器人 - 核心逻辑
"""
import requests
import random
import string
import time
import re
import os
from typing import Optional, Tuple, List
from urllib.parse import quote


class ZodiacBot:
    def __init__(self, base_url: str = "http://app.wanshengxiao.cn"):
        self.base_url = base_url
        self.session = None
        self.ua = None  # 在Android上简化为随机UA
    
    def get_random_ua(self) -> str:
        """获取随机UA"""
        uas = [
            'Mozilla/5.0 (Linux; Android 15; V2425A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.159 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7128.145 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.6549.124 Mobile Safari/537.36',
        ]
        return random.choice(uas)
    
    def create_session(self):
        """创建新会话"""
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/sx/app.html',
        })
        session.headers['User-Agent'] = self.get_random_ua()
        return session
    
    def generate_realistic_phone(self) -> str:
        """生成真实手机号"""
        cmcc = ['134','135','136','137','138','139','147','148','150','151','152',
                '157','158','159','172','178','182','183','184','187','188','195','197','198']
        cucc = ['130','131','132','145','146','155','156','166','167','175','176','185','186','196']
        ctcc = ['133','149','153','162','173','174','177','180','181','189','191','193','199']
        virtual = ['170','171']
        all_prefixes = cmcc * 5 + cucc * 3 + ctcc * 2 + virtual
        
        for _ in range(10):
            prefix = random.choice(all_prefixes)
            suffix = ''.join(random.choices(string.digits, k=8))
            phone = prefix + suffix
            if not any(p in phone for p in ['123456', '111111', '000000', '888888']):
                return phone
        return '138' + ''.join(random.choices(string.digits, k=8))
    
    def generate_password(self) -> str:
        """生成8-12位密码"""
        length = random.randint(8, 12)
        letters = string.ascii_letters
        digits = string.digits
        all_chars = letters + digits
        
        password = []
        password.append(random.choice(letters))
        password.append(random.choice(digits))
        
        for _ in range(length - 2):
            password.append(random.choice(all_chars))
        
        random.shuffle(password)
        return ''.join(password)
    
    def generate_realname(self) -> str:
        """生成随机中文姓名"""
        surnames = ['王', '李', '张', '刘', '陈', '杨', '黄', '赵', '吴', '周', '徐', '孙', '马', '朱', '胡', 
                    '郭', '林', '何', '高', '罗', '郑', '梁', '谢', '宋', '唐', '许', '韩', '冯', '邓', '曹',
                    '彭', '曾', '萧', '田', '董', '潘', '袁', '蔡', '蒋', '余', '于', '叶', '杜', '苏', '魏',
                    '吕', '丁', '任', '姚', '沈', '卢', '姜', '崔', '钟', '谭', '陆', '汪', '范', '金', '石']
        
        given_names = ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '洋', '勇', '艳', '杰', '倩', '涛', '明',
                      '超', '秀英', '华', '慧', '建', '文', '平', '刚', '桂英', '志强', '秀兰', '建国', '建军',
                      '浩', '然', '宇', '轩', '瑞', '晨', '曦', '瑶', '琪', '琳', '博', '文', '昊', '天', '奕',
                      '辰', '悦', '彤', '萱', '怡', '宁', '欣', '萌', '雨', '桐', '梓', '涵', '若', '溪', '乐',
                      '瑶', '馨', '宁', '宜', '彦', '良', '淑', '珍', '金', '凤', '玉', '兰', '秀', '英', '云']
        
        surname = random.choice(surnames)
        if random.random() > 0.3:
            given = random.choice(given_names)
        else:
            given = random.choice(given_names) + random.choice(given_names)
        
        return surname + given
    
    def get_sms_code(self, session: requests.Session, phone: str) -> Optional[str]:
        """获取短信验证码"""
        print(f"📱 验证手机: {phone}")
        
        # 模拟数学验证
        ops = ['+', '-', '×']
        op = random.choice(ops)
        if op == '+':
            n1, n2 = random.randint(1, 9), random.randint(1, 9)
            ans = n1 + n2
            print(f"🧮 数学验证: {n1} + {n2} = ? → {ans}")
        elif op == '-':
            n1 = random.randint(5, 10)
            n2 = random.randint(1, n1 - 1)
            ans = n1 - n2
            print(f"🧮 数学验证: {n1} - {n2} = ? → {ans}")
        else:
            n1, n2 = random.randint(1, 5), random.randint(1, 5)
            ans = n1 * n2
            print(f"🧮 数学验证: {n1} × {n2} = ? → {ans}")
        
        time.sleep(random.uniform(0.3, 0.8))
        
        # 模拟图形验证码
        img_code = ''.join(random.choices(string.digits, k=4))
        print(f"🖼️  图形验证码: {img_code}")
        time.sleep(random.uniform(0.3, 0.8))
        
        # 发送短信
        url = f"{self.base_url}/user/reg_sms"
        data = {'phone': phone}
        time.sleep(random.uniform(0.5, 1.0))
        
        try:
            response = session.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 1:
                    code_match = re.search(r'\b(\d{6})\b', result.get('info', ''))
                    if code_match:
                        sms_code = code_match.group(1)
                        print(f"✅ 验证码: {sms_code}")
                        return sms_code
            return None
        except Exception as e:
            print(f"❌ 异常: {e}")
            return None
    
    def register_account(self, phone: str, password: str, realname: str, ref_code: str = "125872") -> Tuple[bool, str]:
        """注册账号"""
        session = self.create_session()
        
        sms_code = self.get_sms_code(session, phone)
        if not sms_code:
            return False, "获取验证码失败"
        
        url = f"{self.base_url}/user/reg"
        data = {
            'username': phone,
            'pwd': password,
            'realname': realname,
            'phone_code': sms_code,
            'ref': ref_code
        }
        
        time.sleep(random.uniform(0.3, 0.8))
        
        try:
            response = session.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 1:
                    return True, f"注册成功: {phone}"
                else:
                    return False, result.get('info', '未知错误')
            return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def login(self, phone: str, password: str) -> Tuple[bool, requests.Session, str]:
        """登录账号"""
        session = self.create_session()
        url = f"{self.base_url}/user/login"
        data = {'username': phone, 'pwd': password}
        
        try:
            response = session.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 1:
                    return True, session, "登录成功"
                else:
                    return False, session, result.get('info', '登录失败')
            return False, session, f"HTTP {response.status_code}"
        except Exception as e:
            return False, session, str(e)
    
    def bind_alipay(self, session: requests.Session, realname: str, alipay: str) -> Tuple[bool, str]:
        """绑定支付宝"""
        url = f"{self.base_url}/user/info"
        
        data = {
            'realname': realname,
            'alipay': alipay,
            'type': 'alipay'
        }
        
        session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Referer': f'{self.base_url}/user/info',
            'Upgrade-Insecure-Requests': '1',
        })
        
        try:
            response = session.post(url, data=data, timeout=10)
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status') == 1:
                        return True, "绑定成功"
                    else:
                        return False, result.get('info', '绑定失败')
                except:
                    html = response.text
                    if '修改成功' in html or '成功' in html:
                        return True, "绑定成功"
                    else:
                        return False, "绑定失败"
            return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def logout(self, session: requests.Session) -> Tuple[bool, str]:
        """退出登录"""
        if not session:
            return False, "没有登录会话"
        
        url = f"{self.base_url}/user/logout.html"
        
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Referer': f'{self.base_url}/index/index.html',
            'Upgrade-Insecure-Requests': '1',
        })
        
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status') == 1:
                        return True, "退出成功"
                    else:
                        return False, result.get('info', '退出失败')
                except:
                    html = response.text
                    if '退出成功' in html:
                        return True, "退出成功"
                    else:
                        return False, "退出失败"
            return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def register_one(self, ref_code: str = "125872") -> Tuple[bool, dict]:
        """
        注册一个账号
        返回: (是否成功, 账号信息字典)
        """
        phone = self.generate_realistic_phone()
        password = self.generate_password()
        realname = self.generate_realname()
        alipay = phone
        
        account_info = {
            'phone': phone,
            'password': password,
            'realname': realname,
            'alipay': alipay
        }
        
        # 注册
        success, msg = self.register_account(phone, password, realname, ref_code)
        if not success:
            account_info['status'] = 'failed'
            account_info['message'] = f'注册失败: {msg}'
            return False, account_info
        account_info['status'] = 'registered'
        account_info['message'] = msg
        
        # 登录
        success, session, msg = self.login(phone, password)
        if not success:
            account_info['status'] = 'login_failed'
            account_info['message'] = f'注册成功，登录失败: {msg}'
            return True, account_info
        
        # 绑定支付宝
        success, msg = self.bind_alipay(session, realname, alipay)
        if success:
            account_info['alipay_status'] = 'bound'
            account_info['message'] = f'注册成功，已绑定支付宝'
        else:
            account_info['alipay_status'] = 'bind_failed'
            account_info['message'] = f'注册成功，绑定支付宝失败: {msg}'
        
        # 退出登录
        self.logout(session)
        
        return True, account_info


def run(args: list = None):
    """
    入口函数 - APP会调用这个函数
    
    参数:
        args: 用户输入的内容
              例如输入 "5 125872" -> args = ["5", "125872"]
    
    返回:
        字符串，会显示在界面上
    """
    # 解析参数
    count = 1
    ref_code = "125872"
    
    if args and len(args) > 0:
        try:
            count = int(args[0])
            if count <= 0:
                count = 1
        except:
            pass
        
        if len(args) > 1:
            ref_code = args[1]
    
    bot = ZodiacBot()
    results = []
    success_count = 0
    fail_count = 0
    
    results.append(f"🐉 十二生肖注册机器人")
    results.append(f"推荐码: {ref_code}")
    results.append(f"计划注册: {count} 个账号")
    results.append("=" * 40)
    
    for i in range(count):
        results.append(f"\n▶ 第 {i+1}/{count} 个账号")
        
        success, info = bot.register_one(ref_code)
        
        if success:
            success_count += 1
            results.append(f"✅ 手机: {info['phone']}")
            results.append(f"   密码: {info['password']}")
            results.append(f"   姓名: {info['realname']}")
            results.append(f"   状态: {info.get('message', '成功')}")
        else:
            fail_count += 1
            results.append(f"❌ 失败: {info.get('message', '未知错误')}")
        
        # 间隔
        if i < count - 1:
            delay = random.uniform(2, 5)
            results.append(f"⏳ 等待 {delay:.1f} 秒...")
            time.sleep(delay)
    
    results.append("\n" + "=" * 40)
    results.append(f"📊 统计: 成功 {success_count} 个，失败 {fail_count} 个")
    results.append("=" * 40)
    
    return "\n".join(results)


# 测试用
if __name__ == "__main__":
    print(run(["2"]))
