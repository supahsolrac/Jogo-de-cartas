import socket
import random

decknomes=["As","2","3","4","5","6","7","8","9","10","Valete","Rainha","Rei"]
condicao=["maior impar","maior par","menor impar","menor par"]
deck=[4]


def pescar(vezes=1):
	mao=[]
	for x in range(vezes):
		carta=random.randint(0,12)
		while deck[carta]==0:
			carta=random.randint(0,12)
		mao.append(carta)
		deck[carta]-=1
	return mao
def pescarop(dados,vezes=1):
	for x in range(vezes):
		carta=random.randint(0,12)
		while deck[carta]==0:
			carta=random.randint(0,12)
		pacote=carta.to_bytes(length=1,byteorder='big',signed=False)
		dados.send(pacote)

def printmao(mao):
	maon=""
	for x in range(len(mao)):
		maon+=decknomes[mao[x]]
		maon+=' '
	print(maon)

def resetdeck():
	for x in range(len(deck)):
		deck[x]=4

def deckvasio():
	for x in range(len(deck)):
		if(deck[x]!=0): return
	resetdeck()

def resolver(cards,cond):
	if cond==0:
		if cards[0]%2!=0:
			if cards[1]%2!=0:
				return 0
			else: return 2
		if cards[1]%2!=0:
			return 1
		if cards[0]>cards[1]: return 1
		if cards[0]==cards[1]: return 0
		else: return 2
	elif cond==1:
		if cards[0]%2==0:
			if cards[1]%2==0:
				return 0
			else: return 2
		if cards[1]%2==0:
			return 1
		if cards[0]>cards[1]: return 1
		if cards[0]==cards[1]: return 0
		else: return 2
	elif cond==2:
		if cards[0]%2!=0:
			if cards[1]%2!=0:
				return 0
			return 2
		if cards[1]%2!=0:
			return 1
		if cards[0]<cards[1]: return 1
		if cards[0]==cards[1]: return 0
		else: return 2
	else:
		if cards[0]%2==0:
			if cards[1]%2==0:
				return 0
			return 2
		if cards[1]%2==0:
			return 1
		if cards[0]<cards[1]: return 1
		if cards[0]==cards[1]: return 0
		else: return 2


def main():
	escuta= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	porta=42069
	ip="127.0.0.1"
	escuta.bind((ip,porta))
	escuta.listen(1)
	dados, end_client=escuta.accept()
	for x in range(12):
		deck.append(4)
	pontos=[0,0]
	mao=pescar(3)
	pescarop(dados,3)
	#oponente pesca 3 vezes
	while pontos[0]<2 and pontos[1]<2:
		cond=random.randint(0,3)
		pacote=cond.to_bytes(length=1,byteorder='big',signed=False)
		dados.send(pacote)
		print("condicao de vitoria:")
		print(condicao[cond])
		print("sua mao:")
		printmao(mao)
		cardesc=int(input("escolha um card:(1-3)\n"))
		cardesc=mao[cardesc-1]
		mao.remove(cardesc)
		cardesco=dados.recv(1)#card do oponente
		cardesco=int.from_bytes(bytes=cardesco, byteorder='big', signed=False)
		r=resolver([cardesc,cardesco],cond)
		pacote=r.to_bytes(length=1,byteorder='big',signed=False)
		dados.send(pacote)
		if r==0:
			print("empate!")
		else:
			print("o jogador "+str(r)+" ganhou")
			pontos[r-1]+=1;
		mao.extend(pescar(1))
		pescarop(dados,1)
		deckvasio()
		print("pontuacao: "+str(pontos))
	if pontos[0]==2:
		print("Voce ganhou a partida")
	else:
		print("Voce perdeu a partida")

if __name__ == '__main__':
    main()