import unittest
import threading
import time
import re
from selenium import webdriver
from app import create_app, db
from app.models import User, Role, Post


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # запуск Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        try:
            cls.client = webdriver.Chrome(chrome_options=options)
        except:
            pass
        
        # пропустить следующие тесты, если браузер не запустился
        if cls.client:
            # создать приложение
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # подавить вывод сообщений, чтобы очистить
            # вывод от лишнего мусора
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # создать базу данных и наполнить её фиктивными данными
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            # создать учётную запись администратора
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com', name='john', password='cat',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # запустить сервер Flask в отдельном потоке
            cls.server_thread = threading.Thread(target=cls.app.run,
                                                 kwargs={'debug': False})
            cls.server_thread.start()
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # остановить сервер и закрыть браузер
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            # уничтожить базу данных
            db.drop_all()
            db.session.remove()

            # удалить контекст приложения
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # перейти на главную страницу
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger!', self.client.page_source))

        # перейти на страницу аутентификации
        self.client.find_element_by_link_text('Log In').click()
        self.assertTrue('<h1>Login<h1>' in self.client.page_source)

        # выполнить аутентификацию
        self.client.find_element_by_name('email').send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+john', self.client.page_source))

        # перейти на страницу профиля пользователя
        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>john</h1>' in self.client.page_source)