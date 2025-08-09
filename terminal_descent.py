engine_efficiency_dict = {
    "High": 8,
    "Medium": 10,
    "Low": 12
}

gravity_dict = {
    "Low": 0.8,
    "Normal": 1,
    "High": 1.5
}

difficulty_settings = {
    "Easy": {"fuel": 700, "altitude": 600, "velocity": 0.0, "engine_efficiency": engine_efficiency_dict["High"]},
    "Medium": {"fuel": 500, "altitude": 500, "velocity": 10.0, "engine_efficiency": engine_efficiency_dict["Medium"]},
    "Hard": {"fuel": 500, "altitude": 400, "velocity": 20.0, "engine_efficiency": engine_efficiency_dict["Low"]}
}

def play_intro():
    print("──────────────────────────────────────────────────────────")
    print("             Welcome to: TERMINAL DESCENT")
    print("──────────────────────────────────────────────────────────")
    print("You are the last pilot of a stranded vessel, plunging")
    print("toward the surface of an uncharted celestial body. ")
    print("Fuel reserves are low. Gravity is merciless. Only precise")
    print("thrust and steady nerves can prevent catastrophe.")
    print("There is no autopilot. No second chances.")
    print("This is your final approach... Good luck!")
    print()
    input("Press any key to begin descent...")

def select_difficulty():
    print("\nSelect difficulty: [1] Easy - good engine and no intial speed.")
    print("                   [2] Medium - engine not so good and already dropping.")
    print("                   [3] Hard - engine is shot and you're coming in hot.")
    while True:
        choice = input("> ").strip().lower()
        if choice == "1":
            return "Easy", difficulty_settings["Easy"]
        elif choice == "2":
            return "Medium", difficulty_settings["Medium"]
        elif choice == "3":
            return "Hard", difficulty_settings["Hard"]
        else:
            print_invalid()

def select_gravity():
    print("\nSelect gravity: [1] low, [2] normal, [3] high")
    while True:
        choice = input("> ").strip().lower()
        if choice == "1":
            return gravity_dict["Low"]
        elif choice == "2":
            return gravity_dict["Normal"]
        elif choice == "3":
            return gravity_dict["High"]
        else:
            print_invalid()

def print_invalid():
    print("Invalid input. Please enter 'y' or 'n'.")

def print_settings(gravity, fuel, altitude, velocity, engine_efficiency):
    print(f"Gravity: {get_label(gravity, gravity_dict)}  |  Engine Efficiency: {get_label(engine_efficiency, engine_efficiency_dict)}  |  Altitude: {altitude:3.2f} m  |  Speed: {velocity:4.2f} m/s  |  Fuel: {fuel:3.0f} u")

def get_label(value, mapping):
    return next((k for k, v in mapping.items() if v == value), None)

def play_game():
    level, settings = select_difficulty()
    gravity = select_gravity()
    fuel = settings["fuel"]
    altitude = settings["altitude"]  # meters
    velocity = settings["velocity"]     # m/s
    engine_efficiency = settings["engine_efficiency"]

    if level == "Hard" and gravity == gravity_dict["High"]:
        print("🔥 Survivability is 0% - may God have mercy on your soul!")
    
    # Constants
    
    weight = 1000      # kg (not directly used unless we get fancy)
    safe_landing_speed = 5.0  # m/s
    
    tick = 1  # seconds per loop. increase to speed up, decrease to slow down
    
    print(f"\n--- Lunar Descent Initiated --- Playing {level} Mode")
    
    while altitude > 0:
        
        print_settings(gravity, fuel, altitude, velocity, engine_efficiency)

        key_entered = input("Enter thrust (\"q\" to quit): ").strip().lower()
        if key_entered == 'q':
            print("Mission aborted. Returning to orbit...\n")
            exit()

        try:
            thrust = float(key_entered)
        except ValueError:
            thrust = 0.0
        
        thrust = round(max(0.0, min(thrust, fuel)))  # Clamp thrust to available fuel
        
        fuel -= thrust
        acceleration = gravity - thrust / engine_efficiency  # Dividing by 10 to scale thrust impact
        velocity += acceleration * tick
        altitude -= velocity * tick
        
        if altitude <= 0:
            altitude = 0
            print("\n--- Contact with surface ---")
            print(f"Final velocity: {velocity:.2f} m/s")
            if velocity <= safe_landing_speed:
                if fuel > 200:
                    print("You landed with fuel to spare. Efficient work, pilot. ✅")
                elif fuel > 0:
                    print("Fuel was tight, but you made it. Well done. ⚠️")
                else:
                    print("You landed on fumes. That was close. 🔥")
            else:
                print("CRASH! The ship is lost. 💥")
            break

def play_again():

    print("Would you like to play again? [y/n]")
    while True:
        choice = input("> ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            exit()
        else:
            print_invalid()

def start_game():
    while True:
        play_intro()
        play_game()
        if not play_again():
            break

if __name__ == "__main__":
    start_game()
