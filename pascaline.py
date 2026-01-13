def add(numbre1, numbre2):
    result = numbre1 + numbre2
    print (result)

def sub(numbre1, numbre2):
    result = numbre1 - numbre2
    print (result)

def mult(numbre1, numbre2):
    result = numbre1 * numbre2
    print (result)

def div(numbre1, numbre2):
    if numbre2 == 0:
        print("division by 0 impossible")
    else:
        result = numbre1 / numbre2
        print (int(result))
    
while True:
    
    try:
           
        numbre1 = int(input("entre a numbre :"))

        operation = str(input("what operation you wanna use :"))

        numbre2 = int(input("entre a numbre :"))

        if operation == "+":
                add(numbre1,numbre2)
        elif operation == "-":
                sub(numbre1,numbre2)
        elif operation == "*":
                mult(numbre1,numbre2)
        elif operation == "/":
                div(numbre1,numbre2)
        else:
                print("\n opps wrong choice!")

    except KeyboardInterrupt:
          print("\n stopped by user!")
          break
