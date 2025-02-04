# **OT 2024 - FreeTheTerra**

V danom repozitáry je hra ku skúške z OT. Hra je spravená v knižnici pygame

**Autor**: Patrik Šabo

**Vybraná téma**: One level, but constantly changing (Mojom prípade sa level mení pomocou Wave systému)

---
## **1. Úvod**
Táto je hra je ku skúške z OT. V tejto hre sa postava (hráč), nachádza v prostredí kde naň ho útočia roôzne príšery a bossovia.

### **1.1 Inšpirácia**


### **1.2 Herný zážitok**
Cieľom hry je, aby hráč prežil ***čo najdlhšie***, až pokým to na hráča nebude veľa. Hráč sa môže pohybovať po mape a zároveň môže likvidovať nepriateľov, čím sa mu zvyšuje jeho skóre. Keď sa monštrá chytia hráčia, hráčovi sa uberú životy, a počas hry ich už nemá ako nabrať.

### **1.3 Vývojový softvér**
- **Pygame**: python knižnica pre robenie hrier
- **VScode**: vybrané IDE.
- **Itch.io**: zdroj grafických assetov
- **Aseprite**: edit pixelových spritov

---
## **2. Koncept**

### **2.1 Prehľad hry**
Hráč ovláda svoju postavu pomocou SPACE, AS alebo Šipkami. Hráč musí prežiť čo najdlhšie aby získal čo najväčšie skóre. Počas toho ako sa snaží prežiť naň ho útočia monštrá. A každú 5 vlnu je Boss. Hra je zameraná prevažne na prežitie bez nadbytočných vylepšení.

### **2.2 Interpretácia témy (One level, but constantly changing)**
**One level, but constantly changing**
Téma v tomto prípade bola implementovaná takým spôsobom, že máme viaceoj vĺn (waves), je to jeden level ale postupne sa mení jeho obťiažnosť

### **2.3 Základné mechaniky**
- **Pevne stanovené miesta generovania nepriateľov**: nepriatelia sa negenerujú na pravej strane obrazovky, aby nenastala situácia, že sa nepriatelia spawnú na hráčovi.
- **Hráč môže likvidovať nepriateľov**: hráč vystreľuje ohnivú gulu, ktorá pri náraze do nepriateľa spôsobuje jeho zranenie.

### **2.4 Návrh tried**
- **FreeTheTerra.py**: hlavný skript, ktorý managuje to aby sa hra zapla, nainštaluje potrebné knižnice
- **Setting.py**: udržiava v sebe potrebné hodnoty ktoré potrebuje hra získavať aj v iných trieda
- **SoundMusic.py**: má nastarosti hudbu, a zvukové efekty (efekt hovering tlačitok)
#### **UI**
- **UI.py**: táto trieda má nastarosti UI, ako sú Tlačítka, Sliders
- **Text.py** táto trieda má nastarosti Text, aby programátor nemusel managovať vytváranie textu vždy keď ho potrebuje, namiesto toho si vytvorí Text pomocou tejto triedy
#### **UI**
- **SceneManager.py**: má nastarosti scény, má v sebe všetky scény medzi ktorými sa hra prepína
- **Scenes**: toto su jednotlivé scény, napr. MainMenu, GameScene, Options, ...
#### **Entities**
- **Player.py**: Inicializuje hráča, jeho pohyb, má nastarosti celého hráča
- **Enemy.py**: Toto je trieda ktorú neskôr dedia nepriatelia: Orc, Boss, Zombie, Skeleton 

---
## **3. Grafika**

### **3.1 Interpretácia témy (One level, but constantly changing)**
Téma v tomto prípade bola implementovaná takým spôsobom, že máme viaceoj vĺn (waves), je to jeden level ale postupne sa mení jeho obťiažnosť

<p align="center">
  <img src="https://github.com/ppaprik/FreeTheTerra/blob/main/game/assets/sprites/enemies/boss.png" alt="Nepriatelia"">
  <img src="https://github.com/ppaprik/FreeTheTerra/blob/main/game/assets/sprites/enemies/orc.png" alt="Nepriatelia" width="50px">
  <img src="https://github.com/ppaprik/FreeTheTerra/blob/main/game/assets/sprites/enemies/skeleton.png" alt="Nepriatelia">
  
  <br>
  <em>Ukážka sprite-ov nepriateľov</em>
</p>

### **3.2 Dizajn**
V hre boli použité assety z itch.io. z **itch.io** sú použité všetky sprity ako sú enemies, player, alebo pozadie a zem

<p align="center">
  <img src="https://github.com/ppaprik/FreeTheTerra/blob/main/game/assets/sprites/terrain/dirt.png" alt="Level dizajn" width="50px">
  <img src="https://github.com/ppaprik/FreeTheTerra/blob/main/game/assets/sprites/terrain/grass.png" alt="Level dizajn" width="50px">
  <img src="https://github.com/ppaprik/FreeTheTerra/blob/main/game/assets/sprites/terrain/stone.png" alt="Level dizajn" width="50px">
  
  <br>
  <em>Ukážka dizajnu levelu</em>
</p>

---
## **4. Zvuk**

### **4.1 Hudba**
Hudba v hre je prevažne z YouTube no-copy music. Alebo z hry Terarria (Keďže hra slúži prevážne na pobavenie a štúdio ktoré vyvíjalo Terrariu samé dáva vlastnú hudbu free online, tak by to nemal byť problém)

### **4.2 Zvuky**
Zvuky v hre sú prevážne stiahnuté z **itch.io**

---
## **5. Herný zážitok**

### **5.1 Používateľské rozhranie**
Použivateľské rozhranie je že hráč má MainMenu, môže začať a hru, a počas si môže hru pauznuť, alebo podľa potreby zmeniť hlasitosť hudby. Hráč má možnosť kedykoľvek odísť z hry, ale tým pádom bude jeho skóre stratené

### **5.2 Ovládanie**
<ins>**Klávesnica**</ins>
- **AS SPACE**: pohyb hráča po mape.
- **Klávesy šípok**: alternatívne ovládanie pohybu hráča po mape.

<ins>**Myš**</ins> 
- **Ľavé tlačidlo**: výstreľ náboju.
