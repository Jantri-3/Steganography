from mpmath import mp

def n_of_pi_decimals(n):
    n = int(n)

    # we set the number of decimal places +2  as "3." is "counted" aswell
    mp.dps = n + 2

    pi_value = str(mp.pi) #store Pi

    with open("npi_decimals.txt", "w+") as f: #write Pi into a file
        f.write(pi_value)

def frac_of_pi_decimals(frac,n):
    n = int(n)

    # we set the number of decimal places +2 "x." is "counted" aswell
    mp.dps = n + 2

    pi_value = str(mp.pi*frac) #store Pi * frac of day 

    with open("timepi_decimals.txt", "w+") as f: #write it onto corresponding file
        f.write(pi_value)