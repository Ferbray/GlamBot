'''GlamBot - новый эволюционный бот, 
в котором есть мультиплеер.

  • Кодер — GIS
  • Админ — Tenkara
  
Используемые библиотеки: 
  • 𝑣𝑘𝑏𝑜𝑡𝑡𝑙𝑒
  • 𝑝𝑠𝑞𝑙
  • 𝑡𝑒𝑟𝑚𝑜𝑐𝑜𝑙𝑜𝑟
  • 𝑙𝑜𝑔𝑢𝑟𝑢
  • 𝑢𝑣𝑙𝑜𝑜𝑝
  
Date start — 24.01.2020
Это файл создан для перемещения по архитек-
-туре бота и для помощи
"'

АРХИТЕКТУРА:
GlamBot
—shrifts (Все материалы — 5)
—multiplayer
——... 
——... 
——photos (Все материалы — 0)
———mps (Все материалы – 0)
————peaceful_mps (Все материалы — 0)
————neutral_mps (Все материалы — 0)
————evil_mps (Все материалы — 0)
———character (Все материалы — 0)
————skins
————weapons
————foods
————medicines
————clothes
———other_design (Всё материалы — 0)
———building_main_location (Все материалы — 0)
———building_casino_location (Всё материалы — 0)
———building_house_location (Всё материалы — 0)
———building_market_location (Всё материалы — 0)
——generators
———.... 
–——.... 
———... 
—old_materials (Все материалы — 36)
—database_wrapper.py
—qiwi_wrapper.py
—diagram_progress.txt
—architecture.txt

ПОЯСНЕНИЯ КАЖДОЙ ВЕТКИ
GlamBot/shifts — хранятся все шрифты
GlamBot/multiplayer — хранятся все файлы 
по мультиплееру
GlamBot/old_materials — хранятся все старые 
материалы для будущего представления истории
GlamBot/multiplayer/generators — отдельная система, 
разработанная для генерации объектов на карте,
в будущем залью на Github.com
GlamBot/multiplayer/photos - хранятся все фотогра-
-фии по мультиплееру, разделеные в отдельные ка-
-тегории.
GlamBot/database_wrapper - помогает с бесконеч-
ным подключением к БД.
GlamBot/qiwi_wrapper - нужен для доната
