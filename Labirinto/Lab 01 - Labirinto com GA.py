from random import shuffle, randrange, randint, choice, random
import Queue as Q
import math

def make_maze(w = 8, h = 3):
	vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
	nowalls = []
	
	def walk(x, y):
		vis[x][y] = 1
 
		d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
		shuffle(d)
		for (xx, yy) in d:
			if vis[xx][yy]: continue
			nowalls.append((x,y,xx,yy))
			walk(xx, yy)
 
	walk(randrange(h), randrange(w))
	return(nowalls)

def draw_maze(nowalls, w = 8, h = 3):
	ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
	hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

	for (x,y,xx,yy) in nowalls:
		#print(x,y,xx,yy)
		if xx == x: ver[x][max(y, yy)] = "   "
		if yy == y: hor[max(x, xx)][y] = "+  "

	for (a, b) in zip(hor, ver):
		print(''.join(a + ['\n'] + b))		

def posabs(x, y, w):
	return(x*w+y)

def posidx(pos, w):
	return(pos//w, pos%w)

def nowallsabs(nowallsidx, w = 8):
        return [(posabs(x,y,w), posabs(xx,yy,w)) for (x,y,xx,yy) in nowallsidx]

def split_list(lista, idx):
        l1=[]
        l2=[]
        for i in range(idx):
             l1+=[lista[i]]
        for i in xrange(idx,len(lista),1):
             l2+=[lista[i]]
        return [l1, l2]

def caminho_aberto(nwabs, a, b):
        for i, j in enumerate(nwabs):
            if j == (a,b) or j == (b,a):
                return 1
        return 0

def posfinal(crom, nwabs, ini, obj, w, h):
        atual = ini
        for x in xrange(0,len(crom),2):
                pos_des=0
                # Norte:
                if crom[x]==0 and crom[x+1]==0:
                        if not (atual/w == 0):
                                pos_des=atual-w
                                if caminho_aberto(nwabs,atual,pos_des):
                                        atual=pos_des
##                        print 'norte'
                # Sul:
                if crom[x]==0 and crom[x+1]==1:
                        if not (atual/w==h-1):
                                pos_des=atual+w
                                if caminho_aberto(nwabs,atual,pos_des):
                                        atual=pos_des
##                        print 'sul'
                # Leste:
                if crom[x]==1 and crom[x+1]==0:
                        if not(atual%w==w-1):
                                pos_des=atual+1
                                if caminho_aberto(nwabs,atual,pos_des):
                                        atual=pos_des
##                        print 'leste'
                # Oeste:
                if crom[x]==1 and crom[x+1]==1:
                        if not (atual%w==0):
                                pos_des=atual-1
                                if caminho_aberto(nwabs,atual,pos_des):
                                        atual=pos_des
##                        print 'oeste'
        return atual

def croms_ini(tc, pop_ini):
        croms=[]
        for _ in range(pop_ini):
                crom=[]
                for _ in range(tc):
                      crom+=[randint(0,1)]
                croms+=[crom]
        return croms

def cruzamento(n_filhos, tc, X, Y):
        filhos=[]
        for _ in xrange(0,n_filhos,2):
                # Garante que o corte garantirá ao menos um bit trocado:
                p = randint(1,tc-2)
                X_=split_list(X,p)
                Y_=split_list(Y,p)
                F1=X_[0] + Y_[1]
                F2=Y_[0] + X_[1]
                filhos+= [F1] + [F2]
        return filhos

def calc_fitness(croms, ini, obj, w, h):
        fitness=[]
        obj_ = posidx(obj,w)
        for i in range(len(croms)):
                croms[i]
                f = posfinal(croms[i], nwabs, ini,obj,w,h)
                f_ = posidx(f,w)
                x = f_[0]-obj_[0]
                y = f_[1]-obj_[1]
                fitness+=[(w-1)*(h-1)-(abs(x)+abs(y))]
        return fitness

def calc_prob(fitness):
        prob=[]
        acum=0.0
        total=sum(fitness)
        for i in range(len(fitness)):
                acum+=float(fitness[i])/total
                prob+=[acum]
        return prob

def roleta(croms, prob, croms_passados):
        novos_croms=[]
        for _ in range(croms_passados):
                r = random()
                for i in range(len(prob)):
                        if r <= prob[i]:
                                novos_croms+=[croms[i]]
                                break 
        return novos_croms

def GA(ini, obj,w,h):
        # Parâmetros:
        # Tamanho do Cromossomo (Pior caso (h*w>2)):
        tc=(w*h-1)*2
        # População Inicial:
        n_pop_ini=50
        # Número de filhos resultantes do Cruzamento:
        n_filhos=2*3
        # Número máximo de gerações:
        max_geracoes=100
        geracao=0
        # Número de cromossos passados por geração:
        croms_passados=n_pop_ini*3/4
        
        # ==> POPULAÇÃO INICIAL:
        croms=croms_ini(tc,n_pop_ini)

        while True:
                # ==> CRUZAMENTO:
                X = choice(croms)
                Y=choice(croms)
                filhos=cruzamento(n_filhos, tc, X, Y)
                croms+=filhos

                # ==> MUTAÇÃO:
                # i: index garante que os novos filhos não sofrerão mutação
                i = randint(0,len(croms)-n_filhos-1)
                j = randint(0,tc-1)
                if croms[i][j]==0: croms[i][j]=1
                else: croms[i][j]=0 

                # ==> SELEÇÃO:
                fitness=calc_fitness(croms,ini,obj,w,h)
                fit_max=(w-1)*(h-1)
                if fit_max in fitness:
                        i=fitness.index(fit_max)
                        return (True, croms[i], geracao)

                # Remove cromossomos com fitness=0:
                while 0 in fitness:
                        idx=fitness.index(0)
                        del fitness[idx]
                        del croms[idx]

                # Distribuição de probabilidade:
                prob = calc_prob(fitness)
                # Roleta:
                croms = roleta(croms, prob, croms_passados)
        
                # ==> CRITÉRIO DE PARADA:
                if geracao>=max_geracoes: return (False, [], geracao)

                geracao+=1

w0=4
h0=5
inicio=0
objetivo=w0*h0-1

nw = make_maze(w0,h0)
draw_maze(nw,w0,h0)
nwabs = nowallsabs(nw,w0)

b=GA(inicio,objetivo,w0,h0)
if b[0]:
        print '===> SUCESSO'
        print str(b[2]) + ' geracoes'
        print '-> Cromossomo:'
        print b[1]
        print '-> Direções:'
        for x in xrange(0,len(b[1]),2):
                if b[1][x]==0 and b[1][x+1]==0:
                        print '\tnorte'
                if b[1][x]==0 and b[1][x+1]==1:
                        print '\tsul'
                if b[1][x]==1 and b[1][x+1]==0:
                        print '\tleste'
                if b[1][x]==1 and b[1][x+1]==1:
                        print '\toeste'  
else:
        print '===> FALHA'
        print 'Max_geracoes atingida: ' + str(b[2])
