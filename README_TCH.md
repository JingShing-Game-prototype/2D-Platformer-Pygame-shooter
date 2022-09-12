[English](https://github.com/JingShing/2D-Platformer-Pygame-shooter/blob/main/README.md) | 繁體中文

## User Manual

You can get exe here : https://jingshing.itch.io/gunfight-prototype

A 2D platformer shooter.

### keyboard & mouse

* w, a, s, d to move t, y, g, h to move camera
* f to shoot in front of character
* m to switch mouse control camera
* l to open test camera box
* O to active enemy hatred
* mouse to aim
* left mouse key to shoot
* right mouse key to melee attack
* Q, R to switch weapon
* 0 to switch shader
* 9 to resize camera
* \+ , - to scale camera
* T, Y, G, H to move camera
* 8 to fullscreen 

### Joystick

* left joystick to move
* dpad to move. also can move camera by activing camera mode.
* left joystick button to active dpad camera mode.
* right joystick to aim.(need to open aim mode first)
* right joystick button to active aim mode.
* A to jump.
* Y, B to switch weapon.
* RT to shoot.
* LT to melee attack.
* RB, LB to scale camera.

## Ver 0.1

Can use mouse to aim and used keyboard to control camera : scale camera, move camera, mouse control camera.

## Ver 0.2

Add enemies and blood effect.

Enemy has a simple ai to aim player. And need to be trigger.

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

## object pool format process

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
