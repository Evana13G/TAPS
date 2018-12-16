from time import sleep
import xpc

def catch_disconnects(func):
    def wrapper(*args, **kwargs):
        count = 0
        while (count < 3):
            try:
                val = func(*args, **kwargs)
                return val
            except:
                count += 1
                args[0].client = xpc.XPlaneConnect()
                print "recovered from disconnect"
        raise Exception("Client disconnected and failed to reconnect three times")
    return wrapper

class PlaneState(object):

    # Should we use lat, long, elevation or x,y,z?
    def __init__(self, dest_x, dest_y, dest_z, dest_airspeed, reward_function):
        self.client = xpc.XPlaneConnect()
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.dest_z = dest_z
        self.dest_airspeed = dest_airspeed
        self.reward_function = reward_function

    @catch_disconnects
    def get_raw_state(self):
        '''
        get_raw_state returns a state vector containing the following in order
        '''
        refs = [
            "sim/flightmodel/position/local_x", # X is like lat? 0   -6104.765625
            "sim/flightmodel/position/local_y", # Y is like long? 1   2369.8623046875
            "sim/flightmodel/position/local_z", # Z is like altitude? 2  -2721.5224609375
            "sim/flightmodel/position/local_vx", # 3 -2.3089725971221924
            "sim/flightmodel/position/local_vy", # 4 -61.17462921142578
            "sim/flightmodel/position/local_vz", # 5 -32.92040252685547
            "sim/flightmodel/position/true_airspeed", # 6 69.50841522216797
            "sim/flightmodel/position/true_theta", # Pitch 7 -53.9542236328125
            "sim/flightmodel/position/true_phi", # Roll 8 19.321489334106445
            "sim/flightmodel/position/true_psi", # Heading 9 350.67724609375
            "sim/flightmodel/position/P", # The roll rotation rates (relative to the flight) 10 -0.042599815875291824
            "sim/flightmodel/position/Q", # The pitch rotation rates (relative to the flight) 11 -17.799264907836914
            "sim/flightmodel/position/R", # The yaw rotation rates (relative to the flight) 12 5.893492698669434
            "sim/flightmodel/position/groundspeed", # 13 69.50841522216797
        ]
        return [x[0] for x in self.client.getDREFs(refs)]

    @catch_disconnects
    def get_state_vector(self):
        state = self.get_raw_state()
        state.append(self.dest_x - state[0]) # 6104.765625
        state.append(self.dest_y - state[1]) # -2369.8623046875
        state.append(self.dest_z - state[2]) # 2721.5224609375
        state.append(self.dest_airspeed - state[6]) # -69.50841522216797
        return state

    def get_normalized_state_vector(self):
        state = self.get_state_vector()

        # fix position. I havent seen abs(pos) > 10k so dividing by 20k
        state[0] = state[0]/20000
        state[1] = state[1]/20000
        state[2] = state[2]/20000

        state[14] = state[14]/20000
        state[15] = state[15]/20000
        state[16] = state[16]/20000

        # fix velocities. Assuming max 300 for now
        state[3] = state[3]/300
        state[4] = state[4]/300
        state[5] = state[5]/300
        state[6] = state[6]/300

        state[17] = state[17]/600

        state[13] = state[13]/300

        # Fix pitch, roll, and heading to -1 <-> 1
        state[7] = state[7] / 180.0
        state[8] = state[8] / 180.0
        # heading subtract 180 and then divide by the same og range 0 - 360
        state[9] = (state[9] - 180) / 180

        # Roll rates and stuff I am just going to assume have a max of +- 200
        state[10] = state[10] / 200
        state[11] = state[11] / 200
        state[12] = state[12] / 200

        for i in range(len(state)):
            if abs(state[i]) > 1:
                print "%d is bigger than it should be its value is %f" % (i, state[i])

        return state

    @catch_disconnects
    def get_reward(self):
        return self.reward_function(self)

    @catch_disconnects
    def get_action_vectors(self):
        '''
        The control surface values to set. `values` is a array containing up to
        6 elements. If less than 6 elements are specified or any elment is set to `-998`,
        those values will not be changed. The elements in `values` corespond to the
        following:
          * Latitudinal Stick [-1,1]
          * Longitudinal Stick [-1,1]
          * Rudder Pedals [-1, 1]
          * Throttle [-1, 1]
          * Gear (0=up, 1=down)
          * Flaps [0, 1]
          * Speedbrakes [-0.5, 1.5]
        '''
        latitude_opts = [-1, -0.5, 0.0, 0.5, 1]
        longitude_opts = [-1, 0.5, 0.0, 0.5, 1]
        rudder_opts = [-1, 0.5, 0.0, 0.5, 1]
        throttle_opts = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .99]
        gear_opts = [0]
        flap_opts = [0]
        speedbrake_opts = [0]

        action_vectors = []
        for lat in latitude_opts:
            for lon in longitude_opts:
                for rudder in rudder_opts:
                    for throttle in throttle_opts:
                        for gear in gear_opts:
                            # Ignoring flaps and speedbrakes
                            action_vectors.append([lat, lon, rudder, throttle, gear, 0, 0])

        return action_vectors

