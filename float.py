import argparse

# python3 ./float.py 150.000 --offset -50
#output 149.950 

python3 ./float.py 0.85350 --offset 150
#output 0.85500

# create an argument parser
parser = argparse.ArgumentParser()

# add the num argument
parser.add_argument("num", help="a floating point number with variable decimal places")

# add the offset argument
parser.add_argument("--offset", type=int, default=0, help="an integer offset to add to the number")

# parse the arguments
args = parser.parse_args()

# extract the decimal places from the input argument
decimal_places = len(args.num.split(".")[1])

# round the float to the required number of decimal places
num = round(float(args.num), decimal_places)

# add the offset to the rounded number
num += args.offset / (10 ** decimal_places)

# format the number to the required decimal places
output = "{:.{dp}f}".format(num, dp=decimal_places)

# print the output
print(output)
