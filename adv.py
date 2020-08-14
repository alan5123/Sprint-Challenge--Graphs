from room import Room
from player import Player
from world import World

from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# MVP 1000 steps

traversal_path = []
backtrack = []
traversed = {}
reverse = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

traversed[player.current_room.id] = player.current_room.get_exits()

while len(traversed) < len(room_graph):

    # if the room is new, add the room into our traversed dictionary
    room_id = player.current_room.id
    if room_id not in traversed.keys():
        # add the room's exits into each dictionary entry with the key being the id
        traversed[room_id] = player.current_room.get_exits()
        # remove the path it took to get to this room from the exits list so it can continue
        traversed[room_id].remove(backtrack[-1])

    # if there is no valid unexplored exits, backtrack in reverse order until there is
    if len(traversed[room_id]) == 0:
        prev_action = backtrack.pop()
        traversal_path.append(prev_action)
        player.travel(prev_action)

    # when there is a valid exit in the room in the dictionary, travel to that exit
    # append the reverse path to the backtracking sequence
    else:
        next = traversed[room_id].pop()
        traversal_path.append(next)
        backtrack.append(reverse[next])
        player.travel(next)







# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")