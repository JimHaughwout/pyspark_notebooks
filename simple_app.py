"""
Modified SimpleApp.py example
"""
import findspark
findspark.init()

from pyspark import SparkContext

logFile = "declaration.txt"  # Should be some file on your system


sc = SparkContext("local", "Simple App")
logData = sc.textFile(logFile).cache()

numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()

print "*"*80
print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
print "*"*80
