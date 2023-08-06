#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 08:56:42 2021

@author: ekhaledian
"""


import pandas as pd


class translate6frames:
    
    def __init__(self, File , Type):
        self.File = File
        self.Type = Type

    
    class Fasta:
         def __init__(self, sequence , ID):
             self.sequence = sequence
             self.ID = ID
        
    def read_fasta(self):
        file1 = open(self.File, 'r')
        Lines = file1.readlines()
        
        List=[]
        seq=""
        ID=""
        for line in Lines:
            if line[0]=='>':
                List.append(self.Fasta(seq, ID))
                if line[-1:]=="\n":
                    ID=line[:-1]
                else:
                    ID=line
                seq=""
            else:
                if line[-1:]=="\n":
                    seq=seq+line[:-1]
                elif line[-1:] in ['A', 'C', 'G', 'T','U']:
                     seq=seq+line
        List.append(self.Fasta(seq, ID))
        List=List[1:]
        return List


    def replaceRev(self,Sequence):
        Type= self.Type.upper()
        if Type=="DNA":
            transTable = Sequence.maketrans("ATCG", "TAGC", "xyz")
        if Type=="RNA":
            transTable = Sequence.maketrans("AUCG", "UAGC", "xyz")
        Sequence = Sequence.translate(transTable)
        return Sequence
    

        
    
    #Sequence= Seq
    
    def Translate6Frames(self, Sequence):
        T= self.Type
        T= T.upper()
        if T=="DNA":
            gencode = {
              'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
              'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
              'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
              'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
              'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
              'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
              'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
              'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
              'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
              'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
              'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
              'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
              'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
              'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
              'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
              'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}
        if T=="RNA":
            gencode = {
          "UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L",
           "UCU":"S", "UCC":"s", "UCA":"S", "UCG":"S",
           "UAU":"Y", "UAC":"Y", "UAA":"_", "UAG":"_",
           "UGU":"C", "UGC":"C", "UGA":"_", "UGG":"W",
           "CUU":"L", "CUC":"L", "CUA":"L", "CUG":"L",
           "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P",
           "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
           "CGU":"R", "CGC":"R", "CGA":"R", "CGG":"R",
           "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M",
           "ACU":"T", "ACC":"T", "ACA":"T", "ACG":"T",
           "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K",
           "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R",
           "GUU":"V", "GUC":"V", "GUA":"V", "GUG":"V",
           "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A",
           "GAU":"D", "GAC":"D", "GAA":"E", "GAG":"E",
           "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G"}

        Sequence= Sequence.upper()
        Reverse= self.replaceRev(Sequence[::-1])
        S1, S2, S3, S4, S5, S6="","","","","",""
        sequence=str(Sequence[0:])
        S1= ''.join([gencode.get(sequence[3*i:3*i+3]) for i in range(len(sequence)//3)])
        sequence=Sequence[1:]
        S2= ''.join([gencode.get(sequence[3*i:3*i+3]) for i in range(len(sequence)//3)])
        sequence=Sequence[2:]
        S3= ''.join([gencode.get(sequence[3*i:3*i+3]) for i in range(len(sequence)//3)])
        rsequence= Reverse[0:]
        S4= ''.join([gencode.get(rsequence[3*i:3*i+3]) for i in range(len(rsequence)//3)])
        rsequence= Reverse[1:]
        S5= ''.join([gencode.get(rsequence[3*i:3*i+3]) for i in range(len(rsequence)//3)])
        rsequence= Reverse[2:]
        S6= ''.join([gencode.get(rsequence[3*i:3*i+3]) for i in range(len(rsequence)//3)])
        
        return S1, S2, S3, S4, S5, S6
    
    
    
    def Output(self):
        records= self.read_fasta()
        SequenceS=[]
        ID=[]
        Description=[]
        F1, F2, F3, F4, F5, F6, Seq=[],[],[],[],[],[],[]
        for i in range(len(records)):
            Seq= records[i].sequence
            ids= str(records[i].ID).split('-')
            ID.append(ids[-1])
            Description.append(str(records[i].ID))
            SequenceS.append(str(Seq))
            f1, f2, f3, f4, f5, f6=  self.Translate6Frames(str(Seq))
            F1.append(f1), F2.append(f2), F3.append(f3), F4.append(f4), F5.append(f5), F6.append(f6)
            
        
        SixFrames=pd.DataFrame()
        
        SixFrames["Sequence"]=SequenceS
        SixFrames["ID"]=ID
        SixFrames["Description"]=[Description[i][1:] for i in range(len(Description))]
        SixFrames["Frame1 Direct"]=F1
        SixFrames["Frame2 Direct"]=F2
        SixFrames["Frame3 Direct"]=F3
        SixFrames["Frame1 Reverse"]=F4
        SixFrames["Frame2 Reverse"]=F5
        SixFrames["Frame3 Reverse"]=F6
        
        name=str(self.File)
        SixFrames.to_csv(name+"SixFrames.csv")
        
        
        #save to 6 fasta files
        f_1 = open(name+"Frame1Direct.txt", "w")
        f_2 = open(name+"Frame2Direct.txt", "w")
        f_3 = open(name+"Frame3Direct.txt", "w")
        f_4 = open(name+"Frame1Reverse.txt", "w")
        f_5 = open(name+"Frame2Reverse.txt", "w")
        f_6 = open(name+"Frame3Reverse.txt", "w")


        for i in range(len(SixFrames)):
            f_1.write(">"+SixFrames["Description"][i]+"\n")
            f_2.write(">"+SixFrames["Description"][i]+"\n")
            f_3.write(">"+SixFrames["Description"][i]+"\n")
            f_4.write(">"+SixFrames["Description"][i]+"\n")
            f_5.write(">"+SixFrames["Description"][i]+"\n")
            f_6.write(">"+SixFrames["Description"][i]+"\n")
            f_1.write(SixFrames["Frame1 Direct"][i]+"\n")
            f_2.write(SixFrames["Frame2 Direct"][i]+"\n")
            f_3.write(SixFrames["Frame3 Direct"][i]+"\n")
            f_4.write(SixFrames["Frame1 Reverse"][i]+"\n")
            f_5.write(SixFrames["Frame2 Reverse"][i]+"\n")
            f_6.write(SixFrames["Frame3 Reverse"][i]+"\n")
        
        f_1.close()
        f_2.close()
        f_3.close()
        f_4.close()
        f_5.close()
        f_6.close()
            

if __name__ == "__main__":
	pass           
	# p1 = translate6frames("test.fa", "DNA")
	# p1.Output()

