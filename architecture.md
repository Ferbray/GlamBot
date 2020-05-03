### 📜Архитектура:

Данный файл нужен для планирования заполнения папок

```
📓GlamBot
—architecture.md
—diagram_progress.md
—README.md
—database_wrapper.py
—qiwi_wrapper.py
—shrifts
—PhotoDatePlayers
—multiplayer
—old_materials
—materials_bot
——...
——...
——photos
———mps
————peaceful_mps
————neutral_mps
————evil_mps
———character
————skins
————weapons
————foods
————medicines
————clothes
———other_design
———building_main_location
———building_casino_location
———building_house_location
———building_market_location
——generators
———....
———....
———...
```

### 💡Пояснение веток

- GlamBot/shifts — папка с шрифтами
- GlamBot/multiplayer — папка с файлами по мультиплееру
- GlamBot/multiplayer/generators — отдельная система, разработанная для генерации объектов на карте, в будущем будет залита на Github.com
- GlamBot/multiplayer/photos - хранятся все фотографии по мультиплееру, разделеные в отдельные категории
- GlamBot/old_materials — хранятся все старые материалы для будущего представления истории
- GlamBot/database_wrapper - модуль, который помогает с бесконечным подключением к БД
- GlamBot/qiwi_wrapper - модуль для подключения доната в бота
