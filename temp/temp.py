def collinearity(x1, y1, x2, y2):
    if x2 != 0:
        k1 = x1 % x2
        print(k1)
        if k1 == 0:
            ka = True
        else:
            ka = False
    else:
        k1 = 0
        ka = True
    
    if y2 != 0:
        k2 = y1 %y2
        if k2 == 0:
            kb = True
        else:
            kb = False
    else:
        k2 = 0
        kb = True
        
    print(ka, kb)
    if ka == True and kb == True:
        return True
    else:
        return False
    
    

print("Final",collinearity(3, 1, 2, 1))