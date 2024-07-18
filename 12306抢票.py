from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import easygui as g
from selenium.webdriver.support.ui import Select
from lxml import etree
from tkinter import *
import tkinter
import re


class Qp(object):
    def __init__(self):
        #chromedriver对应chrome版本是126.0.6478.63
        self.driver = webdriver.Chrome(executable_path='chromedriver-win64/chromedriver.exe')


    def input(self):
        """
        利用tkinter实现用户界面信息输入
        :return: None
        """
        global root
        global entryName1
        global entryName2
        global entryName3
        global entryName4
        global entryName5
        global entryName6
        root = tkinter.Tk()
        root.geometry("400x380+418+117")
        root.title("车票信息")
        labelName1 = Label(root, text='出发地:', justify=RIGHT, anchor='e', font=("黑体", 15))
        labelName1.place(x=50, y=60, width=120, height=20)
        varName1 = StringVar(root, value='')
        entryName1 = Entry(root, width=80, textvariable=varName1)
        entryName1.place(x=180, y=60, width=100, height=20)
        labelName2 = Label(root, text='目的地:', justify=RIGHT, anchor='e', font=("黑体", 15))
        labelName2.place(x=50, y=100, width=120, height=20)
        varName2 = StringVar(root, value='')
        entryName2 = Entry(root, width=80, textvariable=varName2)
        entryName2.place(x=180, y=100, width=100, height=20)
        labelName3 = Label(root, text='出发日期:', justify=RIGHT, anchor='e', font=("黑体", 15))
        labelName3.place(x=50, y=140, width=120, height=20)
        varName3 = StringVar(root, value='')
        entryName3 = Entry(root, width=80, textvariable=varName3)
        entryName3.place(x=180, y=140, width=100, height=20)
        labelName4 = Label(root, text='座位类型:', justify=RIGHT, anchor='e', font=("黑体", 15))
        labelName4.place(x=50, y=180, width=120, height=20)
        varName4 = StringVar(root, value='')
        entryName4 = Entry(root, width=80, textvariable=varName4)
        entryName4.place(x=180, y=180, width=100, height=20)
        labelName5 = Label(root, text='车票类型:', justify=RIGHT, anchor='e', font=("黑体", 15))
        labelName5.place(x=50, y=220, width=120, height=20)
        varName5 = StringVar(root, value='')
        entryName5 = Entry(root, width=80, textvariable=varName5)
        entryName5.place(x=180, y=220, width=100, height=20)
        labelName6 = Label(root, text='乘车人姓名:', justify=RIGHT, anchor='e', font=("黑体", 15))
        labelName6.place(x=50, y=260, width=120, height=20)
        varName6 = StringVar(root, value='')
        entryName6 = Entry(root, width=80, textvariable=varName6)
        entryName6.place(x=180, y=260, width=100, height=20)
        buttonOk = Button(root, text='确定', font=("黑体", 15), command=self.click_)
        buttonOk.place(x=140, y=300, width=50, height=25)
        root.mainloop()

    def click_(self):
        """
        进入官网，等待信息输入
        :return: None
        """
        #获取用户信息
        self.depart = entryName1.get()
        self.goal = entryName2.get()
        self.time_ = entryName3.get()
        self.sit = entryName4.get()
        self.type_ = entryName5.get()
        self.car_person = entryName6.get()
        # 关闭界面
        root.destroy()
        self.driver.get('https://www.12306.cn/index/index.html')
        #出发地
        tag1 = self.driver.find_element_by_id('fromStationText')
        tag1.clear()
        #目的地
        tag2 = self.driver.find_element_by_id('toStationText')
        tag2.clear()
        #出发时间
        tag3 = self.driver.find_element_by_id('train_date')
        tag3.clear()
        but3 = self.driver.find_element_by_id('search_one')
        button = ActionChains(self.driver)
        button.move_to_element(tag3).send_keys_to_element(tag3, self.time_)
        button.move_to_element(tag1)
        button.send_keys_to_element(tag1, self.depart)
        button.perform()
        tag_1 = self.driver.find_element_by_id('citem_0')
        #模拟用户点击，实例化一个行为链
        ActionChains(self.driver).move_to_element(tag_1).click(tag_1).perform()
        ActionChains(self.driver).move_to_element(tag2).send_keys_to_element(tag2, self.goal).perform()
        tag_2 = self.driver.find_element_by_id('citem_0')  # 不能用tag_1，id还未加载更新
        ActionChains(self.driver).move_to_element(tag_2).click(tag_2).perform()
        if self.type_ == '学生票':
            ActionChains(self.driver).move_to_element(self.driver.find_element_by_id('isStudentDan')).click().perform()
        time.sleep(1)
        ActionChains(self.driver).move_to_element(but3).click(but3).perform()
        self.buy()

    def buy(self):
        """
        购票页面
        :return: None
        """
        self.driver.switch_to_window(self.driver.window_handles[1])
        car_sit ,car_id,judge_sit  = 0,0,0
        if self.sit == '二等座':
            self.sit = "O"
            car_sit = 5
        if self.sit == '一等座':
            self.sit = "M"
            car_sit = 4
        if self.sit == '商务座':
            self.sit = "9"
            car_sit = 2
        if self.sit == '软卧':
            self.sit = '4'
            car_sit = 7
        if self.sit == '硬卧':
            self.sit = '3'
            car_sit = 8
        if self.sit == '硬座':
            self.sit = '1'
            car_sit = 10
        if self.sit == '软座':
            self.sit = '2'
            car_sit = 9
        while True:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "query_ticket"))
            )
            query_button = self.driver.find_element_by_id('query_ticket')#查询按钮
            self.driver.execute_script("arguments[0].click()", query_button)
            # query_button.click()#可能会出现不能点击问题
            self.driver.switch_to_window(self.driver.window_handles[1])
            book = self.driver.find_elements_by_class_name('btn72')#预定按钮
            if book[0].text != '预订':#车票未开售
                time.sleep(1)
                self.driver.refresh()
            else:#开售后取最近一趟列车
                for i in range(len(book)):
                    car_id = re.findall(r'span id="(.*?)"',
                        self.driver.find_element_by_xpath(r'//*[@class="train"]').get_attribute('innerHTML')
                    ,re.S)[0] #会获取标签之间的完整 html
                    judge_sit = self.driver.find_element_by_xpath('//*[@id='+'"'+"ticket_"+str(car_id)[0:18:]+'"'+']/td[' + str(car_sit) + ']')

                    if judge_sit.text != '--':#判断是否有座位
                        book[i].click()
                        WebDriverWait(self.driver,1000).until(
                            EC.presence_of_element_located((By.ID,'submitOrder_id'))
                        )#等待扫码登录
                        self.buy_detail()
                        break

                    else:
                        g.msgbox('无座了','提示')
                break
        time.sleep(30)#买票时间
        self.driver.quit()





    def buy_detail(self):
        """
        购票界面的一些相关信息填写
        :return:None
        """
        self.driver.switch_to_window(self.driver.window_handles[1])
        sel_but1 = Select(self.driver.find_element_by_id('ticketType_1'))
        sel_but1.select_by_visible_text(self.type_)
        sel_but2 = Select(self.driver.find_element_by_id('seatType_1'))
        sel_but2.select_by_value(self.sit)
        sel = self.driver.page_source
        txt = etree.HTML(sel)
        txt = txt.xpath('//*[@id="normal_passenger_id"]')
        j, ID = 1, 0
        for i in txt:
            if i.xpath('./li[' + str(j) + ']/label/text()')[0] == self.car_person:
                break
            j += 1
        for k in range(0, j):
            ID = 'normalPassenger_' + str(k)
        buton = self.driver.find_element_by_id(ID)
        buton.click()
        payment = self.driver.find_element_by_id('submitOrder_id')
        payment.click()


    def run(self):
        self.input()#输入界面操作


if __name__ == '__main__':
    p = Qp()
    p.run()
