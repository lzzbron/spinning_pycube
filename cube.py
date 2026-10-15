import math
import time
import sys

a, b, c = 0, 0, 0 #names a b and c, to be redfined later

cubeWidth = 20 #adjust width if you want
background = " "
width, height = 160, 44
buffer = []
z_buffer = []

distance = 100 
K1 = 40
horizontalOffset = 0


incrementSpeed = 0.95 #going over 1 can cause more buffer collision, 
#change this to make it spin slower or faster

#basic 3d rotation matrix equations, using i j and k as points
#-----------------------------------------------------------------------------------------------------
def calculateX(i, j, k):
    return(
        j * math.sin(a) * math.sin(b) * math.cos(c) - k * math.cos(a) * math.sin(b) * math.cos(c) +
        j * math.cos(a) * math.sin(c) + k * math.sin(a) * math.sin(c) + i * math.cos(b) * math.cos(c)
    )
def calculateY(i, j, k):
    return(
        j * math.cos(a) * math.cos(c) + k * math.sin(a) * math.cos(c) -
        j * math.sin(a) * math.sin(b) * math.sin(c) + k * math.cos(a) * math.sin(b) * math.sin(c) -
        i * math.cos(b) * math.sin(c)
    )
def calculateZ(i, j, k):
    return(
        k * math.cos(a) * math.cos(b) - j * math.sin(a) * math.cos(b) + i * math.sin(b)
    )

def calcForSurface(cubeX, cubeY, cubeZ, ch):
    global z_buffer, buffer

    x = calculateX(cubeX, cubeY, cubeZ)
    y = calculateY(cubeX, cubeY, cubeZ)
    z = calculateZ(cubeX, cubeY, cubeZ) + distance
    ooz = 1/z
    xp = int(width/2 + horizontalOffset + K1 * ooz * x * 2)
    yp = int(height/2 + K1 * ooz * y)

    if (0 <= xp < width and 0 <= yp < height):
        idx = xp + yp * width
        if (0 <= idx < len(z_buffer)):
            if (ooz > z_buffer[idx]):
                z_buffer[idx] = ooz
                buffer[idx]= ch
                
def main(): 
    print("\x1b[23]")
    while(True):
        global a, b, c
        global buffer, z_buffer
        buffer = [background] * (width * height)
        z_buffer = [0.0] * (width * height)
        
        cubeWidth = 23 # adjust width if u desire
        horizontalOffset = -2 * cubeWidth
        #first cube
        cubeX = -cubeWidth
        while (cubeX < cubeWidth):
            cubeY = -cubeWidth

            while (cubeY < cubeWidth):
                calcForSurface(cubeX, cubeY, -cubeWidth, '@')
                calcForSurface(cubeWidth, cubeY, cubeX, '*')
                calcForSurface(-cubeWidth, cubeY, -cubeX, '~')
                calcForSurface(-cubeX, cubeY, cubeWidth, '#')
                calcForSurface(cubeX, -cubeWidth, -cubeY, ';')
                calcForSurface(cubeX, cubeWidth, cubeY, '+')      
                cubeY += incrementSpeed
            cubeX += incrementSpeed

        print("\x1b[H")
        k = int(0)
        while (k < (width*height)):
            row_ch = buffer[k:k+width]
            row_str = "".join(row_ch)
            print(row_str)

            k += width
            
        # A B and C are the values for the velocity for the rotation of each axis. don't make the c 
        #way too high or it will just spin all over the place unless you want to see it go crazy :)
        a += 0.05
        b += 0.05 
        c += 0.01
        time.sleep(0.008) #framerate
    
    return 0
main()
