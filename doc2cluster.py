import re
import sys

class Info:
    def __init__(self,docid,idnum,rank):
        self.docid = docid
        self.idnum = idnum
        self.rank = rank
    

def doc2clus(file):
    doc = re.compile('(.+)?th doc\\:')
    infos = []
    n = 0
    for line in file:
        t = doc.search(line)
        if t:
            buf = line.split()
            docid = int(buf[0])
            idnum = int(buf[4])
            n = 1
            continue
        if n == 1:
            rank = line.split()
            info = Info(docid,idnum,rank)
            n = 0
            print(docid,idnum,rank)
            infos.append(info)
    return(infos)
        

def main():
    with open('output_all.txt','r') as file:
        infos = doc2clus(file)

    rank_nums = []
    rank_probs = []
    print("input accumurative probability limitaion")
    prob_lim = float(sys.stdin.readline())
    print("input differrence probability of 1th and 2th class")
    sub_lim = float(sys.stdin.readline())
    for info in infos:
        n = len(info.rank)
        prob = 0.0
        rank_num = []
        rank_prob = []
        rank_num.append(info.idnum)
        for i in range(1,n-2,2):
            if i ==1:
                rank_num.append(info.rank[i-1])
                rank_prob.append(float(info.rank[i]))
                prob += float(info.rank[i])
                continue
            prob += float(info.rank[i])
            sub = abs(float(info.rank[i]) - float(info.rank[i+2]))
            if prob < prob_lim and sub < sub_lim: 
                rank_num.append(info.rank[i-1])
                rank_prob.append(float(info.rank[i]))

        rank_nums.append(rank_num)
        rank_probs.append(rank_prob)

    send = [rank_nums,rank_probs]

    return(send)
    
            
if __name__ == '__main__':
    send = main()
    rank_nums = send[0]
    rank_probs = send[1]
    print(rank_nums)
    print(rank_probs)
    with open('cluster.txt','w') as f:
        print('docid','\t','clusternum', file=f)
    for i,rank_num in enumerate(rank_nums):
        for j,rank in enumerate(rank_num):
            if rank == rank_num[-1]:
                with open('cluster.txt','a') as f:
                    print(rank,file=f,end='\t')
            else:
                with open('cluster.txt','a') as f:
                    print(rank,file=f,end='\t')
        for k in range(j):
            if k == j-1:
                with open('cluster.txt','a') as f:
                    print(rank_probs[i][k],file=f)
            else:
                with open('cluster.txt','a') as f:
                    print(rank_probs[i][k],file=f,end='\t')
