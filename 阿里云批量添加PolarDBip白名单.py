#!/usr/bin/env python
# coding=utf-8
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QDesktopWidget,QFormLayout,QLineEdit,QMessageBox,QComboBox,QLabel
from PyQt5.QtGui import QFont
import sys
import datetime, urllib.parse, hmac, base64, json ,uuid
import requests

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.data = []
        f = open('./PolarDB.json', 'r',encoding='utf-8')
        self.data = eval(f.read())
        self.initUi(self.data)

    def initUi(self,data):
        size_type = 15
        font_type = '宋体'
        items = []
        for k in data:
            items.append(k['name'])
        self.setWindowTitle('阿里云PolarDB设置IP白名单')
        self.resize(600,400)
        self.center()
        layout = QFormLayout()

        self.combobox = QComboBox()
        self.combobox.addItem('请选择')
        self.combobox.setFont(QFont(font_type, size_type))
        self.combobox.addItems(items)
        self.combobox.currentIndexChanged[int].connect(self.selectionchange)
        self.lab_combobox = QLabel('选项')
        self.lab_combobox.setFont(QFont(font_type,size_type))
        layout.addRow(self.lab_combobox,self.combobox)

        self.IP = QLineEdit()
        self.IP.setFont(QFont(font_type,size_type))
        self.lab_IP = QLabel('IP')
        self.lab_IP.setFont(QFont(font_type,size_type))
        layout.addRow(self.lab_IP, self.IP)
        try:
            self.IP.setText(str(self.get_ip()))

        except:
            self.IP.setPlaceholderText('ip获取失败，请手动输入！！！')

        self.name = QLineEdit()
        self.name.setFont(QFont(font_type, size_type))
        self.lab_name = QLabel('name')
        self.lab_name.setFont(QFont(font_type, size_type))
        layout.addRow(self.lab_name, self.name)
        self.name.setPlaceholderText('imput name')


        self.AccessKey = QLineEdit()
        self.AccessKey.setFont(QFont(font_type, size_type))
        self.lab_AccessKey = QLabel('AccessKey')
        self.lab_AccessKey.setFont(QFont(font_type, size_type))

        layout.addRow(self.lab_AccessKey,self.AccessKey)
        self.AccessKey.setPlaceholderText('imput AccessKey')


        self.AccessSecret = QLineEdit()
        self.AccessSecret.setFont(QFont(font_type, size_type))
        self.lab_AccessSecret = QLabel('AccessSecret')
        self.lab_AccessSecret.setFont(QFont(font_type, size_type))
        layout.addRow(self.lab_AccessSecret,self.AccessSecret)
        self.AccessSecret.setPlaceholderText('imput AccessSecret')


        self.DBClusterId = QLineEdit()
        self.DBClusterId.setFont(QFont(font_type, size_type))
        self.lab_DBClusterId = QLabel('DBClusterId')
        self.lab_DBClusterId.setFont(QFont(font_type, size_type))
        layout.addRow(self.lab_DBClusterId, self.DBClusterId)
        self.DBClusterId.setPlaceholderText('imput DBClusterId')


        # self.dbInstanceId = QLineEdit()
        # self.dbInstanceId.setFont(QFont(font_type, size_type))
        # self.lab_dbInstanceId = QLabel('dbInstanceId')
        # self.lab_dbInstanceId.setFont(QFont(font_type, size_type))
        # layout.addRow(self.lab_dbInstanceId, self.dbInstanceId)
        # self.dbInstanceId.setPlaceholderText('imput dbInstanceId')


        self.DBClusterIPArrayName = QLineEdit()
        self.DBClusterIPArrayName.setFont(QFont(font_type, size_type))
        self.lab_DBClusterIPArrayName = QLabel('DBClusterIPArrayName')
        self.lab_DBClusterIPArrayName.setFont(QFont(font_type, size_type))
        layout.addRow(self.lab_DBClusterIPArrayName, self.DBClusterIPArrayName)
        self.DBClusterIPArrayName.setPlaceholderText('imput DBClusterIPArrayName')


        self.bt1 = QPushButton('提交')
        self.bt1.setFont(QFont(font_type, size_type))
        layout.addWidget(self.bt1)
        self.bt1.clicked.connect(self.clicked_bt1)

        self.setLayout(layout)
        self.show()

    def selectionchange(self,i):
        if i ==0:
            self.name.setText('')
            self.AccessKey.setText('')
            self.AccessSecret.setText('')
            self.DBClusterId.setText('')
            # self.dbInstanceId.setText('')
            self.DBClusterIPArrayName.setText('')
        else:
            data = self.data[i-1]
            self.name.setText(data['name'])
            self.AccessKey.setText(data['AccessKey'])
            self.AccessSecret.setText(data['AccessSecret'])
            self.DBClusterId.setText(data['DBClusterId'])
            # self.dbInstanceId.setText(data['dbInstanceId'])
            self.DBClusterIPArrayName.setText(data['DBClusterIPArrayName'])


    def get_ip(self):
        r = requests.post(url='http://ip.42.pl/raw ')
        return r.text

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        newleft = (screen.width()-size.width())/2
        newright = (screen.height()-size.height())/2
        self.move(int(newleft),int(newright))

    def clicked_bt1(self):
        name = self.name.text()
        AccessKey = self.AccessKey.text()
        AccessSecret =self.AccessSecret.text()
        DBClusterId = self.DBClusterId.text()
        DBClusterIPArrayName = self.DBClusterIPArrayName.text()
        ip = self.IP.text()
        # 阿里云的accessKey,accessKeySecret,endpoint
        endpoint = "http://polardb.aliyuncs.com/"
        # 计算时间戳参数，使用的是utc时间，并格式化成指定的格式
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        # 下面三个参数要求全局唯一，使用uuid生成随机字符串
        # ClientToken = str(uuid.uuid4()) #本示例中用不到
        # Token = str(uuid.uuid4()) #本示例中用不到
        signatureNonce = str(uuid.uuid4())
        # 参考api文档，定义公共参数
        slbCommonParam = {
            "Format": "json",
            "Version": "2017-08-01",
            "AccessKeyId": AccessKey,
            "SignatureMethod": "HMAC-SHA1",
            "Timestamp": timestamp,
            "SignatureVersion": "1.0",
            "SignatureNonce": signatureNonce
        }
        # 自定义参数，即阿里云的api和api请求的参数，示例中简单添加两个参数
        customParams = {
            "Action": "ModifyDBClusterAccessWhitelist",  # 操作参数
            "DBClusterId": DBClusterId,  # 集群ID
            "WhiteListType": "",  # 白名单类型。取值范围如下：IP：IP白名单分组。SecurityGroup：安全组
            "DBClusterIPArrayName": DBClusterIPArrayName,  # IP白名单分组的名称
            "DBClusterIPArrayAttribute": "",  # IP白名单分组属性。设置为hidden后控制台不可见
            "SecurityIps": ip,  # IP白名单分组中的IP地址或地址段,多个IP间用英文逗号（,）隔开
            "ModifyMode": "",  # IP白名单的修改方式，取值范围如下：Cover：覆盖原IP白名单（默认值）。Append：追加IP。Delete：删除IP
            "SecurityGroupIds": ""  # 安全组ID，多个安全组间用英文逗号（,）隔开,当WhiteListType取值为SecurityGroup时该参数才支持配置
        }
        # 下面根据阿里云文档计算待签名字符串
        # 首先合并公共参数和自定义参数，然后排序
        sumParams = {**customParams, **slbCommonParam}
        sortedParams = sorted(sumParams.items(), key=lambda x: x[0])
        # 然后对合并排序后的参数进行urlencode编码，得到的是多个key=value的键值对通过&符号连接后组成的字符串
        urlencodeParams = urllib.parse.urlencode(sortedParams)
        # 再处理一次，将urlencode后的字符串中的“=”和“&”进行percent编码
        urlencodeParams = urllib.parse.quote_plus(urlencodeParams)
        # 最后生成待签名字符串
        toSignStr = "GET" + "&" + urllib.parse.quote_plus("/") + "&" + urlencodeParams
        # 计算签名
        h = hmac.new((AccessSecret + "&").encode(), toSignStr.encode(), "sha1")
        signature = base64.encodebytes(h.digest()).strip().decode()

        # 将Signature添加到请求参数，生成请求url
        sumParams["Signature"] = signature
        url = endpoint + "?" + urllib.parse.urlencode(sumParams)
        # 发送请求并打印结果
        response = requests.get(url)
        res = response.json()
        try:
            Message = res['Message']
            QMessageBox.information(self, '提示', '修改失败！！错误信息：%s' % Message)
        except:
            QMessageBox.information(self, '提示', '%s修改ip地址白名单成功!' % name)









if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Demo()
    sys.exit(app.exec_())