[English](https://github.com/JingShing/2D-Platformer-Pygame-shooter/blob/main/README.md) | 繁體中文

## User Manual用戶手冊

你可以在這取得 EXE : https://jingshing.itch.io/gunfight-prototype

一個2D平台射擊遊戲

### keyboard & mouse 鍵盤和滑鼠

* w, a, s, d 移動角色 t, y, g, h 移動攝影機
* f 射擊。(最新版移除)
* m 更改成滑鼠控制鏡頭
* l 開啟測試鏡頭框
* O 激發敵人仇恨
* 滑鼠瞄準
* 左鍵射擊
* 右鍵近戰
* Q, R 更改武器
* 0 更改濾鏡
* 9 重置縮放
* \+ , - 縮放鏡頭
* T, Y, G, H 移動鏡頭
* 8 更改成全螢幕

### Joystick

* 左搖桿移動
* 方向鍵移動。 可以透過更改成相機模式來移動相機
* 按下左搖桿按鈕，切換到移動相機模式
* 右搖桿瞄準(需要先切換到瞄準模式)
* 右搖桿按鈕切換到瞄準模式
* A 跳躍
* Y, B 切換武器
* RT 射擊
* LT 近戰攻擊
* RB, LB 縮放相機

## Ver 0.1

可以透過滑鼠瞄準，透過鍵盤移動鏡頭 : 縮放鏡頭、平移鏡頭、滑鼠控制鏡頭

## Ver 0.2

新增敵人和噴血特效

敵人會瞄準玩家並且有仇恨系統

## Ver 0.3

* Add entity class to collect similar function and variable from player and enemies.
* Fixed aim line to make it more correct.
* Using weapon fail fixed.
* Shooting will shake weapon now.
* Add China variable to control blood is green or red.

## Ver 0.4

* Add switch weapon feature. Using list and index to change weapon.

* Add melee attack system. Use right mouse button to melee attack.

* AI can melee attack now. Improved AI_attack function.

* Melee attack is part from up pos, down pos and middle pos has different value to edit.

* Enemy will being intense if you attack in front of them.(多方位調整，目前有高、中高、中、低等攻擊位置，有正反兩面，所以有八位攻擊角。)

* Create bullet function fixed. Now will record user.

* Player shoot 8 direction.

* press 8 to fullscreen.

* Classify entity and weapon more graceful.

* Add a dict to control shot bullet type.

* Add resource path to each load to make sure exe will success.

* bullet has health now.

* Add a dict to collect weapon data

* Add shield

* Q can switch last weapon, E can switch next weapon.

* Add map border

* Add invinsible time

* Dynamic bullet amount in map

* Add a object class for item or moving particles.

* Add flesh explode from dying entity.

* Change Entity type and object type setting.

* Add health bar. UI system first part done.

* Add Weapon UI

## Ver 0.5

* Add object pool and 3 function about object pool. Now can store bullet in it.
  * move_to_object_pool(self, object)
  * take_from_object_pool(self, object)
  * seek_object_from_object_pool(self, object_type)
* Update flesh move. Can add x direction by bullet hit.
* Add particle to object pool.
* Add joystick control.
* Add player, enemy and weapon to object pool. -> weapon float bug
* Fixed joystick aim.
* Weapon spawn error fixed.
* Add custom cursor.
* Fixed cursor offset and aiming deviation.
* Add controller detect feature.
* Add load map function.
* Fixed image texture problem. exe all guns.
* Sword can kill bullet by sweeping.
* Add background texture.

## Ver 0.6

* Add controller vibration. (while getting damage or shooting bullet)
* Add sword shield enemy bullet feature.
* Fixed pygame.display.set_mode method import.
* Upgrade camera class.
* Upgrade game class -> put screen and shader in it.

## 物件池運作流程

1. Set used_groups to store groups and old_self function to load new info\

2. Find where you kill this object replace with move_to_object_pool(self)

3. Find where you spawn this object replace with code below

   ```python
   old_object = self.seek_object_from_object_pool('object_type')
   if old_object:
       self.take_from_object_pool(old_particle)
       old_object.old_object(self, reference...)
   ```


## Up to do

- [ ] background particle -> reference sword rain
- [ ] skill
- [ ] Drop item -> new class?
- [ ] Ammo limit -> do it with UI
- [ ] Menu
- [ ] more weapon -> need data dict and file to edit
- [ ] switch map system
- [ ] networking -> socket?
- [ ] Improve AI move
- [ ] Change Character sprite -> I hate spritesheet
- [ ] Add crouch system
- [ ] Parkour system -> wall jump or something
- [ ] Boss Fight
- [ ] Random mode
- [ ] Store System -> need money or credit
- [ ] Mobile
- [ ] bgm
- [ ] more sfx
- [ ] dual gun
- [ ] delta time fix

## Finish

22/8/21

- [x] melee weapon and melee attack system
- [x] switch weapon
- [x] shield
- [x] bullet across wall hack

22/8/22

- [x] enemy body flesh explode effect
- [x] UI -> HP, Enemy info , Ammo, Item Info, Map info ...
- [x] object pool to keep bullet and weapon.

22/8/23

- [x] xbox controller
- [x] Map editor -> map save system

22/8/25

- [x] controller vibration
