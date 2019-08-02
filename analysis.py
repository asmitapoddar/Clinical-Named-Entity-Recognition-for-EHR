import numpy as np

print("TRUE POSITIVES -----------------")
f1 = open("/home/asmita/CliNER/truepositives_myner.txt")
f2 = open("/home/asmita/CliNER/truepositives_cliner")
f1 = f1.read().split()
f2 = f2.read().split()

print("MyNER:", len(f1))
print("CliNER:", len(f2))
f3 = set(f1)&set(f2)

f11 = [item for item in f1 if item not in f3]
f22 = np.setdiff1d(f2,f3)
f22 = [item for item in f2 if item not in f3]

print(f3)
print("Common:", len(f3))

print("Extra in myNER: ", len(f11), f11)
print("Extra in CliNER: ", len(f22), f22)


print("\nFALSE POSITIVES -----------------")

f1 = open("/home/asmita/CliNER/falsenpositives_myner")
f2 = open("/home/asmita/CliNER/falsenpositives_cliner")
f1 = f1.read().split()
f2 = f2.read().split()

print("MyNER:", len(f1))
print("CliNER:", len(f2))
f3 = set(f1)&set(f2)

f11 = [item for item in f1 if item not in f3]
f22 = np.setdiff1d(f2,f3)
f22 = [item for item in f2 if item not in f3]

print(f3)
print("Common:", len(f3))

print("Extra in myNER: ", len(f11), f11)
print("Extra in CliNER: ", len(f22), f22)

print("\nFALSE NEGATIVES -----------------")

f1 = open("/home/asmita/CliNER/falsenegatives_myner")
f2 = open("/home/asmita/CliNER/falsenegatives_cliner")
f1 = f1.read().split()
f2 = f2.read().split()

print("MyNER:", len(f1))
print("CliNER:", len(f2))
f3 = set(f1)&set(f2)

f11 = [item for item in f1 if item not in f3]
f22 = np.setdiff1d(f2,f3)
f22 = [item for item in f2 if item not in f3]

print(f3)
print("Common:", len(f3))

print("Extra in myNER: ", len(f11), f11)
print("Extra in CliNER: ", len(f22), f22)