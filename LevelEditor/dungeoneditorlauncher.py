import dungeoneditorscreen
from dungeoneditorscreen import *

#TODO: make the game launch faster.

#TODO: Trim the room sets in DungeonData, preferrably upon its creation if possible.
     # This means having the roomdata array start at 0,0 and end at the last non-empty room
     # contained in the dungeondata object.

#TODO: make it possible to "paint" tiles in the level editor by holding and dragging the mouse.

#TODO: make it possible to clear tiles in the level editor by right-clicking.

#TODO: make the tiledatas created through the leveleditor correspond more closely with the entites that can actually be created in the game.
    # i.e., get entity sets (monster,platforms, etc) from filepaths or something
    # use the same images/image sets when building the level as when playing the game (with some exceptions, like player start position)

#TODO: once the leveleditor is a little easier to use, test making multiple connected levels and navigating between them in the game.

#TODO: make it possible to add entities to the leveleditor which take up more than 1 tile (will need some kind of dimensions arg)

#TODO: plan out how tiles, entities, images, animated sprites, etc will all be stored in relation to the Dungeon Editor and the game launcher.

#TODO: Flesh out the actual level Editor.
    #make it possible to have more than 2 layers of entity selection.

#NOTE: might end up moving the folder that currently holds sprite data into the LevelEditor folder

#IDEA: give the dungeon grid container a color key explaining what the six different colors mean.

#IDEA: make it clear somehow which levels are empty (no rooms) in the LevelSelectContainer (not the dungeon grid).
    #could grey out the names of these levels
    #could also find a way to represent levels which contain rooms, but whose rooms have no tile data.

#IDEA: a button to move a level (or set of levels, which would be much more complicated) 
    #while also moving the rooms inside the level.
        #i.e., the level itself would not change at all, but simply be in a different part of the dungeon.

#IDEA: a quick way of deleting everything in each room of a level without deleting or resizing the level itself.

#IDEA: make the deselected color of a dungeon grid tile correspond to its associated level's color.
    #A level's color would be set by the user.
    
#IDEA: in the level editor, consider axis labels for the level grid to number rooms/tiles by their coords.
 
#consider a set of "level tags" for the editor, as well as
    #different "layers" that can be toggled (i.e.,background layer, platforms layer, and (at dungeon zoom level)
         #a layer which shows which levels contain which rooms)

def loadMapEditor():
	pygame.init()
	
	dungeon_renderer = Renderer()
	dungeon_renderer.create_screen(DUNGEON_WIN_WIDTH,DUNGEON_WIN_HEIGHT)
	dungeon_renderer.title = "Dungeon Editor"
	dungeon_renderer.color = (250, 250, 250)

	dungeon_editor_screen = DungeonEditorScreen(dungeon_renderer)
	dungeon_editor_screen.openDungeonEditor() #add more args if necessary

if __name__ == "__main__":
	loadMapEditor()