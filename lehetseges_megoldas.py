import mouse
x = 0
y = 0
for i in range(10):
    mouse.move(x,y, True, 1)
    x += 10
    y += 20
    
