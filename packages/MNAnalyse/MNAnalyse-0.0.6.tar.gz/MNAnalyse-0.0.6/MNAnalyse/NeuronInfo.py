    
class NeuronInfo:
    name=''
    sampleid=''
    region=''
    position=''
    hemisphere=''
    type=''
    exclude=''
    comment=''
    properties=''
    def __init__(self,neuronstr):
        self.name =neuronstr[1] if not neuronstr[1] is None else ''
        self.sampleid =neuronstr[2] if not neuronstr[2] is None else ''
        self.region = neuronstr[4] if not neuronstr[4] is None else ''
        self.position = neuronstr[6] if not neuronstr[6] is None else ''
        self.hemisphere =neuronstr[7] if not neuronstr[7] is None else ''
        self.type = neuronstr[8] if not neuronstr[8] is None else ''
        self.exclude = neuronstr[9] if not neuronstr[9] is None else ''
        self.comment =neuronstr[10] if not neuronstr[10] is None else ''
        self.properties = neuronstr[11] if not neuronstr[11] is None else ''
        
        pass
    def __str__(self):
        return 'name: '+self.name+'\t'+\
        'sampleid: '+self.sampleid+'\t'\
        'region: '+self.region+'\t'+\
        'position: '+self.position+'\t'+\
        'hemisphere: '+self.hemisphere+'\t'+\
        'type: '+self.type+'\t'+\
        'exclude: '+self.exclude+'\t'+\
        'comment: '+self.comment+'\t'+\
        'properties: '+str(self.properties)

    