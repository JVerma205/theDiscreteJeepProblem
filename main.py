import numpy as np


class TruckInTheDesert:
    """defines and controls the actions of the Truck in the Desert with fuel camps"""
    def __init__(self, f_curr=0, pos=0, f_max=3, n=5, base_fuel_used=0):
        self.f_curr = f_curr        # Amount of fuel the truck is carrying currently in units
        self.pos = pos              # current position of the truck in terms of fuel camps
        # Base Camp position is 0, Intermediate Camps are positions from 1 to n
        self.f_max = f_max          # Fuel storage capacity in units
        self.n = n                  # Total Number of Fuel camps
        self.camp_dumps = np.zeros(n)   # Units of Fuel dumps in each camp
        self.base_camp_fuel_used = base_fuel_used   # Amt of Base camp fuel used
        self.base_fuel_log = []
        self.camp_dump_log = []

    def refill(self, amt_of_fuel=1):
        if self.f_curr == self.f_max:
            # print("Fuel Tank already full. Won't refill at Fuel Camp ", self.pos)
            return 0
        if self.pos == 0:
            self.base_camp_fuel_used += self.f_max - self.f_curr
            self.f_curr = self.f_max
            self.base_fuel_log.append(self.base_camp_fuel_used)
        else:
            if self.camp_dumps[self.pos - 1] == 0:
                # print("Can't refill from Fuel Camp ", self.pos,
                #       ". Fuel Camp has ", self.camp_dumps[self.pos-1], " units of fuel.")
                return 0
            self.f_curr += amt_of_fuel
            assert self.f_curr <= self.f_max        # Checking whether f_curr exceeds f_max
            self.camp_dumps[self.pos - 1] -= amt_of_fuel
            assert self.camp_dumps[self.pos - 1] >= 0  # Raise error if the camp fuel goes -ive after offering the fuel

    def move_one_right(self):
        if self.pos == self.n:
            print("Target already achieved. Won't go further right.")
            return 0
        if self.f_curr == 0:
            raise ValueError("The fuel tank of the truck is empty. Game Over.")
        self.f_curr -= 1
        self.pos += 1

    def move_one_left(self):
        if self.pos == 0:
            print("Can't go further left. The truck is on the Base camp 0.")
            return 0
        if self.f_curr == 0:
            raise ValueError("The fuel tank of the truck is empty. Game Over.")
        self.f_curr -= 1
        self.pos -= 1

    def unload(self, amt_of_fuel):
        if self.f_curr == 0:
            print("Truck fuel is 0. Can't unload at Fuel Camp ", self.pos)
            return 0
        self.f_curr -= amt_of_fuel
        self.camp_dumps[self.pos - 1] += amt_of_fuel

    def final_trip(self):
        self.refill()
        while self.pos < self.n:
            self.move_one_right()
            self.refill(1)
        print("FINAL TRIP LOG:\n", self.camp_dumps)
        print("Target Camp Number ", self.pos, " Reached! Game Finished with ", self.base_camp_fuel_used,
              "units of fuel used from the base camp")

    def store_one_at(self, destination_camp):
        """command to store 1 unit of fuel at the given camp number"""
        if destination_camp == 1:
            # Refilling the deficit in the fuel tank
            self.refill()
            self.move_one_right()
            self.unload(1)
            self.move_one_left()
            # print("Fuel Camp 1 upped by 1 unit of fuel")
            self.camp_dump_log.append(self.camp_dumps.tolist())
            return 0
        destination_camp_idx = destination_camp - 1

        for idx in range(destination_camp_idx):
            if self.camp_dumps[destination_camp_idx - idx-1] < 2:  # Checking the units of fuel at the preceding camp
                while self.camp_dumps[destination_camp_idx - idx-1] < 2:
                    self.store_one_at(destination_camp - idx - 1)     # Recursive calling

        if destination_camp != 1:
            while self.pos < destination_camp:
                self.refill()
                self.move_one_right()
            self.unload(1)
            while self.pos > 0:
                self.move_one_left()
                self.refill()
            self.camp_dump_log.append(self.camp_dumps.tolist())


num_camps = int(input("Enter the number of intermediate fuel camps including the target camp."))
fuel_cap = 3
desert_obj = TruckInTheDesert(0, 0, fuel_cap, num_camps, 0)
store_target = desert_obj.n - desert_obj.f_max
for i in range(store_target):
    desert_obj.store_one_at(store_target-i)
print("Logs: \n")
print("Units of fuel refilled from the base camp before starting a round trip:", desert_obj.base_fuel_log)
print("Fuel Dump status of the", num_camps, "camps after each trip:", desert_obj.camp_dump_log)
desert_obj.final_trip()
