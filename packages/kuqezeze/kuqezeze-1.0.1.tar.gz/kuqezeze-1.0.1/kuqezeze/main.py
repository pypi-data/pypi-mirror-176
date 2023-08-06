from kuqezeze.guess_module import guess_the_munber

range_nr = int(input("Vendos range nga 1 deri ne n: "))
user_nr = int(input("Mendoni nje number: "))

rezult = guess_the_munber(user_nr, range_nr)
print(rezult)