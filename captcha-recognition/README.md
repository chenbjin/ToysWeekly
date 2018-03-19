# captcha-recognition

CNN验证码整体识别，使用两种不同结构的CNN来做验证码识别。实验数据集是百度莱茨狗的验证码，目前convnet的准确率是82%，忽略大小写准确率89%。

## 数据收集

一开始用简单的tesseract-ocr收集几百张验证码，训练模型准确率20%之后，用模型去预测，保存正确的验证码，继续迭代优化模型，数据集4000左右达到上述效果

## 使用

```bash
pip install -r requirements.txt
python captcha_recognition.py
```
