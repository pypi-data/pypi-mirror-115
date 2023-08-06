# Copyright (c) Facebook, Inc. and its affiliates.
import numpy as np
import os

PATH_DAT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dat")

MAZE_FLAGS = (
    "noteleport",
    "hardfloor",
    "nommap",
    "arboreal",
    "shortsighted",
    "mazelevel",
    "premapped",
    "shroud",
    "graveyard",
    "icedpools",
    "solidify",
    "corrmaze",
    "inaccessibles",
)

MAP_CHARS = [
    " ",  # solid wall
    "#",  # corridor
    ".",  # room floor
    "-",  # horizontal wall
    "|",  # vertical wall
    "+",  # door
    "A",  # air
    "B",  # crosswall
    "C",  # cloud
    "S",  # secret door
    "H",  # secret corridor
    "{",  # fountain
    "\\",  # throne
    "K",  # soml
    "}",  # moat
    "P",  # pool of water
    "L",  # lava pool
    "I",  # ice
    "W",  # water
    "T",  # tree
    "F",  # iron bars
]

TRAP_NAMES = [
    "anti magic",
    "arrow",
    "bear",
    "board",
    "dart",
    "falling rock",
    "fire",
    "hole",
    "land mine",
    "level teleport",
    "magic portal",
    "magic",
    "pit",
    "polymorph",
    "rolling boulder",
    "rust",
    "sleep gas",
    "spiked pit",
    "statue",
    "teleport",
    "trap door",
    "web",
]


