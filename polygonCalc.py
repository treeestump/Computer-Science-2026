#I'm just using slang guys

sides = float(input("Sides? "))
side_length = float(input("Side length? "))
apothem = float(input("Apothem? "))   

perim = sides * side_length
area = perim * apothem / 2

print(f"Area = {area}")
print(f"Perimiter = {perim}")