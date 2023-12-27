from sys import argv
from pickle import load
from statistics import mean, stdev, median
from scipy.stats import sem
import matplotlib.pyplot as plt

#   This script plots two averaged traces and their difference trace (subtracts the traces).
#   COMMAND-LINE ARGUMENTS: python subtract.py path1 path2 trace_length 

def main():

    if len(argv) != 4:
        exit("Usage: python subtract.py [path1] [path2] [trace_length]")
    
    paths = [argv[1], argv[2]]

    for path in paths:
        try:
            with open(path, "rb") as f:
                pass
        except FileNotFoundError:
            exit(f"{path} was not found.")

    # Parameters for the plot
    traceLength = int(argv[3])
    timeAxis = range(traceLength * 1000)
    infoTag = f"Average difference trace: '{formattedName(paths[1])}' - '{formattedName(paths[0])}' - {traceLength} seconds"

    # Plot two original traces and save their average traces in list for later use
    averagedTraces = []
    for path in paths:
        traceSet, site, numRuns = unpickle(path)
        averagedTrace = averager(traceSet)
        averagedTraces.append(averagedTrace)
        plt.plot(timeAxis, averagedTrace, label=formattedName(site))
        descriptors(averagedTrace, site)

    # Plot difference trace and print descriptors
    differenceTrace = subtractTraces(averagedTraces[0], averagedTraces[1])
    plt.plot(timeAxis, differenceTrace, label="Difference", color="green")
    descriptors(differenceTrace, f"Difference between {formattedName(paths[1])} and {formattedName(paths[0])}")

    # Plot's features and labels
    plt.xlabel("Time (ms)")
    plt.ylabel("Averaged counter values")
    plt.title(infoTag + f" - {numRuns} run(s)")
    plt.legend(loc="lower right")
    plt.grid("both")

    plt.show()

def averager(traceSet):

    # Calculate # of elements in a list within traceSet; create list with that size; traceSet[0] is the first
    # trace in the list and SHOULD have the same size as the averaged trace and all the other traces. 
    size = len(traceSet[0])
    averagedTrace = list(range(size))

    # Iterate through all indexes; average the counter values at each index in all traces in traceSet
    for index in range(size):
        sum = 0
        for trace in traceSet:
            sum += trace[index]
        averagedTrace[index] = sum / len(traceSet)

    return averagedTrace

def descriptors(trace, filePath):

    print()
    print(filePath)

    # 'trace' must always be one trace, ideally an averaged trace
    print(f"Mean: {round(mean(trace))} ± {round(sem(trace))}")
    print(f"Median: {round(median(trace))}")
    print(f"Standard deviation: {round(stdev(trace))}")
    print()

def formattedName(site):

    # Splits, say "https://cnn.com", by / and
    # then splits cnn.com (last element, hence -1) by . and returns the first element in the resulting list. Works the same for custom trace files.

    return site.split("/")[-1].split(".")[0]

def subtractTraces(trace1, trace2):

    size = len(trace1) 
    resultTrace = list(range(size))
    for index in range(size): 
        resultTrace[index] = trace2[index] - trace1[index]

    return resultTrace

def unpickle(traceFileName):

    traceFileHandle = open(traceFileName, "rb")
    traceSet = []
    numRuns = 0

    # Call pickle.load multiple times to append multiple traces to the trace set
    # TraceSet is is used by other functions and will always be the first index of the return value of the unpickle function. 
    while True:
        try:
            trace, site = load(traceFileHandle) 
            traceSet.append(trace[0])
            numRuns += 1
        except EOFError:
            break
        traceFileHandle.close()
        return traceSet, site, numRuns

if __name__ == "__main__":
    main()
