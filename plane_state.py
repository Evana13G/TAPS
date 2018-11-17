from time import sleep
import xpc

class PlaneState(object):

    # Should we use lat, long, elevation or x,y,z?
    def __init__(self, dest_x, dest_y, dest_z, dest_airspeed):
        self.client = xpc.XPlaneConnect()
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.dest_z = dest_z
        self.dest_airspeed = dest_airspeed

    def get_raw_state(self):
        '''
        get_raw_state returns a state vector containing the following in order
        '''
        refs = [
            "sim/flightmodel/position/local_x", # X is like lat?
            "sim/flightmodel/position/local_y", # Y is like long?
            "sim/flightmodel/position/local_z", # Z is like altitude?
            "sim/flightmodel/position/local_vx",
            "sim/flightmodel/position/local_vy",
            "sim/flightmodel/position/local_vz",
            "sim/flightmodel/position/true_airspeed",
            "sim/flightmodel/position/true_theta", # Pitch
            "sim/flightmodel/position/true_phi", # Roll
            "sim/flightmodel/position/true_psi", # Heading
            "sim/flightmodel/position/P", # The roll rotation rates (relative to the flight)
            "sim/flightmodel/position/Q", # The pitch rotation rates (relative to the flight)
            "sim/flightmodel/position/R", # The yaw rotation rates (relative to the flight)
            "sim/flightmodel/position/groundspeed",
        ]
        return [x[0] for x in self.client.getDREFs(refs)]

    def get_state_vector(self):
        state = self.get_raw_state()
        state.append(self.dest_x - state[0])
        state.append(self.dest_y - state[1])
        state.append(self.dest_z - state[2])
        state.append(self.dest_airspeed - state[6])
        return state

    def get_reward(self):
        state = self.get_state_vector()
        multiplier = 0
        if abs(state[-2]) < 25 and abs(state[-3]) < 25 and abs(state[-4]) < 25:
            multiplier = 1
        else:
            multiplier = .99 ** ((state[-2] + state[-3] + state[-4])/5)
        if abs(state[-1]) < 1:
            return multiplier * 100
        return -1

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
        latitude_opts = [-1, 0, 1]
        longitude_opts = [-1, 0, 1]
        rudder_opts = [-1, 0, 1]
        throttle_opts = [0, .2, .4, .6, .8]
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

