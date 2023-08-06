import math


class JoystickJhr:

    def __init__(self):
        self.circle = None
        self.joyPoint = None
        # ancho y alto de joystick
        self.widthJ = 0
        self.heightJ = 0
        # radio del circulo interno porcentaje del grande
        self.radioInter = 0.3
        self.radioHijo = 0
        # radio padre
        self.radioPadre = 0
        self.centros = 0
        self.angle = 0

    def joy(self, canvas, widthJ, heightJ, posX, posY,radioHijo):
        self.radioInter = radioHijo
        self.widthJ = widthJ
        self.heightJ = heightJ
        # radio hijo ancho/2 * porcentaje
        self.radioPadre = (posX + widthJ) / 2
        self.radioHijo = self.radioPadre * self.radioInter
        self.centros = [posX + widthJ / 2, posY + heightJ / 2]
        # draw circle padre
        self.circle = canvas.create_oval(posX, posY, posX + widthJ, posY + heightJ, outline="white", width=2)
        self.joyPoint = canvas.create_oval(self.centros[0] - self.radioHijo, self.centros[1] - self.radioHijo,
                                           self.centros[0] + self.radioHijo, self.centros[1] + self.radioHijo,
                                           fill="red")

    def moveJoy(self, canvas, event):
        x = event.x
        y = event.y

        xi_new = x + self.radioHijo
        yi_new = y + self.radioHijo
        xf_new = x - self.radioHijo
        yf_new = y - self.radioHijo

        # center position y normalizo a cero
        # xp = (xi_new + xf_new) / 2 - canvas.winfo_width() / 2
        # yp = (yi_new + yf_new) / 2 - canvas.winfo_height() / 2

        xp = (xi_new + xf_new) / 2 - canvas.winfo_width() / 2
        yp = (yi_new + yf_new) / 2 - canvas.winfo_height() / 2

        if (xp == 0):
            xp = 0.00001

        valueTan = abs(yp / xp)
        angle = math.atan(valueTan)

        # calculo la distancia entre los puntos y el centro de la pista
        dis = math.sqrt(xp * xp + yp * yp)

        if dis > self.radioPadre/2:
            if xp > 0 and yp > 0:
                xi_new = math.cos(angle) * self.radioPadre/2 + canvas.winfo_width() / 2 - self.radioHijo
                yi_new = math.sin(angle) * self.radioPadre/2 + canvas.winfo_height() / 2 - self.radioHijo
                xf_new = xi_new + self.radioHijo * 2
                yf_new = yi_new + self.radioHijo * 2
            else:
                if xp > 0 and yp < 0:
                    xi_new = math.cos(angle) * self.radioPadre/2 + canvas.winfo_width() / 2 - self.radioHijo
                    yi_new = -math.sin(angle) * self.radioPadre/2 + canvas.winfo_height() / 2 - self.radioHijo
                    xf_new = xi_new + self.radioHijo * 2
                    yf_new = yi_new + self.radioHijo * 2
                else:
                    if xp < 0 and yp > 0:
                        xi_new = -math.cos(angle) * self.radioPadre/2 + canvas.winfo_width() / 2 - self.radioHijo
                        yi_new = math.sin(angle) * self.radioPadre/2 + canvas.winfo_height() / 2 - self.radioHijo
                        xf_new = xi_new + self.radioHijo * 2
                        yf_new = yi_new + self.radioHijo * 2
                    else:
                        if xp < 0 and yp < 0:
                            xi_new = -math.cos(
                                angle) * self.radioPadre/2 + canvas.winfo_width() / 2 - self.radioHijo
                            yi_new = -math.sin(
                                angle) * self.radioPadre/2 + canvas.winfo_height() / 2 - self.radioHijo
                            xf_new = xi_new + self.radioHijo * 2
                            yf_new = yi_new + self.radioHijo * 2

        self.getAngle(xp, yp)
        # get angle with cuadrante
        canvas.coords(self.joyPoint, xi_new, yi_new, xf_new, yf_new)

    def returnCenterJoy(self, canvas, event):
        self.angle = 0
        canvas.coords(self.joyPoint, self.centros[0] - self.radioHijo, self.centros[1] - self.radioHijo,
                      self.centros[0] + self.radioHijo, self.centros[1] + self.radioHijo)

    def movement(self, canvas):
        canvas.bind_all('<B1-Motion>', lambda e: self.moveJoy(canvas, e))
        # motion up
        canvas.bind_all('<ButtonRelease-1>', lambda e: self.returnCenterJoy(canvas, e))

    # canvas.bind_all('<B1-Up>',lambda e: self.returnCenterJoy(canvas,e))
    def getAngle(self, xp, yp):
        if xp > 0 and yp > 0:
            self.angle = 360 - math.degrees(math.atan(yp / xp))
        else:
            if xp > 0 and yp < 0:
                self.angle = abs(math.degrees(math.atan(yp / xp)))
            else:
                if xp < 0 and yp > 0:
                    self.angle = 180 - math.degrees(math.atan(yp / xp))
                else:
                    if xp < 0 and yp < 0:
                        self.angle = 180 - math.degrees(math.atan(yp / xp))

    def angle_joy(self):
        return self.angle
