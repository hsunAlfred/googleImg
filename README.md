# googleImg
github原始碼
```python
git clone https://github.com/hsunAlfred/googleImg.git
```


1、安裝相關模組
```python
pip install -r requirements.txt
```

2、開啟googleImg_thumbnail.py，修改傳入main函數的參數，參數設定後將依序搭配一個我們要找的食物當作關鍵字放到google搜尋
&nbsp;&nbsp;&nbsp;&nbsp;eg. 鮭魚 食譜
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;鮭魚 餐盤
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;鮭魚 熟食
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;雞腿肉 食譜
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;雞腿肉 餐盤
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;雞腿肉 熟食
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*我們要找的食物可以在food_kind.json修改
```python
if __name__ == '__main__':
    main("食譜", "餐盤", "熟食")
```

3、程式執行完成後會顯示花費的時間，並依照主菜、副菜、主食輸出至不同資料夾
4、程式執行時如果出現webdrive version相關的問題，請執行chromedriver_autoupdate_logging.py，當顯示press enter to exit，代表執行完成
