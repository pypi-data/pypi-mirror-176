def calcular(a, b, c):
    if (a == 0):
        a = 1
    if (b == 0):
        b = 1
    if (b == 0):
        b = 1

    D = (b**2 - 4*a*c)
    x1 = (-b + D**(1/2)) / (2*a)
    x2 = (-b - D**(1/2)) / (2*a)

    print(f"Valor de x': {x1} x'':{x2}")