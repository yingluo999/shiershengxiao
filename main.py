# -*- coding: utf-8 -*-
"""
十二生肖注册机器人 - GUI界面
"""
import os
import threading
import time
import random
import json
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.logger import Logger

from app.your_code import ZodiacBot

# ========== 字体设置 ==========
def setup_fonts():
    """设置中文字体"""
    font_paths = [
        '/system/fonts/NotoSansCJK-Regular.ttc',
        '/system/fonts/NotoSansSC-Regular.otf',
        '/system/fonts/DroidSansFallback.ttf',
        '/system/fonts/Roboto-Regular.ttf',
    ]
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='ChineseFont', fn_regular=font_path)
                return 'ChineseFont'
            except:
                continue
    return 'Roboto'

DEFAULT_FONT = setup_fonts()

# 颜色主题
COLORS = {
    'bg': get_color_from_hex('#1a1a2e'),
    'card': get_color_from_hex('#16213e'),
    'primary': get_color_from_hex('#e94560'),
    'secondary': get_color_from_hex('#0f3460'),
    'text': get_color_from_hex('#eaeaea'),
    'success': get_color_from_hex('#4ecca3'),
    'error': get_color_from_hex('#ff6b6b'),
    'warning': get_color_from_hex('#ffd93d'),
}


class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = COLORS['card']
        self.foreground_color = COLORS['text']
        self.cursor_color = COLORS['primary']
        if DEFAULT_FONT:
            self.font_name = DEFAULT_FONT
        self.font_size = dp(14)


class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        if DEFAULT_FONT:
            self.font_name = DEFAULT_FONT
        self.font_size = dp(14)


class StyledLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if DEFAULT_FONT:
            self.font_name = DEFAULT_FONT
        self.font_size = dp(14)


class ZodiacApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_running = False
        self.should_stop = False
        self.data_dir = None
        self.accounts_file = None
        self.saved_accounts = []

    def build(self):
        self.title = '十二生肖注册机器人'
        Window.clearcolor = COLORS['bg']

        # 初始化存储
        self.init_storage()

        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 标题
        title = StyledLabel(
            text='注册机器人',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(22),
            bold=True,
            color=COLORS['primary']
        )
        main_layout.add_widget(title)

        # 存储路径显示
        self.path_label = StyledLabel(
            text=f'保存路径: {self.data_dir if self.data_dir else "获取中..."}',
            size_hint_y=None,
            height=dp(25),
            font_size=dp(10),
            color=COLORS['warning']
        )
        main_layout.add_widget(self.path_label)

        # 输入区域
        input_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), spacing=5)

        # 数量输入行
        count_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=10)
        count_label = StyledLabel(text='数量:', size_hint_x=0.2, halign='right')
        count_box.add_widget(count_label)

        self.count_input = StyledTextInput(
            text='1',
            multiline=False,
            size_hint_x=0.3,
            hint_text='输入数量'
        )
        count_box.add_widget(self.count_input)
        count_box.add_widget(Label())
        input_box.add_widget(count_box)

        # 推荐码输入行
        ref_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=10)
        ref_label = StyledLabel(text='推荐码:', size_hint_x=0.2, halign='right')
        ref_box.add_widget(ref_label)

        self.ref_input = StyledTextInput(
            text='125872',
            multiline=False,
            size_hint_x=0.3,
            hint_text='输入推荐码'
        )
        ref_box.add_widget(self.ref_input)
        ref_box.add_widget(Label())
        input_box.add_widget(ref_box)

        main_layout.add_widget(input_box)

        # 按钮区域
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=10)

        self.start_btn = StyledButton(
            text='开始注册',
            background_color=COLORS['primary']
        )
        self.start_btn.bind(on_press=self.start_register)
        btn_layout.add_widget(self.start_btn)

        self.stop_btn = StyledButton(
            text='停止',
            background_color=COLORS['error'],
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_register)
        btn_layout.add_widget(self.stop_btn)

        main_layout.add_widget(btn_layout)

        # 日志区域
        status_label = StyledLabel(
            text='运行日志',
            size_hint_y=None,
            height=dp(30),
            bold=True
        )
        main_layout.add_widget(status_label)

        log_scroll = ScrollView(size_hint_y=0.55)
        self.log_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=2)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        log_scroll.add_widget(self.log_layout)
        main_layout.add_widget(log_scroll)

        # 底部提示
        footer = StyledLabel(
            text='提示: 注册过程需要1-3分钟，请耐心等待',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(12),
            color=COLORS['warning']
        )
        main_layout.add_widget(footer)

        Clock.schedule_once(self.init_logs, 0.5)
        return main_layout

    # ==================== 存储 ====================
    def init_storage(self):
        """初始化存储（请求权限 + 创建目录）"""
        try:
            # 请求权限
            self.request_permissions()

            # 获取存储路径
            self.data_dir = self.get_storage_path()
            self.accounts_file = os.path.join(self.data_dir, 'accounts.json')

            # 加载已保存的账号
            self.load_saved_accounts()

            Logger.info(f'存储目录: {self.data_dir}')
        except Exception as e:
            Logger.error(f'存储初始化失败: {e}')
            # 降级到应用私有目录
            self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
            self.accounts_file = os.path.join(self.data_dir, 'accounts.json')

    def request_permissions(self):
        """请求存储权限"""
        try:
            from android.permissions import request_permissions, Permission
            from android import activity
            
            permissions = [
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE,
            ]
            
            # 请求权限（会弹出系统对话框）
            request_permissions(permissions)
            
            Logger.info('权限请求已发送')
        except Exception as e:
            Logger.warning(f'权限请求失败: {e}')

    def get_storage_path(self) -> str:
        """获取外部存储路径"""
        try:
            from android.storage import primary_external_storage_path
            sdcard = primary_external_storage_path()
        except:
            sdcard = '/storage/emulated/0/'

        # 创建应用专属目录
        app_dir = os.path.join(sdcard, 'ZodiacRegister')
        if not os.path.exists(app_dir):
            os.makedirs(app_dir, exist_ok=True)

        # 测试写入权限
        test_file = os.path.join(app_dir, '.write_test')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            Logger.info(f'写入权限正常: {app_dir}')
        except Exception as e:
            Logger.warning(f'写入权限异常: {e}')
            # 降级到应用私有目录
            app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            if not os.path.exists(app_dir):
                os.makedirs(app_dir, exist_ok=True)

        return app_dir

    def load_saved_accounts(self):
        """加载已保存的账号"""
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    self.saved_accounts = json.load(f)
                    Logger.info(f'加载了 {len(self.saved_accounts)} 个已保存账号')
                    self.add_log(f'📂 已加载 {len(self.saved_accounts)} 个历史账号')
            else:
                self.saved_accounts = []
        except Exception as e:
            Logger.warning(f'加载账号失败: {e}')
            self.saved_accounts = []

    def save_account(self, account_info):
        """保存单个账号到文件"""
        try:
            # 检查是否已存在
            for i, acc in enumerate(self.saved_accounts):
                if acc.get('phone') == account_info.get('phone'):
                    self.saved_accounts[i] = account_info
                    break
            else:
                self.saved_accounts.append(account_info)

            # 写入文件
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(self.saved_accounts, f, ensure_ascii=False, indent=2)

            Logger.info(f'账号已保存: {account_info.get("phone")}')
            return True
        except Exception as e:
            Logger.error(f'保存账号失败: {e}')
            return False

    # ==================== UI ====================
    def init_logs(self, dt):
        self.add_log('程序已启动')
        self.add_log(f'存储路径: {self.data_dir}')
        self.add_log('等待开始注册...')

    @mainthread
    def add_log(self, text):
        timestamp = datetime.now().strftime('%H:%M:%S')

        if '✅' in text:
            color = COLORS['success']
        elif '❌' in text:
            color = COLORS['error']
        elif '⏳' in text or '等待' in text:
            color = COLORS['warning']
        else:
            color = COLORS['text']

        label = StyledLabel(
            text=f'[{timestamp}] {text}',
            size_hint_y=None,
            height=dp(22),
            color=color,
            halign='left',
            valign='middle',
            text_size=(Window.width - 40, dp(22))
        )
        self.log_layout.add_widget(label)
        Clock.schedule_once(self.scroll_to_bottom, 0.1)

    def scroll_to_bottom(self, dt):
        parent = self.log_layout.parent
        if parent and hasattr(parent, 'scroll_y'):
            parent.scroll_y = 0

    def clear_logs(self):
        self.log_layout.clear_widgets()

    # ==================== 注册 ====================
    def start_register(self, instance):
        if self.is_running:
            return

        try:
            count = int(self.count_input.text.strip())
            if count <= 0:
                count = 1
                self.count_input.text = '1'
        except:
            count = 1
            self.count_input.text = '1'

        ref_code = self.ref_input.text.strip() or '125872'

        self.clear_logs()
        self.add_log(f'开始注册 {count} 个账号')
        self.add_log(f'推荐码: {ref_code}')
        self.add_log('-' * 30)

        self.start_btn.disabled = True
        self.start_btn.text = '注册中...'
        self.stop_btn.disabled = False
        self.is_running = True
        self.should_stop = False

        threading.Thread(
            target=self.do_register,
            args=(count, ref_code),
            daemon=True
        ).start()

    def do_register(self, count, ref_code):
        bot = ZodiacBot()
        success_count = 0
        fail_count = 0

        for i in range(count):
            if self.should_stop:
                self.add_log('已停止')
                break

            self.add_log('')
            self.add_log(f'第 {i+1}/{count} 个账号')

            try:
                success, info = bot.register_one(ref_code)

                if success:
                    success_count += 1
                    info['register_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    if self.save_account(info):
                        self.add_log('💾 已保存到文件')

                    self.add_log(f'✅ 手机: {info["phone"]}')
                    self.add_log(f'   密码: {info["password"]}')
                    self.add_log(f'   姓名: {info["realname"]}')
                    self.add_log(f'   状态: {info.get("message", "成功")}')
                else:
                    fail_count += 1
                    self.add_log(f'❌ 失败: {info.get("message", "未知错误")}')
            except Exception as e:
                fail_count += 1
                self.add_log(f'❌ 异常: {str(e)}')

            if self.should_stop:
                break

            if i < count - 1:
                delay = random.uniform(2, 5)
                self.add_log(f'⏳ 等待 {delay:.1f} 秒...')
                time.sleep(delay)

        self.add_log('')
        self.add_log('-' * 30)
        self.add_log(f'统计: 成功 {success_count} 个，失败 {fail_count} 个')
        self.add_log(f'总计: {len(self.saved_accounts)} 个账号')
        self.add_log(f'保存路径: {self.accounts_file}')
        self.add_log('-' * 30)

        if not self.should_stop:
            self.add_log('✅ 注册完成！')

        Clock.schedule_once(self.enable_buttons, 0)

    def enable_buttons(self, dt):
        self.start_btn.disabled = False
        self.start_btn.text = '开始注册'
        self.stop_btn.disabled = True
        self.is_running = False
        self.should_stop = False

    def stop_register(self, instance):
        self.should_stop = True
        self.is_running = False
        self.add_log('正在停止...')
        self.stop_btn.disabled = True


if __name__ == '__main__':
    ZodiacApp().run()
