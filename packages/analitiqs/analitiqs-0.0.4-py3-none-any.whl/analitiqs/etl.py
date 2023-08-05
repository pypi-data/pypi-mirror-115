#etl
#class to process columns
class cols:
  
    def __init__(self, df):
      self.df = df
    
    #lag and compare
    def lagcompare(self):
      return print('test')
    
    #lag chosen col x times
    def lagsum(self, partition, order, col, times):
      #insert try catch and coltype checks
    
      #assign partition
      w = Window.partitionBy(partition).orderBy(order).rowsBetween(-__builtin__.abs(times - 1), 0)

      self.df = self.df.withColumn(col + '_' + str(times),sum(col).over(w))
    
    #return df after applying methods
    def returndf(self):
      return self.df
        