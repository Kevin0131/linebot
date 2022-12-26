基本上我的小助理都是從user state開始的
從下圖我們可以看到各個功能都是從user去出發，經由advanced跑到各個功能對應的state之後再藉由go back跳回user state。


接下來我們就來看各個功能的實作
![螢幕擷取畫面_20221226_055714](https://user-images.githubusercontent.com/74133233/209535348-6470f01a-90be-4411-a9ba-3f64aea25465.png)
這個功能就是當使用者輸入情歌之後會隨機從資料庫中幫使用者選一首情歌，並且在go back時還會跳出訊息嘲諷使用者XD

![螢幕擷取畫面_20221226_055650](https://user-images.githubusercontent.com/74133233/209535635-c0527d1a-71a5-42d7-b560-76112166c48e.png)
這功能就是輸入偶像，機器人就會把資料庫中的球員照片丟給user



![螢幕擷取畫面_20221226_055738](https://user-images.githubusercontent.com/74133233/209535714-f899c367-8a0d-4dad-be7f-ad2f4e9fdd69.png)
接下來就是爬蟲啦，當使用者輸入想搜尋的圖片之後，機器人會去google搜尋使用者要的圖片。

![螢幕擷取畫面_20221226_055714](https://user-images.githubusercontent.com/74133233/209535881-3fdc6afc-ef1c-4e42-b5cf-73ccffad484d.png)
這也是爬蟲的功能，當我們輸入想要搜尋的地點之後輸入，機器會自動去網路搜尋氣象資訊丟給使用者。

![螢幕擷取畫面_20221226_055754](https://user-images.githubusercontent.com/74133233/209535995-8884b915-2d07-461d-9838-5b37495fe81c.png)
當使用者對結果很滿意時說出謝謝，機器人會隨機從資料庫中挑選一句話回應給使用者，但可能不一定是好的回應XD
