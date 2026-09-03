# -*- coding: utf-8 -*-
"""
十二生肖注册机器人 - GUI界面（稳定版）
"""
import os
import threading
import time
import random
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

# 导入注册逻辑
from app.your_code import ZodiacBot

# ========== 字体设置 ==========
def setup_fonts():
    """设置中文字体"""
    font_paths = [
        '/system/fonts/NotoSansCJK-Regular.ttc',
        '/system/fonts/NotoSansSC-Regular.otf',
        '/system/fonts/DroidSansFallback.ttf',
        '/system/fonts/Roboto-Regular.ttf',
        './fonts/NotoSansSC-Regular.ttf',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='ChineseFont', fn_regular=font_path)
                Logger.info('找到字体: {}'.format(font_path))
                return 'ChineseFont'
            except:
                continue
    
    Logger.warning('未找到中文字体，使用默认字体')
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
    """自定义输入框"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = COLORS['card']
        self.foreground_color = COLORS['text']
        self.cursor_color = COLORS['primary']
        if DEFAULT_FONT:
            self.font_name = DEFAULT_FONT
        self.font_size = dp(14)


class StyledButton(Button):
    """自定义按钮"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        if DEFAULT_FONT:
            self.font_name = DEFAULT_FONT
        self.font_size = dp(14)


class StyledLabel(Label):
    """自定义标签"""
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
        
    def build(self):
        self.title = '十二生肖注册机器人'
        Window.clearcolor = COLORS['bg']
        
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
        count_box.add_widget(Label())  # 占位
        
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
        ref_box.add_widget(Label())  # 占位
        
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
        
        # 状态显示
        status_label = StyledLabel(
            text='运行日志',
            size_hint_y=None,
            height=dp(30),
            bold=True
        )
        main_layout.add_widget(status_label)
        
        # 日志显示区域
        log_scroll = ScrollView(size_hint_y=0.6)
        self.log_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=2)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        log_scroll.add_widget(self.log_layout)
        main_layout.add_widget(log_scroll)
        
        # 底部信息
        footer = StyledLabel(
            text='提示: 注册过程需要1-3分钟，请耐心等待',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(12),
            color=COLORS['warning']
        )
        main_layout.add_widget(footer)
        
        # 初始化日志
        Clock.schedule_once(self.init_logs, 0.5)
        
        return main_layout
    
    def init_logs(self, dt):
        """初始化日志"""
        self.add_log('程序已启动')
        self.add_log('等待开始注册...')
    
    @mainthread
    def add_log(self, text):
        """添加日志 - 在主线程执行"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # 根据内容设置颜色
        if '✅' in text:
            color = COLORS['success']
        elif '❌' in text:
            color = COLORS['error']
        elif '⏳' in text or '等待' in text:
            color = COLORS['warning']
        else:
            color = COLORS['text']
        
        label = StyledLabel(
            text='[{}] {}'.format(timestamp, text),
            size_hint_y=None,
            height=dp(22),
            color=color,
            halign='left',
            valign='middle',
            text_size=(Window.width - 40, dp(22))
        )
        self.log_layout.add_widget(label)
        
        # 滚动到底部
        Clock.schedule_once(self.scroll_to_bottom, 0.1)
    
    def scroll_to_bottom(self, dt):
        """滚动到最底部"""
        parent = self.log_layout.parent
        if parent and hasattr(parent, 'scroll_y'):
            parent.scroll_y = 0
    
    def clear_logs(self):
        """清空日志"""
        self.log_layout.clear_widgets()
    
    def start_register(self, instance):
        """开始注册"""
        if self.is_running:
            return
        
        # 获取参数
        try:
            count = int(self.count_input.text.strip())
            if count <= 0:
                count = 1
                self.count_input.text = '1'
        except:
            count = 1
            self.count_input.text = '1'
        
        ref_code = self.ref_input.text.strip() or '125872'
        
        # 清空日志
        self.clear_logs()
        self.add_log('开始注册 {} 个账号'.format(count))
        self.add_log('推荐码: {}'.format(ref_code))
        self.add_log('-' * 30)
        
        # 禁用/启用按钮
        self.start_btn.disabled = True
        self.start_btn.text = '注册中...'
        self.stop_btn.disabled = False
        self.is_running = True
        self.should_stop = False
        
        # 在新线程中执行注册
        threading.Thread(
            target=self.do_register, 
            args=(count, ref_code),
            daemon=True
        ).start()
    
    def do_register(self, count, ref_code):
        """执行注册（在后台线程中）"""
        bot = ZodiacBot()
        success_count = 0
        fail_count = 0
        
        for i in range(count):
            # 检查是否应该停止
            if self.should_stop:
                self.add_log('已停止')
                break
            
            self.add_log('')
            self.add_log('第 {}/{} 个账号'.format(i+1, count))
            
            try:
                # 执行注册
                success, info = bot.register_one(ref_code)
                
                if success:
                    success_count += 1
                    self.add_log('✅ 手机: {}'.format(info['phone']))
                    self.add_log('   密码: {}'.format(info['password']))
                    self.add_log('   姓名: {}'.format(info['realname']))
                    self.add_log('   状态: {}'.format(info.get('message', '成功')))
                else:
                    fail_count += 1
                    self.add_log('❌ 失败: {}'.format(info.get('message', '未知错误')))
            except Exception as e:
                fail_count += 1
                self.add_log('❌ 异常: {}'.format(str(e)))
            
            # 检查是否应该停止
            if self.should_stop:
                break
            
            # 间隔
            if i < count - 1:
                delay = random.uniform(2, 5)
                self.add_log('⏳ 等待 {:.1f} 秒...'.format(delay))
                time.sleep(delay)
        
        # 显示统计
        self.add_log('')
        self.add_log('-' * 30)
        self.add_log('统计: 成功 {} 个，失败 {} 个'.format(success_count, fail_count))
        self.add_log('-' * 30)
        
        if not self.should_stop:
            self.add_log('✅ 注册完成！')
        
        # 恢复按钮状态
        Clock.schedule_once(self.enable_buttons, 0)
    
    def enable_buttons(self, dt):
        """恢复按钮状态"""
        self.start_btn.disabled = False
        self.start_btn.text = '开始注册'
        self.stop_btn.disabled = True
        self.is_running = False
        self.should_stop = False
    
    def stop_register(self, instance):
        """停止注册"""
        self.should_stop = True
        self.is_running = False
        self.add_log('正在停止...')
        self.stop_btn.disabled = True


if __name__ == '__main__':
    ZodiacApp().run()
