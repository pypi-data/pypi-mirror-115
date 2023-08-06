import numpy as np
import time, os

class Donut():
    def __init__(self, _screen_size=40, _frame_rate=60, _theta_spacing=0.07, _phi_spacing=0.02) -> None:
        self.screen_size = _screen_size
        self.theta_spacing = _theta_spacing
        self.phi_spacing = _phi_spacing
        self.frame_rate = _frame_rate

        self.illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

        self.A = 1
        self.B = 1
        self.R1 = 1
        self.R2 = 2
        self.K2 = 5
        self.K1 = self.screen_size * self.K2 * 3 / (8 * (self.R1 + self.R2))


    def render_frame(self, A: float, B: float) -> np.ndarray:
        """
        Returns a frame of the spinning 3D Donut3d.
        Based on the pseudocode from: https://www.a1k0n.net/2011/07/20/donut-math.html
        """
        cos_A = np.cos(A)
        sin_A = np.sin(A)
        cos_B = np.cos(B)
        sin_B = np.sin(B)

        output = np.full((self.screen_size, self.screen_size), " ")  # (40, 40)
        zbuffer = np.zeros((self.screen_size, self.screen_size))  # (40, 40)

        cos_phi = np.cos(phi := np.arange(0, 2 * np.pi, self.phi_spacing))  # (315,)
        sin_phi = np.sin(phi)  # (315,)
        cos_theta = np.cos(theta := np.arange(0, 2 * np.pi, self.theta_spacing))  # (90,)
        sin_theta = np.sin(theta)  # (90,)
        circle_x = self.R2 + self.R1 * cos_theta  # (90,)
        circle_y = self.R1 * sin_theta  # (90,)

        x = (np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x) - circle_y * cos_A * sin_B).T  # (90, 315)
        y = (np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x) + circle_y * cos_A * cos_B).T  # (90, 315)
        z = ((self.K2 + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A).T  # (90, 315)
        ooz = np.reciprocal(z)  # Calculates 1/z
        xp = (self.screen_size / 2 + self.K1 * ooz * x).astype(int)  # (90, 315)
        yp = (self.screen_size / 2 - self.K1 * ooz * y).astype(int)  # (90, 315)
        L1 = (((np.outer(cos_phi, cos_theta) * sin_B) - cos_A * np.outer(sin_phi, cos_theta)) - sin_A * sin_theta)  # (315, 90)
        L2 = cos_B * (cos_A * sin_theta - np.outer(sin_phi, cos_theta * sin_A))  # (315, 90)
        L = np.around(((L1 + L2) * 8)).astype(int).T  # (90, 315)
        mask_L = L >= 0  # (90, 315)
        chars = self.illumination[L]  # (90, 315)

        for i in range(90):
            mask = mask_L[i] & (ooz[i] > zbuffer[xp[i], yp[i]])  # (315,)

            zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
            output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

        return output


    def pprint(self, array: np.ndarray) -> None:
        """Pretty print the frame."""
        os.system('cls' if os.name=='nt' else 'clear')
        print(*[" ".join(row) for row in array], sep="\n")

    def run(self):
        while True:
            for _ in range(self.screen_size * self.screen_size):
                self.A += self.theta_spacing
                self.B += self.phi_spacing
                print("\x1b[H")
                self.pprint(self.render_frame(self.A, self.B))
                time.sleep(1/self.frame_rate)
