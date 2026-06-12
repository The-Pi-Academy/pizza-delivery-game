# **Pizza Delivery Game:** 

# **🍕 Instructor Guide**

## **Station Details**

**Repository**: [https://github.com/The-Pi-Academy/pizza-delivery-game](https://github.com/The-Pi-Academy/pizza-delivery-game)  
**Description**:   
You are a pizza delivery person... in medieval times. Fight your way through guards, leap across gaps, and get the pizza to the door before it gets cold\! This game is written entirely in Python and features basic combat and platforming.

# Disclaimer

At the time of writing this, this station and document should be considered a first draft. This station can be quite technical and the code should be reviewed thoroughly before teaching. While explicit experience with game development is not required, it is highly recommended. 

## **Goals & Learning Objectives**

Game development is something just about everyone has some interest in, but are often intimidated by complexity. The goal with this project is to teach campers the absolute basics of game development so they can build upon this knowledge, show them how games are constructed so that they can eventually make their own games.

1. **Very basics of Python \-** including loops, variables, methods.   
2. **Game Dev Fundamentals** \- The core game loop, physics, collision are essential to understanding how games work.  
3. **Learning by Doing** \- Several parts of the game are intentionally not able to be completed. Students will be encouraged to mess around with code, ask questions, and try different tactics to solve certain problems.

## **Setup**

1. Clone the repo at [https://github.com/The-Pi-Academy/pizza-delivery-game](https://github.com/The-Pi-Academy/pizza-delivery-game)  
2. Open a terminal in the root location of the repo and run: “`bash setup.sh`” or “./[setup.sh](http://setup.sh)”. This will get the environment all set up.  
3. Launch the virtual environment by running “source venv/bin/activate” from the terminal  
4. From here, you can run the game by running “python [run.py](http://run.py)”  
5. For more information including controls, see the [repo readme](https://github.com/The-Pi-Academy/pizza-delivery-game#controls)  
   

# How to Play

The player controls a pizza delivery driver who can swing a breadstick sword to hit enemies and shoot pizza slices out of a pizza cannon. Their goal is to reach the delivery locations and shoot the required number of pizza slices into each location. Once all locations have had their pizza slices delivered, the level is complete and you will see how long it took to complete the level.  
Students will want to complete each level, however some levels will require editing code files in order to complete. This will be covered in more detail below

## **Step-by-Step Lab Progression**

1. **Open Code \-** Use either VS Code or Thonny to open the repository to view the game files  
2. **Break things \-** Tell students this game is meant to be messed with. Encourage them to change player health, weapon damages, move walls around. They aren’t going to permanently break the game, anything can be undone.  
3. **Walk through the game file structure \-** Explain to students that each file is named after the game component that it controls. Teach them how to search for text in their IDE, this will be crucial in finding parts of the game they’d like to change. You do not need to go over every file in the file structure, but it would be good to highlight important ones marked below with a \*  
   * Core game files (should not be edited)  
     * \* [Main.py](http://Main.py) \- The core game loop is in this file, everything is plumbed up in here  
     * [Grid.py](http://Grid.py) \- Logic for the grid system the game is built on  
     * [menu.py](http://menu.py) – Main menu  
     * [save.py](http://save.py) \- Handle game saving  
     * [constants.py](http://constants.py) \- Various constant values used throughout the game  
   * /levels directory  
     * Contains definitions for each level in the game. Each level has a “build” method where the level is built programmatically. There will be a section below explaining how levels are built  
   * Game objects  
     * [player.py](http://player.py) \- The main player character  
     * [enemy.py](http://enemy.py) \- The enemies on the map  
     * breadstick\_sword.py \- The pizza person’s melee weapon  
     * delivery\_target.py \- The locations that need pizza delivered to them  
     * pizza\_cannon.py \- The ranged pizza cannon that fires pizza slices  
     * pizza\_slice.py \- The ammo for the cannon. Can damage enemies as well as be used to deliver pizza to delivery\_targets  
     * And several more which can be identified by their file names  
4. **Demo Level 1 \-** Play a level and show how to swing the sword, shoot pizza slices, and jump around. Show that the delivery location to the far right can have pizza delivered by shooting pizza slices at it.  
5. **Show Developer Mode \-** When in a level, pressing the “M” key toggles “Developer Mode” which adds a grid overlay. Choose level 1 and show the game’s grid system. Grid coordinates show in the individual tiles as (X, Y), ex (24, \-3). **Very important note \- PyGame’s internal coordinate system is top left rooted, meaning the upper left most corner of the game’s pixel is (0,0). This is why the Y coordinates get larger the further down the tile is, and get smaller the higher up they are.**   
6. **Levels 2 and 3 \-** When the students get to these levels, they will need to change the game code in simple ways to overcome some intentional obstacles. See below section “How to Complete Levels”

# How to Edit Levels

Levels are relatively simple to construct. Each level lives in the “levels” directory, and they consist of a “build” method. The “build” method contains a series of statements that add elements to the level. Below are a series of common statements that can be added to the “build” methods. 

NOTE: All objects in the game are spawned by passing in an x and y value to their constructors.  

* **Add enemies** \- use the following

enemies \= \[  
            Enemy(5,  9),  
            Enemy(20, 9\)  
        \]

* The above will add an enemy to grid location 10, 8  
* **Add A Single Stone Tile**   
  * tilemap.add( 3, 8, 1, 1, S)  
  * The above add method accepts five parameters, X, Y, Width, Height, and Tile type. In this example, we are placing a Stone tile (using pre-configured variable “S” at position 3, 8 that is just 1 grid tile wide and tall.  
* **Add a group of Stone Tile**  
  * tilemap.add( 3, 8, 5, 5, S)  
  * This will add a group of tile starting at position (3, 8\) that is 5 tiles wide and 5 tiles tall.  
* The rest of things that can be added follow very similar patterns as listed above.

# 

# How to Complete the Levels

## Level 1

* Completable on its own without modifications  
* Teaches students how the controls work, combat, platforming  
* Player moves all the way to the right until they see the delivery location which will have a “0/3” floating above it indicating it needs 3 slices of pizza. They can press “2” to switch to the pizza cannon, hold “Enter” to charge up a shot, and release “Enter” when ready. They can aim the cannon while charging the shot with the arrow keys

## Level 2

* Requires modifications to complete  
* Obstacle 1 \- Large vertical wall  
  * Can be outright removed by removing line 21 in [Level2.py](http://Level2.py):       


  * \# first impenetrable wall. Change this code to get past here\!  
  * tilemap.add\_range(5, GROUND\_Y, 5, 0, S)  
  * Can also edit the line above so there is a gap to move through  
* Obstacle 2 \- Large Gap  
  * Add a platform to fill in the gap. Tell students to use developer mode to see what tiles need to be filled in. Can be filled in with this line of code near the bottom of the “build” method  
  * tilemap.add\_range(20, GROUND\_ROW, 60, GROUND\_ROW, G)

## Level 2

Similar to level 3, this level has multiple delivery locations, one of which will require students to add a platform to reach. There are also way more enemies, as well as a jet pack item they can use to fly around. The jet pack has limited fuel, but the students can add gas cans to the map to make getting around more reliable by adding this line of code to spawn a gas can at a location:

gas\_cans \= \[  
            GasCan(9, GROUND\_ROW),   
 GasCan(15, \-5),             \# ground, before step 1  
            \# ADD MORE GAS CANS HERE  
        \]

# Troubleshooting

1. **Changes the student made have broken the game** \- To undo ***all*** changes, run “git reset –hard”. To undo individual file changes run “git restore pathTo/MyFile” where pathTo/MyFile is the path to the file you want to revert  
2. **Changes made not reflecting in game \-** Make sure the files were saved, and that the game was restarted since the files were saved

## **Station Checklist**

* **Repository:** The pizza game repository is cloned and ready.  
* **Environment:** Students have a text editor, preferably VS Code.  
* **Activities:** The instructor is prepared to guide students through modifying the Python game code

## 

## 

## **Bored Students Ideas 💡**

* **Encourage students to beat their times, make it competitive and fun**  
* **There is an empty level 4 that students can fill out and make challenging for their fellow students to compete in.**

## **Self-Help**

* PyGame \- [https://www.pygame.org/docs/](https://www.pygame.org/docs/)  
* 

