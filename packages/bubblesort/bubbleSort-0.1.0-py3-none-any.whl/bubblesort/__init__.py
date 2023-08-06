__version__ = '0.1.0'
def bubbleSort(lists):
    n = len(lists)
 
    # Traverse through all array elements
    for i in range(n):
 
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
          print(j)

          #Checks if the number prior is larger than after
          if lists[j] > lists[j+1]:
            #changes the order of of the first number to second and              second to first  
            lists[j], lists[j+1] = lists[j+1], lists[j]