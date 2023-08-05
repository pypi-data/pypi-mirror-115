#etl
#class to process columns
class etl:
  
    def __init__(self, df):
      self.df = df
    
    #lag and compare
    def col_lagcompare(self):
      return print('test')
    
    #lag chosen col x times
    def col_lagsum(self, partition, order, col, times):
      #insert try catch and coltype checks
    
      #assign partition
      w = Window.partitionBy(partition).orderBy(order).rowsBetween(-__builtin__.abs(times - 1), 0)

      self.df = self.df.withColumn(col + '_' + str(times),sum(col).over(w))
    
    #return df after applying methods
    def df_returndf(self):
      return self.df
        