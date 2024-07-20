# Discord_Bot
一個名叫 **Rosmontis** 的 discord bot，內建許多有趣或實用的功能。目前只在私人伺服器裡使用，希望未來 **Rosmontis** 的功能更完善後可以逐漸推廣給其他人。

## Rosmontis.py
機器人的主程式。

### `+load`, `+unload`, `+reload`
這三個指令能夠在維持bot 不離線的情況下，對程式進行更新和修改，在進行bot 功能的測試時是個很好用的指令。

## main.py 
一些比較基礎的功能。

### `+ping`
回傳機器人的延遲，以毫秒 (ms) 顯示。

### `+rosemary`
回傳機器人的頭像。

### `+repeat <message>`
回傳 \<message> 的內容。

### `+say <message>`
和repeat 一樣，回傳 \<message> 的內容，但是會把使用者的指令刪除，這樣可以做出像**Rosmontis** 自己說話的效果。

### `+purge <num>`
刪除當前頻道一共 \<num> 則的訊息

## events.py
這個分類是處理事件觸發時機器人需要作出的回應，針對不同的事件，**Rosmontis** 會在伺服器內發送不同的訊息。

### `on_member_join()`
有新的成員進入伺服器時，會發送歡迎訊息。

### `on_member_leave()`
在成員離開伺服器時，發送離開的訊息。

### `on_message()`
伺服器內有任何訊息傳送都會觸發這個事件，給予不同的回應。

## task.py

### `+stime <time>`
設定時間為 \<time> ，**Rosmontis** 會在指定時間到的時候傳送訊息。  

在寫這段的code 時主要遇到的是時區的問題，因為bot 是放在別的伺服器託管的，但伺服器當地的時區並不是UTC+8 ，所以我需要在程式裡面導入datetime 模組庫來處理時區的差異。

## game.py

### `+roll <num>`
使用指令骰出一個 \<num> 面的骰子

### `+guess <range> <max_attempt>`
猜數字的小遊戲，預設是在 1 到 `99` 的範圍內猜一個數字，有 `5` 次的機會可以猜。可以透過更改 \<range> 來改變範圍，\<max_attempt> 改變猜測的機會次數。  

參考自社群機器人: Mee6 的功能，但和 Mee6 不同的在於，它並不會檢查訊息是否在同一個頻道，意思是說，我可以在不同的頻道傳訊息來猜數字，導致在各個頻道都會有 Mee6 的回覆。雖然通常使用者不會這麼做，但我還是不希望這種事發生，所以我在程式碼裡加入了檢查頻道的功能，只要使用者不是在指定頻道內傳訊息，**Rosmontis** 不會回覆他。  

在寫這段程式時還有遇到一個問題，因為偵測使用者輸入數字的功能會使用到 `on_message()` 這個函式，但一個機器人只能有一個 `on_message()` 函式，在這裡重新寫一個的話會把原本 event.py 底下的函式複寫掉，所以我這邊使用的方法是在 game.py 定義函式，然後在原本的 `on_message()` 中使用 `bot.get_cog()` 的方式進行調用。  
<br/>
<br/>
<br/>
> **Rosmontis** 目前仍屬於開發的階段  
> 還有很多的功能尚未完成  
> 目前我打算以每個星期大約二到三個功能的速度慢慢完成目標。