class LevelGenerator:
    def __init__(
        self,
        map=None,
        w=8,
        h=8,
        fill=".",
        lit=True,
        message="Welcome to MiniHack!",
        flags=("hardfloor",),
        solidfill=" ",
    ):
        assert all(
            f in MAZE_FLAGS for f in flags
        ), f"One of the provided maze flags is incorrect: {flags}"
        flags_str = ",".join(flags)

        self.header = f"""
MAZE: "mylevel", ' '
FLAGS:{flags_str}
MESSAGE: \"{message}\"
INIT_MAP: solidfill,'{solidfill}'
GEOMETRY:center,center
"""
        self.mapify = lambda x: "MAP\n" + x + "ENDMAP\n"
        self.init_map(map, w, h, fill)

        litness = "lit" if lit else "unlit"
        self.footer = f'REGION:(0,0,{self.x},{self.y}),{litness},"ordinary"\n'

        self.stair_up_exist = False

    def init_map(self, map=None, x=8, y=8, fill="."):
        if map is None:
            # Creating empty area
            self.x = x
            self.y = y
            self.map = np.array([[fill] * x] * y, dtype=str)
        else:
            lines = [list(line) for line in map.split("\n") if len(line) > 0]
            self.y = len(lines)
            self.x = max(len(line) for line in lines)
            new_lines = [line + [" "] * (self.x - len(line)) for line in lines]
            self.map = np.array(new_lines)

    def get_map_str(self):
        """Returns the map as a string."""
        map_list = [
            "".join(self.map[i]) + "\n" for i in range(self.map.shape[0])
        ]
        return "".join(map_list)

    def get_map_array(self):
        """Returns the map as an np array."""
        return self.map

    def get_des(self):
        """Returns the description file."""
        return self.header + self.mapify(self.get_map_str()) + self.footer

    @staticmethod
    def validate_place(place):
        if place is None:
            place = "random"
        elif isinstance(place, tuple):
            place = LevelGenerator.validate_coord(place)
            place = str(place)
        elif isinstance(place, str):
            pass
        else:
            raise ValueError("Invalid place provided.")

        return place

    @staticmethod
    def validate_coord(coord):
        assert (
            isinstance(coord, tuple)
            and len(coord) == 2
            and isinstance(coord[0], int)
            and isinstance(coord[1], int)
        )
        return coord

    def add_object(
        self, name="random", symbol="%", place=None, cursestate=None
    ):
        place = self.validate_place(place)
        assert isinstance(symbol, str) and len(symbol) == 1
        assert isinstance(
            name, str
        )  # TODO maybe check object exists in NetHack

        if name != "random":
            name = f'"{name}"'
            self.footer += f"OBJECT:('{symbol}',{name}),{place}"

            if cursestate is not None:
                assert cursestate in [
                    "blessed",
                    "uncursed",
                    "cursed",
                    "random",
                ]
                if cursestate != "random":
                    self.footer += f",{cursestate}"

            self.footer += "\n"

        else:
            self.footer += f"OBJECT:random,{place}\n"

    def add_object_area(
        self, area_name, name="random", symbol="%", cursestate=None
    ):
        place = f"rndcoord({area_name})"
        self.add_object(name, symbol, place, cursestate)

    def add_monster(self, name="random", symbol=None, place="random", args=()):
        place = self.validate_place(place)
        assert (
            symbol == "random"
            or symbol is None
            or (isinstance(symbol, str) and len(symbol) == 1)
        )
        assert isinstance(
            name, str
        )  # TODO maybe check object exists in NetHac

        if name != "random":
            name = f'"{name}"'

        if symbol is not None:
            name = f"('{symbol}',{name})"

        self.footer += f"MONSTER:{name},{place}"

        if len(args) > 0:
            assert any(
                arg in ["hostile", "peaceful", "asleep", "awake"]
                for arg in args
            )
            for arg in args:
                self.footer += f",{arg}"

        self.footer += "\n"

    def add_terrain(self, coord, flag, in_footer=False):
        coord = self.validate_coord(coord)
        assert flag in MAP_CHARS

        if in_footer:
            self.footer += f"TERRAIN: {str(coord)}, '{flag}'\n"
        else:
            x, y = coord
            self.map[y, x] = flag

    def fill_terrain(self, type, x1, y1, x2, y2, flag):
        """Fill the areas between (x1, y1) and (x2, y2) with feature descibed
        in flag as follows:

        type:
        - "rect" - An unfilled rectangle, containing just the edges and none
            of the interior points.
        - "fillrect" - A filled rectangle containing the edges and all of the
            interior points.
        - "line" - A straight line drawn from one pair of coordinates to the
            other using Bresenham's line algorithm.
        """
        assert type in ("rect", "fillrect", "line")
        assert flag in MAP_CHARS
        self.footer += f"TERRAIN:{type} ({x1},{y1},{x2},{y2}),'{flag}'\n"

    def set_area_variable(
        self,
        var_name,  # Should start with $ sign
        type,
        x1,
        y1,
        x2,
        y2,
    ):
        """Set a variable representing an area on the map.

        type:
        - "rect" - An unfilled rectangle, containing just the edges and none
            of the interior points.
        - "fillrect" - A filled rectangle containing the edges and all of the
            interior points.
        - "line" - A straight line drawn from one pair of coordinates to the
            other using Bresenham's line algorithm.
        """

        assert type in ("rect", "fillrect", "line")
        if var_name[0] != "$":
            var_name = "$" + var_name
        self.footer += f"{var_name} = selection:{type} ({x1},{y1},{x2},{y2})\n"

    def add_goal_pos(self, place="random"):
        self.add_stair_down(place)

    def add_stair_down(self, place="random"):
        place = self.validate_place(place)
        self.footer += f"STAIR:{place},down\n"

    def set_start_pos(self, coord):
        self.add_stair_up(coord)

    def set_start_rect(self, p1, p2):
        self.add_stair_up_rect(p1, p2)

    def add_stair_up(self, coord):
        if self.stair_up_exist:
            return
        x, y = self.validate_coord(coord)
        _x, _y = abs(x - 1), abs(y - 1)  # any different coordinate than (x,y)
        self.footer += f"BRANCH:({x},{y},{x},{y}),({_x},{_y},{_x},{_y})\n"
        self.stair_up_exist = True

    def add_stair_up_rect(self, p1, p2):
        if self.stair_up_exist:
            return
        x1, y1 = self.validate_coord(p1)
        x2, y2 = self.validate_coord(p2)
        self.footer += f"BRANCH:({x1},{y1},{x2},{y2}),({0},{0},{0},{0})\n"
        self.stair_up_exist = True

    def add_door(self, state, place="random"):
        place = self.validate_place(place)
        assert state in ["nodoor", "locked", "closed", "open", "random"]
        self.footer += f"DOOR:{state},{place}\n"

    def add_altar(self, place="random", align="random", type="random"):
        place = self.validate_place(place)
        assert align in [
            "noalign",
            "law",
            "neutral",
            "chaos",
            "coaligned",
            "noncoaligned",
            "random",
        ]
        assert type in ["sanctum", "shrine", "altar", "random"]
        self.footer += f"ALTAR:{place},{align},{type}\n"

    def add_sink(self, place="random"):
        place = self.validate_place(place)
        self.footer += f"SINK:{place}\n"

    def add_trap(self, name="teleport", place="random"):
        place = self.validate_place(place)
        assert name in TRAP_NAMES
        self.footer += f'TRAP:"{name}",{place}\n'

    def add_fountain(self, place):
        place = self.validate_place(place)
        self.footer += f"FOUNTAIN: {place}\n"

    def add_boulder(self, place="random"):
        place = self.validate_place(place)
        self.footer += f'OBJECT: "boulder", {place}\n'

    def wallify(self):
        self.footer += "WALLIFY\n"

    def add_mazewalk(self, coord=None, dir="east"):
        if coord is not None:
            x, y = self.validate_coord(coord)
        else:
            x, y = self.x // 2, self.y // 2

        self.footer += f"MAZEWALK:({x},{y}),{dir}\n"

    def add_line(self, str):
        self.footer += str + "\n"


class KeyRoomGenerator:
    def __init__(self, room_size, subroom_size, lit):
        des_path = os.path.join(PATH_DAT_DIR, "key_and_door_tmp.des")
        with open(des_path) as f:
            df = f.read()

        df = df.replace("RS", str(room_size))
        df = df.replace("SS", str(subroom_size))
        if not lit:
            df = df.replace("lit", str("unlit"))

        self.des_file = df

    def get_des(self):
        return self.des_file
