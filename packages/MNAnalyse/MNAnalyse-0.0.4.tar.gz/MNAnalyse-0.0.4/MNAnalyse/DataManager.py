import pymysql
import NeuronInfo
import Sample
import Anatation

class DataManager:
    def __init__(self):
        self.host='10.10.48.110';
        self.user='readonly';
        self.password='123456';
        self.database='bap';
        self.connect();
        self.anatation=Anatation.Anatation()
        
        
    def connect(self):
        self.connector = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database);
        self.cursor = self.connector.cursor()
        
    def GetHIPSamplesID(self):
        self.cursor.execute("call getHIPSamples()");
        samples=[]
        results= self.cursor.fetchall();
        for sample in results:
            samples.append(Sample.Sample(sample[0]))
        return samples
        
      
    def GetNeurons(self,sample):
        self.cursor.execute("call getNeurons("+sample.id+")");
        results = self.cursor.fetchall()
        neurons=[]
        for neuronstr in results:
            neurons.append(NeuronInfo.NeuronInfo(neuronstr))
        return neurons