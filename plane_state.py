from time import sleep
import xpc

class PlaneState(object):

    # Should we use lat, long, elevation or x,y,z?
    def __init__(self, _dest_x, _dest_y, _dest_z, _t_vel_x, _t_vel_y, _t_vel_z, _client=xpc.XPlaneConnect()):
        self.client = _client
        self.dest_x = _dest_x
        self.dest_y = _dest_y
        self.dest_z = _dest_z
        self.t_vel_x = _t_vel_x
        self.t_vel_y = _t_vel_y
        self.t_vel_z = _t_vel_z

    def get_raw_state(self):
        '''
        get_raw_state returns a state vector containing the following in order
        '''
        refs = [
            "sim/flightmodel/position/local_x", # X is like lat?
            "sim/flightmodel/position/local_y", # Y is like long?
            "sim/flightmodel/position/local_z", # Z is like altitude?
            "sim/flightmodel/position/true_theta", # Pitch
            "sim/flightmodel/position/true_phi", # Roll
            "sim/flightmodel/position/true_psi", # Heading
            "sim/flightmodel/position/P", # The roll rotation rates (relative to the flight)
            "sim/flightmodel/position/Q", # The pitch rotation rates (relative to the flight)
            "sim/flightmodel/position/R", # The yaw rotation rates (relative to the flight)
            "sim/flightmodel/position/groundspeed",
            "sim/flightmodel/position/true_airspeed",
            "sim/flightmodel/position/local_vx",
            "sim/flightmodel/position/local_vy",
            "sim/flightmodel/position/local_vz",
        ]
        return [x[0] for x in self.client.getDREFs(refs)]
