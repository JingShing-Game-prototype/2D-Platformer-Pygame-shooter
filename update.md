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

## Up to do

- [ ] background particle -> reference sword rain
- [ ] bullet across wall hack
- [ ] skill
- [ ] Drop item -> new class?
- [ ] Ammo limit -> do it with UI
- [ ] UI -> HP, Enemy info , Ammo, Item Info, Map info ...
- [ ] Menu
- [ ] enemy body flesh explode effect
- [ ] more weapon -> need data dict and file to edit
- [ ] switch map system
- [ ] networking -> socket?
- [ ] Improve AI move
- [ ] Change Character sprite -> I hate spritesheet
- [ ] Add crouch system
- [ ] Parkour system -> wall jump or something
- [ ] Boss Fight
- [ ] Random mode
- [ ] Store System

## Finish

22/8/21

- [x] melee weapon and melee attack system
- [x] switch weapon
- [x] shield

