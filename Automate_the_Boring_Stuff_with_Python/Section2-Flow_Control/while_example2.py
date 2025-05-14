spam = 0
while spam < 5:
    spam = spam + 1
    if spam == 3:
        continue
    print('spam is ' + str(spam))
# The code above prints the value of `spam` from 1 to 5, but skips the print statement when `spam` is equal to 3. The `continue` statement causes the loop to skip the current iteration and move to the next one.